const { query } = require('../config/database');

const getFinancialReport = async () => {
  const rows = await query(`
    SELECT
      c.id AS course_id,
      c.title AS course_title,
      u.name AS student_name,
      p.amount,
      p.status
    FROM courses c
    LEFT JOIN enrollments e ON e.course_id = c.id
    LEFT JOIN users u ON u.id = e.user_id
    LEFT JOIN payments p ON p.enrollment_id = e.id
    ORDER BY c.id
  `);

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
