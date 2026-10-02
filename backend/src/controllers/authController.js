const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../config/database');
const { sanitizeUser } = require('../utils/helpers');

exports.register = async (req, res, next) => {
  try {
    const { name, email, password, role = 'STUDENT', department, phone } = req.body;

    // Only allow STUDENT or FACULTY self-registration
    const allowedRoles = ['STUDENT', 'FACULTY'];
    if (!allowedRoles.includes(role)) {
      return res.status(400).json({ success: false, message: 'Invalid role for self-registration' });
    }

    const [existing] = await db.execute('SELECT id FROM users WHERE email = ?', [email]);
    if (existing.length > 0) {
      return res.status(400).json({ success: false, message: 'Email already registered' });
    }

    const salt = await bcrypt.genSalt(10);
    const password_hash = await bcrypt.hash(password, salt);

    const [result] = await db.execute(
      'INSERT INTO users (name, email, password_hash, role, department, phone) VALUES (?, ?, ?, ?, ?, ?)',
      [name, email, password_hash, role, department || null, phone || null]
    );

    const token = jwt.sign({ id: result.insertId, role }, process.env.JWT_SECRET, {
      expiresIn: process.env.JWT_EXPIRES_IN || '7d'
    });

    res.status(201).json({
      success: true,
      token,
      user: { id: result.insertId, name, email, role, department, phone }
    });
  } catch (err) {
    next(err);
  }
};

exports.login = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const [users] = await db.execute(
      'SELECT * FROM users WHERE email = ? AND is_active = TRUE',
      [email]
    );
    if (users.length === 0) {
      return res.status(401).json({ success: false, message: 'Invalid credentials' });
    }

    const user = users[0];
    // Schema uses password_hash column
    const isMatch = await bcrypt.compare(password, user.password_hash);

    if (!isMatch) {
      return res.status(401).json({ success: false, message: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET, {
      expiresIn: process.env.JWT_EXPIRES_IN || '7d'
    });

    res.status(200).json({
      success: true,
      token,
      user: sanitizeUser(user)
    });
  } catch (err) {
    next(err);
  }
};

exports.getMe = async (req, res, next) => {
  try {
    const [users] = await db.execute(
      'SELECT * FROM users WHERE id = ? AND is_active = TRUE',
      [req.user.id]
    );
    if (users.length === 0) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    res.status(200).json({
      success: true,
      user: sanitizeUser(users[0])
    });
  } catch (err) {
    next(err);
  }
};
