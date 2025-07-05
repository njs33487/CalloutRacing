# Stripe Setup Guide for CalloutRacing

## 🚀 Quick Setup

### 1. Environment Variables

**Backend (.env file):**
```bash
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_51RhK8wIMXFPBDR0oDiPPqp0XsfS95yGQaXcj7WTMD3scZtuFy2nhcbvryorYrD8ihxbCobNtzf77bOwJNAtksMdR00Mier3nb7
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE
FRONTEND_URL=http://localhost:5173
MARKETPLACE_COMMISSION_PERCENTAGE=0.05
```

**Frontend (.env file):**
```bash
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_51RhK8wIMXFPBDR0oDiPPqp0XsfS95yGQaXcj7WTMD3scZtuFy2nhcbvryorYrD8ihxbCobNtzf77bOwJNAtksMdR00Mier3nb7
```

### 2. Get Your Stripe Keys

1. **Secret Key**: Go to [Stripe Dashboard > Developers > API Keys](https://dashboard.stripe.com/apikeys)
   - Copy your **Secret key** (starts with `sk_test_`)

2. **Webhook Secret**: Go to [Stripe Dashboard > Developers > Webhooks](https://dashboard.stripe.com/webhooks)
   - Click "Add endpoint"
   - URL: `https://your-domain.com/api/stripe-webhook/`
   - Events to listen for:
     - `checkout.session.completed`
     - `customer.subscription.created`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `invoice.paid`
     - `invoice.payment_failed`
   - Copy the **Signing secret** (starts with `whsec_`)

### 3. Create Products and Prices

In [Stripe Dashboard > Products](https://dashboard.stripe.com/products):

**Basic Plan:**
- Name: "CalloutRacing Basic"
- Price: $9.99/month
- Price ID: `price_basic` (note this ID)

**Pro Plan:**
- Name: "CalloutRacing Pro"
- Price: $19.99/month
- Price ID: `price_pro` (note this ID)

### 4. Update Price IDs in Code

In `backend/api/views/subscription_views.py`, update the price mapping:
```python
subscription_type_map = {
    'price_basic': 'basic',  # Replace with your actual price ID
    'price_pro': 'pro',      # Replace with your actual price ID
}
```

### 5. Test the Integration

**Test Cards:**
- Success: `4242 4242 4242 4242`
- Requires Authentication: `4000 0025 0000 3155`
- Declined: `4000 0000 0000 9995`

**Test the Flow:**
1. Start your backend: `python manage.py runserver`
2. Start your frontend: `npm run dev`
3. Navigate to `/subscription`
4. Select a plan and complete payment

### 6. Webhook Testing (Development)

Install Stripe CLI:
```bash
# Windows
# Download from: https://github.com/stripe/stripe-cli/releases/latest

# Forward webhooks to your local server
stripe listen --forward-to localhost:8000/api/stripe-webhook/
```

### 7. Database Migrations

Run Django migrations for the new models:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 8. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## 🔧 Configuration Details

### Backend Settings
The following settings are already configured in `backend/calloutracing/settings.py`:
- Stripe API key configuration
- Webhook secret verification
- Frontend URL for redirects
- Marketplace commission percentage

### Frontend Configuration
The following components are ready:
- `SubscriptionPage.tsx` - Plan selection and embedded checkout
- `SubscriptionSuccessPage.tsx` - Payment success handling
- `SubscriptionCancelPage.tsx` - Payment cancellation
- `CustomerPortalButton.tsx` - Subscription management

### API Endpoints
- `POST /api/subscriptions/create-checkout-session/` - Create checkout session
- `GET /api/subscriptions/session-status/` - Check session status
- `POST /api/subscriptions/customer-portal/` - Create customer portal session
- `POST /api/stripe-webhook/` - Handle webhook events

## 🚨 Important Notes

1. **Never commit your secret keys** to version control
2. **Use test keys** for development, live keys for production
3. **Set up webhooks** in production for proper event handling
4. **Test thoroughly** with Stripe's test cards before going live
5. **Monitor webhook events** in Stripe Dashboard

## 🎯 Next Steps

1. Replace `YOUR_SECRET_KEY_HERE` with your actual Stripe secret key
2. Replace `YOUR_WEBHOOK_SECRET_HERE` with your webhook signing secret
3. Create your products and prices in Stripe Dashboard
4. Update the price IDs in the code
5. Test the complete flow
6. Set up production webhooks when ready to deploy

## 📞 Support

If you encounter issues:
1. Check Stripe Dashboard for webhook delivery status
2. Verify environment variables are set correctly
3. Check browser console for frontend errors
4. Check Django logs for backend errors
5. Use Stripe CLI for local webhook testing 