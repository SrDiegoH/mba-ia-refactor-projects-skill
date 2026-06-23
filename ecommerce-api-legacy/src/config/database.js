const sqlite3 = require('sqlite3').verbose();
const { hashPassword } = require('../utils/crypto');

const db = new sqlite3.Database(':memory:');

const get = (sql, params = []) => new Promise((resolve, reject) => {
  db.get(sql, params, (err, row) => {
    if (err) reject(err);
    else resolve(row);
  });
});

const query = (sql, params = []) => new Promise((resolve, reject) => {
  db.all(sql, params, (err, rows) => {
    if (err) reject(err);
    else resolve(rows);
  });
});

const run = (sql, params = []) => new Promise((resolve, reject) => {
  db.run(sql, params, function(err) {
    if (err) reject(err);
    else resolve({ lastID: this.lastID, changes: this.changes });
  });
});

const withTransaction = async (fn) => {
  await run('BEGIN TRANSACTION');
  try {
    const result = await fn();
    await run('COMMIT');
    return result;
  } catch (err) {
    await run('ROLLBACK');
    throw err;
  }
};

const initDb = async () => {
  await run('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, pass TEXT)');
  await run('CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)');
  await run('CREATE TABLE enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)');
  await run('CREATE TABLE payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)');
  await run('CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)');

  const seedPass = process.env.SEED_ADMIN_PASS || 'admin-dev-only-change-in-prod';
  const seedHash = await hashPassword(seedPass);
  await run("INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', ?)", [seedHash]);
  await run("INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1)");
  await run("INSERT INTO courses (title, price, active) VALUES ('Docker', 497.00, 1)");
  await run('INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)');
  await run("INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')");
};

module.exports = { get, query, run, withTransaction, initDb };
