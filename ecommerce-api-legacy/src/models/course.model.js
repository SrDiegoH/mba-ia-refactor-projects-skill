const { get } = require('../config/database');

const findActiveById = (id) => get('SELECT * FROM courses WHERE id = ? AND active = 1', [id]);

module.exports = { findActiveById };
