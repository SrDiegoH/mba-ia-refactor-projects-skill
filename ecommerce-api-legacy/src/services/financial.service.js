const financialModel = require('../models/financial.model');

const getFinancialReport = async () => {
  const rows = await financialModel.getFinancialRows();

  const reportMap = new Map();

  rows.forEach(row => {
    if (!reportMap.has(row.course_id)) {
      reportMap.set(row.course_id, { course: row.course_title, revenue: 0, students: [] });
    }

    const courseData = reportMap.get(row.course_id);

    if (row.student_name !== null && row.student_name !== undefined) {
      if (row.status === 'PAID') {
        courseData.revenue += row.amount;
      }
      courseData.students.push({
        student: row.student_name || 'Unknown',
        paid: row.amount || 0
      });
    }
  });

  return Array.from(reportMap.values());
};

module.exports = { getFinancialReport };
