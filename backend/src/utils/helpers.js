/**
 * Generate a unique complaint number in format: CMP-YYYYMMDD-XXXXXX
 */
exports.generateComplaintId = () => {
  const now = new Date();
  const datePart = now.toISOString().slice(0, 10).replace(/-/g, '');
  const random = Math.floor(Math.random() * 900000 + 100000).toString();
  return `CMP-${datePart}-${random}`;
};

/**
 * Format a date to readable string
 */
exports.formatDate = (date) => {
  if (!date) return null;
  const d = new Date(date);
  return d.toISOString().slice(0, 19).replace('T', ' ');
};

/**
 * Remove password_hash from user object before sending to client
 * Schema column is password_hash (not password)
 */
exports.sanitizeUser = (user) => {
  const { password_hash, ...sanitizedUser } = user;
  return sanitizedUser;
};
