// Supplements by Hazel: mobile menu, the Shop dropdown and the scroll reveal. No dependencies.
(function () {
  var header = document.querySelector("header.site");
  var toggle = document.querySelector(".menu-toggle");
  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var open = !header.classList.contains("nav-open");
      header.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Dropdown: click/tap or keyboard opens it; Escape or a click elsewhere closes it.
  document.querySelectorAll(".has-menu").forEach(function (li) {
    var btn = li.querySelector(".drop");
    btn.addEventListener("click", function () {
      var open = !li.classList.contains("open");
      document.querySelectorAll(".has-menu.open").forEach(function (o) { o.classList.remove("open"); o.querySelector(".drop").setAttribute("aria-expanded", "false"); });
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
    li.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
    });
  });
  document.addEventListener("click", function (e) {
    if (e.target.closest(".has-menu")) return;
    document.querySelectorAll(".has-menu.open").forEach(function (o) { o.classList.remove("open"); o.querySelector(".drop").setAttribute("aria-expanded", "false"); });
  });

  // Mark the Shop menu as current on shop and product pages.
  if (document.querySelector("#buy-panel, .product-grid") && /shop|clarity|peri|rosy|hair-skin|perform|bundle|iron/.test(location.pathname)) {
    var d = document.querySelector(".has-menu .drop"); if (d) d.style.fontWeight = "500";
  }

  // Shop page: filter the products by health goal (?goal=energy). Links still work without script.
  var grid = document.querySelector("[data-filterable]");
  if (grid) {
    var LABELS = {};
    document.querySelectorAll(".chip[data-goal]").forEach(function (c) { LABELS[c.dataset.goal] = c.textContent; });
    var applyGoal = function (goal) {
      grid.querySelectorAll(".card").forEach(function (card) {
        card.hidden = !!goal && (" " + card.dataset.goals + " ").indexOf(" " + goal + " ") === -1;
      });
      document.querySelectorAll(".chip[data-goal]").forEach(function (c) { c.setAttribute("aria-current", c.dataset.goal === goal ? "true" : "false"); });
      var note = document.querySelector("[data-goal-note]");
      if (note) { note.hidden = !goal; note.textContent = goal ? "Showing products for " + (LABELS[goal] || goal).toLowerCase() + "." : ""; }
    };
    document.querySelectorAll(".chip[data-goal]").forEach(function (c) {
      c.addEventListener("click", function (e) {
        e.preventDefault();
        var g = c.dataset.goal;
        history.replaceState(null, "", g ? "?goal=" + g + "#products" : location.pathname + "#products");
        applyGoal(g);
      });
    });
    applyGoal(new URLSearchParams(location.search).get("goal") || "");
  }

  // Header tightens once the page has scrolled.
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 24); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  // Big numbers count up the first time they come into view.
  var nums = document.querySelectorAll("[data-count]");
  if (nums.length && "IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var el = en.target, end = parseFloat(el.dataset.count), dec = parseInt(el.dataset.decimals || "0", 10), t0 = null;
        if (!end) return;
        var step = function (t) {
          if (t0 === null) t0 = t;
          var k = Math.min(1, (t - t0) / 1100), eased = 1 - Math.pow(1 - k, 3);
          el.textContent = (end * eased).toFixed(dec);
          if (k < 1) requestAnimationFrame(step); else el.textContent = end.toFixed(dec);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { cio.observe(n); });
  }

  // Content rises in as it scrolls into view.
  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    items.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  items.forEach(function (el) { io.observe(el); });
})();
