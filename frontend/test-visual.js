const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  console.log('🔍 Testing Homepage...');
  await page.goto('http://localhost:3001');
  await page.waitForLoadState('networkidle');
  
  // Scroll to FAQ
  await page.evaluate(() => {
    document.querySelector('#faq')?.scrollIntoView({ behavior: 'smooth' });
  });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'screenshot-faq.png', fullPage: false });
  console.log('✓ FAQ screenshot saved');

  // Scroll to Testimonials
  await page.evaluate(() => {
    document.querySelector('#testimonials')?.scrollIntoView({ behavior: 'smooth' });
  });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'screenshot-testimonials.png', fullPage: false });
  console.log('✓ Testimonials screenshot saved');

  console.log('🔍 Testing Blog Page...');
  await page.goto('http://localhost:3001/blog');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshot-blog-hero.png', fullPage: false });
  console.log('✓ Blog hero screenshot saved');

  // Test FAQ accordion
  console.log('🔍 Testing FAQ Accordion...');
  await page.goto('http://localhost:3001');
  await page.evaluate(() => {
    document.querySelector('#faq')?.scrollIntoView({ behavior: 'smooth' });
  });
  await page.waitForTimeout(500);
  
  // Click first FAQ item
  const firstFaq = page.locator('.faq-question').first();
  await firstFaq.click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'screenshot-faq-open.png', fullPage: false });
  console.log('✓ FAQ accordion open screenshot saved');

  await browser.close();
  console.log('✅ All screenshots saved!');
})();
