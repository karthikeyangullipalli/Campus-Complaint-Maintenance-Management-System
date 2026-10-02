// Load environment variables FIRST, before anything else
require('dotenv').config({ path: require('path').resolve(__dirname, '../../..', '.env') });
// Also try the standard location (backend/.env when run from backend/)
require('dotenv').config();

const mysql = require('mysql2');

const pool = mysql.createPool({
  host:     process.env.DB_HOST || 'localhost',
  port:     parseInt(process.env.DB_PORT || '3306', 10),
  user:     process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD,   // no fallback — must be set in .env
  database: process.env.DB_NAME || 'ccms_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Verify connection on startup and log result (no password in logs)
pool.getConnection((err, connection) => {
  if (err) {
    console.error('[DB] Connection FAILED:', err.message);
    console.error('[DB] Check that backend/.env exists with correct DB_PASSWORD');
  } else {
    console.log(`[DB] Connected to MySQL: ${process.env.DB_NAME || 'ccms_db'} on ${process.env.DB_HOST || 'localhost'}:${process.env.DB_PORT || 3306}`);
    connection.release();
  }
});

module.exports = pool.promise();
