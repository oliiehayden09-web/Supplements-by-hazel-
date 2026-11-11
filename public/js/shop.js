// Supplements by Hazel: live prices on product cards, the product page buy box and the basket.
// Data and commerce go through the Wix storefront modules in /js/wix/ (the same ones Perform uses).
//
// In the Hazel store each pack size is its own Wix product (1, 3 and 6 tubs, or 1, 3 and 6 months
// of a bundle), each with its own Subscribe & save plan. The buy box lists those products as the
// pack choices (from the page's data-packs) and runs one product store per pack.
import { createProductDetailStore, ONE_TIME_PLAN } from "/js/wix/product-detail-store.js";
import { fetchProducts } from "/js/wix/catalog.js";
import {
  subscribeCart, getCartState, updateLineQuantity, removeCartLine,
  goToCheckout, setCartOpen,
} from "/js/wix/cart-store.js";

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const sized = (url, w, h) => (url && url.includes("static.wixstatic.com/media/") && !url.includes("/v1/"))
  ? `${url}/v1/fill/w_${w},h_${h},al_c,q_85,enc_auto/image.webp` : url;
const EMAIL = "hello@supplementsbyhazel.com";

/* ---------- live prices on product cards ---------- */
const slots = document.querySelectorAll("[data-price-slug]");
if (slots.length) {
  fetchProducts({ limit: 100 }).then((list) => {
    const bySlug = new Map(list.map((p) => [p.slug, p]));
    slots.forEach((el) => {
      const p = bySlug.get(el.dataset.priceSlug);
      if (!p) { el.textContent = ""; return; }
      el.innerHTML = `${esc(p.price)}${p.compareAtPrice ? `<s>${esc(p.compareAtPrice)}</s>` : ""}`;
    });
    document.querySelectorAll("[data-badge-slug]").forEach((el) => {
      const p = bySlug.get(el.dataset.badgeSlug);
      if (!p) return;
      const out = p.availability === "OUT_OF_STOCK" && !p.preorder;
      const label = out ? "Out of stock" : p.ribbon || (p.compareAtPrice ? "On offer" : p.discountNames?.[0] || "");
      if (!label) return;
      el.textContent = label;
      el.classList.toggle("out", out);
      el.classList.toggle("soft", !out && !p.compareAtPrice && !p.ribbon);
      el.hidden = false;
    });
  }).catch(() => slots.forEach((el) => { el.textContent = ""; }));
}

