const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

class TestDriver {
  constructor() {
    this.driver = null;
  }

  async setup() {
    console.log('setup');
    let options = new chrome.Options();
    options.setChromeBinaryPath('/usr/bin/chromium');
    options.addArguments(
      '--headless=new',
      '--disable-gpu',
      '--disable-software-rasterizer',
      '--disable-extensions',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--ignore-certificate-errors',
      '--ignore-ssl-errors=true',
      '--window-size=1920,1080',
      '--remote-debugging-port=9222',
    );

    this.driver = await new Builder().forBrowser('chrome').setChromeOptions(options).build();

    await this.driver.manage().setTimeouts({
      implicit: 10000,
      pageLoad: 30000,
      script: 30000,
    });

    return this.driver;
  }

  async cleanup() {
    if (this.driver) {
      await this.driver.quit();
    }
  }
}

module.exports = { TestDriver };
