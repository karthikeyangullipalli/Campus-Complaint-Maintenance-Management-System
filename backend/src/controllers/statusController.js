const db = require('../config/database');

const VALID_TRANSITIONS = {
  'NEW': ['VERIFIED', 'REJECTED'],
  'VERIFIED': ['ASSIGNED', 'REJECTED'],
  'ASSIGNED': ['IN_PROGRESS'],
  'IN_PROGRESS': ['RESOLVED'],
  'RESOLVED': ['CLOSED', 'REOPENED'],
  'CLOSED': ['REOPENED'],
  'REJECTED': [],
  'REOPENED': ['VERIFIED', 'ASSIGNED']
};

exports.updateStatus = async (req, res, next) => {
  try {
    const complaintId = req.params.id;
    const { new_status, remarks } = req.body;
    const userId = req.user.id;

    await db.query('START TRANSACTION');

    const [complaints] = await db.execute('SELECT status FROM complaints WHERE id = ? FOR UPDATE', [complaintId]);
    if (complaints.length === 0) {
      await db.query('ROLLBACK');
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    const currentStatus = complaints[0].status;

    if (!VALID_TRANSITIONS[currentStatus] || !VALID_TRANSITIONS[currentStatus].includes(new_status)) {
      await db.query('ROLLBACK');
      return res.status(400).json({ success: false, message: `Invalid status transition from ${currentStatus} to ${new_status}` });
    }

    await db.execute('UPDATE complaints SET status = ? WHERE id = ?', [new_status, complaintId]);

    await db.execute(
      'INSERT INTO complaint_updates (complaint_id, user_id, old_status, new_status, remarks) VALUES (?, ?, ?, ?, ?)',
      [complaintId, userId, currentStatus, new_status, remarks]
    );

    await db.query('COMMIT');

    res.status(200).json({ success: true, message: `Status updated to ${new_status}` });
  } catch (err) {
    await db.query('ROLLBACK');
    next(err);
  }
};
