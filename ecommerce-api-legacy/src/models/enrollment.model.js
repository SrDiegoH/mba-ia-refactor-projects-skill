const { run, query } = require('../config/database');

const create = (userId, courseId) =>
  run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]);

const findByUserId = (userId) =>
  query('SELECT id FROM enrollments WHERE user_id = ?', [userId]);

const deleteByUserId = (userId) =>
  run('DELETE FROM enrollments WHERE user_id = ?', [userId]);

module.exports = { create, findByUserId, deleteByUserId };
