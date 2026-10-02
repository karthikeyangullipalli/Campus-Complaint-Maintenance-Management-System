const db = require('../config/database');

exports.assignComplaint = async (req, res, next) => {
  try {
    const complaintId = req.params.id;
    const { maintenance_staff_id, notes } = req.body;
    const adminId = req.user.id;

    if (!maintenance_staff_id) {
      return res.status(400).json({ success: false, message: 'maintenance_staff_id is required' });
    }

    // Verify the target user is actually MAINTENANCE role
    const [staffRows] = await db.execute(
      'SELECT id, role FROM users WHERE id = ? AND is_active = TRUE',
      [maintenance_staff_id]
    );
    if (staffRows.length === 0) {
      return res.status(404).json({ success: false, message: 'Maintenance staff not found' });
    }
    if (staffRows[0].role !== 'MAINTENANCE') {
      return res.status(400).json({ success: false, message: 'Selected user is not a maintenance staff member' });
    }

    // Fetch current complaint
    const [complaints] = await db.execute(
      'SELECT id, status FROM complaints WHERE id = ?',
      [complaintId]
    );
    if (complaints.length === 0) {
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    const currentStatus = complaints[0].status;
    // Can only assign if VERIFIED or REOPENED
    if (!['VERIFIED', 'REOPENED'].includes(currentStatus)) {
      return res.status(400).json({
        success: false,
        message: `Cannot assign complaint with status ${currentStatus}. Must be VERIFIED or REOPENED.`
      });
    }

    // Insert assignment record
    await db.execute(
      'INSERT INTO complaint_assignments (complaint_id, maintenance_staff_id, assigned_by, notes) VALUES (?, ?, ?, ?)',
      [complaintId, maintenance_staff_id, adminId, notes || null]
    );

    // Update complaint status to ASSIGNED
    await db.execute(
      'UPDATE complaints SET status = "ASSIGNED" WHERE id = ?',
      [complaintId]
    );

    // Record in audit trail — column is updated_by (matches schema)
    await db.execute(
      'INSERT INTO complaint_updates (complaint_id, updated_by, old_status, new_status, remarks) VALUES (?, ?, ?, ?, ?)',
      [complaintId, adminId, currentStatus, 'ASSIGNED', `Assigned to maintenance staff (ID: ${maintenance_staff_id})`]
    );

    res.status(200).json({ success: true, message: 'Complaint assigned successfully' });
  } catch (err) {
    next(err);
  }
};

exports.getAssignments = async (req, res, next) => {
  try {
    const [assignments] = await db.execute(`
      SELECT ca.id, ca.assigned_at, ca.notes,
             c.id as complaint_id, c.complaint_number, c.title as complaint_title, c.status as complaint_status,
             staff.name as staff_name, staff.email as staff_email,
             admin.name as assigned_by_name
      FROM complaint_assignments ca
      JOIN complaints c ON ca.complaint_id = c.id
      JOIN users staff ON ca.maintenance_staff_id = staff.id
      JOIN users admin ON ca.assigned_by = admin.id
      ORDER BY ca.assigned_at DESC
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
      SELECT ca.id, ca.assigned_at, ca.notes,
             c.id as complaint_id, c.complaint_number, c.title, c.description,
             c.status, c.priority,
             CONCAT(l.building, ' - ', IFNULL(l.floor,''), ' ', IFNULL(l.room,'')) as location_name,
             cc.name as category_name
      FROM complaint_assignments ca
      JOIN complaints c ON ca.complaint_id = c.id
      LEFT JOIN locations l ON c.location_id = l.id
      LEFT JOIN complaint_categories cc ON c.category_id = cc.id
      WHERE ca.maintenance_staff_id = ?
      ORDER BY ca.assigned_at DESC
    `, [staffId]);
    res.status(200).json({ success: true, count: assignments.length, data: assignments });
  } catch (err) {
    next(err);
  }
};
