# Stripe Connect Direct Charges Implementation Guide

## Overview

This guide explains the implementation of Stripe Connect's Direct Charges model in CalloutRacing's marketplace. This approach allows buyers to pay directly to sellers' Stripe accounts while CalloutRacing collects a platform fee (commission).

## Key Concepts

### Direct Charges Model
- **Customer Experience**: Buyers see the seller's branding and the charge appears on the seller's Stripe account
- **Fund Flow**: Full payment goes to seller's Stripe balance, platform fee goes to CalloutRacing's account
- **Branding**: Uses seller's Stripe account branding (logo, colors) on checkout pages
- **Best Use Case**: Marketplace platforms where buyers should feel they're transacting directly with sellers

### Implementation Architecture

```
Buyer → CalloutRacing Frontend → Backend API → Stripe Connect → Seller's Account
                                    ↓
                              Platform Fee (5%)
```

## Backend Implementation

### 1. User Model Updates

**File**: `backend/core/models/auth.py`
```python
class User(AbstractUser):
    # ... existing fields ...
    stripe_connect_account_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text='Stripe Connect account ID for marketplace sellers'
    )
```

### 2. Direct Charges API Endpoints

**File**: `backend/api/views/marketplace_views.py`

#### Hosted Checkout (Redirect)
```python
@action(detail=True, methods=['post'], permission_classes=['IsAuthenticated'])
def create_direct_charge_session(self, request, pk=None):
    """Create a Stripe Checkout Session for Direct Charges with application fees."""
    # Creates hosted checkout session
    # Redirects buyer to Stripe's hosted payment page
    # Uses seller's branding
```

#### Embedded Checkout
```python
@action(detail=True, methods=['post'], permission_classes=['IsAuthenticated'])
def create_embedded_direct_charge(self, request, pk=None):
    """Create an embedded Checkout Session for Direct Charges."""
    # Creates embedded checkout session
    # Payment form appears on CalloutRacing site
    # Still uses seller's branding
```

#### Session Status Check
```python
@action(detail=False, methods=['get'], permission_classes=['IsAuthenticated'])
def session_status(self, request):
    """Get the status of a Checkout Session."""
    # Check payment status after redirect
```

### 3. Webhook Handler

**File**: `backend/api/views/marketplace_views.py`

```python
@csrf_exempt
def marketplace_webhook(request):
    """Handle Stripe webhook events for marketplace Direct Charges."""
    # Handles events:
    # - checkout.session.completed
    # - checkout.session.async_payment_succeeded
    # - checkout.session.async_payment_failed
    # - payment_intent.succeeded
    # - payment_intent.payment_failed
```

### 4. URL Configuration

**File**: `backend/api/urls.py`
```python
# Marketplace listing endpoints
router.register(r'marketplace-listings', MarketplaceListingViewSet, basename='marketplace-listing')

# Webhook endpoint
marketplace_patterns = [
    path('marketplace/webhook/', marketplace_webhook, name='marketplace-webhook'),
]
```

## Frontend Implementation

### 1. Direct Charge Checkout Component

**File**: `frontend/src/components/DirectChargeCheckout.tsx`

Features:
- Supports both hosted and embedded checkout modes
- Handles session creation and status checking
- Displays platform fee information
- Error handling and loading states

### 2. Success/Cancel Pages

**Files**: 
- `frontend/src/pages/MarketplacePurchaseSuccess.tsx`
- `frontend/src/pages/MarketplacePurchaseCancel.tsx`

Handle return flows from hosted checkout.

## Configuration

### 1. Environment Variables

**Backend** (`.env`):
```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=http://localhost:5173
MARKETPLACE_COMMISSION_PERCENTAGE=0.05
```

**Frontend** (`.env`):
```bash
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
VITE_API_URL=http://localhost:8000/api
```

### 2. Stripe Dashboard Setup

