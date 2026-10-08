// usage: node shoot.js <out-dir> <page.html>:<width>[:full|:vp] ...
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const F = path.join(__dirname, 'fonts/node_modules/@fontsource');
const face = (fam, dir, w) => `@font-face{font-family:'${fam}';font-weight:${w};font-style:normal;font-display:block;src:url(http://127.0.0.1:8765/tools/fonts/node_modules/@fontsource/${dir}/files/${dir}-latin-${w}-normal.woff2) format('woff2')}`;
const css = [500,700,800].map(w=>face('Shippori Mincho B1','shippori-mincho-b1',w)).join('') + [400,500,700].map(w=>face('Zen Kaku Gothic New','zen-kaku-gothic-new',w)).join('');
(async () => {
  const [out, ...jobs] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const job of jobs) {
    const [file, w, mode='full', scheme='light'] = job.split(':');
    const ctx = await b.newContext({ viewport: { width: +w, height: +w < 600 ? 844 : 900 }, deviceScaleFactor: 1, colorScheme: scheme, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
    await p.route(/fonts\.googleapis\.com/, r => r.fulfill({ status: 200, contentType: 'text/css', body: css }));
    await p.route(/fonts\.gstatic\.com/, r => r.abort());
    await p.route(u => !/127\.0\.0\.1|fonts\./.test(u.href), r => r.abort());
    await p.goto('http://127.0.0.1:8765/' + file, { waitUntil: 'load' });
    await p.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); await document.fonts.ready; });
    await p.waitForTimeout(400);
    const ov = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    const name = path.basename(file, '.html') + '-' + w + (scheme==='dark'?'-dark':'') + (mode==='vp'?'-vp':'') + '.png';
    await p.screenshot({ path: path.join(out, name), fullPage: mode !== 'vp' });
    console.log(name, 'overflow:', ov.sw > ov.cw ? `YES ${ov.sw}>${ov.cw}` : 'no', errs.length ? 'ERR ' + errs.slice(0,3).join(' | ') : '');
    await ctx.close();
  }
  await b.close();
})();
