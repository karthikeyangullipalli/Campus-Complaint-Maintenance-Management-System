const db = require('../config/database');

// Schema: locations table has columns: id, building, floor, room, description, is_active, created_at
// There is NO 'name' column — location display uses CONCAT(building, floor, room)

exports.getLocations = async (req, res, next) => {
  try {
    const [locations] = await db.execute(
      'SELECT *, CONCAT(building, IFNULL(CONCAT(" - ", floor), ""), IFNULL(CONCAT(", ", room), "")) as display_name FROM locations WHERE is_active = TRUE ORDER BY building, floor, room'
    );
    res.status(200).json({ success: true, count: locations.length, data: locations });
  } catch (err) {
    next(err);
  }
};

exports.createLocation = async (req, res, next) => {
  try {
    const { building, floor, room, description } = req.body;
    if (!building) {
      return res.status(400).json({ success: false, message: 'Building name is required' });
    }
    const [result] = await db.execute(
      'INSERT INTO locations (building, floor, room, description) VALUES (?, ?, ?, ?)',
      [building, floor || null, room || null, description || null]
    );
    res.status(201).json({ success: true, message: 'Location created', id: result.insertId });
  } catch (err) {
    next(err);
  }
};

exports.updateLocation = async (req, res, next) => {
  try {
    const { building, floor, room, description, is_active } = req.body;
    const [result] = await db.execute(
      'UPDATE locations SET building = ?, floor = ?, room = ?, description = ?, is_active = ? WHERE id = ?',
      [building, floor || null, room || null, description || null,
       is_active !== undefined ? is_active : true, req.params.id]
    );
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
    // Soft delete
    const [result] = await db.execute(
      'UPDATE locations SET is_active = FALSE WHERE id = ?',
      [req.params.id]
    );
    if (result.affectedRows === 0) {
      return res.status(404).json({ success: false, message: 'Location not found' });
    }
    res.status(200).json({ success: true, message: 'Location deactivated' });
  } catch (err) {
    next(err);
  }
};
