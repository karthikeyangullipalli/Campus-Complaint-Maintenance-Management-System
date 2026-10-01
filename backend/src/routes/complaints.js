const express = require('express');
const { createComplaint, getComplaints, getComplaintById, updateComplaint, deleteComplaint } = require('../controllers/complaintController');
const { assignComplaint } = require('../controllers/assignmentController');
const { updateStatus } = require('../controllers/statusController');
const { submitFeedback, getFeedback } = require('../controllers/feedbackController');
const { verifyToken, requireRole } = require('../middleware/auth');
const upload = require('../middleware/upload');

const router = express.Router();

router.use(verifyToken);

router.post('/', upload.single('image'), createComplaint);
router.get('/', getComplaints);
router.get('/:id', getComplaintById);
router.put('/:id', updateComplaint);
router.delete('/:id', requireRole('ADMIN'), deleteComplaint);

// Assignments
router.post('/:id/assign', requireRole('ADMIN'), assignComplaint);

// Status
router.put('/:id/status', updateStatus);

// Feedback
router.post('/:id/feedback', submitFeedback);
router.get('/:id/feedback', getFeedback);

module.exports = router;