#### Webhook Configuration
1. Go to [Stripe Dashboard > Webhooks](https://dashboard.stripe.com/webhooks)
2. Add endpoint: `https://your-domain.com/api/marketplace/webhook/`
3. Events to listen for:
   - `checkout.session.completed`
   - `checkout.session.async_payment_succeeded`
   - `checkout.session.async_payment_failed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`

#### Connect Account Settings
1. Enable Connect in your Stripe account
2. Configure Express dashboard settings
3. Set up application fee handling

## Usage Examples

### 1. Creating a Direct Charge (Hosted)

```javascript
// Frontend
const response = await api.post(`/marketplace-listings/${listingId}/create_direct_charge_session/`);
const { url } = response.data;
window.location.href = url; // Redirect to Stripe hosted checkout
```

### 2. Creating a Direct Charge (Embedded)

```javascript
// Frontend
const response = await api.post(`/marketplace-listings/${listingId}/create_embedded_direct_charge/`);
const { clientSecret } = response.data;
// Use clientSecret with Stripe.js embedded checkout
```

### 3. Checking Session Status

```javascript
// Frontend
const response = await api.get(`/marketplace-listings/session_status/?session_id=${sessionId}`);
const { status, payment_status } = response.data;
```

## Database Schema

### Orders Table
```sql
CREATE TABLE core_order (
    id INTEGER PRIMARY KEY,
    buyer_id INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    platform_commission DECIMAL(10,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'pending',
    stripe_payment_intent_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Users Table
```sql
ALTER TABLE core_user ADD COLUMN stripe_connect_account_id VARCHAR(255);
```

## Testing

### 1. Test Cards
Use Stripe's test card numbers:
- **Success**: `4242424242424242`
- **Decline**: `4000000000000002`
- **Authentication Required**: `4000002500003155`

### 2. Test Scenarios
1. **Successful Payment**: Complete checkout with valid card
2. **Failed Payment**: Use declined card
3. **Authentication**: Use 3D Secure card
4. **Webhook Handling**: Test webhook events
5. **Seller Onboarding**: Test Connect account creation

### 3. Testing Commands

```bash
# Backend tests
python manage.py test api.tests.test_marketplace_features

# Frontend tests
npm run test -- DirectChargeCheckout.test.tsx
```

## Security Considerations

### 1. Webhook Security
- Verify webhook signatures
- Use HTTPS endpoints
- Validate event data

### 2. API Security
- Require authentication for all endpoints
- Validate user permissions
- Sanitize input data

### 3. Error Handling
- Don't expose sensitive Stripe errors
- Log errors for debugging
- Provide user-friendly error messages

## Monitoring and Analytics

### 1. Key Metrics
- Payment success rate
- Average order value
- Platform fee revenue
- Seller onboarding conversion

### 2. Logging
```python
# Log successful payments
print(f"Order {order.id} marked as paid successfully")

# Log failed payments
print(f"Order {order.id} payment failed")
```

## Troubleshooting

### Common Issues

1. **"Seller not onboarded" Error**
   - Ensure seller has completed Stripe Connect onboarding
   - Check `stripe_connect_account_id` field in user profile

2. **Webhook Not Receiving Events**
   - Verify webhook URL is accessible
   - Check webhook secret configuration
   - Ensure events are enabled in Stripe Dashboard

3. **Payment Failing**
   - Check seller's Connect account status
   - Verify application fee amount
   - Review Stripe error logs

### Debug Commands

```bash
# Check webhook events
stripe events list --limit 10

# Test webhook endpoint
curl -X POST https://your-domain.com/api/marketplace/webhook/ \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## Production Deployment

### 1. Environment Setup
- Use production Stripe keys
- Configure production webhook URLs
- Set up monitoring and alerting

### 2. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Testing Checklist
- [ ] Test with production Stripe keys
- [ ] Verify webhook endpoints
- [ ] Test Connect account onboarding
- [ ] Validate payment flows
- [ ] Check error handling

## Benefits of Direct Charges

1. **Better User Experience**: Buyers see seller branding
2. **Simplified Compliance**: Seller is merchant of record
3. **Reduced Chargebacks**: Direct seller-customer relationship
4. **Flexible Fee Structure**: Easy to adjust platform fees
5. **Brand Trust**: Leverages seller's existing brand

## Next Steps

1. **Enhanced Embedded Checkout**: Integrate Stripe.js for embedded payments
2. **Seller Dashboard**: Add seller-specific analytics and payout tracking
3. **Multi-Currency Support**: Add support for different currencies
4. **Advanced Fee Structures**: Implement dynamic fee calculations
5. **Dispute Handling**: Add automated dispute resolution

## Resources

- [Stripe Connect Documentation](https://docs.stripe.com/connect)
- [Direct Charges Guide](https://docs.stripe.com/connect/direct-charges)
- [Webhook Events](https://docs.stripe.com/webhooks)
- [Test Cards](https://docs.stripe.com/testing#cards)
- [Connect Onboarding](https://docs.stripe.com/connect/onboarding) 