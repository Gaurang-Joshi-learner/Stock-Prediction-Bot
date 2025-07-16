const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const PORT = 5000;
const path = require('path');
const scriptPath = path.join(__dirname,  'Trading_Bot.py');

// Middleware
app.use(cors());
app.use(express.json()); // built-in body-parser

// ✅ Basic root route to check if backend is running
app.get('/', (req, res) => {
    res.send('Trading Bot Backend is running 🚀');
});

// ✅ Prediction route
app.post('/predict', (req, res) => {
    const ticker = req.body.ticker;
    const timeframe=req.body.timeframe;

    if (!ticker||!timeframe) {
        return res.status(400).json({ error: "Ticker and timeframe is required" });
    }

    const py = spawn('python', ['Trading_Bot.py', ticker,timeframe]);
    

    let result = '';

 py.stdout.on('data', (data) => {
    console.log("Python output:", data.toString());
    result += data.toString();
});

    py.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    py.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        console.log(`Result from Python: ${result}`);
        res.json({ prediction: result.trim() });
    });
});

// ✅ Start the server
app.listen(PORT, () => {
    console.log(`✅ Server listening on: http://localhost:${PORT}`);
});
