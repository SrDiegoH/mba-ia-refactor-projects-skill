const { run } = require('../config/database');

const log = (action) =>
  run("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);

module.exports = { log };
