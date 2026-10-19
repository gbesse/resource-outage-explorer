import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
const port = 18770,
  base = `http://127.0.0.1:${port}`,
  server = spawn(
    process.env.PYTHON || 'python3',
    ['-m', 'outage_explorer', 'serve', String(port)],
    { stdio: ['ignore', 'pipe', 'inherit'] },
  );
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {}
    if (server.exitCode !== null) throw Error('server exited');
    if (i === 99) throw Error('server timeout');
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1300, height: 1200 } }),
    errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const lang of ['fr', 'en', 'es']) {
    await page.goto(`${base}/?lang=${lang}`);
    await page.waitForFunction(() => document.getElementById('shortfall').textContent === '6');
    assert.equal(await page.locator('html').getAttribute('lang'), lang);
    assert.equal(await page.locator('#cut').textContent(), '2');
    assert.equal(await page.locator('.upgrade').count(), 3);
    assert.equal(await page.locator('.upgrade.best').count(), 1);
    const event = page.waitForEvent('download');
    await page.locator('#download').click();
    assert.equal((await event).suggestedFilename(), 'resource-outage-evidence.json');
    await page.locator('#outage-budget').selectOption('0');
    await page.locator('#analyze').click();
    await page.waitForFunction(() => document.getElementById('shortfall').textContent === '0');
    assert.equal(await page.locator('#scenarios').textContent(), '1');
    await page.locator('#outage-budget').selectOption('2');
    await page.locator('#investment-budget').selectOption('0');
    await page.locator('#analyze').click();
    await page.waitForFunction(() => document.getElementById('scenarios').textContent === '7');
    assert.equal(await page.locator('.upgrade').count(), 0);
  }
  await page.goto(`${base}/?lang=fr`);
  await page.waitForFunction(() => document.getElementById('shortfall').textContent === '6');
  await mkdir('.local', { recursive: true });
  await page.screenshot({ path: '.local/preview-fr.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.deepEqual(errors, []);
  console.log(
    'FR/EN/ES: outage catalog, cut certificate, upgrade comparison, budgets, export and mobile verified.',
  );
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}
