const db = require('../config/database');

exports.getLocations = async (req, res, next) => {
  try {
    const [locations] = await db.execute('SELECT * FROM locations ORDER BY name ASC');
    res.status(200).json({ success: true, count: locations.length, data: locations });
  } catch (err) {
    next(err);
  }
};

exports.createLocation = async (req, res, next) => {
  try {
    const { name, description } = req.body;
    const [result] = await db.execute('INSERT INTO locations (name, description) VALUES (?, ?)', [name, description]);
    res.status(201).json({ success: true, message: 'Location created', id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateLocation = async (req, res, next) => {
  try {
    const { name, description } = req.body;
    const [result] = await db.execute('UPDATE locations SET name = ?, description = ? WHERE id = ?', [name, description, req.params.id]);
    
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Location not found' });
    }
    res.status(200).json({ success: true, message: 'Location updated' });
  } catch (err) {
    next(err);
  }
};

exports.deleteLocation = async (req, res, next) => {
  try {
    const [result] = await db.execute('DELETE FROM locations WHERE id = ?', [req.params.id]);
    
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Location not found' });
    }
    res.status(200).json({ success: true, message: 'Location deleted' });
  } catch (err) {
    next(err);
  }
};
