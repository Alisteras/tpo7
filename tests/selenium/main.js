const { testLoginInvalidCredentials } = require('./tests/incorrect-credentials-login.test');
const { testLoginSuccess } = require('./tests/success-login.test');
const { sleep } = require('./utils/sleep');

const fs = require('fs');
const path = require('path');

function createJUnitReport(testResults, outputPath, suiteName = 'Test Suite') {
  const absolutePath = path.resolve(process.cwd(), outputPath);
  const dir = path.dirname(absolutePath);

  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const timestamp = new Date().toISOString();
  const totalTests = testResults.length;
  const failures = testResults.filter((result) => result.result === 'error').length;

  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<testsuite name="${escapeXml(
    suiteName,
  )}" tests="${totalTests}" failures="${failures}" errors="0" timestamp="${timestamp}">\n`;

  testResults.forEach((result, index) => {
    const testName = result.test || `Test ${index + 1}`;
    const isSuccess = result.result === 'ok';

    xml += `  <testcase name="${escapeXml(testName)}" classname="${escapeXml(suiteName)}">\n`;

    if (!isSuccess) {
      xml += `    <failure message="Test failed">Test "${escapeXml(testName)}" failed</failure>\n`;
    }

    xml += `  </testcase>\n`;
  });

  xml += `</testsuite>`;

  fs.writeFileSync(absolutePath, xml);
  console.log(`JUnit report created: ${absolutePath}`);
}

function escapeXml(unsafe) {
  if (typeof unsafe !== 'string') return unsafe;

  return unsafe.replace(/[<>&'"]/g, (c) => {
    switch (c) {
      case '<':
        return '&lt;';
      case '>':
        return '&gt;';
      case '&':
        return '&amp;';
      case "'":
        return '&apos;';
      case '"':
        return '&quot;';
      default:
        return c;
    }
  });
}

async function runTests() {
  const testResults = [];

  await sleep(5000);
  try {
    await testLoginSuccess();
    testResults.push({ test: 'Login success `correct`', result: 'ok' });
  } catch (e) {
    testResults.push({ test: 'Login success `failed`', result: 'error' });
  }
  await sleep(5000);
  try {
    await testLoginInvalidCredentials();
    testResults.push({ test: 'Login invalid creds `correct`', result: 'ok' });
  } catch (e) {
    testResults.push({ test: 'Login invalid creds `failed`', result: 'error' });
  }

  createJUnitReport(testResults, '../../reports/selenium-junit.xml', 'Selenium UI Tests');
}
runTests().catch(console.error);
