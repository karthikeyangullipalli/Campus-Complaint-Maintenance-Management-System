const db = require('../config/database');

exports.submitFeedback = async (req, res, next) => {
  try {
    const complaintId = req.params.id;
    const userId = req.user.id;
    const { rating, comments } = req.body;

    const [complaints] = await db.execute('SELECT user_id, status FROM complaints WHERE id = ?', [complaintId]);
    
    if (complaints.length === 0) {
      return res.status(404).json({ success: false, message: 'Complaint not found' });
    }

    if (complaints[0].user_id !== userId) {
      return res.status(403).json({ success: false, message: 'You can only provide feedback for your own complaints' });
    }

    if (complaints[0].status !== 'RESOLVED' && complaints[0].status !== 'CLOSED') {
      return res.status(400).json({ success: false, message: 'Feedback can only be provided for resolved or closed complaints' });
    }

    await db.execute(
      'INSERT INTO feedback (complaint_id, user_id, rating, comments) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE rating = ?, comments = ?',
      [complaintId, userId, rating, comments, rating, comments]
    );

    res.status(201).json({ success: true, message: 'Feedback submitted successfully' });
  } catch (err) {
    next(err);
  }
};

exports.getFeedback = async (req, res, next) => {
  try {
    const complaintId = req.params.id;
    const [feedbacks] = await db.execute(`
      SELECT f.*, u.name as user_name 
      FROM feedback f 
      JOIN users u ON f.user_id = u.id 
      WHERE f.complaint_id = ?
    `, [complaintId]);

    res.status(200).json({ success: true, data: feedbacks });
  } catch (err) {
    next(err);
  }
};
