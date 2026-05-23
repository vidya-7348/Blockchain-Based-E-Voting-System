const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 8081;  // Different port to avoid conflict

// Simple proxy for testing
app.use('/api', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api': '',  // remove /api prefix
    },
    onProxyReq: function(proxyReq, req, res) {
        console.log('[Debug Proxy] Forwarding API request:', req.method, req.url);
        console.log('[Debug Proxy] Target URL:', 'http://127.0.0.1:8000' + req.url.replace('/api', ''));
    },
    onProxyRes: function(proxyRes, req, res) {
        console.log('[Debug Proxy] API response status:', proxyRes.statusCode);
    },
    onError: function(err, req, res) {
        console.log('[Debug Proxy] API proxy error:', err);
        res.status(504).json({ error: 'API Proxy error: ' + err.message });
    }
}));

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Debug proxy server running on http://localhost:${PORT}`);
});