// Supplements by Hazel: "Find your formula" quiz. Four questions, then a suggestion built from the
// product data the page carries (#quiz-data). Runs entirely in the browser; nothing is sent anywhere.
import { addLine } from "/js/wix/cart-store.js";
import { fetchProducts } from "/js/wix/catalog.js";

const root = document.getElementById("quiz");
const P = JSON.parse(document.getElementById("quiz-data").textContent);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const QUESTIONS = [
  { id: "who", q: "Who are you shopping for?", options: [["me", "Myself"], ["other", "Someone else"]] },
  { id: "stage", q: "Which sounds most like {you} right now?", options: [
    ["pre", "Periods are changing, or {you're} in {your} late 30s or 40s"],
    ["mid", "Going through the menopause"],
    ["post", "Periods stopped more than a year ago"],
    ["unsure", "Not sure"]] },
  { id: "focus", q: "What would {you} most like to support?", options: [
    ["energy", "Energy and tiredness"],
    ["mood", "Mood and mind"],
    ["hair", "Hair, skin and nails"],
    ["bones", "Bones, muscles and immunity"],
    ["all", "Overall wellbeing"]] },
  { id: "diet", q: "Any dietary needs?", options: [["vegan", "Vegan"], ["veggie", "Vegetarian"], ["none", "No restrictions"]] },
];
const answers = {};
let step = -1;

