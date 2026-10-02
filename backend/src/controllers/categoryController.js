const db = require('../config/database');

// Table name: complaint_categories (NOT 'categories')

exports.getCategories = async (req, res, next) => {
  try {
    const [categories] = await db.execute(
      'SELECT * FROM complaint_categories WHERE is_active = TRUE ORDER BY name ASC'
    );
    res.status(200).json({ success: true, count: categories.length, data: categories });
  } catch (err) {
    next(err);
  }
};

exports.createCategory = async (req, res, next) => {
  try {
    const { name, description } = req.body;
    if (!name) {
      return res.status(400).json({ success: false, message: 'Category name is required' });
    }
    const [result] = await db.execute(
      'INSERT INTO complaint_categories (name, description) VALUES (?, ?)',
      [name, description || null]
    );
    res.status(201).json({ success: true, message: 'Category created', id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateCategory = async (req, res, next) => {
  try {
    const { name, description, is_active } = req.body;
    const [result] = await db.execute(
      'UPDATE complaint_categories SET name = ?, description = ?, is_active = ? WHERE id = ?',
      [name, description || null, is_active !== undefined ? is_active : true, req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Category not found' });
    }
    res.status(200).json({ success: true, message: 'Category updated' });
  } catch (err) {
    next(err);
  }
};

exports.deleteCategory = async (req, res, next) => {
  try {
    // Soft delete — set is_active = FALSE
    const [result] = await db.execute(
      'UPDATE complaint_categories SET is_active = FALSE WHERE id = ?',
      [req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Category not found' });
    }
    res.status(200).json({ success: true, message: 'Category deactivated' });
  } catch (err) {
    next(err);
  }
};
