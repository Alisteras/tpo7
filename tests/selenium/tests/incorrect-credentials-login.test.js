const { By } = require('selenium-webdriver');
const { openbmc } = require('../config/openbmc.config.js');
const { TestDriver } = require('../utils/test-driver.js');
const { sleep } = require('../utils/sleep.js');

async function testLoginInvalidCredentials() {
  const driverManager = new TestDriver();
  const driver = await driverManager.setup();

  try {
    await driver.get(openbmc.baseUrl);

    const usernameField = await driver.findElement(By.css('[data-test-id="login-input-username"]'));
    await usernameField.sendKeys(openbmc.credentials.invalid.username);

    const passwordField = await driver.findElement(By.css('[data-test-id="login-input-password"]'));
    await passwordField.sendKeys(openbmc.credentials.invalid.password);

    const loginButton = await driver.findElement(By.css('[data-test-id="login-button-submit"]'));
    await loginButton.click();

    await sleep(3000);

    await driver.navigate().back();

    const errorAlert = await driver.findElement(By.css('div.alert.alert-danger'));

    if (errorAlert) {
      console.log('✓ Ошибка при неверных пользовательских данных');
    } else {
      throw new Error(`Ошибка при неверных пользовательских данных не была найдена`);
    }
  } finally {
    await driverManager.cleanup();
  }
}

module.exports = { testLoginInvalidCredentials };
