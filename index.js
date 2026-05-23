const express = require('express');
const path = require('path');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { add_candidate, set_voting_dates } = require('./Database_API/blockchain');

// For making HTTP requests to backend
const axios = require('axios');

const app = express();
const PORT = 8080;  // Frontend server port
const SECRET_KEY = process.env.SECRET_KEY || 'fallback_secret_key';

// Direct API route for users endpoint - placed at the very beginning
// app.get('/api/users', async (req, res) => {
//     try {
//         console.log('[Direct API] Forwarding users request to backend');
//         const headers = {};
//         if (req.headers.authorization) {
//             headers['Authorization'] = req.headers.authorization;
//         }
//         
//         const response = await axios.get('http://127.0.0.1:8000/api/users', { headers });
//         console.log('[Direct API] Backend response status:', response.status);
//         res.status(response.status).json(response.data);
//     } catch (error) {
//         console.log('[Direct API] Error:', error.message);
//         if (error.response) {
//             res.status(error.response.status).json(error.response.data);
//         } else {
//             res.status(500).json({ error: 'Internal server error' });
//         }
//     }
// });

// Direct API route for candidates endpoint - placed at the very beginning
// app.get('/api/candidates', async (req, res) => {
//     try {
//         console.log('[Direct API] Forwarding candidates request to backend');
//         const headers = {};
//         if (req.headers.authorization) {
//             headers['Authorization'] = req.headers.authorization;
//         }
//         
//         const response = await axios.get('http://127.0.0.1:8000/api/candidates', { headers });
//         console.log('[Direct API] Backend response status:', response.status);
//         res.status(response.status).json(response.data);
//     } catch (error) {
//         console.log('[Direct API] Error:', error.message);
//         if (error.response) {
//             res.status(error.response.status).json(error.response.data);
//         } else {
//             res.status(500).json({ error: 'Internal server error' });
//         }
//     }
// });

// Direct API route for results endpoint - placed at the very beginning
// app.get('/api/results', async (req, res) => {
//     try {
//         console.log('[Direct API] Forwarding results request to backend');
//         const headers = {};
//         if (req.headers.authorization) {
//             headers['Authorization'] = req.headers.authorization;
//         }
//         
//         const response = await axios.get('http://127.0.0.1:8000/api/results', { headers });
//         console.log('[Direct API] Backend response status:', response.status);
//         res.status(response.status).json(response.data);
//     } catch (error) {
//         console.log('[Direct API] Error:', error.message);
//         if (error.response) {
//             res.status(error.response.status).json(error.response.data);
//         } else {
//             res.status(500).json({ error: 'Internal server error' });
//         }
//     }
// });

// Direct API route for user results endpoint - placed at the very beginning
// app.get('/api/user/results', async (req, res) => {
//     try {
//         console.log('[Direct API] Forwarding user results request to backend');
//         const headers = {};
//         if (req.headers.authorization) {
//             headers['Authorization'] = req.headers.authorization;
//         }
//         
//         const response = await axios.get('http://127.0.0.1:8000/api/user/results', { headers });
//         console.log('[Direct API] Backend response status:', response.status);
//         res.status(response.status).json(response.data);
//     } catch (error) {
//         console.log('[Direct API] Error:', error.message);
//         if (error.response) {
//             res.status(error.response.status).json(error.response.data);
//         } else {
//             res.status(500).json({ error: 'Internal server error' });
//         }
//     }
// });

// Proxy middleware must be defined BEFORE body parsing middleware
const { createProxyMiddleware } = require('http-proxy-middleware');

// Proxy for OTP, register, and login endpoints
app.use('/otp', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        console.log('[Proxy] Forwarding OTP request to backend');
    },
    onProxyRes: (proxyRes, req, res) => {
        console.log('[Proxy] Received response from backend for OTP request');
    }
}));

// Proxy for register endpoint
app.use('/register', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        console.log('[Proxy] Forwarding register request to backend');
    }
}));

// Proxy for login endpoint
app.use('/login', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        console.log('[Proxy] Forwarding login request to backend');
    }
}));

// Specific proxies for API endpoints (ORDER MATTERS - these must come before the general /api proxy)
app.use('/api/voting-dates', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api/voting-dates': '/voting-dates'
    }
}));

// Proxy for candidates endpoint
app.use('/api/candidates', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api/candidates': '/candidates'
    },
    onError: (err, req, res) => {
        console.log('[Proxy Error] Candidates endpoint error:', err);
        res.status(500).json({ error: 'Proxy error: ' + err.message });
    }
}));

// Proxy for vote endpoint
app.use('/api/vote', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api/vote': '/vote'
    },
    onError: (err, req, res) => {
        console.log('[Proxy Error] Vote endpoint error:', err);
        res.status(500).json({ error: 'Proxy error: ' + err.message });
    }
}));

// Specific proxy for user results endpoint
app.use('/api/user/results', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api/user/results': '/api/user/results'
    }
}));

// Proxy for results endpoint (admin)
app.use('/api/results', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
        '^/api/results': '/api/results'
    }
}));

// General proxy for other API endpoints (THIS MUST COME LAST)
app.use('/api', createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    onError: (err, req, res) => {
        console.log('[Proxy Error] API endpoint error:', err);
        res.status(500).json({ error: 'Proxy error: ' + err.message });
    }
}));

// Middleware (must be defined AFTER proxy middleware)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the "uploads" directory
app.use('/uploads', express.static('uploads'));

// Serve static files from the "src/dist" directory
app.use('/dist', express.static('src/dist'));

// Security headers
app.use((req, res, next) => {
    // Content Security Policy
    res.header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-src 'none'; object-src 'none'");
    // Prevent XSS
    res.header('X-Content-Type-Options', 'nosniff');
    // Prevent clickjacking
    res.header('X-Frame-Options', 'DENY');
    // XSS protection
    res.header('X-XSS-Protection', '1; mode=block');
    // CORS
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    next();
});

// Authentication middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.sendStatus(401);
    }
    
    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) {
            return res.sendStatus(403);
        }
        req.user = user;
        next();
    });
};

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'choose_type.html'));
});

// Serve HTML files
app.get('/login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'login.html'));
});

app.get('/register.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'register.html'));
});

app.get('/admin.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'admin.html'));
});

app.get('/admin_login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'admin_login.html'));
});

app.get('/index.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'index.html'));
});

app.get('/voting.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'voting.html'));
});

app.get('/result.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'result.html'));
});

app.get('/choose_type.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'choose_type.html'));
});

app.get('/test_fetch.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'test_fetch.html'));
});

app.get('/test_otp_functionality.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'test_otp_functionality.html'));
});

app.get('/test_otp_simple.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'test_otp_simple.html'));
});

app.get('/debug_fetch.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'debug_fetch.html'));
});

app.get('/detailed_debug.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'detailed_debug.html'));
});

app.get('/test_result_page.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'test_result_page.html'));
});

// Serve static files (this should be after API routes to avoid conflicts)
// Serve only specific directories and file types to avoid conflicts with API routes
app.use('/css', express.static('src/css'));
app.use('/js', express.static('src/js'));
app.use('/images', express.static('src/images'));

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});