# OTP System Fix and Troubleshooting Guide

## Overview
This guide explains how to fix and troubleshoot the OTP (One-Time Password) system in the Decentralized Voting System.

## Common Issues and Solutions

### 1. "Failed to send OTP. Please try again." Error

This error typically occurs due to one of the following reasons:

#### Email Configuration Issues
- **Missing or incorrect email credentials** in the .env file
- **Gmail security settings** preventing login
- **Network connectivity issues**

#### Solution:
1. Check your .env file for correct email configuration:
   ```
   EMAIL_ENABLED=true
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

2. For Gmail, you need to use an **App Password** instead of your regular password:
   - Go to your Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for "Mail"
   - Use this App Password in the SMTP_PASSWORD field

3. Make sure OTP_DEBUG is set to true in your .env file:
   ```
   OTP_DEBUG=true
   ```

### 2. Development Mode OTP Display

In development mode (OTP_DEBUG=true), even if email sending fails, the OTP code will be displayed:
- In the browser console (press F12 to open developer tools)
- In the backend server console
- In an alert dialog

## How to Test OTP Functionality

1. **Start the backend server**:
   ```bash
   cd Database_API
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start the frontend server**:
   ```bash
   node index.js
   ```

3. **Open your browser** and navigate to `http://localhost:8080`

4. **Test OTP**:
   - Go to the registration page
   - Enter an email address
   - Click "Send Email OTP"
   - Check the browser console and backend console for the OTP code
   - Enter the OTP code in the appropriate field

## Testing with the Test Script

You can also run the test script to verify OTP functionality:

```bash
python test_otp_functionality.py
```

## Troubleshooting Steps

1. **Check Backend Console**: Look for error messages when trying to send OTP
2. **Verify .env Configuration**: Make sure all email settings are correct
3. **Test Network Connectivity**: Ensure you can connect to smtp.gmail.com:587
4. **Check Gmail Settings**: Make sure 2FA is enabled and you're using an App Password
5. **Verify OTP_DEBUG**: Ensure OTP_DEBUG=true is set in your .env file

## Fallback Solution

If email sending continues to fail, the system will still work in development mode:
- The OTP code will be displayed in the console
- You can manually enter this code to proceed with registration/login
- This is intended for development and testing purposes only

## Contact Support

If you continue to experience issues, please provide:
1. Screenshots of error messages
2. Backend console output
3. Your .env file configuration (without passwords)