const express = require('express');
const router = express.Router();
const { getFinancialReport } = require('../controllers/financial.controller');
const { requireAdmin } = require('../middleware/auth');

router.get('/admin/financial-report', requireAdmin, getFinancialReport);

module.exports = router;
