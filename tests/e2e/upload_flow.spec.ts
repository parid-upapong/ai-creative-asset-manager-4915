import { test, expect } from '@playwright/test';

/**
 * E2E Test: Full Asset Lifecycle
 * Scenario: A creator uploads a photo, waits for AI tagging, and verifies metadata.
 */
test('Creator can upload asset and see AI generated tags', async ({ page }) => {
  // 1. Login
  await page.goto('/login');
  await page.fill('input[name="email"]', 'tester@creatornexus.ai');
  await page.fill('input[name="password"]', 'Automation123!');
  await page.click('button[type="submit"]');

  // 2. Navigate to Dashboard & Upload
  await expect(page).toHaveURL('/dashboard');
  
  // File upload simulation
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.click('text=Upload New Asset');
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles('./tests/fixtures/sample_stock_photo.jpg');

  // 3. Monitor Progress
  await expect(page.locator('text=Processing with AI...')).toBeVisible();

  // 4. Verify AI Results (Wait up to 30s for processing)
  const tagBadge = page.locator('.tag-badge').first();
  await expect(tagBadge).toBeVisible({ timeout: 30000 });
  
  const tags = await page.locator('.tag-badge').allInnerTexts();
  expect(tags.length).toBeGreaterThan(5); // Ensure AI generated multiple tags
  
  // 5. Save and Finish
  await page.click('text=Approve Metadata');
  await expect(page.locator('text=Asset Ready for Distribution')).toBeVisible();
});