// Supplements by Hazel: order confirmation page. Wix's checkout sends the buyer back with ?orderId=…;
// the order is read with the buyer's own visitor/member token (Wix only returns it to the
// person who placed it). If it can't be read, the page still confirms the order and points
// to the confirmation email.
import { wixRequest } from "/js/wix/client.js";
import { imgSrc } from "/js/wix/media.js";

const CONTACT = "hello@supplementsbyhazel.com";
const PHONE = "0117 462 3935";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const tr = (v) => (v && typeof v === "object" ? v.translated || v.original || "" : v || "");
const money = (m) => m?.formattedAmount || (m?.amount != null && m.amount !== "" ? `£${Number(m.amount).toFixed(2)}` : "");
const zero = (m) => !m || Number(m.amount || 0) === 0;
const date = (d) => { const t = d ? new Date(d) : null; return t && !isNaN(t) ? t.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) : ""; };
const COUNTRIES = { GB: "United Kingdom", JE: "Jersey" };
const UNIT = { DAY: "day", WEEK: "week", MONTH: "month", YEAR: "year" };
const every = (s) => { const u = UNIT[s?.frequency]; if (!u) return ""; const n = s.interval > 1 ? s.interval : 1; return n > 1 ? `every ${n} ${u}s` : `every ${u}`; };

const head = document.getElementById("ty-intro");
const root = document.getElementById("ty-order");
const orderId = new URLSearchParams(location.search).get("orderId");

function lineHtml(l) {
  const img = l.image ? imgSrc(l.image, 160, 160) : "";
  const desc = (l.descriptionLines || []).map((d) => {
    const name = tr(d.name); const val = tr(d.plainText) || tr(d.colorInfo) || "";
    return val ? `${esc(name)}: ${esc(val)}` : esc(name);
  }).filter(Boolean);
  const sub = l.subscriptionInfo;
  const subText = sub ? [tr(sub.subscriptionOptionTitle), every(sub.subscriptionSettings)].filter(Boolean).join(", ") : "";
  return `<li class="ty-line">
    ${img ? `<img src="${esc(img)}" alt="" width="80" height="80">` : `<div class="line-ph" aria-hidden="true"></div>`}
    <div class="ty-line-main">
      <p class="ty-line-name">${esc(tr(l.productName))}${l.quantity > 1 ? ` × ${l.quantity}` : ""}</p>
      ${desc.map((d) => `<p class="ty-line-desc">${d}</p>`).join("")}
      ${subText ? `<p class="ty-line-desc ty-line-sub">Subscription: ${esc(subText)}</p>` : ""}
    </div>
    <p class="ty-line-price">${esc(money(l.totalPriceAfterTax) || money(l.price))}</p>
  </li>`;
}

function addressHtml(a, who) {
  if (!a) return "";
  const parts = [who, a.addressLine1 || a.addressLine, a.addressLine2, a.city, a.subdivisionFullname && a.country !== "GB" ? a.subdivisionFullname : "", a.postalCode, COUNTRIES[a.country] || a.country].filter(Boolean);
  return parts.map(esc).join("<br>");
}

function render(o) {
  const email = o.buyerInfo?.email || o.billingInfo?.contactDetails?.email || "";
  const subs = (o.lineItems || []).map((l) => l.subscriptionInfo).filter(Boolean);
  head.innerHTML = `Thank you${o.billingInfo?.contactDetails?.firstName ? `, ${esc(o.billingInfo.contactDetails.firstName)}` : ""}. Your order is confirmed${email ? ` and a receipt is on its way to <strong>${esc(email)}</strong>` : ""}.`;

  const ps = o.priceSummary || {};
  const ship = o.shippingInfo;
  const dest = ship?.logistics?.shippingDestination;
  const cd = dest?.contactDetails || o.recipientInfo?.contactDetails;
  const who = cd ? [cd.firstName, cd.lastName].filter(Boolean).join(" ") : "";
  const addr = addressHtml(dest?.address || o.recipientInfo?.address, who);
  const rows = [
    ["Subtotal", money(ps.subtotal)],
    !zero(ps.discount) ? ["Discount", `−${money(ps.discount)}`] : null,
    ["Delivery", ship ? (zero(ps.shipping) ? "Free" : money(ps.shipping)) : ""],
    !zero(ps.tax) && !o.taxIncludedInPrices ? ["Tax", money(ps.tax)] : null,
  ].filter((r) => r && r[1]);

  root.innerHTML = `
    <div class="ty-card">
      <div class="ty-card-head">
        <div><p class="ty-label">Order number</p><p class="ty-number">#${esc(o.number)}</p></div>
        <div><p class="ty-label">Date</p><p>${esc(date(o.purchasedDate || o.createdDate))}</p></div>
        ${o.paymentStatus ? `<div><p class="ty-label">Payment</p><p>${o.paymentStatus === "PAID" ? "Paid" : o.paymentStatus === "PENDING" ? "Processing" : "Received"}</p></div>` : ""}
      </div>
      <ul class="ty-lines">${(o.lineItems || []).map(lineHtml).join("")}</ul>
      <div class="ty-sums">
        ${rows.map(([k, v]) => `<div class="sum"><span>${esc(k)}</span><span>${esc(v)}</span></div>`).join("")}
        <div class="sum total"><span>Total</span><span>${esc(money(ps.total))}</span></div>
        ${o.taxIncludedInPrices && !zero(ps.tax) ? `<p class="sum-note">Includes ${esc(money(ps.tax))} VAT.</p>` : ""}
      </div>
      ${addr || ship?.title ? `<dl class="info-rows ty-info">
        ${addr ? `<div><dt>Delivering to</dt><dd>${addr}</dd></div>` : ""}
        ${ship?.title ? `<div><dt>Delivery</dt><dd>${esc(tr(ship.title))}${ship.logistics?.deliveryTime ? `, ${esc(ship.logistics.deliveryTime)}` : ""}</dd></div>` : ""}
      </dl>` : ""}
    </div>`;
  document.querySelectorAll("[data-ty-sub]").forEach((el) => { el.hidden = !subs.length; });
  if (subs.length) {
    const when = every(subs[0].subscriptionSettings);
    document.querySelectorAll("[data-ty-sub-when]").forEach((el) => { el.textContent = when ? `Your next payment and delivery happen automatically ${when}, starting from today.` : "Your next payment and delivery happen automatically."; });
  }
}

function fallback() {
  head.innerHTML = `Thank you. Your order is confirmed, and your receipt is on its way to the email address you gave at checkout.`;
  root.innerHTML = `<div class="ty-card"><p class="state">Your confirmation email has your order number and full details. If it hasn't arrived within an hour, check your junk folder, or email <a class="textlink" href="mailto:${CONTACT}?subject=${encodeURIComponent("My order")}">${CONTACT}</a> or call ${PHONE}.</p></div>`;
}

if (!orderId) fallback();
else {
  wixRequest(`/ecom/v1/orders/${encodeURIComponent(orderId)}`, { method: "GET" })
    .then((r) => (r?.order ? render(r.order) : fallback()))
    .catch(fallback);
}
