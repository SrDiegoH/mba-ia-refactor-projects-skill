const requireAdmin = (req, res, next) => {
  const adminToken = process.env.ADMIN_TOKEN;
  if (!adminToken) {
    console.warn('[WARN] ADMIN_TOKEN não definido. Endpoints admin desprotegidos.');
  }
  const provided = req.headers['x-admin-token'];
  if (!provided || provided !== adminToken) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
};

module.exports = { requireAdmin };
