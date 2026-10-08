// Contrast audit: every visible text element, light + dark, WCAG 2.2 AA (4.5:1, 3:1 for large text).
// usage: node tools/contrast_audit.js <base-url> <page> [page...]
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
(async () => {
  const [base, ...pages] = process.argv.slice(2);
  const b = await chromium.launch(); let total = 0;
  for (const scheme of ['light', 'dark']) for (const pg of pages) for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme, reducedMotion: 'reduce' });
    await p.route(u => !u.href.startsWith(base), r => r.abort());
    await p.goto(base + pg); await p.waitForTimeout(200);
    const fails = await p.evaluate(() => {
      const parse = c => { const m = c.match(/[\d.]+/g); if (!m) return null; const v = m.map(Number); if (/^color\(srgb/.test(c)) { const [r, g, b, a] = v; return [r * 255, g * 255, b * 255, a ?? 1]; } return v; };
      const lum = ([r, g, b]) => [r, g, b].map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((a, v, i) => a + v * [.2126, .7152, .0722][i], 0);
      const blend = (fg, bg) => { const a = fg[3] ?? 1; return [0, 1, 2].map(i => fg[i] * a + bg[i] * (1 - a)); };
      const bgOf = el => { const stack = []; for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.backgroundImage !== 'none' && !/gradient/.test(s.backgroundImage)) return null; const c = parse(s.backgroundColor); if (c && (c[3] ?? 1) > 0) { stack.push(c); if ((c[3] ?? 1) >= 1) break; } } let bg = [255, 255, 255]; for (const c of stack.reverse()) bg = blend(c, bg); return bg; };
      const out = [];
      document.querySelectorAll('body *').forEach(el => {
        if (!el.offsetParent && getComputedStyle(el).position !== 'fixed') return;
        const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (!own) return;
        const s = getComputedStyle(el); if (s.visibility === 'hidden' || +s.opacity === 0) return;
        if (el.closest('.sr-only,[aria-hidden="true"],svg,.ig,.dir__art,.spec,.desk,.swatch__chip,.cpair,.ratio,.code,.misuse')) return;
        const bg = bgOf(el); if (!bg) return;
        const fg = blend(parse(s.color), bg);
        const L1 = lum(fg), L2 = lum(bg), cr = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
        const size = parseFloat(s.fontSize), bold = +s.fontWeight >= 700, large = size >= 24 || (bold && size >= 18.66);
        if (cr < (large ? 3 : 4.5)) out.push(`${cr.toFixed(2)} ${el.tagName.toLowerCase()}.${String(el.className).slice(0, 30)} "${el.textContent.trim().slice(0, 40)}"`);
      });
      return [...new Set(out)];
    });
    if (fails.length) { console.log(`\n${scheme} ${w} ${pg}: ${fails.length}`); fails.slice(0, 12).forEach(f => console.log('  ' + f)); total += fails.length; }
    await p.close();
  }
  console.log('\nTOTAL FAILS', total); await b.close();
})();
