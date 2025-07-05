import stripe
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Subscription
from core.secret_store import get_stripe_secret_key, get_stripe_webhook_secret
from django.contrib.auth.models import User

# Configure Stripe with secure secret store
stripe.api_key = get_stripe_secret_key()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """Create a Stripe Checkout Session for subscription using embedded checkout."""
    try:
        # Get price_id from frontend (e.g., for 'basic' or 'pro' plan)
        price_id = request.data.get('price_id')
        if not price_id:
            return JsonResponse({'error': 'Price ID is required'}, status=400)

        # Create the Checkout Session
        session = stripe.checkout.Session.create({
            'success_url': f"{settings.FRONTEND_URL}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}",
            'cancel_url': f"{settings.FRONTEND_URL}/subscription/cancel",
            'mode': 'subscription',
            'ui_mode': 'embedded',
            'line_items': [{
                'quantity': 1,
                'price': price_id,
            }],
            'metadata': {
                'user_id': request.user.id,
                'price_id': price_id,
            },
        })

        return JsonResponse({
            'clientSecret': session.client_secret,
            'sessionId': session.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def session_status(request):
    """Retrieve Checkout Session status."""
    try:
        session_id = request.GET.get('session_id')
        if not session_id:
            return JsonResponse({'error': 'Session ID is required'}, status=400)

        session = stripe.checkout.Session.retrieve(session_id)
        customer = stripe.Customer.retrieve(session.customer) if session.customer else None

        return JsonResponse({
            'status': session.status,
            'payment_status': session.payment_status,
            'customer_email': customer.email if customer else None,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_customer_portal_session(request):
    """Create a customer portal session for subscription management."""
    try:
        # Get customer ID from user's subscription or create one
        user_sub, created = Subscription.objects.get_or_create(user=request.user)
        
        # In a real implementation, you'd store the Stripe customer ID
        # For now, we'll create a customer portal session
        session = stripe.billing_portal.Session.create(
            customer=user_sub.stripe_customer_id if hasattr(user_sub, 'stripe_customer_id') else None,
            return_url=f"{settings.FRONTEND_URL}/app",
        )
        
        return JsonResponse({'url': session.url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events."""
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
        user_id = session['metadata'].get('user_id')
        price_id = session['metadata'].get('price_id')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_sub, created = Subscription.objects.get_or_create(user=user)
                
                # Map price_id to subscription type
                subscription_type_map = {
                    'price_basic': 'basic',
                    'price_pro': 'pro',
                    'price_premium': 'premium',
                }
                
                user_sub.subscription_type = subscription_type_map.get(price_id, 'basic')
                user_sub.status = 'active'
                user_sub.save()
                print(f"User {user.username} subscribed successfully!")
            except User.DoesNotExist:
                print(f"User with ID {user_id} not found for subscription.")

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        status = subscription.get('status')
        
        # Update subscription status in your database
        print(f"Subscription updated to status: {status}")

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Handle subscription cancellation
        print(f"Subscription cancelled: {subscription.id}")

    elif event['type'] == 'invoice.paid':
        # Continue to provision the subscription as payments continue to be made
        invoice = event['data']['object']
        print(f"Invoice paid: {invoice.id}")

    elif event['type'] == 'invoice.payment_failed':
        # The payment failed or the customer does not have a valid payment method
        invoice = event['data']['object']
        print(f"Invoice payment failed: {invoice.id}")

    return HttpResponse(status=200) 