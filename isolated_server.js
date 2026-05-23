const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 8084;  // Different port to avoid conflict

// Direct API route for users endpoint
app.get('/api/users', async (req, res) => {
    try {
        console.log('[Isolated Server] Forwarding users request to backend');
        const headers = {};
        if (req.headers.authorization) {
            headers['Authorization'] = req.headers.authorization;
        }
        
        const response = await axios.get('http://127.0.0.1:8000/api/users', { headers });
        console.log('[Isolated Server] Backend response status:', response.status);
        res.status(response.status).json(response.data);
    } catch (error) {
        console.log('[Isolated Server] Error:', error.message);
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({ error: 'Internal server error' });
        }
    }
});

// Serve static files
app.use(express.static('src'));

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Isolated server running on http://localhost:${PORT}`);
});