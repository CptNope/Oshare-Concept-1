/* Oshare site behaviour: live open/closed, mobile nav, pitch notes, menu tools, gallery. No dependencies. */
(function () {
  "use strict";
  var doc = document.documentElement;

  /* ---------- hours (restaurant's own site, 2026-10-08). 0 = Sunday ---------- */
  var HOURS = [[690, 1260], null, [960, 1260], [960, 1260], [960, 1260], [690, 1320], [690, 1320]];
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function fmt(min) {
    var h = Math.floor(min / 60), m = min % 60, ap = h >= 12 ? "PM" : "AM";
    h = h % 12 || 12;
    return h + (m ? ":" + String(m).padStart(2, "0") : "") + " " + ap;
  }
  function lowellNow() {
    try {
      var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
      var o = {}; parts.forEach(function (p) { o[p.type] = p.value; });
      var day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(o.weekday);
      return { day: day, min: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
    } catch (e) { var d = new Date(); return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() }; }
  }
  function status() {
    var n = lowellNow(), today = HOURS[n.day];
    if (today && n.min >= today[0] && n.min < today[1]) {
      var left = today[1] - n.min;
      return { open: true, short: "Open now", detail: left <= 60 ? "Kitchen closes soon, at " + fmt(today[1]) : "Until " + fmt(today[1]) + " tonight" };
    }
    if (today && n.min < today[0]) return { open: false, short: "Closed now", detail: "Opens today at " + fmt(today[0]) };
    for (var i = 1; i <= 7; i++) {
      var d = (n.day + i) % 7;
      if (HOURS[d]) return { open: false, short: "Closed now", detail: "Opens " + (i === 1 ? "tomorrow" : DAYS[d]) + " at " + fmt(HOURS[d][0]) };
    }
    return { open: false, short: "Closed", detail: "" };
  }
  var st = status(), today = lowellNow().day;
  document.querySelectorAll("[data-status]").forEach(function (el) {
    el.dataset.open = String(st.open);
    var b = el.querySelector("b"), s = el.querySelector("[data-status-detail]");
    if (b) b.textContent = st.short;
    if (s) s.textContent = st.detail;
  });
  document.querySelectorAll("[data-day]").forEach(function (el) {
    if (Number(el.dataset.day) === today) el.setAttribute("aria-current", "date");
  });

  /* ---------- mobile nav ---------- */
  var hdr = document.querySelector(".hdr"), mb = document.querySelector(".menu-btn");
  if (hdr && mb) {
    mb.addEventListener("click", function () {
      var open = hdr.dataset.open === "true";
      hdr.dataset.open = String(!open);
      mb.setAttribute("aria-expanded", String(!open));
      mb.setAttribute("aria-label", open ? "Open menu" : "Close menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && hdr.dataset.open === "true") { hdr.dataset.open = "false"; mb.setAttribute("aria-expanded", "false"); mb.focus(); }
    });
  }

  /* ---------- pitch notes toggle ---------- */
  var KEY = "oshare-hide-notes";
  try { if (localStorage.getItem(KEY) === "1") doc.classList.add("hide-notes"); } catch (e) {}
  document.querySelectorAll("[data-notes-toggle]").forEach(function (btn) {
    function label() { var h = doc.classList.contains("hide-notes"); btn.textContent = h ? "Show pitch notes" : "Hide pitch notes"; btn.setAttribute("aria-pressed", String(!h)); }
    label();
    btn.addEventListener("click", function () {
      doc.classList.toggle("hide-notes");
      try { localStorage.setItem(KEY, doc.classList.contains("hide-notes") ? "1" : "0"); } catch (e) {}
      document.querySelectorAll("[data-notes-toggle]").forEach(function (b) { b.dispatchEvent(new Event("relabel")); });
      label();
    });
    btn.addEventListener("relabel", label);
  });

  /* ---------- menu: scrollspy, filters, search ---------- */
  var cats = document.querySelectorAll(".cats a");
  if (cats.length) {
    var sections = Array.prototype.map.call(cats, function (a) { return document.getElementById(a.hash.slice(1)); });
    var setCur = function (id) {
      cats.forEach(function (a) {
        var on = a.hash.slice(1) === id;
        if (on) { a.setAttribute("aria-current", "true"); var r = a.parentElement; var l = a.offsetLeft - r.offsetLeft; if (l < r.scrollLeft || l + a.offsetWidth > r.scrollLeft + r.clientWidth) r.scrollTo({ left: l - 12, behavior: "smooth" }); }
        else a.removeAttribute("aria-current");
      });
    };
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) setCur(en.target.id); });
      }, { rootMargin: "-35% 0px -60% 0px" });
      sections.forEach(function (s) { if (s) io.observe(s); });
    }
    setCur(sections[0] && sections[0].id);

    var q = document.getElementById("menu-search"), noRaw = document.getElementById("f-noraw"), hot = document.getElementById("f-hot");
    var items = document.querySelectorAll(".mitem"), live = document.getElementById("menu-live");
    function apply() {
      var term = (q && q.value || "").trim().toLowerCase(), shown = 0;
      var nr = noRaw && noRaw.getAttribute("aria-pressed") === "true", h = hot && hot.getAttribute("aria-pressed") === "true";
      items.forEach(function (it) {
        var ok = (!term || it.dataset.text.indexOf(term) > -1) && (!nr || it.dataset.raw !== "true") && (!h || Number(it.dataset.hot) > 0);
        it.hidden = !ok; if (ok) shown++;
      });
      document.querySelectorAll(".mcat").forEach(function (sec) {
        var any = sec.querySelector(".mitem:not([hidden])");
        sec.hidden = !any && (term || nr || h) ? true : false;
      });
      if (live) live.textContent = (term || nr || h) ? shown + " dishes match" : "";
      var empty = document.getElementById("menu-empty"); if (empty) empty.hidden = shown > 0;
    }
    [noRaw, hot].forEach(function (b) { if (b) b.addEventListener("click", function () { b.setAttribute("aria-pressed", String(b.getAttribute("aria-pressed") !== "true")); apply(); }); });
    if (q) q.addEventListener("input", apply);
    /* phones: search + filters live behind one toggle so the sticky bar stays one row */
    var mt = document.querySelector(".mtools"), ft = document.querySelector(".ftoggle"), dot = document.querySelector(".ftoggle__dot");
    if (mt && ft) {
      var setOpen = function (open) { mt.dataset.filters = open ? "open" : "closed"; ft.setAttribute("aria-expanded", String(open)); };
      ft.addEventListener("click", function () { var open = mt.dataset.filters !== "open"; setOpen(open); if (open && q) q.focus(); });
      mt.addEventListener("keydown", function (e) { if (e.key === "Escape" && mt.dataset.filters === "open") { setOpen(false); ft.focus(); } });
      var mark = function () { var active = (q && q.value.trim()) || (noRaw && noRaw.getAttribute("aria-pressed") === "true") || (hot && hot.getAttribute("aria-pressed") === "true"); if (dot) dot.hidden = !active; };
      [q, noRaw, hot].forEach(function (el) { if (el) el.addEventListener(el === q ? "input" : "click", mark); });
    }
    var clear = document.getElementById("menu-clear");
    if (clear) clear.addEventListener("click", function () { if (q) q.value = ""; [noRaw, hot].forEach(function (b) { if (b) b.setAttribute("aria-pressed", "false"); }); apply(); if (q) { q.dispatchEvent(new Event("input")); q.focus(); } });
  }

  /* ---------- gallery lightbox ---------- */
  var dlg = document.querySelector("dialog.lightbox");
  if (dlg && dlg.showModal) {
    var tiles = Array.prototype.slice.call(document.querySelectorAll(".gallery button")), idx = 0;
    var im = dlg.querySelector("img"), cap = dlg.querySelector("figcaption span"), count = dlg.querySelector("[data-count]");
    function show(i) {
      idx = (i + tiles.length) % tiles.length;
      var t = tiles[idx], src = t.querySelector("img");
      im.src = src.currentSrc || src.src; im.alt = src.alt; cap.textContent = t.dataset.caption || src.alt;
      count.textContent = (idx + 1) + " / " + tiles.length;
    }
    tiles.forEach(function (t, i) { t.addEventListener("click", function () { show(i); dlg.showModal(); }); });
    dlg.querySelector("[data-prev]").addEventListener("click", function () { show(idx - 1); });
    dlg.querySelector("[data-next]").addEventListener("click", function () { show(idx + 1); });
    dlg.querySelector("[data-close]").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") show(idx - 1); if (e.key === "ArrowRight") show(idx + 1); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () { var t = tiles[idx]; if (t) t.focus(); });
  }

  /* ---------- copy phone (tel: links are unreliable inside an artifact frame) ---------- */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.dataset.copy, done = function () { var o = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = o; }, 1400); };
      if (navigator.clipboard) navigator.clipboard.writeText(v).then(done, function () {});
    });
  });
})();
