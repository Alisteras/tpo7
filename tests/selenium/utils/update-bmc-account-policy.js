const { exec } = require("child_process");

async function updateBmcAccountPolicy(threshlod, duration) {
  const data = JSON.stringify({
    AccountLockoutThreshold: threshlod,
    AccountLockoutDuration: duration,
  });

  const curlCommand = `curl -k --http1.1 -X PATCH "https://localhost:2443/redfish/v1/AccountService/" -H "Content-Type: application/json" -H "Authorization: Basic ${Buffer.from("root:0penBmc").toString("base64")}" -d '${data}' -w "HTTP_STATUS:%{http_code}"`;

  return new Promise((resolve, reject) => {
    exec(curlCommand, (error, stdout, stderr) => {
      if (error) {
        console.error(
          "Ошибка при обновлении политик работы с пользователями:",
          error.message,
        );
        reject(error);
        return;
      }

      const httpStatusMatch = stdout.match(/HTTP_STATUS:(\d+)/);
      const httpStatus = httpStatusMatch ? httpStatusMatch[1] : "unknown";

      console.log(
        `Политики работы с пользователями Успешно Обновлены. Статус: ${httpStatus}`,
      );

      resolve({ stdout, httpStatus });
    });
  });
}

module.exports = { updateBmcAccountPolicy };
