// Supplements by Hazel: customer account page. Log in / sign up on our own form, then the member's
// subscription, orders, details and delivery address.
// Session and login run through the Wix members modules in /js/wix/ (installed on the site);
// every data call goes through ./client.js with the member's own token.
import { subscribeMember, getMemberState, login, register, verifyEmail, logout } from "/js/wix/member-store.js";
import { wixRequest } from "/js/wix/client.js";

const root = document.getElementById("account");
const intro = document.getElementById("account-intro");
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const CONTACT = "hello@supplementsbyhazel.com";
const mail = (subject) => `mailto:${CONTACT}?subject=${encodeURIComponent(subject)}`;
const tr = (v) => (v && typeof v === "object" ? v.translated || v.original || "" : v || "");
const money = (m) => m?.formattedAmount || (m?.amount ? `£${Number(m.amount).toFixed(2)}` : "");
const date = (d) => { const t = d ? new Date(d) : null; return t && !isNaN(t) ? t.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) : ""; };
const COUNTRIES = { GB: "United Kingdom", JE: "Jersey" };

/* ---------- logged-out: the login / sign-up form ---------- */
let mode = "login"; // login | signup | verify | pending
let busy = false;
let formError = "";
let lastEmail = "";

function renderForm() {
  intro.textContent = "Log in to see your subscription, your orders and your delivery address.";
  if (mode === "pending") {
    root.innerHTML = `<div class="auth-card"><h2>Thanks for signing up</h2>
      <p>Your account is waiting for approval. You'll be able to log in once it's approved.</p>
      <button type="button" class="linkbtn" data-mode="login">Back to log in</button></div>`;
    return;
  }
  if (mode === "verify") {
    root.innerHTML = `<form class="auth-card" data-form="verify" novalidate>
      <h2>Check your email</h2>
      <p>We've sent a code to ${esc(lastEmail)}. Enter it below to finish.</p>
      <label class="field"><span>Code</span><input name="code" inputmode="numeric" autocomplete="one-time-code" required></label>
      ${formError ? `<p class="err" role="alert">${esc(formError)}</p>` : ""}
      <button type="submit" class="btn wide" ${busy ? "disabled" : ""}>${busy ? "Checking…" : "Confirm"}</button>
    </form>`;
    root.querySelector("input").focus();
    return;
  }
  const signup = mode === "signup";
  root.innerHTML = `<div class="auth-grid">
    <form class="auth-card" data-form="${mode}" novalidate>
      <div class="auth-tabs" role="tablist" aria-label="Log in or create an account">
        <button type="button" role="tab" aria-selected="${!signup}" data-mode="login">Log in</button>
        <button type="button" role="tab" aria-selected="${signup}" data-mode="signup">Create account</button>
      </div>
      ${signup ? `<div class="field-row">
        <label class="field"><span>First name</span><input name="firstName" autocomplete="given-name"></label>
        <label class="field"><span>Last name</span><input name="lastName" autocomplete="family-name"></label>
      </div>` : ""}
      <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email" value="${esc(lastEmail)}" required></label>
      <label class="field"><span>Password</span><input name="password" type="password" autocomplete="${signup ? "new-password" : "current-password"}" minlength="4" required></label>
      ${signup ? `<label class="nl-choice"><input type="checkbox" name="subscribe" class="nl-checkbox"><span>Email me news and offers from Supplements by Hazel. You can unsubscribe at any time.</span></label>` : ""}
      ${formError ? `<p class="err" role="alert">${esc(formError)}</p>` : ""}
      <button type="submit" class="btn wide" ${busy ? "disabled" : ""}>${busy ? "Please wait…" : signup ? "Create account" : "Log in"}</button>
      ${signup ? "" : `<p class="hint">Forgotten your password? Email <a class="textlink" href="${mail("Password reset")}">${CONTACT}</a> and we'll help.</p>`}
    </form>
    <aside class="auth-aside">
      <h2>With an account you can</h2>
      <ul class="sub-terms">
        <li>See your Subscribe &amp; save plan</li>
        <li>Check your past orders</li>
        <li>Keep your delivery address up to date</li>
      </ul>
      <p class="hint">You don't need an account to buy. Checkout works without one.</p>
    </aside>
  </div>`;
}

async function submitForm(form) {
  const data = Object.fromEntries(new FormData(form));
  formError = "";
  if (form.dataset.form !== "verify") {
    lastEmail = String(data.email || "").trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(lastEmail)) { formError = "Enter a valid email address."; renderForm(); return; }
    if (!data.password) { formError = "Enter your password."; renderForm(); return; }
  }
  busy = true; renderForm();
  let result;
  try {
    if (form.dataset.form === "verify") result = await verifyEmail(String(data.code || "").trim());
    else if (form.dataset.form === "signup") {
      const profile = {};
      if (data.firstName) profile.firstName = String(data.firstName).trim();
      if (data.lastName) profile.lastName = String(data.lastName).trim();
      if (data.subscribe) profile.subscription = true; // marketing consent, only when ticked
      result = await register(lastEmail, String(data.password), profile);
    } else result = await login(lastEmail, String(data.password));
  } catch (e) {
    result = { state: "FAILURE", error: e instanceof Error ? e.message : String(e) };
  }
  busy = false;
  if (result.state === "EMAIL_VERIFICATION_REQUIRED") mode = "verify";
  else if (result.state === "OWNER_APPROVAL_REQUIRED") mode = "pending";
  else if (result.state === "FAILURE") formError = friendly(result);
  if (result.state !== "SUCCESS") renderForm();
  // SUCCESS: the store refreshes the session and render() shows the account.
}

function friendly(r) {
  switch (r.errorCode) {
    case "invalidPassword": return "That password isn't right. Try again.";
    case "invalidEmail": return "We can't find an account with that email. Create one instead?";
    case "emailAlreadyExists": return "There's already an account with that email. Log in instead.";
    case "resetPassword": return `Your password needs resetting. Email ${CONTACT} and we'll help.`;
    default: return r.error || "Something went wrong. Please try again.";
  }
}

