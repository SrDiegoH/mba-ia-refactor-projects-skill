const { withTransaction } = require('../config/database');
const userModel = require('../models/user.model');
const enrollmentModel = require('../models/enrollment.model');
const paymentModel = require('../models/payment.model');

const deleteUser = async (id) => {
  await withTransaction(async () => {
    const enrollments = await enrollmentModel.findByUserId(id);
    const enrollmentIds = enrollments.map(e => e.id);
    await paymentModel.deleteByEnrollmentIds(enrollmentIds);
    await enrollmentModel.deleteByUserId(id);
    await userModel.deleteById(id);
  });
};

module.exports = { deleteUser };
