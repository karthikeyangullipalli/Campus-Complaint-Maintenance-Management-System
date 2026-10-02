const db = require('../config/database');

// Valid state transitions — matches the implemented complaint lifecycle exactly
// NEW → VERIFIED → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED
// NEW/VERIFIED → REJECTED
// RESOLVED/CLOSED → REOPENED → ASSIGNED (or VERIFIED)
const VALID_TRANSITIONS = {
  'NEW':        ['VERIFIED', 'REJECTED'],
  'VERIFIED':   ['ASSIGNED', 'REJECTED'],
  'ASSIGNED':   ['IN_PROGRESS'],
  'IN_PROGRESS':['RESOLVED'],
  'RESOLVED':   ['CLOSED', 'REOPENED'],
  'CLOSED':     ['REOPENED'],
  'REJECTED':   [],
  'REOPENED':   ['VERIFIED', 'ASSIGNED']
};

// Role-based allowed transitions
const ROLE_ALLOWED_TRANSITIONS = {
  'ADMIN':       ['VERIFIED', 'REJECTED', 'ASSIGNED', 'CLOSED', 'REOPENED'],
  'MAINTENANCE': ['IN_PROGRESS', 'RESOLVED'],
  'STUDENT':     ['REOPENED'],
  'FACULTY':     ['REOPENED']
};

exports.updateStatus = async (req, res, next) => {
  try {
    const complaintId = req.params.id;
    const { new_status, remarks } = req.body;
    const userId   = req.user.id;
    const userRole = req.user.role;

    if (!new_status) {
      return res.status(400).json({ success: false, message: 'new_status is required' });
    }

    // Fetch current status
    const [complaints] = await db.execute(
      'SELECT id, status, user_id FROM complaints WHERE id = ?',
      [complaintId]
    );
    if (complaints.length === 0) {
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    const complaint = complaints[0];
    const currentStatus = complaint.status;

    // Check valid state machine transition
    const allowedNext = VALID_TRANSITIONS[currentStatus] || [];
    if (!allowedNext.includes(new_status)) {
      return res.status(400).json({
        success: false,
        message: `Invalid status transition from ${currentStatus} to ${new_status}. Allowed: [${allowedNext.join(', ')}]`
      });
    }

    // Check role-based permission for this specific transition
    const roleAllowed = ROLE_ALLOWED_TRANSITIONS[userRole] || [];
    if (!roleAllowed.includes(new_status)) {
      return res.status(403).json({
        success: false,
        message: `Role ${userRole} is not permitted to set status to ${new_status}`
      });
    }

    // STUDENT/FACULTY can only reopen their OWN complaint
    if ((userRole === 'STUDENT' || userRole === 'FACULTY') && complaint.user_id !== userId) {
      return res.status(403).json({ success: false, message: 'You can only update your own complaints' });
    }

    // Determine timestamp fields
    const tsFields = {};
    if (new_status === 'RESOLVED') tsFields.resolved_at = new Date();
    if (new_status === 'CLOSED')   tsFields.closed_at   = new Date();

    let updateQuery = 'UPDATE complaints SET status = ?';
    const updateParams = [new_status];

    if (tsFields.resolved_at) {
      updateQuery += ', resolved_at = ?';
      updateParams.push(tsFields.resolved_at);
    }
    if (tsFields.closed_at) {
      updateQuery += ', closed_at = ?';
      updateParams.push(tsFields.closed_at);
    }
    updateQuery += ' WHERE id = ?';
    updateParams.push(complaintId);

    await db.execute(updateQuery, updateParams);

    // Record in audit trail — column is updated_by (matches schema)
    await db.execute(
      'INSERT INTO complaint_updates (complaint_id, updated_by, old_status, new_status, remarks) VALUES (?, ?, ?, ?, ?)',
      [complaintId, userId, currentStatus, new_status, remarks || null]
    );

    res.status(200).json({
      success: true,
      message: `Complaint status updated from ${currentStatus} to ${new_status}`
    });
  } catch (err) {
    next(err);
  }
};
