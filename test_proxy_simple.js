const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 8081; // Use a different port to avoid conflicts

// Proxy for OTP endpoints
app.use('/otp', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true
}));

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Test proxy server running on http://localhost:${PORT}`);
});