/* ---------- gallery thumbnails ---------- */
document.querySelectorAll("[data-thumb]").forEach((b) => b.addEventListener("click", () => {
  const main = $("#shop-img");
  if (main) main.src = b.dataset.thumb;
  document.querySelectorAll("[data-thumb]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
}));

/* ---------- buy box ---------- */
const buy = $("#buy-panel");
if (buy) {
  const packs = JSON.parse(buy.dataset.packs || "[]");
  const name = buy.dataset.name || "this product";
  const unit = buy.dataset.unit || "tub";
  const stores = packs.map((p) => createProductDetailStore({ slug: p.slug }));
  let active = 0;
  let subscribing = false;

  const planOf = (s) => (s.plans || []).find((pl) => pl.visible !== false) || null;
  const every = (pl) => {
    if (!pl) return "";
    const f = String(pl.frequency || "MONTH").toLowerCase();
    return pl.interval > 1 ? `every ${pl.interval} ${f}s` : `every ${f}`;
  };
  const savePct = (pl) => { const m = /(\d+)\s*%/.exec(`${pl?.description || ""} ${pl?.name || ""}`); return m ? m[1] : "5"; };

  function choosePack(i) {
    active = i;
    const s = stores[i].getState();
    const plan = planOf(s);
    stores[i].selectPlan(subscribing && plan ? plan.id : ONE_TIME_PLAN);
    if (subscribing && !plan) subscribing = false;
    render();
  }
  function chooseBuyType(sub) {
    subscribing = sub;
    const s = stores[active].getState();
    const plan = planOf(s);
    stores[active].selectPlan(sub && plan ? plan.id : ONE_TIME_PLAN);
    if (sub) stores[active].setQuantity(1);
    render();
  }

  function render() {
    const states = stores.map((st) => st.getState());
    const s = states[active];
    const p = s.product;

    if (states.every((x) => x.notFound)) {
      buy.innerHTML = `<p class="state">${esc(name)} isn't available to buy online right now. Please email <a class="textlink" href="mailto:${EMAIL}">${EMAIL}</a> or call 0117 462 3935.</p>`;
      return;
    }
    if (!p) return; // skeleton stays until the active pack has loaded

    const plan = planOf(s);
    const sub = subscribing && !!plan;
    const outOf = (x) => x.product && !x.canAdd && !x.isPreorder && /stock/i.test(x.blockedReason || "out of stock");

    const packHtml = packs.length > 1 ? `
      <fieldset class="picker"><legend>Choose your supply</legend><div class="choices" role="radiogroup" aria-label="Choose your supply">
        ${packs.map((pk, i) => {
          const x = states[i];
          const price = x.product ? x.product.price : "";
          const out = outOf(x);
          return `<button type="button" class="choice" role="radio" aria-checked="${i === active}" data-pack="${i}" ${x.notFound ? "disabled" : ""}>
            <span class="choice-name">${esc(pk.label)}</span>
            <span class="choice-note">${out ? "Out of stock" : `${esc(price)}${pk.note && i > 0 ? ` · <span class="save">${esc(pk.note)}</span>` : pk.note ? ` · ${esc(pk.note)}` : ""}`}</span>
          </button>`;
        }).join("")}
      </div></fieldset>` : "";

    const planPrice = plan ? (s.variant?.subscriptionPrices?.[plan.id] || plan.price || "") : "";
    const buyTypeHtml = plan && p.allowOneTimePurchase !== false ? `
      <fieldset class="picker"><legend>How to buy</legend><div class="choices two" role="radiogroup" aria-label="How to buy">
        <button type="button" class="choice" role="radio" aria-checked="${!sub}" data-buytype="once">
          <span class="choice-name">One-time purchase</span><span class="choice-note">${esc(s.variant?.price || p.price)}</span>
        </button>
        <button type="button" class="choice" role="radio" aria-checked="${sub}" data-buytype="sub">
          <span class="choice-name">Subscribe &amp; save ${esc(savePct(plan))}%</span><span class="choice-note">${esc(planPrice)} ${esc(every(plan))}</span>
        </button>
      </div></fieldset>` : "";

    const pk = packs[active];
    const subTerms = sub ? `<ul class="sub-terms">
        <li>${esc(pk.label)} of ${esc(name)} delivered ${esc(every(plan))}</li>
        <li>${esc(savePct(plan))}% off every delivery${active > 0 ? `, on top of the ${esc((pk.note || "").replace(/^save\s*/i, "").toLowerCase())} multi-buy saving` : ""}</li>
        <li>No minimum term. Cancel any time</li>
      </ul>` : "";

    const atMax = s.quantity >= s.maxQuantity;
    const struck = sub ? (s.variant?.price || "") : (s.compareAtPrice || "");
    buy.innerHTML = `
      ${packHtml}
      ${buyTypeHtml}
      ${subTerms}
      <div class="buy-price">
        <strong>${esc(s.price)}${sub ? `<small> ${esc(every(plan))}</small>` : ""}</strong>
        ${struck ? `<s aria-label="${sub ? "One-time price" : "Was"} ${esc(struck)}">${esc(struck)}</s>` : ""}
        ${s.remaining != null && s.remaining <= 10 && s.remaining > 0 ? `<span class="stock">Only ${s.remaining} left</span>` : ""}
      </div>
      ${p.discountNames?.length ? `<p class="hint">${p.discountNames.map(esc).join(" · ")}</p>` : ""}
      <div class="buy-row">
        <div class="qty" aria-label="Quantity" ${sub ? "hidden" : ""}>
          <button type="button" data-qty="-1" aria-label="Decrease quantity" ${s.quantity <= 1 ? "disabled" : ""}>–</button>
          <output aria-live="polite">${s.quantity}</output>
          <button type="button" data-qty="1" aria-label="Increase quantity" ${atMax ? "disabled" : ""}>+</button>
        </div>
        <button type="button" class="btn add" data-add ${s.canAdd && !s.adding ? "" : "disabled"}>${s.adding ? "Adding…" : !s.canAdd && outOf(s) ? "Out of stock" : sub ? "Subscribe" : s.isPreorder ? "Pre-order" : "Add to basket"}</button>
      </div>
      ${outOf(s) ? `<p class="hint">This ${unit === "bundle" ? "supply" : "pack"} is out of stock just now. Email <a class="textlink" href="mailto:${EMAIL}?subject=${encodeURIComponent(`${name}: back in stock`)}">${EMAIL}</a> and we'll tell you when it's back.</p>` : s.blockedReason ? `<p class="hint">${esc(s.blockedReason)}</p>` : ""}
      ${s.preorderMessage ? `<p class="hint">${esc(s.preorderMessage)}</p>` : ""}
      ${s.error ? `<p class="err" role="alert">${esc(s.error)}</p>` : ""}
    `;

    // the pack's own photo, once (the page shows the range photo until a pack is chosen)
    if (active > 0 && s.imageUrl) { const img = $("#shop-img"); const src = sized(s.imageUrl, 1000, 1000); if (img && img.getAttribute("src") !== src) img.src = src; }
  }

  buy.addEventListener("click", (e) => {
    const pk = e.target.closest("[data-pack]");
    if (pk && !pk.disabled) { choosePack(Number(pk.dataset.pack)); return; }
    const bt = e.target.closest("[data-buytype]");
    if (bt) { chooseBuyType(bt.dataset.buytype === "sub"); return; }
    const q = e.target.closest("[data-qty]");
    if (q && !q.disabled) { const st = stores[active]; st.setQuantity(st.getState().quantity + Number(q.dataset.qty)); return; }
    const add = e.target.closest("[data-add]");
    if (add && !add.disabled) stores[active].add().catch(() => {});
  });

  stores.forEach((st) => { st.selectPlan(ONE_TIME_PLAN); st.subscribe(render); st.start(); });
}

/* ---------- basket drawer ---------- */
const drawer = $("#cart");
const panel = $("#cart-panel");
let returnFocus = null;

function renderCart() {
  const { cart, busy, error, open } = getCartState();
  const count = cart?.itemCount ?? 0;
  document.querySelectorAll("[data-cart-count]").forEach((el) => { el.textContent = count ? String(count) : ""; });
  document.querySelectorAll("[data-cart-open]").forEach((el) => el.setAttribute("aria-label", count ? `Open basket, ${count} item${count === 1 ? "" : "s"}` : "Open basket"));

  const wasOpen = !drawer.hidden;
  drawer.hidden = !open;
  document.documentElement.classList.toggle("lock", open);
  if (open && !wasOpen) { returnFocus = document.activeElement; setTimeout(() => $("#cart-close").focus(), 0); }
  if (!open && wasOpen && returnFocus) { returnFocus.focus(); returnFocus = null; }

  const lines = cart?.lines ?? [];
  const body = $("#cart-body");
  if (!lines.length) {
    body.innerHTML = `<p class="state">Your basket is empty.</p><div class="cart-empty-links"><a class="btn line" href="/shop.html">Shop the range</a></div>${error ? `<p class="err" role="alert">${esc(error)}</p>` : ""}`;
    $("#cart-foot").hidden = true;
    return;
  }
  body.innerHTML = lines.map((l) => {
    const cap = l.availableQuantity ?? 99999;
    const status = l.status === "OUT_OF_STOCK" ? "Out of stock" : l.status === "PARTIALLY_IN_STOCK" ? `Only ${l.availableQuantity} available` : l.status === "REMOVED_FROM_CATALOG" ? "No longer available" : "";
    return `
      <div class="cart-line">
        ${l.imageUrl ? `<img src="${esc(sized(l.imageUrl, 160, 160))}" alt="" width="72" height="72">` : `<div class="line-ph" aria-hidden="true"></div>`}
        <div class="line-main">
          <p class="line-name">${esc(l.productName)}</p>
          ${l.descriptionLines.map((d) => `<p class="line-desc">${esc(d)}</p>`).join("")}
          ${l.subscription ? `<p class="line-desc line-sub">${esc(l.subscription)}</p>` : ""}
          ${status ? `<p class="err">${esc(status)}</p>` : ""}
          <div class="line-row">
            <div class="qty small">
              <button type="button" data-line-qty="${esc(l.lineItemId)}" data-q="${l.quantity - 1}" aria-label="Decrease quantity" ${busy || l.quantity <= 1 ? "disabled" : ""}>–</button>
              <output>${l.quantity}</output>
              <button type="button" data-line-qty="${esc(l.lineItemId)}" data-q="${l.quantity + 1}" aria-label="Increase quantity" ${busy || l.quantity >= cap ? "disabled" : ""}>+</button>
            </div>
            <button type="button" class="linkbtn" data-remove="${esc(l.lineItemId)}" ${busy ? "disabled" : ""}>Remove</button>
          </div>
        </div>
        <div class="line-price">${esc(l.linePrice)}${l.compareAtLinePrice ? `<s>${esc(l.compareAtLinePrice)}</s>` : ""}</div>
      </div>`;
  }).join("") + (error ? `<p class="err" role="alert">${esc(error)}</p>` : "");

  const rows = [`<div class="sum"><span>Subtotal</span><span>${esc(cart.subtotal)}</span></div>`];
  for (const d of cart.discounts ?? []) rows.push(`<div class="sum"><span>${esc(d.name)}</span><span>−${esc(d.amount)}</span></div>`);
  for (const f of cart.fees ?? []) rows.push(`<div class="sum"><span>${esc(f.name)}</span><span>${esc(f.amount)}</span></div>`);
  if (!cart.pricesIncludeTax) for (const t of cart.taxes ?? []) rows.push(`<div class="sum"><span>${esc(t.name)}</span><span>${esc(t.amount)}</span></div>`);
  if (cart.total) rows.push(`<div class="sum total"><span>Total</span><span>${esc(cart.total)}</span></div>`);
  $("#cart-sums").innerHTML = rows.join("") + `<p class="sum-note">Delivery to the UK and Jersey is added at checkout.</p>`;
  $("#cart-checkout").disabled = busy;
  $("#cart-foot").hidden = false;
}

if (drawer) {
  drawer.addEventListener("click", (e) => {
    if (e.target.closest("[data-cart-close]")) { setCartOpen(false); return; }
    const q = e.target.closest("[data-line-qty]");
    if (q && !q.disabled) { updateLineQuantity(q.dataset.lineQty, Number(q.dataset.q)).catch(() => {}); return; }
    const r = e.target.closest("[data-remove]");
    if (r && !r.disabled) removeCartLine(r.dataset.remove).catch(() => {});
  });
  $("#cart-checkout").addEventListener("click", () => { goToCheckout().catch(() => {}); });
  document.querySelectorAll("[data-cart-open]").forEach((b) => b.addEventListener("click", () => setCartOpen(true)));
  document.addEventListener("keydown", (e) => {
    if (drawer.hidden) return;
    if (e.key === "Escape") { setCartOpen(false); return; }
    if (e.key === "Tab") { // keep focus inside the drawer
      const f = [...panel.querySelectorAll("button:not([disabled]), a[href]")];
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  subscribeCart(renderCart);
  renderCart();
}
