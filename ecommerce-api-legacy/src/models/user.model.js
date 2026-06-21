const { get, run } = require('../config/database');

const findByEmail = (email) => get('SELECT id, name, email FROM users WHERE email = ?', [email]);

const create = (name, email, hashedPassword) =>
  run('INSERT INTO users (name, email, pass) VALUES (?, ?, ?)', [name, email, hashedPassword]);

const deleteById = (id) => run('DELETE FROM users WHERE id = ?', [id]);

module.exports = { findByEmail, create, deleteById };
