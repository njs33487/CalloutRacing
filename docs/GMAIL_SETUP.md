# Gmail App Password Setup for Contact Form

## Step-by-Step Instructions

### 1. Enable 2-Factor Authentication
1. Go to your Google Account settings: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", click on "2-Step Verification"
4. Follow the prompts to enable 2-factor authentication

### 2. Generate App Password
1. Go to your Google Account settings: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", click on "App passwords"
4. You may need to verify your identity
5. Select "Mail" as the app and "Other" as the device
6. Click "Generate"
7. Copy the 16-character password that appears

### 3. Use the App Password
- Use this 16-character password as your `EMAIL_HOST_PASSWORD` in Railway
- Do NOT use your regular Gmail password
- The app password will look something like: `abcd efgh ijkl mnop`

### 4. Test the Setup
After setting up the environment variables:
1. Deploy your application
2. Go to your contact form
3. Submit a test message
4. Check if you receive the email at digibin@digitalbinarysolutionsllc.com

## Troubleshooting

### If emails don't send:
1. Verify the app password is correct (16 characters, no spaces)
2. Check that 2-factor authentication is enabled
3. Ensure the email address is correct
4. Check Railway logs for any email errors

### Security Notes:
- Keep your app password secure
- Don't share it in code or logs
- You can revoke app passwords at any time from Google Account settings
- Each app password is unique and can only be used for the specified app 