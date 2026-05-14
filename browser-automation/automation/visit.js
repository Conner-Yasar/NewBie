const { chromium } = require('playwright');

async function main() {
  const url = process.argv[2] || process.env.URL || 'https://example.com';
  const screenshotPath = process.argv[3] || process.env.SCREENSHOT || 'artifacts/visit.png';

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 });
  await page.screenshot({ path: screenshotPath, fullPage: true });

  console.log(JSON.stringify({
    url: page.url(),
    title: await page.title(),
    screenshot: screenshotPath,
  }, null, 2));

  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
