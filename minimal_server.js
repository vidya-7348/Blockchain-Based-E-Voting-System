const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 8083;  // Different port to avoid conflict

// Direct API route for users endpoint
app.get('/api/users', async (req, res) => {
    try {
        console.log('[Minimal Server] Forwarding users request to backend');
        const headers = {};
        if (req.headers.authorization) {
            headers['Authorization'] = req.headers.authorization;
        }
        
        const response = await axios.get('http://127.0.0.1:8000/api/users', { headers });
        console.log('[Minimal Server] Backend response status:', response.status);
        res.status(response.status).json(response.data);
    } catch (error) {
        console.log('[Minimal Server] Error:', error.message);
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({ error: 'Internal server error' });
        }
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Minimal server running on http://localhost:${PORT}`);
});