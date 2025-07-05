import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from core.models.marketplace import MarketplaceListing, Order, OrderItem
from api.serializers import MarketplaceListingSerializer
from core.secret_store import get_stripe_webhook_secret

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def marketplace_webhook(request):
    """Handle Stripe webhook events for marketplace Direct Charges."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, get_stripe_webhook_secret()
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session_completed(session)
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        handle_checkout_session_completed(session)
    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        handle_checkout_session_failed(session)
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_intent_failed(payment_intent)
    else:
        print(f'Unhandled event type {event["type"]}')

    return HttpResponse(status=200)

def handle_checkout_session_completed(session):
    """Handle successful checkout session completion."""
    try:
        # Find the order by PaymentIntent ID
        payment_intent_id = session.get('payment_intent')
        if not payment_intent_id:
            print(f"No payment_intent found in session {session['id']}")
            return

        order = Order.objects.filter(stripe_payment_intent_id=payment_intent_id).first()
        if not order:
            print(f"No order found for payment_intent {payment_intent_id}")
            return

        # Update order status
        order.status = 'paid'
        order.save()

        # Update listing if needed (e.g., mark as sold)
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            listing = item.listing
            # You might want to mark the listing as sold or reduce inventory
            # listing.is_sold = True
            # listing.save()

        print(f"Order {order.id} marked as paid successfully")

    except Exception as e:
        print(f"Error handling checkout session completed: {str(e)}")

def handle_checkout_session_failed(session):
    """Handle failed checkout session."""
    try:
        payment_intent_id = session.get('payment_intent')
        if not payment_intent_id:
            return

        order = Order.objects.filter(stripe_payment_intent_id=payment_intent_id).first()
        if order:
            order.status = 'cancelled'
            order.save()
            print(f"Order {order.id} marked as cancelled due to payment failure")

    except Exception as e:
        print(f"Error handling checkout session failed: {str(e)}")

def handle_payment_intent_succeeded(payment_intent):
    """Handle successful payment intent."""
    try:
        order = Order.objects.filter(stripe_payment_intent_id=payment_intent['id']).first()
        if order and order.status == 'pending':
            order.status = 'paid'
            order.save()
            print(f"Order {order.id} payment confirmed")

    except Exception as e:
        print(f"Error handling payment intent succeeded: {str(e)}")

def handle_payment_intent_failed(payment_intent):
    """Handle failed payment intent."""
    try:
        order = Order.objects.filter(stripe_payment_intent_id=payment_intent['id']).first()
        if order:
            order.status = 'cancelled'
            order.save()
            print(f"Order {order.id} payment failed")

    except Exception as e:
        print(f"Error handling payment intent failed: {str(e)}")

class MarketplaceListingViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceListing.objects.all()
    serializer_class = MarketplaceListingSerializer

    @action(detail=True, methods=['post'], permission_classes=['IsAuthenticated'])
    def create_direct_charge_session(self, request, pk=None):
        """Create a Stripe Checkout Session for Direct Charges with application fees."""
        listing = self.get_object()
        buyer = request.user
        
        # Get seller's Stripe Connect account ID
        seller_stripe_account_id = listing.seller.stripe_connect_account_id
        
        if not seller_stripe_account_id:
            return Response(
                {'error': 'Seller not onboarded for payments. Please contact the seller to complete their Stripe Connect setup.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Calculate commission (e.g., 5% platform fee)
            platform_fee_percentage = settings.MARKETPLACE_COMMISSION_PERCENTAGE
            platform_fee_amount = int(listing.price * platform_fee_percentage * 100)  # Cents

            # Create a Checkout Session for Direct Charges
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': listing.title,
                            'description': listing.description[:255],  # Stripe limit
                        },
                        'unit_amount': int(listing.price * 100),  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{settings.FRONTEND_URL}/marketplace/purchase/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/marketplace/purchase/cancel",
                # Direct Charges configuration
                payment_intent_data={
                    'application_fee_amount': platform_fee_amount,
                    'transfer_data': {
                        'destination': seller_stripe_account_id,
                    },
                },
                metadata={
                    'listing_id': listing.id,
                    'buyer_id': buyer.id,
                    'seller_id': listing.seller.id,
                    'order_type': 'marketplace_direct_charge',
                    'platform_fee_amount': platform_fee_amount,
                },
                # Use seller's branding (optional)
                # customer_email=buyer.email,  # Pre-fill customer email
            )

            # Create a pending Order in your database
            order = Order.objects.create(
                buyer=buyer,
                total_amount=listing.price,
                platform_commission=platform_fee_amount / 100,  # Store in dollars
                stripe_payment_intent_id=session.payment_intent,  # Store the PaymentIntent ID
                status='pending'
            )
            OrderItem.objects.create(
                order=order, 
                listing=listing, 
                quantity=1, 
                price=listing.price
            )

            return Response({
                'sessionId': session.id,
                'url': session.url,  # Redirect URL for hosted checkout
                'order_id': order.id
            })

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=['IsAuthenticated'])
    def create_embedded_direct_charge(self, request, pk=None):
        """Create an embedded Checkout Session for Direct Charges."""
        listing = self.get_object()
        buyer = request.user
        
        # Get seller's Stripe Connect account ID
        seller_stripe_account_id = listing.seller.stripe_connect_account_id
        
        if not seller_stripe_account_id:
            return Response(
                {'error': 'Seller not onboarded for payments'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Calculate commission
            platform_fee_percentage = settings.MARKETPLACE_COMMISSION_PERCENTAGE
            platform_fee_amount = int(listing.price * platform_fee_percentage * 100)

            # Create embedded Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': listing.title,
                            'description': listing.description[:255],
                        },
                        'unit_amount': int(listing.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                ui_mode='embedded',
                return_url=f"{settings.FRONTEND_URL}/marketplace/purchase/return?session_id={{CHECKOUT_SESSION_ID}}",
                # Direct Charges configuration
                payment_intent_data={
                    'application_fee_amount': platform_fee_amount,
                    'transfer_data': {
                        'destination': seller_stripe_account_id,
                    },
                },
                metadata={
                    'listing_id': listing.id,
                    'buyer_id': buyer.id,
                    'seller_id': listing.seller.id,
                    'order_type': 'marketplace_direct_charge_embedded',
                    'platform_fee_amount': platform_fee_amount,
                },
            )

            # Create pending order
            order = Order.objects.create(
                buyer=buyer,
                total_amount=listing.price,
                platform_commission=platform_fee_amount / 100,
                stripe_payment_intent_id=session.payment_intent,
                status='pending'
            )
            OrderItem.objects.create(
                order=order, 
                listing=listing, 
                quantity=1, 
                price=listing.price
            )

            return Response({
                'clientSecret': session.client_secret,
                'sessionId': session.id,
                'order_id': order.id
            })

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], permission_classes=['IsAuthenticated'])
    def session_status(self, request):
        """Get the status of a Checkout Session."""
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response({'error': 'Session ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return Response({
                'status': session.status,
                'payment_status': session.payment_status,
            })
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Keep the old purchase method for backward compatibility
    @action(detail=True, methods=['post'], permission_classes=['IsAuthenticated'])
    def purchase(self, request, pk=None):
        """Legacy purchase method - now redirects to Direct Charges."""
        return self.create_direct_charge_session(request, pk) 