// Supplements by Hazel: the Journal. Posts are written in the Wix Blog (dashboard > Blog) and read
// live here with the visitor token, so new posts appear without a rebuild.
//   blog.html  lists every post, with topic filters
//   post.html?slug=…  shows one post (old /post/<slug> links redirect here)
import { wixRequest } from "/js/wix/client.js";

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const media = (id, w, h) => {
  if (!id) return "";
  const url = /^https?:/.test(id) ? id : `https://static.wixstatic.com/media/${id}`;
  return url.includes("static.wixstatic.com/media/") && !url.includes("/v1/") ? `${url}/v1/fill/w_${w},h_${h},al_c,q_85,enc_auto/image.webp` : url;
};
const postImage = (p) => p?.media?.wixMedia?.image?.url || p?.media?.wixMedia?.image?.id || p?.coverMedia?.image?.url || "";
const fmtDate = (d) => { const t = d ? new Date(d) : null; return t && !isNaN(t) ? t.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) : ""; };

/* ---------- topics: matched on the title, so posts need no tagging ---------- */
const TOPICS = [
  ["Menopause", /menopaus|midlife|hormone|world menopause/i],
  ["Nutrients", /vitamin|magnesium|astaxanthin|cultures|nutrient|label|b12|iron/i],
  ["Sleep & stress", /sleep|stress|energy|routine/i],
  ["Our products", /clarity|peri formula|rosy|hair & skin|i take the supplements/i],
  ["Men's health", /\bmen\b|man's/i],
];

/* ---------- list ---------- */
const list = document.getElementById("post-list");
if (list) {
  const filters = document.getElementById("post-filters");
  const feature = document.getElementById("post-feature");
  let posts = [];
  let topic = "All";

  const card = (p) => `<li><a class="post-card" href="/post.html?slug=${encodeURIComponent(p.slug)}">
      <img src="${esc(media(postImage(p), 640, 400))}" alt="" width="640" height="400" loading="lazy">
      <div><span class="post-meta">${esc(fmtDate(p.firstPublishedDate))}${p.minutesToRead ? ` · ${p.minutesToRead} min read` : ""}</span><h3>${esc(p.title)}</h3><p>${esc((p.excerpt || "").slice(0, 170))}${(p.excerpt || "").length > 170 ? "…" : ""}</p></div>
    </a></li>`;

  function render() {
    const shown = topic === "All" ? posts : posts.filter((p) => TOPICS.find(([t]) => t === topic)[1].test(p.title));
    const [first, ...rest] = shown;
    feature.innerHTML = first ? `<a class="post-feature" href="/post.html?slug=${encodeURIComponent(first.slug)}">
        <img src="${esc(media(postImage(first), 960, 600))}" alt="" width="960" height="600">
        <div><span class="post-meta">${esc(fmtDate(first.firstPublishedDate))}${first.minutesToRead ? ` · ${first.minutesToRead} min read` : ""}</span><h2>${esc(first.title)}</h2><p class="hint">${esc((first.excerpt || "").slice(0, 220))}…</p><span class="card-cta">Read the article</span></div>
      </a>` : "";
    list.innerHTML = rest.map(card).join("") || (first ? "" : `<li class="state">No articles in this topic yet.</li>`);
    filters.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.topic === topic)));
  }

  filters.innerHTML = ["All", ...TOPICS.map(([t]) => t)].map((t) => `<button type="button" data-topic="${esc(t)}" aria-pressed="${t === "All"}">${esc(t)}</button>`).join("");
  filters.addEventListener("click", (e) => { const b = e.target.closest("[data-topic]"); if (b) { topic = b.dataset.topic; render(); } });

  (async () => {
    try {
      let offset = 0;
      for (;;) {
        const r = await wixRequest("/v3/posts", { method: "GET", query: { "paging.limit": "100", "paging.offset": String(offset), sort: "PUBLISHED_DATE_DESC" } });
        posts.push(...(r?.posts || []));
        if (!r?.posts?.length || r.posts.length < 100) break;
        offset += 100;
      }
      if (posts.length) render(); // otherwise keep the built-in list
    } catch { /* keep the built-in list */ }
  })();
}

