# OTP Troubleshooting Guide

## Common Issues and Solutions

### 1. "Failed to fetch" Error

This error typically indicates a network connectivity issue between the frontend and backend servers.

#### Solution Steps:

1. **Verify both servers are running:**
   - Backend server should be running on `http://localhost:8000`
   - Frontend server should be running on `http://localhost:8080`

2. **Restart both servers:**
   - Stop any running servers
   - Start the backend server:
     ```
     cd Database_API
     python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
     ```
   - Start the frontend server:
     ```
     node index.js
     ```

3. **Check Windows Firewall:**
   - Ensure Windows Firewall is not blocking the ports 8000 and 8080
   - You may need to add exceptions for Python and Node.js

4. **Test direct backend access:**
   - Open browser and go to `http://localhost:8000/otp/send`
   - You should see a 405 Method Not Allowed error (this is expected since it only accepts POST)

5. **Test proxy access:**
   - Open browser and go to `http://localhost:8080/otp/send`
   - You should see a 405 Method Not Allowed error (this confirms the proxy is working)

### 2. CORS Issues

If you see CORS-related errors in the browser console:

1. **Check backend CORS configuration:**
   - The backend should have CORS enabled for all origins (*)

2. **Clear browser cache:**
   - Hard refresh the page (Ctrl+F5)
   - Clear browser cache and cookies for localhost

### 3. Network/Firewall Issues

If the servers are running but you still can't connect:

1. **Check port availability:**
   ```
   netstat -ano | findstr :8000
   netstat -ano | findstr :8080
   ```

2. **Kill conflicting processes:**
   ```
   taskkill /PID <process_id> /F
   ```

3. **Try different ports:**
   - Change backend port in [start_backend.bat](file:///c:/Users/Genius/Desktop/voting%20mainfullmainnn0002%20(4)/voting%20mainfullmainnn0002/voting%20mainfullmainnn%20(2)/voting%20mainfullmainnn/voting%20mainfull/voting%20main01/Decentralized-Voting-System-main/start_backend.bat):
     ```
     uvicorn main:app --reload --host 127.0.0.1 --port 8001
     ```
   - Update proxy configuration in [index.js](file:///c:/Users/Genius/Desktop/voting%20mainfullmainnn0002%20(4)/voting%20mainfullmainnn0002/voting%20mainfullmainnn%20(2)/voting%20mainfullmainnn/voting%20mainfull/voting%20main01/Decentralized-Voting-System-main/index.js) accordingly

### 4. Debugging Steps

1. **Check browser console:**
   - Press F12 to open Developer Tools
   - Go to Console tab
   - Look for error messages when clicking "Send OTP"

2. **Check server logs:**
   - Look at the terminal/output where the backend server is running
   - Look for any error messages when requests are made

3. **Test with curl/postman:**
   - Test backend directly:
     ```
     curl -X POST http://localhost:8000/otp/send -H "Content-Type: application/json" -d "{\"email\": \"test@example.com\"}"
     ```

### 5. Development Mode Benefits

Since `OTP_DEBUG=true` is set in your [.env](file:///c:/Users/Genius/Desktop/voting%20mainfullmainnn0002%20(4)/voting%20mainfullmainnn0002/voting%20mainfullmainnn%20(2)/voting%20mainfullmainnn/voting%20mainfull/voting%20main01/Decentralized-Voting-System-main/.env) file, even if email sending fails:
- The OTP code will be displayed in the backend console
- The OTP code will be sent in the response to the frontend
- You can use this code for testing without needing actual email delivery

Look for lines like this in the backend console:
```
============================================================
OTP Generated for test@example.com: 123456
Response: {'success': True, 'message': 'OTP sent', 'dev_otp': '123456', 'note': 'Development mode: OTP shown for testing. Email was attempted.'}
============================================================
```

## Quick Fix Checklist

- [ ] Both frontend and backend servers are running
- [ ] No firewall blocking ports 8000 and 8080
- [ ] Correct proxy configuration in [index.js](file:///c:/Users/Genius/Desktop/voting%20mainfullmainnn0002%20(4)/voting%20mainfullmainnn0002/voting%20mainfullmainnn%20(2)/voting%20mainfullmainnn/voting%20mainfull/voting%20main01/Decentralized-Voting-System-main/index.js)
- [ ] Backend binds to 127.0.0.1, not 0.0.0.0
- [ ] Browser cache cleared
- [ ] Using supported browser (Chrome, Firefox, Edge)

If you continue to experience issues, please share:
1. Browser console errors
2. Backend server logs
3. Frontend server logs
4. Output of `netstat -ano | findstr :8000` and `netstat -ano | findstr :8080`