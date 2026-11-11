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
