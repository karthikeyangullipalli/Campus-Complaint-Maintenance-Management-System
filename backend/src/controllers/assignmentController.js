const db = require('../config/database');

exports.assignComplaint = async (req, res, next) => {
  try {
    const complaintId = req.params.id;
    const { maintenance_staff_id, estimated_completion_date } = req.body;
    const adminId = req.user.id;

    await db.query('START TRANSACTION');

    const [complaints] = await db.execute('SELECT status FROM complaints WHERE id = ?', [complaintId]);
    if (complaints.length === 0) {
      await db.query('ROLLBACK');
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    await db.execute(
      'INSERT INTO complaint_assignments (complaint_id, maintenance_staff_id, assigned_by) VALUES (?, ?, ?)',
      [complaintId, maintenance_staff_id, adminId]
    );

    await db.execute(
      'UPDATE complaints SET status = "ASSIGNED" WHERE id = ?',
      [complaintId]
    );

    await db.execute(
      'INSERT INTO complaint_updates (complaint_id, user_id, old_status, new_status, remarks) VALUES (?, ?, ?, ?, ?)',
      [complaintId, adminId, complaints[0].status, 'ASSIGNED', 'Complaint assigned to maintenance staff']
    );

    await db.query('COMMIT');

    res.status(200).json({ success: true, message: 'Complaint assigned successfully' });
  } catch (err) {
    await db.query('ROLLBACK');
    next(err);
  }
};

exports.getAssignments = async (req, res, next) => {
  try {
    const [assignments] = await db.execute(`
      SELECT ca.*, c.title as complaint_title, u.name as staff_name, a.name as admin_name
      FROM complaint_assignments ca
      JOIN complaints c ON ca.complaint_id = c.id
      JOIN users u ON ca.maintenance_staff_id = u.id
      JOIN users a ON ca.assigned_by = a.id
    `);
    res.status(200).json({ success: true, count: assignments.length, data: assignments });
  } catch (err) {
    next(err);
  }
};

exports.getMyAssignments = async (req, res, next) => {
  try {
    const staffId = req.user.id;
    const [assignments] = await db.execute(`
      SELECT ca.*, c.title as complaint_title, c.status as complaint_status
      FROM complaint_assignments ca
      JOIN complaints c ON ca.complaint_id = c.id
      WHERE ca.maintenance_staff_id = ?
    `, [staffId]);
    res.status(200).json({ success: true, count: assignments.length, data: assignments });
  } catch (err) {
    next(err);
  }
};