/* ---------- logged-in: the account ---------- */
let data = null; // { profile, subs, orders } once loaded
let loadingFor = null;
let editing = false;
let saveError = "";
let saving = false;

async function loadAccount(memberId) {
  loadingFor = memberId;
  let profile = null;
  try { profile = (await wixRequest("/members/v1/members/my", { query: { fieldsets: "FULL" } }))?.member ?? null; } catch { /* shown as unavailable */ }
  const contactId = profile?.contactId || getMemberState().member?.contactId || "";
  const [s, o] = await Promise.allSettled([
    wixRequest("/ecom/subscription-contracts/v1/subscription-contracts/query", { method: "POST", body: { query: { filter: { "buyerInfo.contactId": { $eq: contactId } }, cursorPaging: { limit: 20 } } } }),
    wixRequest("/ecom/v1/orders/search", { method: "POST", body: { search: { cursorPaging: { limit: 50 } } } }),
  ]);
  // only ever this customer's own records
  const own = (list) => (list || []).filter((x) => x?.buyerInfo?.contactId === contactId);
  const orders = contactId && o.status === "fulfilled" ? own(o.value?.orders) : null;
  // Wix doesn't let customers read subscription records directly, so when that read is refused
  // the subscription is built from the customer's own orders (each subscription order names its plan).
  const subs = contactId && s.status === "fulfilled" ? own(s.value?.subscriptionContracts) : orders ? subsFromOrders(orders) : null;
  if (loadingFor !== memberId) return;
  data = { profile, subs, orders };
  render();
}

function subsFromOrders(orders) {
  const byId = new Map();
  for (const o of [...orders].sort((a, b) => String(a.createdDate).localeCompare(String(b.createdDate)))) {
    for (const l of o.lineItems || []) {
      const info = l.subscriptionInfo;
      if (!info?.id) continue;
      const c = byId.get(info.id) || { id: info.id, createdDate: o.createdDate, payments: 0 };
      c.subscriptionSettings = info.subscriptionSettings || c.subscriptionSettings;
      c.lineItems = [l];
      c.priceSummary = o.priceSummary;
      c.shippingInfo = o.shippingInfo;
      c.lastOrder = o.createdDate;
      c.payments += 1;
      byId.set(info.id, c);
    }
  }
  return [...byId.values()].reverse();
}

const frequency = (st) => {
  const n = st?.interval || 1, f = String(st?.frequency || "MONTH").toLowerCase();
  return n === 1 ? `Every ${f}` : `Every ${n} ${f}s`;
};
const addressText = (a) => a ? [a.addressLine || [a.streetAddress?.number, a.streetAddress?.name].filter(Boolean).join(" "), a.addressLine2, a.city, a.postalCode, COUNTRIES[a.country] || a.country].filter(Boolean).map(esc).join("<br>") : "";

