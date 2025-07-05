# Secure Secret Management Guide for CalloutRacing

## 🚨 CRITICAL SECURITY NOTICE

**NEVER commit live API keys to version control!** Your live Stripe secret key has been exposed in this conversation. You should:

1. **Immediately rotate your Stripe keys** in the Stripe Dashboard
2. **Use environment variables** for all secrets
3. **Set up proper secret management** for production

## 🔐 Secure Secret Store Implementation

I've created a secure secret management system for CalloutRacing:

### Files Created:
- `backend/core/secret_store.py` - Secure secret store with encryption
- `backend/core/management/commands/validate_secrets.py` - Validation command
- `backend/requirements.txt` - Added cryptography dependency

### Features:
- ✅ **Environment variable validation**
- ✅ **Key format validation** (test vs live)
- ✅ **Encryption support** for sensitive data
- ✅ **Django management command** for validation
- ✅ **Stripe API connectivity testing**

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Your .env File
Create `backend/.env` with your secrets:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-django-secret-key

# Stripe Configuration (USE YOUR NEW KEYS AFTER ROTATION)
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_NEW_PUBLISHABLE_KEY
STRIPE_SECRET_KEY=sk_live_YOUR_NEW_SECRET_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET

# Frontend URL
FRONTEND_URL=http://localhost:5173

# Marketplace Commission
MARKETPLACE_COMMISSION_PERCENTAGE=0.05

# Encryption Key (auto-generated if not provided)
ENCRYPTION_KEY=your-encryption-key-here
```

### 3. Validate Your Secrets
```bash
cd backend
python manage.py validate_secrets --test-stripe
```

This will:
- ✅ Check all environment variables are present
- ✅ Validate key formats
- ✅ Test Stripe API connectivity
- ✅ Warn if using live keys

### 4. Test the Integration
```bash
# Backend
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm run dev
```

## 🔄 Key Rotation Process

### Step 1: Rotate Your Stripe Keys
1. Go to [Stripe Dashboard > Developers > API Keys](https://dashboard.stripe.com/apikeys)
2. Click "Roll key" for your live secret key
3. Copy the new secret key
4. Update your publishable key if needed

### Step 2: Update Environment Variables
Replace the old keys in your `.env` file with the new ones.

### Step 3: Test the New Keys
```bash
python manage.py validate_secrets --test-stripe
```

## 🏗️ Production Deployment

### For Railway/Heroku:
Set environment variables in your hosting platform:

```bash
STRIPE_SECRET_KEY=sk_live_YOUR_NEW_SECRET_KEY
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_NEW_PUBLISHABLE_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET
FRONTEND_URL=https://your-domain.com
```

### For Docker:
Add to your `docker-compose.yml`:
```yaml
environment:
  - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
  - STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY}
  - STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
```

## 🔍 Secret Validation

The validation command checks:

### Stripe Keys:
- ✅ Secret key present and valid format
- ✅ Publishable key present and valid format
- ✅ Webhook secret present and valid format
- ✅ API connectivity test
- ⚠️ Live key detection and warning

### Other Secrets:
- ✅ Database password
- ✅ Email password
- ✅ OAuth secrets

## 🛡️ Security Best Practices

### ✅ DO:
- Use environment variables for all secrets
- Rotate keys regularly
- Use different keys for test/production
- Validate secrets before deployment
- Monitor for unauthorized usage

### ❌ DON'T:
- Commit secrets to version control
- Share keys in chat/email
- Use the same keys for test/production
- Store secrets in plain text files
- Use weak encryption

## 🚨 Emergency Response

If you suspect your keys are compromised:

1. **Immediately rotate** the affected keys
2. **Check Stripe Dashboard** for unauthorized charges
3. **Review webhook logs** for suspicious activity
4. **Update all environments** with new keys
5. **Monitor closely** for the next 24-48 hours

## 📞 Support Commands

### Validate All Secrets:
```bash
python manage.py validate_secrets
```

### Test Stripe Connectivity:
```bash
python manage.py validate_secrets --test-stripe
```

### Check Key Types:
The validation will show if you're using test or live keys and warn appropriately.

## 🔐 Advanced Security (Optional)

For enhanced security, consider:

1. **AWS Secrets Manager** for production
2. **HashiCorp Vault** for enterprise
3. **Azure Key Vault** for Microsoft stack
4. **Google Secret Manager** for GCP

The current implementation uses environment variables which is secure for most use cases.

---

**Remember: Security is everyone's responsibility. Always validate your secrets before deploying to production!** 