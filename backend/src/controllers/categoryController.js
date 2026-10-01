const db = require('../config/database');

exports.getCategories = async (req, res, next) => {
  try {
    const [categories] = await db.execute('SELECT * FROM categories ORDER BY name ASC');
    res.status(200).json({ success: true, count: categories.length, data: categories });
  } catch (err) {
    next(err);
  }
};

exports.createCategory = async (req, res, next) => {
  try {
    const { name, description } = req.body;
    const [result] = await db.execute('INSERT INTO categories (name, description) VALUES (?, ?)', [name, description]);
    res.status(201).json({ success: true, message: 'Category created', id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateCategory = async (req, res, next) => {
  try {
    const { name, description } = req.body;
    const [result] = await db.execute('UPDATE categories SET name = ?, description = ? WHERE id = ?', [name, description, req.params.id]);
    
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
    const [result] = await db.execute('DELETE FROM categories WHERE id = ?', [req.params.id]);
    
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Category not found' });
    }
    res.status(200).json({ success: true, message: 'Category deleted' });
  } catch (err) {
    next(err);
  }
};
