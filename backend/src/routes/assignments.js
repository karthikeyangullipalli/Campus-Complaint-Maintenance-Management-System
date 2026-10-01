const express = require('express');
const { getAssignments, getMyAssignments } = require('../controllers/assignmentController');
const { verifyToken, requireRole } = require('../middleware/auth');

const router = express.Router();

router.use(verifyToken);

router.get('/', requireRole('ADMIN'), getAssignments);
router.get('/my', requireRole('MAINTENANCE'), getMyAssignments);

module.exports = router;
