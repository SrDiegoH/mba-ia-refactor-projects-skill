const { run } = require('../config/database');
const courseModel = require('../models/course.model');
const userModel = require('../models/user.model');
const enrollmentModel = require('../models/enrollment.model');
const paymentModel = require('../models/payment.model');
const auditLogModel = require('../models/auditLog.model');
const { hashPassword } = require('../utils/crypto');

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

  const status = card.startsWith('4') ? 'PAID' : 'DENIED';
  if (status === 'DENIED') {
    const err = new Error('Pagamento recusado');
    err.status = 400;
    throw err;
  }

  console.log(`[LOG] Processando pagamento para checkout do curso ${c_id}`);

  await run('BEGIN TRANSACTION');
  try {
    const enrollment = await enrollmentModel.create(user.id, c_id);
    await paymentModel.create(enrollment.lastID, course.price, status);
    await auditLogModel.log(`Checkout curso ${c_id} por ${user.id}`);
    await run('COMMIT');
    console.log(`[LOG] Checkout concluído: ${course.title} para usuário ${user.id}`);
    return { msg: 'Sucesso', enrollment_id: enrollment.lastID };
  } catch (err) {
    await run('ROLLBACK');
    throw err;
  }
};

module.exports = { processCheckout };