function subsHtml(subs) {
  if (subs === null) return `<p class="state">We can't show your subscription here just now. Your confirmation email has the details, or email <a class="textlink" href="${mail("My subscription")}">${CONTACT}</a>.</p>`;
  if (!subs.length) return `<p class="state">You don't have a subscription yet.</p><a class="btn line" href="/shop.html">Subscribe &amp; save</a>`;
  return subs.map((c) => {
    const items = (c.lineItems || []).map((l) => `${esc(tr(l.productName))}${l.quantity > 1 ? ` × ${l.quantity}` : ""}`).join(", ") || "Your subscription";
    const ship = c.shippingInfo?.logistics?.shippingDestination?.address || c.recipientInfo?.address;
    return `<div class="sub-card">
      <div class="sub-head"><h3>${esc(tr(c.subscriptionTitle) || "Subscribe & save")}</h3><span class="tag">Subscription</span></div>
      <dl class="info-rows">
        <div><dt>What you get</dt><dd>${items}</dd></div>
        <div><dt>How often</dt><dd>${esc(frequency(c.subscriptionSettings))}</dd></div>
        ${money(c.priceSummary?.total) ? `<div><dt>Each payment</dt><dd>${esc(money(c.priceSummary.total))}</dd></div>` : ""}
        ${c.createdDate ? `<div><dt>Started</dt><dd>${esc(date(c.createdDate))}</dd></div>` : ""}
        ${c.lastOrder ? `<div><dt>Last order</dt><dd>${esc(date(c.lastOrder))}${c.payments > 1 ? ` (${c.payments} so far)` : ""}</dd></div>` : ""}
        ${ship ? `<div><dt>Delivered to</dt><dd>${addressText(ship)}</dd></div>` : ""}
      </dl>
      ${cancelHtml(c)}
    </div>`;
  }).join("");
}

/* ---------- cancel ----------
   This Wix site has no "Subscription request" form yet, so a cancellation opens a pre-filled
   email to the customer team, who cancel it in Wix (Store > Subscriptions) and reply to confirm.
   To make it one click, create that form in Wix and submit to it from here. */
const CANCEL_KEY = "hazel-cancelled:";
const cancelledOn = (id) => { try { return localStorage.getItem(CANCEL_KEY + id); } catch { return null; } };
const REASONS = ["I have enough for now", "It's too expensive", "I didn't notice a difference", "I'd rather buy when I need it", "Something else"];
let cancelOpen = null;   // subscription id with the confirm panel open
let cancelError = "";

function cancelHtml(c) {
  const done = cancelledOn(c.id);
  if (done) return `<div class="sub-cancelled" role="status"><strong>Cancellation requested on ${esc(date(done))}.</strong> We'll cancel it before your next payment and email you to confirm. If the email didn't send, <a class="textlink" href="${mail("Cancel my subscription")}">email us here</a> or call 0117 462 3935.</div>`;
  if (cancelOpen !== c.id) return `<div class="sub-actions">
      <button type="button" class="btn line" data-cancel-open="${esc(c.id)}">Cancel subscription</button>
      <a class="textlink" href="${mail("Change my subscription")}">Pause or change it instead</a>
    </div>`;
  return `<form class="cancel-panel" data-form="cancel" data-sub="${esc(c.id)}" novalidate>
      <h4>Cancel your subscription?</h4>
      <p>We'll open an email to our team with your subscription details filled in. Send it and we'll cancel before your next payment and confirm by email. Any order already paid for will still be delivered. You can also call 0117 462 3935.</p>
      <label class="field"><span>Mind telling us why? (optional)</span><select name="reason"><option value="">Choose a reason</option>${REASONS.map((r) => `<option>${esc(r)}</option>`).join("")}</select></label>
      ${cancelError ? `<p class="err" role="alert">${esc(cancelError)}</p>` : ""}
      <div class="sub-actions">
        <button type="submit" class="btn">Email my cancellation</button>
        <button type="button" class="linkbtn" data-cancel-close>Keep my subscription</button>
      </div>
    </form>`;
}

