module.exports = {
  openbmc: {
    baseUrl: 'https://localhost:2443',
    credentials: {
      valid: {
        username: 'root',
        password: '0penBmc',
      },
      invalid: {
        username: 'user',
        password: 'wrongpassword',
      },
    },
    timeouts: {
      implicit: 10000,
      pageLoad: 30000,
    },
  },
};
