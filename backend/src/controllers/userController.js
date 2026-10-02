const db = require('../config/database');

exports.getUsers = async (req, res, next) => {
  try {
    const { role } = req.query;
    let query = 'SELECT id, name, email, role, department, phone, is_active, created_at FROM users';
    const params = [];
    if (role) {
      query += ' WHERE role = ?';
      params.push(role);
    }
    query += ' ORDER BY name ASC';
    const [users] = await db.execute(query, params);
    res.status(200).json({ success: true, count: users.length, data: users });
  } catch (err) {
    next(err);
  }
};

exports.getUserById = async (req, res, next) => {
  try {
    const [users] = await db.execute(
      'SELECT id, name, email, role, department, phone, is_active, created_at FROM users WHERE id = ?',
      [req.params.id]
    );
    if (users.length === 0) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    res.status(200).json({ success: true, data: users[0] });
  } catch (err) {
    next(err);
  }
};

exports.updateUser = async (req, res, next) => {
  try {
    const { name, phone, department, is_active } = req.body;
    const [result] = await db.execute(
      'UPDATE users SET name = ?, phone = ?, department = ?, is_active = ? WHERE id = ?',
      [name, phone || null, department || null, is_active !== undefined ? is_active : true, req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    res.status(200).json({ success: true, message: 'User updated' });
  } catch (err) {
    next(err);
  }
};

exports.deleteUser = async (req, res, next) => {
  try {
    // Soft delete — deactivate instead of hard delete
    const [result] = await db.execute(
      'UPDATE users SET is_active = FALSE WHERE id = ?',
      [req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    res.status(200).json({ success: true, message: 'User deactivated' });
  } catch (err) {
    next(err);
  }
};