function submitCancel(form) {
  const id = form.dataset.sub;
  const c = (data?.subs || []).find((s) => s.id === id) || {};
  const m = getMemberState().member || {};
  const email = data?.profile?.loginEmail || m.loginEmail || "";
  const first = data?.profile?.contact?.firstName || m.firstName || "";
  const reason = String(new FormData(form).get("reason") || "");
  if (!email) { cancelError = `We couldn't find your email address. Please email ${CONTACT} to cancel.`; render(); return; }
  const items = (c.lineItems || []).map((l) => `${tr(l.productName)}${l.quantity > 1 ? ` x ${l.quantity}` : ""}`).join(", ") || "Subscription";
  const details = [
    "Sent from the account page. Please cancel this subscription in Wix (Store > Subscriptions) before the next payment date.",
    `Subscription: ${tr(c.subscriptionTitle) || "Subscribe & save"} (${frequency(c.subscriptionSettings)}), ${items}`,
    `Subscription ID: ${id}`,
    c.createdDate ? `Started: ${date(c.createdDate)}` : "",
    c.lastOrder ? `Last order: ${date(c.lastOrder)}` : "",
    `Reason: ${reason || "not given"}`,
  ].filter(Boolean).join("\n");
  const body = `Hello,\n\nPlease cancel my subscription.\n\nName: ${first}\nAccount email: ${email}\n${details}\n\nThank you`;
  location.href = `mailto:${CONTACT}?subject=${encodeURIComponent("Cancel my subscription")}&body=${encodeURIComponent(body)}`;
  try { localStorage.setItem(CANCEL_KEY + id, new Date().toISOString()); } catch { /* the email still goes */ }
  cancelOpen = null; cancelError = ""; render();
}

function ordersHtml(orders) {
  if (orders === null) return `<p class="state">We can't show your orders here just now. Each order confirmation is in your email.</p>`;
  if (!orders.length) return `<p class="state">No orders yet.</p>`;
  return `<div class="orders">${orders.map((o) => `
    <div class="order-row">
      <div><strong>Order ${esc(o.number || "")}</strong><span>${esc(date(o.createdDate))}</span></div>
      <div>${(o.lineItems || []).map((l) => `${esc(tr(l.productName))}${l.quantity > 1 ? ` × ${l.quantity}` : ""}`).join(", ")}</div>
      <div class="order-total">${esc(money(o.priceSummary?.total))}</div>
    </div>`).join("")}</div>`;
}

function addressHtml(profile) {
  const a = profile?.contact?.addresses?.[0];
  if (editing) {
    return `<form class="addr-form" data-form="address" novalidate>
      <label class="field"><span>Address line 1</span><input name="addressLine" autocomplete="address-line1" value="${esc(a?.addressLine || "")}" required></label>
      <label class="field"><span>Address line 2 (optional)</span><input name="addressLine2" autocomplete="address-line2" value="${esc(a?.addressLine2 || "")}"></label>
      <div class="field-row">
        <label class="field"><span>Town or city</span><input name="city" autocomplete="address-level2" value="${esc(a?.city || "")}" required></label>
        <label class="field"><span>Postcode</span><input name="postalCode" autocomplete="postal-code" value="${esc(a?.postalCode || "")}" required></label>
      </div>
      <label class="field"><span>Country</span><select name="country" autocomplete="country">
        ${Object.entries(COUNTRIES).map(([k, v]) => `<option value="${k}" ${(a?.country || "GB") === k ? "selected" : ""}>${v}</option>`).join("")}
      </select></label>
      ${saveError ? `<p class="err" role="alert">${esc(saveError)}</p>` : ""}
      <div class="sub-actions">
        <button type="submit" class="btn" ${saving ? "disabled" : ""}>${saving ? "Saving…" : "Save address"}</button>
        <button type="button" class="linkbtn" data-edit="cancel">Cancel</button>
      </div>
      <p class="hint">This saves the address to your account. To change where a subscription is sent, please also send us a request below.</p>
    </form>`;
  }
  return `${a ? `<p class="addr">${addressText(a)}</p>` : `<p class="state">No address saved yet.</p>`}
    ${profile ? `<button type="button" class="btn line" data-edit="open">${a ? "Edit address" : "Add address"}</button>` : ""}`;
}

async function saveAddress(form) {
  const d = Object.fromEntries(new FormData(form));
  if (!String(d.addressLine).trim() || !String(d.city).trim() || !String(d.postalCode).trim()) {
    saveError = "Fill in the first address line, town and postcode."; render(); return;
  }
  const profile = data.profile;
  const existing = profile.contact?.addresses || [];
  const next = {
    ...(existing[0]?.id ? { id: existing[0].id } : {}),
    addressLine: String(d.addressLine).trim(),
    addressLine2: String(d.addressLine2 || "").trim(),
    city: String(d.city).trim(),
    postalCode: String(d.postalCode).trim().toUpperCase(),
    country: String(d.country || "GB"),
  };
  saving = true; saveError = ""; render();
  try {
    const res = await wixRequest(`/members/v1/members/${profile.id}`, { method: "PATCH", body: { member: { contact: { addresses: [next, ...existing.slice(1)] } } } });
    data.profile = res?.member ? { ...profile, ...res.member, contact: { ...profile.contact, ...res.member.contact } } : { ...profile, contact: { ...profile.contact, addresses: [next, ...existing.slice(1)] } };
    editing = false;
  } catch (e) {
    saveError = "We couldn't save your address. Please try again, or email us the new address.";
  }
  saving = false; render();
}

