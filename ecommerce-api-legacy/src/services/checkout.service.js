const { withTransaction } = require('../config/database');
const courseModel = require('../models/course.model');
const userModel = require('../models/user.model');
const enrollmentModel = require('../models/enrollment.model');
const paymentModel = require('../models/payment.model');
const auditLogModel = require('../models/auditLog.model');
const { hashPassword } = require('../utils/crypto');
const logger = require('../utils/logger');

const isValidCard = (number) => {
  const digits = String(number).replace(/\D/g, '').split('').reverse().map(Number);
  if (digits.length < 13) return false;
  const sum = digits.reduce((acc, d, i) => {
    if (i % 2 !== 0) { d *= 2; if (d > 9) d -= 9; }
    return acc + d;
  }, 0);
  return sum % 10 === 0;
};

const processCheckout = async ({ usr, eml, pwd, c_id, card }) => {
  const course = await courseModel.findActiveById(c_id);
  if (!course) {
    const err = new Error('Curso não encontrado');
    err.status = 404;
    throw err;
  }

  let user = await userModel.findByEmail(eml);
  if (!user) {
    const hash = await hashPassword(pwd || '123456');
    const result = await userModel.create(usr, eml, hash);
    user = { id: result.lastID };
  }

  if (!isValidCard(card)) {
    const err = new Error('Pagamento recusado');
    err.status = 400;
    throw err;
  }

  logger.info(`Processando checkout do curso ${c_id}`);

  return await withTransaction(async () => {
    const enrollment = await enrollmentModel.create(user.id, c_id);
    await paymentModel.create(enrollment.lastID, course.price, 'PAID');
    await auditLogModel.log(`Checkout curso ${c_id} por ${user.id}`);
    logger.info(`Checkout concluído: ${course.title} para usuário ${user.id}`);
    return { msg: 'Sucesso', enrollment_id: enrollment.lastID };
  });
};

module.exports = { processCheckout };
