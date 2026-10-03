const db = require('../config/database');
const { generateComplaintId } = require('../utils/helpers');

exports.createComplaint = async (req, res, next) => {
  try {
    const { title, description, category_id, location_id, priority = 'MEDIUM' } = req.body;
    const user_id = req.user.id;
    const complaint_number = generateComplaintId();
    const image_path = req.file ? `/uploads/${req.file.filename}` : null;

    const [result] = await db.execute(
      `INSERT INTO complaints 
      (complaint_number, user_id, category_id, location_id, title, description, priority, status, image_path) 
      VALUES (?, ?, ?, ?, ?, ?, ?, 'NEW', ?)`,
      [complaint_number, user_id, category_id, location_id, title, description, priority, image_path]
    );

    // Log the creation in complaint_updates
    await db.execute(
      'INSERT INTO complaint_updates (complaint_id, updated_by, old_status, new_status, remarks) VALUES (?, ?, ?, ?, ?)',
      [result.insertId, user_id, null, 'NEW', 'Complaint submitted']
    );

    res.status(201).json({
      success: true,
      message: 'Complaint created successfully',
      complaintId: result.insertId,
      complaint_number
    });
  } catch (err) {
    next(err);
  }
};

exports.getComplaints = async (req, res, next) => {
  try {
    const { role, id: userId } = req.user;
    let query = `
      SELECT c.*, cc.name as category_name, 
             CONCAT(l.building, ' - ', IFNULL(l.floor,''), ' ', IFNULL(l.room,'')) as location_name,
             u.name as user_name,
             (SELECT GROUP_CONCAT(mu.name SEPARATOR ', ') 
              FROM complaint_assignments ca 
              JOIN users mu ON ca.maintenance_staff_id = mu.id 
              WHERE ca.complaint_id = c.id) as assigned_staff
      FROM complaints c
      LEFT JOIN complaint_categories cc ON c.category_id = cc.id
      LEFT JOIN locations l ON c.location_id = l.id
      LEFT JOIN users u ON c.user_id = u.id
    `;
    const params = [];

    if (role === 'STUDENT' || role === 'FACULTY') {
      query += ` WHERE c.user_id = ?`;
      params.push(userId);
    } else if (role === 'MAINTENANCE') {
      query += ` INNER JOIN complaint_assignments ca_filter ON c.id = ca_filter.complaint_id WHERE ca_filter.maintenance_staff_id = ?`;
      params.push(userId);
    }

    query += ` ORDER BY c.created_at DESC`;

    const [complaints] = await db.execute(query, params);
    res.status(200).json({ success: true, count: complaints.length, data: complaints });
  } catch (err) {
    next(err);
  }
};

exports.getComplaintById = async (req, res, next) => {
  try {
    const idParam = req.params.id;
    const [complaints] = await db.execute(`
      SELECT c.*, cc.name as category_name,
             CONCAT(l.building, ' - ', IFNULL(l.floor,''), ' ', IFNULL(l.room,'')) as location_name,
             u.name as user_name
      FROM complaints c
      LEFT JOIN complaint_categories cc ON c.category_id = cc.id
      LEFT JOIN locations l ON c.location_id = l.id
      LEFT JOIN users u ON c.user_id = u.id
      WHERE c.id = ? OR c.complaint_number = ?
    `, [idParam, idParam]);

    if (complaints.length === 0) {
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    const complaint = complaints[0];

    // Also fetch updates history using complaint.id (numeric PK)
    const [updates] = await db.execute(`
      SELECT cu.*, u.name as updated_by_name
      FROM complaint_updates cu
      LEFT JOIN users u ON cu.updated_by = u.id
      WHERE cu.complaint_id = ?
      ORDER BY cu.created_at ASC
    `, [complaint.id]);

    res.status(200).json({ success: true, data: { ...complaint, updates } });
  } catch (err) {
    next(err);
  }
};

exports.updateComplaint = async (req, res, next) => {
  try {
    const { title, description, priority } = req.body;
    const [result] = await db.execute(
      'UPDATE complaints SET title = ?, description = ?, priority = ? WHERE id = ? AND status = "NEW"',
      [title, description, priority, req.params.id]
    );

    if (result.affectedRows === 0) {
      return res.status(400).json({ success: false, message: 'Complaint not found or cannot be edited after submission' });
    }

    res.status(200).json({ success: true, message: 'Complaint updated' });
  } catch (err) {
    next(err);
  }
};

exports.deleteComplaint = async (req, res, next) => {
  try {
    const [result] = await db.execute('DELETE FROM complaints WHERE id = ?', [req.params.id]);

    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    res.status(200).json({ success: true, message: 'Complaint deleted' });
  } catch (err) {
    next(err);
  }
};
