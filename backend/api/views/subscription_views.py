"""
Stripe Subscription Views

This module handles Stripe subscription management including:
- Creating checkout sessions for subscriptions
- Handling webhooks for payment events
- Managing customer portal sessions
- Processing marketplace payments with commissions
"""

import stripe
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from core.models.payments import Subscription, Payment, UserWallet, MarketplaceTransaction
from core.models.marketplace import MarketplaceListing
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription_checkout_session(request):
    """Create a Stripe checkout session for subscription."""
    try:
        price_id = request.data.get('price_id')
        if not price_id:
            return Response({'error': 'Price ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create Stripe customer
        customer = None
        if hasattr(request.user, 'stripe_customer_id') and request.user.stripe_customer_id:
            customer = request.user.stripe_customer_id
        else:
            # Create new customer
            customer_data = stripe.Customer.create(
                email=request.user.email,
                name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                metadata={'user_id': request.user.id}
            )
            customer = customer_data.id
            # Update user with customer ID
            request.user.stripe_customer_id = customer
            request.user.save()

        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            customer=customer,
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f"{settings.FRONTEND_URL}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/subscription/cancel",
            metadata={
                'user_id': request.user.id,
                'price_id': price_id
            },
            allow_promotion_codes=True,
            billing_address_collection='required',
        )

        return Response({
            'sessionId': checkout_session.id,
            'url': checkout_session.url
        }, status=status.HTTP_200_OK)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in create_subscription_checkout_session: {str(e)}")
        return Response({'error': 'Payment processing error'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in create_subscription_checkout_session: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_customer_portal_session(request):
    """Create a customer portal session for subscription management."""
    try:
        if not hasattr(request.user, 'stripe_customer_id') or not request.user.stripe_customer_id:
            return Response({'error': 'No subscription found'}, status=status.HTTP_400_BAD_REQUEST)

        session = stripe.billing_portal.Session.create(
            customer=request.user.stripe_customer_id,
            return_url=f"{settings.FRONTEND_URL}/subscription/manage",
        )

        return Response({'url': session.url}, status=status.HTTP_200_OK)

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in create_customer_portal_session: {str(e)}")
        return Response({'error': 'Payment processing error'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in create_customer_portal_session: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscription_status(request):
    """Get current user's subscription status."""
    try:
        subscription = Subscription.objects.filter(
            user=request.user,
            status__in=['active', 'trialing']
        ).first()

        if subscription:
            return Response({
                'has_active_subscription': True,
                'subscription': {
                    'id': subscription.id,
                    'status': subscription.status,
                    'current_period_end': subscription.current_period_end,
                    'cancel_at_period_end': subscription.cancel_at_period_end,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'has_active_subscription': False
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in get_subscription_status: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_marketplace_payment_intent(request, item_id):
    """Create a payment intent for marketplace item purchase."""
    try:
        # Get the marketplace item
        item = MarketplaceListing.objects.get(id=item_id, is_active=True)
        
        # Get seller's Stripe Connect account
        seller_wallet = UserWallet.objects.filter(user=item.seller).first()
        if not seller_wallet or not seller_wallet.stripe_account_id:
            return Response({'error': 'Seller is not onboarded for payments'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate amounts in cents
        item_price_cents = int(item.price * 100)
        commission_rate = getattr(settings, 'MARKETPLACE_COMMISSION_PERCENTAGE', 0.05)
        commission_cents = int(item_price_cents * commission_rate)
        seller_amount_cents = item_price_cents - commission_cents

        # Create PaymentIntent on the connected account
        payment_intent = stripe.PaymentIntent.create(
            amount=item_price_cents,
            currency='usd',
            automatic_payment_methods={"enabled": True},
            application_fee_amount=commission_cents,
            metadata={
                'item_id': item.id,
                'buyer_id': request.user.id,
                'seller_id': item.seller.id,
                'platform_commission_cents': commission_cents,
                'seller_amount_cents': seller_amount_cents,
                'transaction_type': 'marketplace'
            },
            stripe_account=seller_wallet.stripe_account_id
        )

        return Response({
            'clientSecret': payment_intent.client_secret,
            'paymentIntentId': payment_intent.id,
            'amount': item.price,
            'commission': commission_cents / 100,
            'seller_amount': seller_amount_cents / 100
        }, status=status.HTTP_200_OK)

    except MarketplaceListing.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in create_marketplace_payment_intent: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in create_marketplace_payment_intent: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Handle Stripe webhook events."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        handle_checkout_session_completed(event['data']['object'])
    elif event['type'] == 'payment_intent.succeeded':
        handle_payment_intent_succeeded(event['data']['object'])
    elif event['type'] == 'payment_intent.payment_failed':
        handle_payment_intent_failed(event['data']['object'])
    elif event['type'] == 'invoice.payment_succeeded':
        handle_invoice_payment_succeeded(event['data']['object'])
    elif event['type'] == 'invoice.payment_failed':
        handle_invoice_payment_failed(event['data']['object'])
    elif event['type'] == 'customer.subscription.updated':
        handle_subscription_updated(event['data']['object'])
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    else:
        logger.info(f"Unhandled event type: {event['type']}")

    return HttpResponse(status=200)


def handle_checkout_session_completed(session):
    """Handle successful checkout session completion."""
    try:
        if session.get('mode') == 'subscription':
            # Handle subscription creation
            user_id = session.metadata.get('user_id')
            price_id = session.metadata.get('price_id')
            
            if user_id and price_id:
                user = User.objects.get(id=user_id)
                
                # Create or update subscription
                subscription, created = Subscription.objects.get_or_create(
                    stripe_subscription_id=session.subscription,
                    defaults={
                        'user': user,
                        'stripe_customer_id': session.customer,
                        'stripe_price_id': price_id,
                        'status': 'active'
                    }
                )
                
                if not created:
                    subscription.status = 'active'
                    subscription.save()
                
                logger.info(f"Subscription created/updated for user {user_id}")
        
        # Handle one-time payments if needed
        elif session.get('mode') == 'payment':
            # Handle one-time payment completion
            pass
            
    except Exception as e:
        logger.error(f"Error handling checkout session completed: {e}")


def handle_payment_intent_succeeded(payment_intent):
    """Handle successful payment intent."""
    try:
        transaction_type = payment_intent.metadata.get('transaction_type')
        
        if transaction_type == 'marketplace':
            # Handle marketplace transaction
            item_id = payment_intent.metadata.get('item_id')
            buyer_id = payment_intent.metadata.get('buyer_id')
            seller_id = payment_intent.metadata.get('seller_id')
            commission_cents = payment_intent.metadata.get('platform_commission_cents', 0)
            seller_amount_cents = payment_intent.metadata.get('seller_amount_cents', 0)
            
            # Create marketplace transaction record
            transaction = MarketplaceTransaction.objects.create(
                buyer_id=buyer_id,
                seller_id=seller_id,
                item_id=item_id,
                stripe_payment_intent_id=payment_intent.id,
                amount=payment_intent.amount / 100,
                seller_amount=seller_amount_cents / 100,
                platform_commission=commission_cents / 100,
                status='completed'
            )
            
            # Mark item as sold
            item = MarketplaceListing.objects.get(id=item_id)
            item.is_sold = True
            item.save()
            
            logger.info(f"Marketplace transaction completed: {transaction.id}")
        
        # Create payment record
        user_id = payment_intent.metadata.get('buyer_id')
        if user_id:
            Payment.objects.create(
                user_id=user_id,
                stripe_payment_intent_id=payment_intent.id,
                amount=payment_intent.amount / 100,
                currency=payment_intent.currency,
                status='succeeded',
                payment_type='marketplace' if transaction_type == 'marketplace' else 'one_time',
                description=f"Payment for {transaction_type}",
                metadata=payment_intent.metadata
            )
            
    except Exception as e:
        logger.error(f"Error handling payment intent succeeded: {e}")


def handle_payment_intent_failed(payment_intent):
    """Handle failed payment intent."""
    try:
        user_id = payment_intent.metadata.get('buyer_id')
        if user_id:
            Payment.objects.create(
                user_id=user_id,
                stripe_payment_intent_id=payment_intent.id,
                amount=payment_intent.amount / 100,
                currency=payment_intent.currency,
                status='failed',
                payment_type='marketplace',
                description="Failed payment",
                metadata=payment_intent.metadata
            )
            
    except Exception as e:
        logger.error(f"Error handling payment intent failed: {e}")


def handle_invoice_payment_succeeded(invoice):
    """Handle successful invoice payment."""
    try:
        # Update subscription period
        subscription = Subscription.objects.filter(
            stripe_subscription_id=invoice.subscription
        ).first()
        
        if subscription:
            subscription.current_period_start = invoice.period_start
            subscription.current_period_end = invoice.period_end
            subscription.save()
            
    except Exception as e:
        logger.error(f"Error handling invoice payment succeeded: {e}")


def handle_invoice_payment_failed(invoice):
    """Handle failed invoice payment."""
    try:
        subscription = Subscription.objects.filter(
            stripe_subscription_id=invoice.subscription
        ).first()
        
        if subscription:
            subscription.status = 'past_due'
            subscription.save()
            
    except Exception as e:
        logger.error(f"Error handling invoice payment failed: {e}")


def handle_subscription_updated(subscription):
    """Handle subscription updates."""
    try:
        db_subscription = Subscription.objects.filter(
            stripe_subscription_id=subscription.id
        ).first()
        
        if db_subscription:
            db_subscription.status = subscription.status
            db_subscription.current_period_start = subscription.current_period_start
            db_subscription.current_period_end = subscription.current_period_end
            db_subscription.cancel_at_period_end = subscription.cancel_at_period_end
            db_subscription.save()
            
    except Exception as e:
        logger.error(f"Error handling subscription updated: {e}")


def handle_subscription_deleted(subscription):
    """Handle subscription deletion."""
    try:
        db_subscription = Subscription.objects.filter(
            stripe_subscription_id=subscription.id
        ).first()
        
        if db_subscription:
            db_subscription.status = 'canceled'
            db_subscription.save()
            
    except Exception as e:
        logger.error(f"Error handling subscription deleted: {e}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscription_plans(request):
    """Get available subscription plans."""
    try:
        plans_dict = settings.SUBSCRIPTION_PLANS
        # Convert dictionary to list format for frontend compatibility
        plans_list = []
        for plan_key, plan_data in plans_dict.items():
            plans_list.append({
                'id': plan_key,
                'name': plan_data.get('name', 'Unknown'),
                'price': plan_data.get('price', 0),
                'price_id': plan_data.get('price_id', ''),
                'features': plan_data.get('features', [])
            })
        return Response(plans_list, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting subscription plans: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 