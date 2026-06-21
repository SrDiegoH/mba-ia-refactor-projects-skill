const financialService = require('../services/financial.service');

const getFinancialReport = async (req, res) => {
  try {
    const report = await financialService.getFinancialReport();
    res.json(report);
  } catch (err) {
    res.status(500).send('Erro DB');
  }
};

module.exports = { getFinancialReport };
