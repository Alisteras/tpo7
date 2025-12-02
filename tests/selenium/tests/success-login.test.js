const { By } = require('selenium-webdriver');
const { openbmc } = require('../config/openbmc.config.js');
const { TestDriver } = require('../utils/test-driver.js');

async function testLoginSuccess() {
  const driverManager = new TestDriver();
  const driver = await driverManager.setup();

  try {
    await driver.get(openbmc.baseUrl);

    const usernameField = await driver.findElement(By.css('[data-test-id="login-input-username"]'));
    await usernameField.sendKeys(openbmc.credentials.valid.username);

    const passwordField = await driver.findElement(By.css('[data-test-id="login-input-password"]'));
    await passwordField.sendKeys(openbmc.credentials.valid.password);

    const loginButton = await driver.findElement(By.css('[data-test-id="login-button-submit"]'));
    await loginButton.click();

    await driver.findElement(By.css('h1'));
    const overviewText = await driver.findElement(By.css('h1')).getText();

    if (overviewText === 'Overview') {
      console.log('✓ Успешный логин, Overview загружен');
    } else {
      throw new Error(`Ожидался Overview, но получен: ${overviewText}`);
    }
  } finally {
    await driverManager.cleanup();
  }
}

module.exports = { testLoginSuccess };
