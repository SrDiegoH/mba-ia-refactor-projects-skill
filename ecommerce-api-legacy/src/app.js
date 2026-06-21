require('dotenv').config();
const express = require('express');
const { initDb } = require('./config/database');
const checkoutRoutes = require('./routes/checkout.routes');
const financialRoutes = require('./routes/financial.routes');
const userRoutes = require('./routes/user.routes');

const PORT = process.env.PORT || 3000;
const app = express();

app.use(express.json());
app.use('/api', checkoutRoutes);
app.use('/api', financialRoutes);
app.use('/api', userRoutes);

initDb().then(() => {
  app.listen(PORT, () => {
    console.log(`Frankenstein LMS rodando na porta ${PORT}...`);
  });
});
