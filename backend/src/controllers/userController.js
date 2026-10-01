const db = require('../config/database');
const { sanitizeUser } = require('../utils/helpers');

exports.getUsers = async (req, res, next) => {
  try {
    const [users] = await db.execute('SELECT id, name, email, role, phone, created_at FROM users');
    res.status(200).json({ success: true, count: users.length, data: users });
  } catch (err) {
    next(err);
  }
};

exports.getUserById = async (req, res, next) => {
  try {
    const [users] = await db.execute('SELECT id, name, email, role, phone, created_at FROM users WHERE id = ?', [req.params.id]);
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
    const { name, phone, role } = req.body;
    const [result] = await db.execute(
      'UPDATE users SET name = ?, phone = ?, role = ? WHERE id = ?',
      [name, phone, role, req.params.id]
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
    const [result] = await db.execute('DELETE FROM users WHERE id = ?', [req.params.id]);
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    res.status(200).json({ success: true, message: 'User deleted' });
  } catch (err) {
    next(err);
  }
};