const voice = (t) => answers.who === "other"
  ? t.replace(/\{you\}/g, "they").replace(/\{you're\}/g, "they're").replace(/\{your\}/g, "their")
  : t.replace(/\{you\}/g, "you").replace(/\{you're\}/g, "you're").replace(/\{your\}/g, "your");

function recommend() {
  const { stage, focus, diet } = answers;
  const plantOnly = diet === "vegan" || diet === "veggie";
  let main = stage === "pre" ? "peri" : stage === "post" ? "rosy" : "clarity";
  const why = [];
  if (main === "peri" && diet === "vegan") { main = "clarity"; why.push("Peri isn't vegan, so we've suggested Clarity, which is."); }
  let pair = null;
  if (focus === "hair" && !plantOnly) pair = "hair-skin";
  else if (focus === "hair" && plantOnly) why.push("Hair & Skin contains marine collagen, so it isn't suitable for vegetarians or vegans.");
  else if (focus === "mood" && main === "peri") pair = "clarity";
  else if (focus === "bones" && main === "peri") pair = "clarity";
  else if ((focus === "energy" || focus === "all") && main === "rosy") pair = "clarity";
  else if (focus === "energy" && main === "clarity" && stage === "pre" && diet !== "vegan") pair = "peri";
  let bundle = null;
  if (!plantOnly) bundle = stage === "pre" ? "wellbeing" : "hormone";
  if (pair === main) pair = null;
  return { main, pair, bundle, why };
}

const reason = {
  peri: "Peri is for the years before the menopause. It has ashwagandha and saffron, and biotin to help maintain normal skin and hair.*",
  clarity: "Clarity is for during the menopause. Its magnesium, vitamin D and B12 help with tiredness, psychological function and bones.*",
  rosy: "Rosy is for after the menopause: vitamins C and D3 with L-theanine and carotenoids, taken in the evening.*",
  "hair-skin": "Hair & Skin adds biotin and zinc, which help maintain normal hair, skin and nails, plus vitamin C and marine collagen.*",
  wellbeing: "The Wellbeing Bundle is Clarity, Peri and Hair & Skin in one order, with a free gift the first time.",
  hormone: "The Hormone Health Bundle is Clarity, Rosy and Hair & Skin in one order, with a free gift the first time.",
};

function card(key, label) {
  const p = P[key];
  return `<article class="quiz-card" data-acc="${esc(p.acc)}">
    <img src="${esc(p.image)}" alt="" width="200" height="200">
    <div>
      <span class="stage">${esc(label)}</span>
      <h3><a href="/${esc(p.file)}">${esc(p.name)}</a></h3>
      <p>${esc(reason[key] || p.card)}</p>
      <ul class="card-ticks">${p.benefits.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>
      <div class="quiz-actions">
        <span class="card-price" data-quiz-price="${esc(p.slug)}"></span>
        <a class="btn" href="/${esc(p.file)}">View ${esc(p.name)}</a>
        <button type="button" class="btn line" data-quiz-add="${esc(p.slug)}">Add to basket</button>
      </div>
    </div>
  </article>`;
}

function render() {
  if (step < QUESTIONS.length) {
    const Q = QUESTIONS[step];
    root.innerHTML = `
      <div class="quiz-progress" aria-hidden="true"><span style="width:${((step + 1) / QUESTIONS.length) * 100}%"></span></div>
      <p class="quiz-step">Question ${step + 1} of ${QUESTIONS.length}</p>
      <h1 class="quiz-q">${esc(voice(Q.q))}</h1>
      <div class="quiz-options" role="group" aria-label="${esc(voice(Q.q))}">
        ${Q.options.map(([v, t]) => `<button type="button" class="quiz-option" data-answer="${esc(v)}" aria-pressed="${answers[Q.id] === v}">${esc(voice(t))}</button>`).join("")}
      </div>
      ${step > 0 ? `<button type="button" class="linkbtn" data-back>Back</button>` : ""}`;
    root.querySelector(".quiz-option")?.focus();
    return;
  }
  const r = recommend();
  root.innerHTML = `
    <span class="eyebrow">Your suggestion</span>
    <h1>We think ${answers.who === "other" ? "they'd" : "you'd"} suit ${esc(P[r.main].name)}</h1>
    ${r.why.map((w) => `<p class="hint">${esc(w)}</p>`).join("")}
    <div class="quiz-results">
      ${card(r.main, "Best match")}
      ${r.pair ? card(r.pair, "Pairs well with") : ""}
      ${r.bundle ? card(r.bundle, "Or save with a bundle") : ""}
    </div>
    <p class="footnote">*Claims authorised under the EU/UK Nutrition and Health Claims Register.</p>
    <button type="button" class="linkbtn" data-restart>Start again</button>`;
  fillPrices();
  root.querySelector("h1")?.focus?.();
}

let products = null;
async function fillPrices() {
  try {
    products ??= new Map((await fetchProducts({ limit: 100 })).map((p) => [p.slug, p]));
    root.querySelectorAll("[data-quiz-price]").forEach((el) => {
      const p = products.get(el.dataset.quizPrice);
      if (p) el.innerHTML = `${esc(p.price)}${p.compareAtPrice ? `<s>${esc(p.compareAtPrice)}</s>` : ""}`;
      const btn = root.querySelector(`[data-quiz-add="${CSS.escape(el.dataset.quizPrice)}"]`);
      if (btn && p && p.availability === "OUT_OF_STOCK") { btn.disabled = true; btn.textContent = "Out of stock"; }
    });
  } catch { /* prices stay blank; the View link still works */ }
}

root.addEventListener("click", async (e) => {
  if (e.target.closest("[data-quiz-start]")) { step = 0; render(); return; }
  const a = e.target.closest("[data-answer]");
  if (a) { answers[QUESTIONS[step].id] = a.dataset.answer; step += 1; render(); return; }
  if (e.target.closest("[data-back]")) { step = Math.max(0, step - 1); render(); return; }
  if (e.target.closest("[data-restart]")) { step = 0; for (const k in answers) delete answers[k]; render(); return; }
  const add = e.target.closest("[data-quiz-add]");
  if (add && !add.disabled) {
    const p = products?.get(add.dataset.quizAdd);
    if (!p) return;
    add.disabled = true; add.textContent = "Adding…";
    try { await addLine(p.id, p.minPriceVariantId); add.textContent = "Added"; }
    catch { add.textContent = "Couldn't add"; add.disabled = false; }
  }
});
