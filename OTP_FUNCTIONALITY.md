# OTP Functionality Guide

## How OTP Works in This System

The OTP (One-Time Password) system in this voting application works differently for email and phone:

### Email OTP
- When a user requests an email OTP, the system:
  1. Generates a 6-digit code
  2. Stores it in memory with expiration time
  3. Attempts to send it via email (if EMAIL_ENABLED=true)
  4. Returns success response to frontend

### Phone OTP
- When a user requests a phone OTP, the system:
  1. Generates a 6-digit code
  2. Stores it in memory with expiration time
  3. Does NOT automatically send an SMS (requires Twilio configuration)
  4. Returns success response to frontend

## Why You See "Failed to send OTP" Message

The "Failed to send OTP" message appears when:

1. **Network issues** - Cannot connect to the backend
2. **Backend errors** - Server-side exceptions
3. **Incorrect request format** - Malformed JSON data
4. **Frontend response handling** - Not properly parsing the backend response

## How to Fix the Issue

### 1. Check Console for Details
Open browser developer tools (F12) and check the Console tab for error messages.

### 2. Verify Backend is Running
Make sure both servers are running:
- Node.js server (port 8080): `node index.js`
- Python backend (port 8000): `cd Database_API && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`

### 3. Use Development Mode
In development mode, OTP codes are shown in:
- Browser alerts
- Browser console
- Backend console

Ensure `OTP_DEBUG=true` in your `.env` file.

### 4. Test Directly
You can test the OTP endpoints directly using curl or Postman:

```bash
# Send email OTP
curl -X POST http://localhost:8000/otp/send \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Send phone OTP
curl -X POST http://localhost:8000/otp/send \
  -H "Content-Type: application/json" \
  -d '{"contact_number": "1234567890"}'

# Verify OTP
curl -X POST http://localhost:8000/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "otp": "123456"}'
```

## Common Issues and Solutions

### Issue: "Failed to send OTP" for Phone Numbers
**Cause**: The frontend expects the same response format for both email and phone OTPs, but there might be inconsistencies.

**Solution**: 
1. Check that the backend is returning `{ "success": true, "message": "OTP sent" }` for both cases
2. Ensure the frontend properly handles the response

### Issue: OTP Not Received via Email
**Cause**: Gmail SMTP configuration issues.

**Solution**:
1. Verify `SMTP_USERNAME` and `SMTP_PASSWORD` in `.env`
2. Use Gmail App Password instead of regular password
3. Enable 2-Factor Authentication on Gmail account

### Issue: OTP Codes Not Shown in Development Mode
**Cause**: `OTP_DEBUG` not set to true.

**Solution**:
1. Set `OTP_DEBUG=true` in your `.env` file
2. Restart the backend server

## Testing OTP Functionality

Run the test script to verify OTP functionality:
```bash
python test_otp_functionality.py
```

This will test both email and phone OTP sending without requiring the full frontend.

## File Locations

- Backend API: `Database_API/main.py` (routes `/otp/send` and `/otp/verify`)
- Frontend JavaScript: `src/js/login.js`
- Frontend HTML: `src/html/login.html` and `src/html/register.html`
- Environment Config: `.env` and `Database_API/.env`

## Expected Behavior

1. Click "Send OTP" button
2. System generates and stores OTP code
3. For email: Attempts to send via SMTP (if enabled) OR shows in console
4. For phone: Stores OTP in memory (SMS sending requires Twilio setup)
5. User receives OTP via alert/console
6. User enters OTP in verification field
7. System verifies OTP against stored value
8. If valid, proceeds with login/registration