/* ---------- single post ---------- */
const article = document.getElementById("article");
if (article) {
  const slug = new URLSearchParams(location.search).get("slug") || (location.pathname.match(/\/post\/([^/?#]+)/) || [])[1];

  const marks = (text, decos = []) => {
    let out = esc(text).replace(/\n/g, "<br>");
    for (const d of decos) {
      if (d.type === "BOLD" && (d.fontWeightValue ?? 700) >= 600) out = `<strong>${out}</strong>`;
      else if (d.type === "ITALIC" && d.italicData !== false) out = `<em>${out}</em>`;
      else if (d.type === "UNDERLINE" && !decos.some((x) => x.type === "LINK")) out = `<u>${out}</u>`;
      else if (d.type === "LINK" && d.linkData?.link?.url) {
        const url = d.linkData.link.url;
        const ext = !/supplementsbyhazel\.com/.test(url) && /^https?:/.test(url);
        out = `<a href="${esc(url)}"${ext ? ' target="_blank" rel="noopener"' : ""}>${out}</a>`;
      }
    }
    return out;
  };
  const kids = (n) => (n.nodes || []).map(node).join("");
  const isEmpty = (n) => !(n.nodes || []).some((c) => c.type !== "TEXT" || (c.textData?.text || "").trim());
  function node(n) {
    switch (n.type) {
      case "TEXT": return marks(n.textData?.text || "", n.textData?.decorations);
      case "PARAGRAPH": return isEmpty(n) ? "" : `<p>${kids(n)}</p>`;
      case "HEADING": { const l = Math.min(Math.max((n.headingData?.level || 2), 2), 4); return isEmpty(n) ? "" : `<h${l}>${kids(n)}</h${l}>`; }
      case "BULLETED_LIST": return `<ul>${kids(n)}</ul>`;
      case "ORDERED_LIST": return `<ol>${kids(n)}</ol>`;
      case "LIST_ITEM": return `<li>${(n.nodes || []).map((c) => (c.type === "PARAGRAPH" ? kids(c) : node(c))).join("")}</li>`;
      case "BLOCKQUOTE": return `<blockquote>${kids(n)}</blockquote>`;
      case "DIVIDER": return "<hr>";
      case "IMAGE": {
        const src = n.imageData?.image?.src; const id = src?.id || src?.url;
        if (!id) return "";
        const w = n.imageData.image.width || 1200, h = n.imageData.image.height || 800;
        const scale = Math.min(1, 1200 / w);
        return `<figure><img src="${esc(media(id, Math.round(w * scale), Math.round(h * scale)))}" alt="${esc(n.imageData?.altText || "")}" width="${Math.round(w * scale)}" height="${Math.round(h * scale)}" loading="lazy" style="max-width:${Math.min(w, 760)}px"></figure>`;
      }
      default: return kids(n);
    }
  }

  (async () => {
    try {
      if (!slug) throw new Error("no slug");
      const r = await wixRequest(`/v3/posts/slugs/${encodeURIComponent(slug)}`, { method: "GET", query: { fieldsets: ["RICH_CONTENT", "URL"] } });
      const p = r?.post;
      if (!p) throw new Error("not found");
      document.title = `${p.title} | Supplements by Hazel`;
      document.querySelector('meta[name="description"]')?.setAttribute("content", (p.excerpt || "").slice(0, 160));
      document.querySelector('link[rel="canonical"]')?.setAttribute("href", `https://www.supplementsbyhazel.com/post.html?slug=${encodeURIComponent(p.slug)}`);
      const nodes = p.richContent?.nodes || [];
      const hero = postImage(p);
      // drop a leading image that repeats the cover
      const body = nodes.filter((n, i) => !(i < 3 && n.type === "IMAGE" && hero && hero.includes(n.imageData?.image?.src?.id || "§"))).map(node).join("");
      article.innerHTML = `
        <header class="article-head">
          <nav class="crumb" aria-label="Breadcrumb" style="padding-top:0"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/blog.html">Journal</a></nav>
          <h1>${esc(p.title)}</h1>
          <p class="post-meta">By Hazel Hayden · ${esc(fmtDate(p.firstPublishedDate))}${p.minutesToRead ? ` · ${p.minutesToRead} min read` : ""}</p>
        </header>
        ${hero ? `<img class="article-hero" src="${esc(media(hero, 1400, 788))}" alt="" width="1400" height="788">` : ""}
        <div class="prose article-body">${body}</div>
        <div class="author-box"><img src="/assets/hazel.jpg" alt="" width="72" height="72"><p><strong>Hazel Hayden</strong> is a Consultant Nurse and British Menopause Society Registered Specialist, and the founder of Supplements by Hazel and the Bristol Menopause Clinic.</p></div>
        <p class="footnote">This article is for general information and isn't medical advice. Food supplements are not medicines. Speak to a healthcare professional about your own health.</p>`;
      document.dispatchEvent(new CustomEvent("post:loaded"));
    } catch {
      article.innerHTML = `<div class="notfound" style="padding:60px 0"><h1>We can't find that article</h1><p class="lead" style="margin:14px auto 0">It may have moved. Browse all our articles instead.</p><div class="actions"><a class="btn" href="/blog.html">Go to the Journal</a></div></div>`;
    }
  })();
}
