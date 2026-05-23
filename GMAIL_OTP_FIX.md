# Gmail OTP Fix Instructions

## Issue
The "Failed to send OTP" error typically occurs when the system cannot authenticate with Gmail's SMTP server. This is usually due to incorrect credentials or Gmail security settings.

## Solution

### 1. Verify Gmail Configuration
Check your `.env` file in both the root directory and `Database_API` directory:

```env
# Email Configuration
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

### 2. Enable 2-Factor Authentication and Generate App Password
Gmail requires an App Password for third-party applications:

1. Go to your Google Account settings: https://myaccount.google.com/
2. Enable 2-Factor Authentication if not already enabled
3. Navigate to Security > App passwords
4. Generate a new App Password for "Mail"
5. Copy the 16-character password (with spaces)
6. Use this App Password in your `.env` file as `SMTP_PASSWORD`

### 3. Verify Environment Variables
The system now loads environment variables from both locations:
- Root directory `.env`
- `Database_API/.env`

Make sure both files have the correct email configuration.

### 4. Test the Configuration
Run the test script to verify your configuration:

```bash
python test_gmail_otp.py
```

### 5. Common Issues and Solutions

#### SMTP Authentication Error
- **Cause**: Wrong username/password or not using App Password
- **Solution**: Use App Password instead of regular Gmail password

#### Connection Timeout
- **Cause**: Firewall or network issues
- **Solution**: Check your internet connection and firewall settings

#### TLS/SSL Issues
- **Cause**: Outdated SSL certificates
- **Solution**: The updated code now uses proper SSL context for Gmail

### 6. Development Mode
If you still have issues, you can use development mode where OTP codes are shown in the console:

```env
OTP_DEBUG=true
EMAIL_ENABLED=false
```

With this configuration, OTP codes will be displayed in the backend console and frontend alerts.

## Updated Code Features

1. **Improved Error Handling**: Better error messages for common Gmail issues
2. **SSL Context**: Proper SSL context for Gmail connections
3. **Dual .env Loading**: Loads from both root and Database_API directories
4. **Fallback Variables**: Uses EMAIL_* variables if SMTP_* not found

## Testing
After making changes:
1. Restart your backend server
2. Try sending an OTP from the login page
3. Check the backend console for detailed logs