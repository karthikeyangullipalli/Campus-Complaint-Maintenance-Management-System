const express = require('express');
const { getStudentDashboard, getMaintenanceDashboard, getAdminDashboard } = require('../controllers/dashboardController');
const { verifyToken, requireRole } = require('../middleware/auth');

const router = express.Router();

router.use(verifyToken);

router.get('/student', requireRole('STUDENT', 'FACULTY'), getStudentDashboard);
router.get('/maintenance', requireRole('MAINTENANCE'), getMaintenanceDashboard);
router.get('/admin', requireRole('ADMIN'), getAdminDashboard);

module.exports = router;
