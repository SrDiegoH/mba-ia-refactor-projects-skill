const log = (level, message) => {
  console.log(JSON.stringify({ timestamp: new Date().toISOString(), level, message }));
};

module.exports = {
  info: (msg) => log('INFO', msg),
  warn: (msg) => log('WARN', msg),
  error: (msg) => log('ERROR', msg),
};