function renderAccount(state) {
  const m = state.member;
  const p = data?.profile;
  const first = p?.contact?.firstName || m?.firstName || "";
  intro.textContent = first ? `Welcome back, ${first}.` : "Welcome back.";
  if (!data) { root.innerHTML = `<div class="skeleton"></div><div class="skeleton short"></div>`; return; }
  const name = [p?.contact?.firstName || m?.firstName, p?.contact?.lastName || m?.lastName].filter(Boolean).join(" ") || m?.displayName || "";
  root.innerHTML = `
    <div class="help-block" id="subscription">
      <aside><h2>My subscription</h2><p>Subscribe &amp; save: a further 5% off every delivery, monthly, every 3 months or every 6 months. No minimum term: cancel at any time.</p></aside>
      <div>${subsHtml(data.subs)}</div>
    </div>
    <div class="help-block" id="orders">
      <aside><h2>My orders</h2></aside>
      <div>${ordersHtml(data.orders)}</div>
    </div>
    <div class="help-block" id="details">
      <aside><h2>My details</h2></aside>
      <dl class="info-rows">
        ${name ? `<div><dt>Name</dt><dd>${esc(name)}</dd></div>` : ""}
        <div><dt>Email</dt><dd>${esc(p?.loginEmail || m?.loginEmail || "")}</dd></div>
        ${m?.memberSince ? `<div><dt>Member since</dt><dd>${esc(date(m.memberSince))}</dd></div>` : ""}
      </dl>
    </div>
    <div class="help-block" id="address">
      <aside><h2>Delivery address</h2></aside>
      <div>${addressHtml(p)}</div>
    </div>
    <div class="help-block" id="payment">
      <aside><h2>Payment</h2></aside>
      <div class="prose">
        <p>Your card details are entered on the secure Wix checkout and aren't stored on this website. Subscription payments are taken from the card you used when you subscribed.</p>
        <p>To change the card for your subscription, email <a class="textlink" href="mailto:hello@supplementsbyhazel.com?subject=Update%20my%20payment%20card">hello@supplementsbyhazel.com</a> and we'll send you a secure link. You can also call <a class="textlink" href="tel:+441174623935">0117 462 3935</a>.</p>
      </div>
    </div>
    <div class="account-foot"><button type="button" class="btn line" data-logout>Log out</button></div>`;
}

/* ---------- manage block: pause, change address or card, by email or phone ---------- */
const manage = document.getElementById("manage");
function showRequestForm(state) { if (manage) manage.hidden = !state.loggedIn; }

/* ---------- wiring ---------- */
function render() {
  const s = getMemberState();
  showRequestForm(s);
  if (s.loading) { root.innerHTML = `<div class="skeleton"></div><div class="skeleton short"></div>`; return; }
  if (!s.loggedIn) { data = null; loadingFor = null; renderForm(); return; }
  const id = s.member?.id || "me";
  if (loadingFor !== id) { data = null; loadAccount(id).catch(() => { data = { profile: null, subs: null, orders: null }; render(); }); }
  renderAccount(s);
}

root.addEventListener("click", (e) => {
  const m = e.target.closest("[data-mode]");
  if (m) { mode = m.dataset.mode; formError = ""; renderForm(); return; }
  const ed = e.target.closest("[data-edit]");
  if (ed) { editing = ed.dataset.edit === "open"; saveError = ""; render(); if (editing) root.querySelector(".addr-form input")?.focus(); return; }
  const co = e.target.closest("[data-cancel-open]");
  if (co) { cancelOpen = co.dataset.cancelOpen; cancelError = ""; render(); root.querySelector(".cancel-panel select")?.focus(); return; }
  if (e.target.closest("[data-cancel-close]")) { cancelOpen = null; cancelError = ""; render(); return; }
  if (e.target.closest("[data-logout]")) { logout("/account.html").catch(() => {}); }
});
root.addEventListener("submit", (e) => {
  const form = e.target.closest("form");
  if (!form) return;
  e.preventDefault();
  if (form.dataset.form === "address") saveAddress(form);
  else if (form.dataset.form === "cancel") submitCancel(form);
  else submitForm(form);
});

subscribeMember(render);
render();
