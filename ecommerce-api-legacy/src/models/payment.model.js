const { run } = require('../config/database');

const create = (enrollmentId, amount, status) =>
  run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)', [enrollmentId, amount, status]);

const deleteByEnrollmentIds = (enrollmentIds) => {
  if (enrollmentIds.length === 0) return Promise.resolve();
  const placeholders = enrollmentIds.map(() => '?').join(', ');
  return run(`DELETE FROM payments WHERE enrollment_id IN (${placeholders})`, enrollmentIds);
};

module.exports = { create, deleteByEnrollmentIds };
