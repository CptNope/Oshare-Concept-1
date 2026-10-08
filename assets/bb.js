(function () {
  "use strict";
  /* contents scrollspy */
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc ol a[href^='#']"));
  if ("IntersectionObserver" in window && links.length) {
    var map = {};
    links.forEach(function (a) { map[a.hash.slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute("aria-current"); });
        var a = map[en.target.id];
        if (a) { a.setAttribute("aria-current", "true"); var t = a.closest(".toc"); var r = a.getBoundingClientRect(), tr = t.getBoundingClientRect(); if (r.top < tr.top + 60 || r.bottom > tr.bottom - 40) t.scrollTo({ top: a.offsetTop - t.clientHeight / 3, behavior: "smooth" }); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }
  /* mobile contents closes after a pick */
  document.querySelectorAll(".toc-m a").forEach(function (a) { a.addEventListener("click", function () { a.closest("details").open = false; }); });

  /* copy code */
  document.querySelectorAll("[data-copy-code]").forEach(function (b) {
    b.addEventListener("click", function () {
      var pre = document.getElementById(b.dataset.copyCode), txt = pre ? pre.textContent : "";
      var done = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1500); };
      var fallback = function () { var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = "Selected, press Ctrl+C"; };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, fallback); else fallback();
    });
  });

  /* approval checklist: remembered per viewer */
  var KEY = "oshare-approvals-v1", saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
  var boxes = Array.prototype.slice.call(document.querySelectorAll(".check input[type=checkbox]"));
  var bar = document.querySelector(".progress i"), count = document.querySelector("[data-check-count]");
  function sync() {
    var n = boxes.filter(function (b) { return b.checked; }).length;
    if (bar) bar.style.transform = "scaleX(" + (n / boxes.length) + ")";
    if (count) count.textContent = n + " of " + boxes.length + " confirmed";
  }
  boxes.forEach(function (b) {
    if (saved[b.id]) b.checked = true;
    b.addEventListener("change", function () { saved[b.id] = b.checked; try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {} sync(); });
  });
  sync();

  /* replay the brush */
  var rp = document.querySelector("[data-replay]");
  if (rp) rp.addEventListener("click", function () {
    var r = document.getElementById(rp.dataset.replay);
    r.classList.remove("paint"); void r.offsetWidth; r.classList.add("paint");
  });
})();
