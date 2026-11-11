// Supplements by Hazel: mailing-list sign-up above the footer on every page.
// The fields come from the "Mailing List" Wix form (edit it in the Wix dashboard under Forms);
// the shipped renderer draws them, validates and submits, and shows the form's thank-you.
import { renderForm } from "/js/wix/form-renderer.js";

const FORM_ID = "70bca7b7-9f3f-4ab9-a8eb-4f7be5c206cd";
const root = document.getElementById("newsletter-form");

function start() {
  renderForm(root, { formId: FORM_ID, classPrefix: "nl", text: { submit: "Subscribe", loading: "Loading…" } });
}

if (root) {
  // load the form when the band is close to view, not on every first paint
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { io.disconnect(); start(); }
    }, { rootMargin: "400px" });
    io.observe(root);
  } else start();
}
