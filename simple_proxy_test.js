const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 8082;

// Simple proxy that logs everything
app.use('/api', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api': '/api',
    },
    onProxyReq: function(proxyReq, req, res) {
        console.log('[Simple Proxy] Request received:', req.method, req.url);
        console.log('[Simple Proxy] Forwarding to:', 'http://127.0.0.1:8000' + req.url);
    },
    onProxyRes: function(proxyRes, req, res) {
        console.log('[Simple Proxy] Response status:', proxyRes.statusCode);
    },
    onError: function(err, req, res) {
        console.log('[Simple Proxy] Error:', err);
        res.status(500).json({ error: 'Proxy error' });
    }
}));

app.listen(PORT, () => {
    console.log(`Simple proxy server running on http://localhost:${PORT}`);
});