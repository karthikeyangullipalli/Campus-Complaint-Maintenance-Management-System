const express = require('express');
const cors = require('cors');
const path = require('path');

const authRoutes = require('./routes/auth');
const complaintRoutes = require('./routes/complaints');
const categoryRoutes = require('./routes/categories');
const locationRoutes = require('./routes/locations');
const userRoutes = require('./routes/users');
const dashboardRoutes = require('./routes/dashboard');
const assignmentRoutes = require('./routes/assignments');

const app = express();

app.use(cors({ origin: process.env.FRONTEND_URL || '*' }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const uploadDir = process.env.UPLOAD_DIR || 'uploads';
app.use('/uploads', express.static(path.join(__dirname, '..', uploadDir)));

app.use('/api/auth', authRoutes);
app.use('/api/complaints', complaintRoutes);
app.use('/api/categories', categoryRoutes);
app.use('/api/locations', locationRoutes);
app.use('/api/users', userRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/assignments', assignmentRoutes);

app.get('/api/health', (req, res) => {
  res.json({ success: true, message: 'CCMS API is running', timestamp: new Date().toISOString() });
});

app.use((req, res, next) => {
  res.status(404).json({ success: false, message: 'API route not found' });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Internal Server Error'
  });
});

module.exports = app;
