const { run } = require('../config/database');
const userModel = require('../models/user.model');
const enrollmentModel = require('../models/enrollment.model');
const paymentModel = require('../models/payment.model');

const deleteUser = async (id) => {
  await run('BEGIN TRANSACTION');
  try {
    const enrollments = await enrollmentModel.findByUserId(id);
    const enrollmentIds = enrollments.map(e => e.id);
    await paymentModel.deleteByEnrollmentIds(enrollmentIds);
    await enrollmentModel.deleteByUserId(id);
    await userModel.deleteById(id);
    await run('COMMIT');
  } catch (err) {
    await run('ROLLBACK');
    throw err;
  }
};

module.exports = { deleteUser };
