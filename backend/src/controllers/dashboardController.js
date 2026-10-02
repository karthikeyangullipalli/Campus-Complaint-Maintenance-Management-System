const db = require('../config/database');

exports.getStudentDashboard = async (req, res, next) => {
  try {
    const userId = req.user.id;

    // Count complaints by status for this user
    const [stats] = await db.execute(`
      SELECT status, COUNT(*) as count 
      FROM complaints 
      WHERE user_id = ? 
      GROUP BY status
    `, [userId]);

    // Recent complaints
    const [recent] = await db.execute(`
      SELECT c.id, c.complaint_number, c.title, c.status, c.priority, c.created_at,
             cc.name as category_name
      FROM complaints c
      LEFT JOIN complaint_categories cc ON c.category_id = cc.id
      WHERE c.user_id = ?
      ORDER BY c.created_at DESC
      LIMIT 5
    `, [userId]);

    // Totals
    const total = stats.reduce((acc, s) => acc + s.count, 0);
    const open  = stats.filter(s => ['NEW','VERIFIED','ASSIGNED','IN_PROGRESS'].includes(s.status))
                       .reduce((acc, s) => acc + s.count, 0);

    res.status(200).json({
      success: true,
      data: {
        byStatus: stats,
        total,
        open,
        recent
      }
    });
  } catch (err) {
    next(err);
  }
};

exports.getMaintenanceDashboard = async (req, res, next) => {
  try {
    const staffId = req.user.id;

    // Count assigned complaints by status
    const [stats] = await db.execute(`
      SELECT c.status, COUNT(*) as count 
      FROM complaints c
      JOIN complaint_assignments ca ON c.id = ca.complaint_id
      WHERE ca.maintenance_staff_id = ?
      GROUP BY c.status
    `, [staffId]);

    // Recent assigned tasks
    const [tasks] = await db.execute(`
      SELECT c.id, c.complaint_number, c.title, c.status, c.priority, ca.assigned_at,
             CONCAT(l.building, ' - ', IFNULL(l.floor,''), ' ', IFNULL(l.room,'')) as location_name,
             cc.name as category_name
      FROM complaints c
      JOIN complaint_assignments ca ON c.id = ca.complaint_id
      LEFT JOIN locations l ON c.location_id = l.id
      LEFT JOIN complaint_categories cc ON c.category_id = cc.id
      WHERE ca.maintenance_staff_id = ?
      ORDER BY ca.assigned_at DESC
      LIMIT 10
    `, [staffId]);

    res.status(200).json({
      success: true,
      data: {
        byStatus: stats,
        tasks
      }
    });
  } catch (err) {
    next(err);
  }
};

exports.getAdminDashboard = async (req, res, next) => {
  try {
    // Complaints by status
    const [statusStats] = await db.execute(
      'SELECT status, COUNT(*) as count FROM complaints GROUP BY status'
    );

    // Complaints by category — correct table name: complaint_categories
    const [categoryStats] = await db.execute(`
      SELECT cc.name, COUNT(c.id) as count 
      FROM complaint_categories cc 
      LEFT JOIN complaints c ON cc.id = c.category_id 
      WHERE cc.is_active = TRUE
      GROUP BY cc.id, cc.name
      ORDER BY count DESC
    `);

    // Complaints by priority
    const [priorityStats] = await db.execute(
      'SELECT priority, COUNT(*) as count FROM complaints GROUP BY priority'
    );

    // High/Critical count
    const [criticalCount] = await db.execute(
      "SELECT COUNT(*) as count FROM complaints WHERE priority IN ('HIGH','CRITICAL') AND status NOT IN ('CLOSED','REJECTED')"
    );

    // Total users by role
    const [userStats] = await db.execute(
      'SELECT role, COUNT(*) as count FROM users WHERE is_active = TRUE GROUP BY role'
    );

    // Recent complaints (last 10)
    const [recentComplaints] = await db.execute(`
      SELECT c.id, c.complaint_number, c.title, c.status, c.priority, c.created_at,
             u.name as user_name,
             cc.name as category_name
      FROM complaints c
      JOIN users u ON c.user_id = u.id
      LEFT JOIN complaint_categories cc ON c.category_id = cc.id
      ORDER BY c.created_at DESC
      LIMIT 10
    `);

    res.status(200).json({
      success: true,
      data: {
        byStatus: statusStats,
        byCategory: categoryStats,
        byPriority: priorityStats,
        criticalOpen: criticalCount[0].count,
        userStats,
        recent: recentComplaints
      }
    });
  } catch (err) {
    next(err);
  }
};
