const express = require('express');
const router = express.Router();
const { getFinancialReport } = require('../controllers/financial.controller');

router.get('/admin/financial-report', getFinancialReport);

module.exports = router;
