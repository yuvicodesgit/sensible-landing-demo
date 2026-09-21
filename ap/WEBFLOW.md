# Pushing /solutions/accounts-payable to Webflow

Files
- `fragment.html`  page body only (no nav, footer or closing CTA: those are the site's existing components)
- `ap.css`         every selector is scoped under `.ap` and prefixed `ap-` (no collisions with `dt-*`, `sp-*`, `d12-*`, `c2-*`)
- `ap.js`          tabs, hover-linking, GSAP + ScrollTrigger motion (one file, no dependencies besides GSAP)

Verified against the live Sensible site (site `69d90e4abf8f50428ec28825`)
- `window.gsap` and `window.ScrollTrigger` are **not** present on sensible.so pages, so GSAP has to be loaded by us.
- Live pages already load ~10 hosted scripts from `cdn.prod.website-files.com` via Webflow's registered-script mechanism, so a hosted script per page is an established pattern.
- Largest existing HTML embed on a comparable page: ~1.6 KB. Largest inline script: ~8.4 KB. The AP fragment is ~64 KB and the CSS ~24 KB, so it should NOT go in as one Code Embed.
- MCP `data_scripts_tool`: `register_hosted_script` (needs an SRI hash + semver) then `add_page_script` (footer). Inline registered scripts are capped at 2000 chars, so `ap.js` (8 KB) goes as a hosted script or page footer code, not as an inline registered script.
- MCP `data_whtml_builder`: `html` and `css` are separate params (no `<style>` in html), max 5 fragments per call.

Not verified (no test page was created on the production site)
- Exact character limit of a Code Embed / page-level custom code.
- Whether `data_whtml_builder` accepts inline `<svg>`, `<details>/<summary>` and `data-*` attributes, and how it treats `::before`, `@media` and `@keyframes` in the `css` param. Test on a throwaway draft page before the real push.
- How the site's CSP (if any) treats scripts from cdn.jsdelivr.net. Safer alternative: upload gsap.min.js / ScrollTrigger.min.js and host them beside the other site scripts.

Suggested order
1. Create a draft page under `/solutions` (`draft: true`).
2. Insert sections with `data_whtml_builder` (one section per call, css alongside).
3. `register_hosted_script` for gsap, ScrollTrigger and `ap.js`, then `add_page_script` (footer, in that order).
4. Add `<script>document.documentElement.classList.add('ap-js')</script>` to the page **head** custom code (prevents a flash before GSAP runs).
5. Swap `.ap-logos` for the existing customer-logo component.

Fallbacks built in
- If GSAP fails to load, or the visitor prefers reduced motion, `ap.js` removes the `ap-js` class and every section stays visible and interactive.
