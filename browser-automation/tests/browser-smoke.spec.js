const { test, expect } = require('@playwright/test');

test('opens a page and reads the title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example Domain/);
});
