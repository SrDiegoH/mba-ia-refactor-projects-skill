const checkoutService = require('../services/checkout.service');

const checkout = async (req, res) => {
  const { usr, eml, pwd, c_id, card } = req.body;

  if (!usr || !eml || !c_id || !card) {
    return res.status(400).send('Bad Request');
  }

  try {
    const result = await checkoutService.processCheckout({ usr, eml, pwd, c_id, card });
    res.status(200).json(result);
  } catch (err) {
    if (err.status) {
      return res.status(err.status).send(err.message);
    }
    res.status(500).send('Erro interno');
  }
};

module.exports = { checkout };
