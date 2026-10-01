const db = require('../config/database');

exports.getStudentDashboard = async (req, res, next) => {
  try {
    const userId = req.user.id;
    const [stats] = await db.execute(`
      SELECT status, COUNT(*) as count 
      FROM complaints 
      WHERE user_id = ? 
      GROUP BY status
    `, [userId]);

    res.status(200).json({ success: true, data: stats });
  } catch (err) {
    next(err);
  }
};

exports.getMaintenanceDashboard = async (req, res, next) => {
  try {
    const staffId = req.user.id;
    const [stats] = await db.execute(`
      SELECT c.status, COUNT(*) as count 
      FROM complaints c
      JOIN complaint_assignments ca ON c.id = ca.complaint_id
      WHERE ca.maintenance_staff_id = ?
      GROUP BY c.status
    `, [staffId]);

    res.status(200).json({ success: true, data: stats });
  } catch (err) {
    next(err);
  }
};

exports.getAdminDashboard = async (req, res, next) => {
  try {
    const [statusStats] = await db.execute('SELECT status, COUNT(*) as count FROM complaints GROUP BY status');
    const [categoryStats] = await db.execute(`
      SELECT cat.name, COUNT(c.id) as count 
      FROM categories cat 
      LEFT JOIN complaints c ON cat.id = c.category_id 
      GROUP BY cat.id
    `);
    const [priorityStats] = await db.execute('SELECT priority, COUNT(*) as count FROM complaints GROUP BY priority');
    
    const [recentComplaints] = await db.execute(`
      SELECT c.id, c.complaint_id_str, c.title, c.status, c.created_at, u.name as user_name
      FROM complaints c
      JOIN users u ON c.user_id = u.id
      ORDER BY c.created_at DESC
      LIMIT 10
    `);

    res.status(200).json({
      success: true,
      data: {
        byStatus: statusStats,
        byCategory: categoryStats,
        byPriority: priorityStats,
        recent: recentComplaints
      }
    });
  } catch (err) {
    next(err);
  }
};
