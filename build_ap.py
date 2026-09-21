#!/usr/bin/env python3
"""Assembles accounts-payable.html: shared CSS + nav/footer/CTA reused from index.html
(which already mirrors sensible.so), plus the new AP-specific sections."""
import re

src = open('index.html').read().split('\n')
L = lambda a, b: '\n'.join(src[a - 1:b])          # 1-indexed inclusive

base_css = L(20, 249)                              # fonts, tokens, reset, nav, buttons
marquee_css = L(497, 546)
sechead_css = L(548, 597)
faq_css = L(876, 926)
cta_footer_css = L(998, 1160)

full = '\n'.join(src)
nav_html = full[full.index('<!-- Navbar -->'):full.index('<!-- 1. HERO FOLD')]
marq_html = full[full.index('<!-- ANIMATED LOGO MARQUEE'):full.index('<!-- 2. TWO-CARD')]
footer_html = full[full.index('<footer class="footer">'):full.index('</footer>') + len('</footer>')]

marq_html = marq_html.replace('Trusted by teams turning complex documents into production data',
                              'Trusted by teams turning documents into production data')

new_css = r"""
    .sensible-font { font-family: 'Matter SQ', var(--font-sans); font-weight: 500; }
    section[id] { scroll-margin-top: 80px; }

    /* ---------- shared bits ---------- */
    .eyebrow {
      font-family: var(--font-mono); font-size: 12px; font-weight: 600;
      letter-spacing: 0.14em; text-transform: uppercase; color: var(--brand-magenta);
    }
    .sec { padding: 96px 0; }
    .sec.white { background: var(--bg-white); }
    .sec.stone { background: var(--bg-stone-subtle); }
    .sec-head { margin-bottom: 52px; }
    .sec-head .sec-eyebrow { display: block; }
    .chip {
      display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 999px;
      background: var(--bg-white); border: 1px solid var(--border-stone);
      font-size: 13.5px; color: var(--text-body); line-height: 1.2; white-space: nowrap;
    }
    .chip.mono { font-family: var(--font-mono); font-size: 12px; }

    /* ---------- 1. HERO ---------- */
    .ap-hero { padding: 72px 0 40px; text-align: center;
      background: radial-gradient(ellipse at 50% -10%, rgba(132,0,85,0.07), transparent 60%), var(--bg-stone); }
    .ap-hero .eyebrow { display: inline-block; margin-bottom: 20px; }
    .ap-h1 {
      font-family: var(--font-serif); font-weight: 400; color: var(--text-dark);
      font-size: clamp(2.3rem, 5.2vw, 3.9rem); line-height: 1.06; letter-spacing: -0.025em;
      max-width: 900px; margin: 0 auto 24px;
    }
    .ap-h1 em { font-style: italic; color: var(--brand-magenta); }
    .ap-frame { max-width: 780px; margin: 0 auto 32px; font-size: 17.5px; line-height: 1.7; color: var(--text-body); }
    .ap-hero-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 14px; }
    .ap-hero-note { font-family: var(--font-mono); font-size: 12px; color: var(--text-muted); letter-spacing: 0.04em; }

    /* ---------- 2. LIVE DEMO ---------- */
    .demo-sec { padding: 24px 0 88px; background: var(--bg-stone); }
    .demo-tabs { display: flex; gap: 8px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
    .demo-tab {
      font-family: var(--font-sans); font-size: 14px; font-weight: 500; cursor: pointer;
      padding: 9px 18px; border-radius: 999px; border: 1px solid var(--border-stone);
      background: var(--bg-white); color: var(--text-body); transition: all .2s;
    }
    .demo-tab:hover { border-color: var(--text-muted); }
    .demo-tab[aria-selected="true"] { background: var(--text-dark); color: #fff; border-color: var(--text-dark); }
    .demo-frame {
      display: grid; grid-template-columns: 1.02fr 1fr; gap: 0; background: var(--bg-white);
      border: 1px solid var(--border-stone); border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-float);
    }
    .demo-pane { display: none; }
    .demo-pane.active { display: contents; }
    .demo-doc-col { padding: 28px; background: var(--bg-stone-subtle); border-right: 1px solid var(--border-stone); }
    .demo-col-label {
      font-family: var(--font-mono); font-size: 11px; letter-spacing: .14em; text-transform: uppercase;
      color: var(--text-muted); margin-bottom: 14px; display: flex; justify-content: space-between; gap: 8px;
    }
    .doc {
      background: #fff; border: 1px solid var(--border-stone); border-radius: 6px; padding: 26px 26px 22px;
      font-size: 12.5px; color: #2b2630; box-shadow: 0 6px 24px rgba(20,17,24,.06); line-height: 1.45;
    }
    .doc-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 18px; }
    .doc-vendor b { display: block; font-family: var(--font-serif); font-size: 16px; font-weight: 500; letter-spacing: -.01em; }
    .doc-vendor span { color: var(--text-muted); font-size: 11px; }
    .doc-title { text-align: right; }
    .doc-title b { display: block; font-family: var(--font-mono); font-size: 15px; letter-spacing: .16em; }
    .doc-title span { font-family: var(--font-mono); font-size: 11.5px; color: var(--text-muted); }
    .doc-meta { display: grid; grid-template-columns: 1.2fr 1fr; gap: 14px 20px; margin-bottom: 16px; }
    .doc-meta dt { font-family: var(--font-mono); font-size: 9.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); }
    .doc-meta dd { margin: 0 0 6px; }
    .doc-table { width: 100%; border-collapse: collapse; margin-bottom: 12px; }
    .doc-table th { font-family: var(--font-mono); font-size: 9.5px; letter-spacing: .1em; text-transform: uppercase; color: var(--text-muted);
      text-align: right; padding: 6px 4px; border-bottom: 1px solid var(--border-stone); font-weight: 500; }
    .doc-table th:first-child, .doc-table td:first-child { text-align: left; }
    .doc-table td { text-align: right; padding: 7px 4px; border-bottom: 1px solid var(--border-light); vertical-align: top; }
    .doc-table td small { display: block; color: var(--text-muted); font-size: 10.5px; }
    .doc-totals { margin-left: auto; width: 62%; }
    .doc-totals div { display: flex; justify-content: space-between; padding: 3px 0; }
    .doc-totals .grand { border-top: 1.5px solid var(--text-dark); margin-top: 4px; padding-top: 7px; font-weight: 600; font-size: 13.5px; }
    .doc-foot { margin-top: 14px; padding-top: 10px; border-top: 1px dashed var(--border-stone); color: var(--text-muted); font-size: 10.5px; }
    [data-f] { border-radius: 3px; transition: background .15s, box-shadow .15s; }
    [data-f].hl { background: rgba(226,121,191,.28); box-shadow: 0 0 0 2px rgba(226,121,191,.28); }

    .demo-json-col { background: var(--bg-darkest); color: #E8E3DB; display: flex; flex-direction: column; min-width: 0; }
    .api-bar { display: flex; align-items: center; gap: 10px; padding: 14px 20px; border-bottom: 1px solid rgba(255,255,255,.08);
      font-family: var(--font-mono); font-size: 12.5px; flex-wrap: wrap; }
    .api-bar .verb { background: rgba(0,135,90,.22); color: #5fd6a6; padding: 2px 8px; border-radius: 4px; font-weight: 600; }
    .api-bar .ok { margin-left: auto; color: #5fd6a6; }
    .json-body { padding: 18px 20px; font-family: var(--font-mono); font-size: 11.5px; line-height: 1.7; overflow-x: auto; flex: 1; }
    .jl { display: block; white-space: pre-wrap; overflow-wrap: anywhere; padding-left: 26px !important; text-indent: -20px; padding: 0 6px; border-radius: 3px; transition: background .15s; }
    .jl.hl { background: rgba(226,121,191,.22); }
    .jk { color: #E279BF; } .js { color: #9fd0ff; } .jn { color: #F5B95F; } .jc { color: #8B857B; } .jp { color: #6f6a78; }
    .json-foot { padding: 12px 20px; border-top: 1px solid rgba(255,255,255,.08); font-family: var(--font-mono);
      font-size: 11px; color: #8B857B; display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .demo-caption { text-align: center; margin-top: 18px; font-size: 13.5px; color: var(--text-muted); }

    /* ---------- 3. TRUST STRIP ---------- */
    .trust-stats { background: var(--bg-white); padding: 0 0 56px; }
    .stats-row { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--border-stone); border-radius: 14px; background: var(--bg-stone); overflow: hidden; }
    .stat { padding: 26px 28px; border-left: 1px solid var(--border-stone); }
    .stat:first-child { border-left: none; }
    .stat b { display: block; font-family: var(--font-serif); font-weight: 400; font-size: 34px; letter-spacing: -.02em; color: var(--text-dark); line-height: 1.1; margin-bottom: 6px; }
    .stat span { font-size: 14px; color: var(--text-body); line-height: 1.45; display: block; }
    .stat.hot b { color: var(--brand-magenta); }

    /* ---------- 4. WHY HARD ---------- */
    .hard-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .hard-card { background: var(--bg-white); border: 1px solid var(--border-stone); border-radius: 14px; padding: 32px; position: relative; }
    .hard-card.ap { border-color: rgba(132,0,85,.45); background: linear-gradient(180deg, #fff, #fdf7fb); }
    .hard-num { font-family: var(--font-mono); font-size: 12px; letter-spacing: .12em; color: var(--brand-magenta); margin-bottom: 14px; display: flex; gap: 10px; align-items: center; }
    .hard-tag { font-size: 10.5px; padding: 3px 8px; border-radius: 999px; background: var(--brand-magenta); color: #fff; letter-spacing: .08em; }
    .hard-card h3 { font-family: var(--font-serif); font-weight: 400; font-size: 24px; letter-spacing: -.015em; color: var(--text-dark); margin-bottom: 12px; line-height: 1.2; }
    .hard-card p { font-size: 15.5px; color: var(--text-body); line-height: 1.65; }
    .hard-card p + p { margin-top: 10px; }

    /* ---------- 5. FIELDS ---------- */
    .fields-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .field-card { background: var(--bg-stone); border: 1px solid var(--border-stone); border-radius: 14px; padding: 30px; }
    .field-card .hard-num { margin-bottom: 8px; }
    .field-card h3 { font-family: var(--font-serif); font-weight: 400; font-size: 26px; letter-spacing: -.015em; margin-bottom: 18px; }
    .field-list { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; }
    .fields-note { margin: 28px auto 0; max-width: 760px; text-align: center; font-size: 15.5px; color: var(--text-body); line-height: 1.65; }

    /* ---------- 6. PIPELINE ---------- */
    .pipe-scope { border: 1.5px dashed rgba(132,0,85,.45); border-radius: 20px; padding: 26px 22px 24px; position: relative; background: rgba(255,255,255,.55); }
    .pipe-scope-label { position: absolute; top: -12px; left: 24px; background: var(--bg-stone-subtle); padding: 0 12px; font-family: var(--font-mono);
      font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--brand-magenta); font-weight: 600; }
    .pipe-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 22px; }
    .pl-stage { background: var(--bg-white); border: 1px solid var(--border-stone); border-radius: 14px; padding: 22px 18px 20px; position: relative; display: flex; flex-direction: column; box-shadow: var(--shadow-soft); }
    .pl-stage:not(:last-child)::after { content: ''; position: absolute; right: -19px; top: 44px; width: 16px; height: 16px;
      border-top: 2px solid var(--brand-magenta); border-right: 2px solid var(--brand-magenta); transform: rotate(45deg); opacity: .7; }
    .pl-num { width: 30px; height: 30px; border-radius: 50%; background: var(--brand-gradient); color: #fff; font-family: var(--font-mono);
      font-size: 13px; font-weight: 600; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }
    .pl-stage h3 { font-family: var(--font-serif); font-weight: 400; font-size: 22px; letter-spacing: -.015em; margin-bottom: 8px; }
    .pl-stage p { font-size: 14px; color: var(--text-body); line-height: 1.55; flex: 1; }
    .pl-io { margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--border-stone); font-family: var(--font-mono); font-size: 11px; line-height: 1.55; color: var(--text-muted); }
    .pl-io b { color: var(--brand-magenta-dark); font-weight: 600; }
    .pipe-handoff { display: flex; flex-direction: column; align-items: center; margin: 0 auto; }
    .pipe-handoff .stem { width: 2px; height: 30px; background: repeating-linear-gradient(180deg, var(--text-muted) 0 5px, transparent 5px 9px); }
    .pipe-handoff .lbl { font-family: var(--font-mono); font-size: 11px; color: var(--text-muted); letter-spacing: .1em; text-transform: uppercase; padding: 6px 0; }
    .pipe-down { border: 1.5px dashed var(--border-stone); border-radius: 14px; padding: 18px 24px; text-align: center; background: var(--bg-stone); }
    .pipe-down b { display: block; font-family: var(--font-serif); font-weight: 400; font-size: 19px; margin-bottom: 4px; }
    .pipe-down span { font-size: 14px; color: var(--text-body); }
    .trace-strip { margin-top: 26px; background: var(--bg-darkest); border-radius: 12px; padding: 16px 22px; display: flex; flex-wrap: wrap; gap: 8px 22px;
      align-items: center; font-family: var(--font-mono); font-size: 12.5px; color: #E8E3DB; }
    .trace-strip .tl { color: #8B857B; text-transform: uppercase; letter-spacing: .12em; font-size: 11px; }
    .trace-strip .k { color: #E279BF; } .trace-strip .v { color: #F5B95F; }

    /* ---------- 7. VALIDATION ---------- */
    .val-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: center; }
    .val-copy h2 { font-family: var(--font-serif); font-weight: 400; font-size: clamp(1.85rem, 3.5vw, 2.6rem); letter-spacing: -.015em; line-height: 1.12; margin-bottom: 20px; }
    .val-copy p { font-size: 16.5px; line-height: 1.7; color: var(--text-body); margin-bottom: 16px; }
    .val-quote { border-left: 3px solid var(--brand-magenta); padding: 4px 0 4px 18px; margin: 22px 0 0; font-family: var(--font-serif); font-size: 18px; line-height: 1.5; color: var(--text-dark); }
    .val-card { background: var(--bg-white); border: 1px solid var(--border-stone); border-radius: 16px; box-shadow: var(--shadow-medium); overflow: hidden; }
    .val-head { padding: 16px 22px; background: var(--bg-stone-subtle); border-bottom: 1px solid var(--border-stone); font-family: var(--font-mono); font-size: 11.5px; letter-spacing: .1em; text-transform: uppercase; color: var(--text-muted); display: flex; justify-content: space-between; gap: 10px; }
    .val-row { display: grid; grid-template-columns: 26px 1fr auto; gap: 14px; align-items: start; padding: 16px 22px; border-bottom: 1px solid var(--border-light); }
    .val-row:last-child { border-bottom: none; }
    .val-ic { width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #fff; margin-top: 1px; }
    .val-ic.ok { background: var(--check-green); } .val-ic.warn { background: #E08D1F; }
    .val-row b { display: block; font-size: 14.5px; font-weight: 600; color: var(--text-dark); margin-bottom: 2px; }
    .val-row span.d { font-size: 13.5px; color: var(--text-body); line-height: 1.5; }
    .val-res { font-family: var(--font-mono); font-size: 12px; color: var(--text-muted); text-align: right; white-space: nowrap; }
    .val-row.flag { background: #fff8ee; }
    .val-row.flag .val-res { color: #B36A0A; }

    /* ---------- 8. MANAGED ---------- */
    .managed { background: var(--bg-darkest); color: #FEFDFB; border-radius: 24px; padding: 60px; position: relative; overflow: hidden;
      background-image: radial-gradient(circle at 15% 0%, rgba(132,0,85,.35), transparent 55%), radial-gradient(circle at 100% 100%, rgba(248,156,42,.10), transparent 50%); }
    .managed .eyebrow { color: var(--brand-magenta-accent); }
    .managed h2 { font-family: var(--font-serif); font-weight: 400; font-size: clamp(1.9rem, 3.6vw, 2.8rem); letter-spacing: -.02em; line-height: 1.12; margin: 14px 0 16px; max-width: 760px; }
    .managed h2 em { font-style: italic; color: var(--brand-magenta-accent); }
    .managed > p { font-size: 17px; color: #D9D3CB; max-width: 680px; line-height: 1.65; margin-bottom: 34px; }
    .m-steps { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 36px; }
    .m-step { background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 12px; padding: 18px 16px; }
    .m-step i { font-style: normal; font-family: var(--font-mono); font-size: 12px; color: var(--brand-magenta-accent); letter-spacing: .12em; }
    .m-step b { display: block; font-family: var(--font-serif); font-weight: 400; font-size: 20px; margin: 6px 0 6px; }
    .m-step span { font-size: 13.5px; color: #C9C2BA; line-height: 1.5; display: block; }
    .m-actions { display: flex; gap: 12px; flex-wrap: wrap; }
    .m-btn { padding: 12px 24px; border-radius: 6px; font-weight: 600; font-size: 15px; transition: all .2s; }
    .m-btn.p { background: #F89C2A; color: #1A1520; } .m-btn.p:hover { background: #e08d1f; }
    .m-btn.s { border: 1px solid rgba(255,255,255,.3); color: #FEFDFB; } .m-btn.s:hover { border-color: rgba(255,255,255,.6); }

    /* ---------- 9. FORMATS ---------- */
    .fmt-list { max-width: 980px; margin: 0 auto; border: 1px solid var(--border-stone); border-radius: 16px; overflow: hidden; background: var(--bg-stone); }
    .fmt-row { display: grid; grid-template-columns: 200px 1fr; gap: 24px; padding: 26px 30px; border-bottom: 1px solid var(--border-stone); align-items: start; }
    .fmt-row:last-child { border-bottom: none; }
    .fmt-row h3 { font-family: var(--font-serif); font-weight: 400; font-size: 21px; letter-spacing: -.01em; }
    .fmt-row h3 small { display: block; font-family: var(--font-mono); font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--brand-magenta); margin-top: 4px; }
    .fmt-note { max-width: 980px; margin: 22px auto 0; font-size: 15px; color: var(--text-body); line-height: 1.65; text-align: center; }

    /* ---------- 10/11 ---------- */
    .faq-group-label { font-family: var(--font-mono); font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--brand-magenta); margin: 18px 0 -6px; }
    .faq-content p + p { margin-top: 10px; }


    /* ---------- HERO: split layout, demo in first fold ---------- */
    .ap-hero { padding: 44px 0 64px; text-align: left; }
    .ap-hero-grid { display: grid; grid-template-columns: minmax(0, 0.78fr) minmax(0, 1.5fr); gap: 44px; align-items: center; }
    .ap-hero-copy .eyebrow { margin-bottom: 18px; }
    .ap-h1 { font-size: clamp(2rem, 3.3vw, 3.05rem); margin: 0 0 20px; max-width: none; }
    .ap-frame { font-size: 16.5px; line-height: 1.65; margin: 0 0 26px; max-width: 470px; }
    .ap-hero-actions { justify-content: flex-start; }
    .ap-hero-demo { min-width: 0; }
    .ap-hero-demo .demo-tabs { justify-content: flex-start; margin-bottom: 12px; }
    .ap-hero-demo .demo-tab { padding: 7px 14px; font-size: 13px; }
    .ap-hero-demo .demo-doc-col { padding: 14px; }
    .ap-hero-demo .demo-col-label { margin-bottom: 10px; font-size: 10px; }
    .ap-hero-demo .doc { padding: 16px; font-size: 11px; }
    .ap-hero-demo .doc-top { margin-bottom: 12px; }
    .ap-hero-demo .doc-vendor b { font-size: 14px; }
    .ap-hero-demo .doc-meta { margin-bottom: 10px; gap: 8px 14px; }
    .ap-hero-demo .doc-table td { padding: 5px 3px; }
    .ap-hero-demo .doc-foot { display: none; }
    .ap-hero-demo .api-bar { padding: 11px 14px; font-size: 11.5px; }
    .ap-hero-demo .json-body { padding: 12px 14px; font-size: 10.5px; line-height: 1.6; }
    .ap-hero-demo .json-foot { padding: 9px 14px; font-size: 10px; }
    .ap-hero-demo .demo-caption { text-align: left; margin-top: 12px; font-size: 12.5px; }
    @media (max-width: 1100px) {
      .ap-hero-grid { grid-template-columns: 1fr; gap: 36px; }
      .ap-frame { max-width: 640px; }
    }



    /* ---------- HERO: minimised, fixed-size demo + stats bar ---------- */
    .ap-hero { padding: 36px 0 44px; }
    .ap-hero-grid { grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.5fr); gap: 40px; }
    .ap-hero .ap-h1 { font-size: clamp(1.9rem, 3vw, 2.7rem); }
    .ap-hero-demo .demo-frame { height: 486px; grid-template-columns: 0.8fr 1.2fr; grid-template-rows: minmax(0, 1fr); }
    .ap-hero-demo .demo-doc-col { padding: 12px; overflow: hidden; min-height: 0; }
    .ap-hero-demo .demo-json-col { min-height: 0; overflow: hidden; }
    .ap-hero-demo .json-body { overflow-y: auto; min-height: 0; line-height: 1.5; font-size: 10.5px; padding: 10px 12px; }
    .ap-hero-demo .demo-col-label span:last-child { display: none; }
    .ap-hero-demo .doc { padding: 13px; font-size: 10.5px; line-height: 1.4; }
    .ap-hero-demo .doc-top { margin-bottom: 9px; }
    .ap-hero-demo .doc-vendor b { font-size: 13px; }
    .ap-hero-demo .doc-vendor span { display: none; }
    .ap-hero-demo .doc-title b { font-size: 12px; }
    .ap-hero-demo .doc-title span { font-size: 10px; }
    .ap-hero-demo .doc-meta { grid-template-columns: 1fr; margin-bottom: 8px; gap: 4px; }
    .ap-hero-demo .doc-meta dt { font-size: 8.5px; }
    .ap-hero-demo .doc-meta dd { margin: 0 0 3px; }
        .ap-hero-demo .doc-meta > div:last-child { display: grid; grid-template-columns: 1fr 1fr; gap: 0 10px; }
    .ap-hero-demo .doc-table th { font-size: 8.5px; padding: 4px 2px; }
    .ap-hero-demo .doc-table td { padding: 4px 2px; }
    .ap-hero-demo .doc-table td small { display: none; }
    .ap-hero-demo .doc-table td:not(:first-child) { white-space: nowrap; }
    .ap-hero-demo .doc-totals { width: 78%; }
    .ap-hero-demo .doc-totals div { padding: 2px 0; }
    .ap-hero-demo .doc-totals .grand { font-size: 12px; padding-top: 5px; }

    .ap-hero .stats-row { margin-top: 28px; background: var(--bg-white); }
    .ap-hero .stat { padding: 16px 22px; }
    .ap-hero .stat b { font-size: 26px; margin-bottom: 3px; }
    .ap-hero .stat span { font-size: 13px; line-height: 1.4; }
    @media (max-width: 991px) {
      .ap-hero-demo .demo-frame { height: auto; grid-template-columns: 1fr; grid-template-rows: none; }
      .ap-hero-demo .demo-json-col { max-height: 460px; }
    }


    /* ---------- FIELDS TABLE ---------- */
    .ft-wrap { max-width: 1100px; margin: 0 auto; }
    .ft-tabs { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .ft-tab { cursor: pointer; font-family: var(--font-sans); font-size: 14.5px; font-weight: 500; padding: 10px 18px; border-radius: 10px;
      border: 1px solid var(--border-stone); background: var(--bg-white); color: var(--text-body); display: inline-flex; gap: 10px; align-items: center; transition: all .2s; }
    .ft-tab span { font-family: var(--font-mono); font-size: 11px; color: var(--text-muted); }
    .ft-tab:hover { border-color: var(--text-muted); }
    .ft-tab[aria-selected="true"] { background: var(--brand-gradient); color: #fff; border-color: transparent; box-shadow: 0 2px 8px var(--brand-magenta-glow); }
    .ft-tab[aria-selected="true"] span { color: rgba(255,255,255,.75); }
    .ft-table { border: 1px solid var(--border-stone); border-radius: 14px; overflow: hidden; background: var(--bg-white); box-shadow: var(--shadow-soft); }
    .ft-table { min-height: 652px; }
    .ft-pane { display: none; } .ft-pane.active { display: block; }
    .ft-row { display: grid; grid-template-columns: 1.05fr 1.2fr .7fr 2.6fr .9fr; gap: 18px; padding: 15px 24px; align-items: start; border-bottom: 1px solid var(--border-light); font-size: 14px; color: var(--text-body); line-height: 1.5; }
    .ft-row:last-child { border-bottom: none; }
    .ft-row:not(.ft-head):hover { background: var(--bg-stone); }
    .ft-head { background: var(--bg-stone-subtle); font-family: var(--font-mono); font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); padding-top: 12px; padding-bottom: 12px; }
    .ft-field { font-family: var(--font-serif); font-size: 16px; color: var(--text-dark); letter-spacing: -.005em; }
    .ft-key code, .ft-note code { font-family: var(--font-mono); font-size: 12px; color: var(--brand-magenta); background: rgba(132,0,85,.06); padding: 2px 6px; border-radius: 4px; }
    .ft-t { font-family: var(--font-mono); font-size: 11px; padding: 3px 8px; border-radius: 999px; border: 1px solid var(--border-stone); background: var(--bg-stone); color: var(--text-body); }
    .ft-t.t-currency { color: #B36A0A; border-color: #f1d9b3; background: #fff8ee; }
    .ft-t.t-date { color: #1F5FA6; border-color: #cfe0f3; background: #f3f8fd; }
    .ft-t.t-number { color: #B36A0A; border-color: #f1d9b3; background: #fff8ee; }
    .ft-check { font-family: var(--font-mono); font-size: 11px; font-weight: 600; color: var(--check-green); background: rgba(0,135,90,.1); padding: 3px 9px; border-radius: 999px; }
    .ft-none { color: var(--border-stone); }
    .ft-schema { max-width: 1100px; margin: 28px auto 0; display: grid; grid-template-columns: 1fr 1.2fr; gap: 32px; align-items: center;
      padding: 26px 30px; border: 1px solid var(--border-stone); border-radius: 14px; background: var(--bg-stone); }
    .ft-schema-copy b { font-family: var(--font-serif); font-weight: 400; font-size: 21px; letter-spacing: -.01em; display: block; margin-bottom: 6px; color: var(--text-dark); }
    .ft-schema-copy p { font-size: 14.5px; line-height: 1.6; color: var(--text-body); }
    .ft-schema-chips .lbl { display: block; font-family: var(--font-mono); font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; }
    @media (max-width: 991px) { .ft-schema { grid-template-columns: 1fr; gap: 20px; } }
    @media (max-width: 860px) {
      .ft-head { display: none; }
      .ft-row { grid-template-columns: 1fr auto; gap: 6px 12px; padding: 16px 18px; }
      .ft-field { grid-column: 1; } .ft-type { grid-column: 2; grid-row: 1; text-align: right; }
      .ft-key, .ft-note, .ft-chk { grid-column: 1 / -1; }
    }

    /* ---------- LIGHT THEME OVERRIDES: no black anywhere on this page ---------- */
    .demo-tab[aria-selected="true"] { background: var(--brand-gradient); color: #fff; border-color: transparent; box-shadow: 0 2px 8px var(--brand-magenta-glow); }
    .demo-json-col { background: var(--bg-white); color: var(--text-dark); border-left: 1px solid var(--border-stone); }
    .api-bar { border-bottom: 1px solid var(--border-stone); background: var(--bg-stone); color: var(--text-dark); }
    .api-bar .verb { background: rgba(0,135,90,.12); color: var(--check-green); }
    .api-bar .ok { color: var(--check-green); }
    .json-body { background: var(--bg-stone); }
    .jk { color: var(--brand-magenta); } .js { color: #1F5FA6; } .jn { color: #B36A0A; } .jc { color: var(--text-muted); } .jp { color: var(--text-muted); }
    .jl.hl { background: rgba(226,121,191,.24); }
    .json-foot { border-top: 1px solid var(--border-stone); color: var(--text-muted); background: var(--bg-white); }
    .trace-strip { background: var(--bg-white); border: 1px solid var(--border-stone); color: var(--text-body); }
    .trace-strip .tl { color: var(--text-muted); }
    .trace-strip .k { color: var(--brand-magenta); } .trace-strip .v { color: #B36A0A; }

    .managed { background: var(--bg-white); color: var(--text-dark); border: 1px solid var(--border-stone); box-shadow: var(--shadow-medium);
      background-image: radial-gradient(circle at 12% 0%, rgba(132,0,85,.08), transparent 55%), radial-gradient(circle at 100% 100%, rgba(248,156,42,.08), transparent 50%); }
    .managed .eyebrow { color: var(--brand-magenta); }
    .managed h2 em { color: var(--brand-magenta); }
    .managed > p { color: var(--text-body); }
    .m-step { background: var(--bg-stone); border: 1px solid var(--border-stone); }
    .m-step i { color: var(--brand-magenta); }
    .m-step b { color: var(--text-dark); }
    .m-step span { color: var(--text-body); }
    .m-btn.p { background: var(--brand-gradient); color: #fff; box-shadow: 0 2px 8px var(--brand-magenta-glow); }
    .m-btn.p:hover { background: linear-gradient(135deg, var(--brand-magenta-dark), var(--brand-magenta)); }
    .m-btn.s { border: 1px solid var(--border-stone); color: var(--text-dark); background: var(--bg-white); }
    .m-btn.s:hover { border-color: var(--text-muted); }

    /* ---------- responsive ---------- */
    @media (max-width: 1100px) {
      .pipe-grid { grid-template-columns: 1fr; gap: 26px; }
      .pl-stage:not(:last-child)::after { right: auto; left: 32px; top: auto; bottom: -19px; transform: rotate(135deg); }
      .m-steps { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 991px) {
      .demo-frame { grid-template-columns: 1fr; }
      .demo-doc-col { border-right: none; border-bottom: 1px solid var(--border-stone); }
      .val-grid { grid-template-columns: 1fr; gap: 36px; }
      .fields-grid { grid-template-columns: 1fr; }
      .stats-row { grid-template-columns: 1fr 1fr; }
      .stat:nth-child(3) { border-left: none; }
      .stat:nth-child(n+3) { border-top: 1px solid var(--border-stone); }
      .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px 24px; }
    }
    @media (max-width: 860px) {
      .navbar-inner { height: 60px; }
      .nav-links { display: none; }
      .nav-cta-group { display: none !important; }
      .mobile-toggle { display: block; }
    }
    @media (max-width: 767px) {
      .container { padding: 0 20px; }
      .sec { padding: 60px 0; }
      .sec-h2 { font-size: 28px; } .sec-desc { font-size: 16px; }
      .ap-hero { padding: 48px 0 28px; } .ap-frame { font-size: 16px; }
      .hard-grid { grid-template-columns: 1fr; }
      .hard-card, .field-card { padding: 24px; }
      .doc { padding: 18px; } .demo-doc-col { padding: 16px; }
      .fmt-row { grid-template-columns: 1fr; gap: 12px; padding: 22px; }
      .managed { padding: 36px 24px; border-radius: 18px; }
      .m-steps { grid-template-columns: 1fr; }
      .val-row { grid-template-columns: 26px 1fr; } .val-res { grid-column: 2; text-align: left; }
      .faq-summary { padding: 20px 22px; font-size: 16px; } .faq-content { padding: 0 22px 22px; font-size: 15px; }
      .cta-h2 { font-size: 28px; } .cta-banner { padding: 56px 24px; }
      .footer { padding: 64px 0 40px; }
      .footer-grid { grid-template-columns: 1fr; gap: 40px; padding-bottom: 40px; }
      .footer-bottom { flex-direction: column; align-items: flex-start; }
    }
    @media (max-width: 520px) {
      .stats-row { grid-template-columns: 1fr; }
      .stat { border-left: none !important; border-top: 1px solid var(--border-stone); } .stat:first-child { border-top: none; }
      .nav-logo img { height: 22px !important; }
      .btn { padding: 10px 20px; font-size: 14px; }
    }
    @media (prefers-reduced-motion: reduce) { .marquee-track { animation: none; } }
"""


# ---------- helpers for JSON panes ----------
def jl(text, f=None):
    a = f' data-f="{f}"' if f else ''
    return f'<span class="jl"{a}>{text}</span>'

K = lambda s: f'<span class="jk">"{s}"</span>'
S = lambda s: f'<span class="js">"{s}"</span>'
N = lambda s: f'<span class="jn">{s}</span>'
P = lambda s: f'<span class="jp">{s}</span>'
C = lambda s: f'<span class="jc">{s}</span>'

def field(key, source, value, typ, f, comma=True, num=False):
    v = N(value) if num else S(value)
    return jl(f'  {K(key)}: {{ {K("source")}: {S(source)}, {K("value")}: {v}, {K("type")}: {S(typ)} }}{"," if comma else ""}', f)

def pane_inv():
    rows = [
        jl('{'),
        jl(f'  {K("invoice_number")}: {S("NB-2024-0418")},', 'no'),
        jl(f'  {K("vendor")}: {S("Northbridge Studio LLC")},', 'vendor'),
        jl(f'  {K("bill_to")}: {S("Stillwater Robotics, Inc.")},', 'billto'),
        jl(f'  {K("po_number")}: {S("PO-2024-0284")},', 'po'),
        field('issue_date', 'Apr 18, 2024', '2024-04-18', 'date', 'issue'),
        field('due_date', 'May 18, 2024', '2024-05-18', 'date', 'due'),
        jl(f'  {K("payment_terms")}: {S("Net 30")},', 'terms'),
        jl(f'  {K("line_items")}: ['),
        jl(f'    {{ {K("description")}: {S("Strategy workshop facilitation")}, {K("qty")}: {N("2")}, {K("unit_price")}: {N("1850.00")}, {K("amount")}: {N("3700.00")} }},', 'li1'),
        jl(f'    {{ {K("description")}: {S("UX research interviews")}, {K("qty")}: {N("8")}, {K("unit_price")}: {N("425.00")}, {K("amount")}: {N("3400.00")} }},', 'li2'),
        jl(f'    {C("// + 3 more rows")}'),
        jl('  ],'),
        field('subtotal', '$14,204.00', '14204.00', 'currency', 'sub', num=True),
        field('tax_total', '$887.75', '887.75', 'currency', 'tax', num=True),
        jl(f'  {K("total_due")}: {{ {K("source")}: {S("$15,091.75")}, {K("value")}: {N("15091.75")}, {K("type")}: {S("currency")}, {K("confidence")}: {N("0.99")} }},', 'total'),
        jl(f'  {K("validation")}: {{', 'sub'),
        jl(f'    {K("line_items_sum_to_subtotal")}: {S("pass")}, {K("tax_matches_rate")}: {S("pass")},'),
        jl(f'    {K("total_reconciles")}: {S("pass")}, {K("po_reference_format")}: {S("pass")}'),
        jl('  }'),
        jl('}'),
    ]
    return '\n'.join(rows)

def pane_po():
    rows = [
        jl('{'),
        jl(f'  {K("po_number")}: {S("PO-2024-0284")},', 'po'),
        field('order_date', 'Mar 28, 2024', '2024-03-28', 'date', 'odate'),
        jl(f'  {K("buyer")}: {S("Stillwater Robotics, Inc.")},', 'buyer'),
        jl(f'  {K("vendor")}: {S("Northbridge Studio LLC")},', 'vendor'),
        jl(f'  {K("payment_terms")}: {S("Net 30")},', 'terms'),
        jl(f'  {K("line_items")}: ['),
        jl(f'    {{ {K("description")}: {S("Strategy workshop facilitation")}, {K("qty")}: {N("2")}, {K("unit_price")}: {N("1850.00")}, {K("amount")}: {N("3700.00")} }},', 'li1'),
        jl(f'    {{ {K("description")}: {S("UX research interviews")}, {K("qty")}: {N("8")}, {K("unit_price")}: {N("425.00")}, {K("amount")}: {N("3400.00")} }},', 'li2'),
        jl(f'    {C("// + 3 more rows")}'),
        jl('  ],'),
        field('subtotal', '$14,220.00', '14220.00', 'currency', 'sub', num=True),
        jl(f'  {K("total")}: {{ {K("source")}: {S("$14,220.00")}, {K("value")}: {N("14220.00")}, {K("type")}: {S("currency")}, {K("confidence")}: {N("0.99")} }},', 'total'),
        jl(f'  {K("validation")}: {{', 'sub'),
        jl(f'    {K("line_items_sum_to_subtotal")}: {S("pass")}, {K("total_reconciles")}: {S("pass")}'),
        jl('  }'),
        jl('}'),
    ]
    return '\n'.join(rows)

def pane_cm():
    rows = [
        jl('{'),
        jl(f'  {K("credit_memo_number")}: {S("CM-2024-0031")},', 'no'),
        jl(f'  {K("original_invoice")}: {S("NB-2024-0418")},', 'ref'),
        jl(f'  {K("po_number")}: {S("PO-2024-0284")},', 'po'),
        field('issue_date', 'May 2, 2024', '2024-05-02', 'date', 'issue'),
        jl(f'  {K("vendor")}: {S("Northbridge Studio LLC")},', 'vendor'),
        jl(f'  {K("reason")}: {S("Billable hours adjustment")},', 'reason'),
        jl(f'  {K("line_items")}: ['),
        jl(f'    {{ {K("description")}: {S("Account management: hours credited")}, {K("qty")}: {N("-2")}, {K("unit_price")}: {N("185.00")}, {K("amount")}: {N("-370.00")} }}', 'li1'),
        jl('  ],'),
        field('subtotal', '−$370.00', '-370.00', 'currency', 'sub', num=True),
        field('tax_total', '−$23.13', '-23.13', 'currency', 'tax', num=True),
        jl(f'  {K("total_credit")}: {{ {K("source")}: {S("−$393.13")}, {K("value")}: {N("-393.13")}, {K("type")}: {S("currency")}, {K("confidence")}: {N("0.98")} }},', 'total'),
        jl(f'  {K("validation")}: {{', 'sub'),
        jl(f'    {K("tax_matches_rate")}: {S("pass")}, {K("total_reconciles")}: {S("pass")},'),
        jl(f'    {K("references_known_invoice")}: {S("pass")}'),
        jl('  }'),
        jl('}'),
    ]
    return '\n'.join(rows)

def doc_inv():
    return '''
<div class="doc">
  <div class="doc-top">
    <div class="doc-vendor" data-f="vendor"><b>Northbridge Studio</b><span>Design · Strategy · Brand</span></div>
    <div class="doc-title"><b>INVOICE</b><span data-f="no">NB-2024-0418</span></div>
  </div>
  <dl class="doc-meta">
    <div><dt>Bill to</dt><dd data-f="billto">Stillwater Robotics, Inc.<br>2840 Innovation Way, Suite 410<br>Cambridge, MA 02142</dd></div>
    <div>
      <dt>Issue date</dt><dd data-f="issue">Apr 18, 2024</dd>
      <dt>Due date</dt><dd data-f="due">May 18, 2024</dd>
      <dt>PO #</dt><dd data-f="po">PO-2024-0284</dd>
      <dt>Terms</dt><dd data-f="terms">Net 30</dd>
    </div>
  </dl>
  <table class="doc-table">
    <tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
    <tr data-f="li1"><td>Strategy workshop facilitation<small>2-day on-site engagement</small></td><td>2</td><td>$1,850.00</td><td>$3,700.00</td></tr>
    <tr data-f="li2"><td>UX research interviews<small>8 sessions · recorded &amp; transcribed</small></td><td>8</td><td>$425.00</td><td>$3,400.00</td></tr>
    <tr><td>Design system audit</td><td>1</td><td>$4,200.00</td><td>$4,200.00</td></tr>
    <tr><td>Account management<small>March · 12 hrs billable</small></td><td>12</td><td>$185.00</td><td>$2,220.00</td></tr>
    <tr><td>Travel &amp; expenses</td><td>1</td><td>$684.00</td><td>$684.00</td></tr>
  </table>
  <div class="doc-totals">
    <div data-f="sub"><span>Subtotal</span><span>$14,204.00</span></div>
    <div data-f="tax"><span>Sales tax (MA 6.25%)</span><span>$887.75</span></div>
    <div class="grand" data-f="total"><span>Total due</span><span>$15,091.75</span></div>
  </div>
  <div class="doc-foot">Net 30. Payable by ACH to Northbridge Studio LLC. Late fee 1.5%/mo on past-due balances.</div>
</div>'''

def doc_po():
    return '''
<div class="doc">
  <div class="doc-top">
    <div class="doc-vendor" data-f="buyer"><b>Stillwater Robotics, Inc.</b><span>Procurement · Cambridge, MA</span></div>
    <div class="doc-title"><b>PURCHASE ORDER</b><span data-f="po">PO-2024-0284</span></div>
  </div>
  <dl class="doc-meta">
    <div><dt>Vendor</dt><dd data-f="vendor">Northbridge Studio LLC<br>114 Brattle Street<br>Cambridge, MA 02138</dd></div>
    <div>
      <dt>Order date</dt><dd data-f="odate">Mar 28, 2024</dd>
      <dt>Terms</dt><dd data-f="terms">Net 30</dd>
      <dt>Project</dt><dd>Phoenix Rebrand</dd>
    </div>
  </dl>
  <table class="doc-table">
    <tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
    <tr data-f="li1"><td>Strategy workshop facilitation</td><td>2</td><td>$1,850.00</td><td>$3,700.00</td></tr>
    <tr data-f="li2"><td>UX research interviews</td><td>8</td><td>$425.00</td><td>$3,400.00</td></tr>
    <tr><td>Design system audit</td><td>1</td><td>$4,200.00</td><td>$4,200.00</td></tr>
    <tr><td>Account management</td><td>12</td><td>$185.00</td><td>$2,220.00</td></tr>
    <tr><td>Travel &amp; expenses (not to exceed)</td><td>1</td><td>$700.00</td><td>$700.00</td></tr>
  </table>
  <div class="doc-totals">
    <div data-f="sub"><span>Subtotal</span><span>$14,220.00</span></div>
    <div class="grand" data-f="total"><span>Order total</span><span>$14,220.00</span></div>
  </div>
  <div class="doc-foot">Invoices must quote this PO number. Goods receipt / service acceptance required before payment.</div>
</div>'''

def doc_cm():
    return '''
<div class="doc">
  <div class="doc-top">
    <div class="doc-vendor" data-f="vendor"><b>Northbridge Studio</b><span>Design · Strategy · Brand</span></div>
    <div class="doc-title"><b>CREDIT MEMO</b><span data-f="no">CM-2024-0031</span></div>
  </div>
  <dl class="doc-meta">
    <div><dt>Credit to</dt><dd>Stillwater Robotics, Inc.<br>2840 Innovation Way, Suite 410</dd></div>
    <div>
      <dt>Issue date</dt><dd data-f="issue">May 2, 2024</dd>
      <dt>Against invoice</dt><dd data-f="ref">NB-2024-0418</dd>
      <dt>PO #</dt><dd data-f="po">PO-2024-0284</dd>
    </div>
  </dl>
  <table class="doc-table">
    <tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
    <tr data-f="li1"><td>Account management: hours credited<small data-f="reason">Billable hours adjustment</small></td><td>−2</td><td>$185.00</td><td>−$370.00</td></tr>
  </table>
  <div class="doc-totals">
    <div data-f="sub"><span>Subtotal</span><span>−$370.00</span></div>
    <div data-f="tax"><span>Sales tax (6.25%)</span><span>−$23.13</span></div>
    <div class="grand" data-f="total"><span>Total credit</span><span>−$393.13</span></div>
  </div>
  <div class="doc-foot">Credit applied against the open balance on the referenced invoice.</div>
</div>'''

def demo_pane(pid, active, doc, endpoint, label, json_html, count):
    return f'''
<div class="demo-pane{' active' if active else ''}" id="pane-{pid}" role="tabpanel">
  <div class="demo-doc-col">
    <div class="demo-col-label"><span>Source document</span><span>{label}</span></div>
    {doc}
  </div>
  <div class="demo-json-col">
    <div class="api-bar"><span class="verb">POST</span><span>{endpoint}</span><span class="ok">200 OK</span></div>
    <div class="json-body">{json_html}</div>
    <div class="json-foot"><span>{count} fields</span><span>every value traces to page + bounding box</span></div>
  </div>
</div>'''

demo = ''.join([
    demo_pane('inv', True, doc_inv(), '/v0/extract/invoice', 'supplier invoice · PDF', pane_inv(), 14),
    demo_pane('po', False, doc_po(), '/v0/extract/purchase_order', 'purchase order · PDF', pane_po(), 9),
    demo_pane('cm', False, doc_cm(), '/v0/extract/credit_memo', 'credit memo · PDF', pane_cm(), 10),
])

def chips(items, mono=False):
    return ''.join(f'<li class="chip{" mono" if mono else ""}">{i}</li>' for i in items)

def faq(q, a, open_=False):
    return f'<details class="faq-accordion"{" open" if open_ else ""}><summary class="faq-summary">{q}<span class="faq-icon">+</span></summary><div class="faq-content">{a}</div></details>'

faqs_ap = [
    faq('Does Sensible do invoice-to-PO-to-receipt three-way matching itself?',
        '<p>No. Sensible is the extraction layer. It reads the invoice, the purchase order and the goods receipt, and captures the reference fields that tie them together (PO number, line quantities, unit prices, totals) in a consistent, schema-validated shape. The matching logic itself, including tolerances and exception handling, lives downstream in your AP system, ERP or matching engine.</p>', True),
    faq('Can Sensible flag likely duplicate invoices?',
        '<p>Not as a built-in feature. Sensible&rsquo;s validation rules run against one document at a time, and spotting a duplicate needs a comparison across documents you have already processed.</p><p>What Sensible does give you is a reliable duplicate key on every invoice: vendor, invoice number, invoice date and grand total, extracted the same way each time. Checking that key against your history belongs in your AP system or ERP. If you want that wired in as part of the pipeline, our managed-services team can help with the integration.</p>'),
    faq('How does per-document pricing work for high-volume AP teams?',
        '<p>Sensible prices per document, not per token, so cost is predictable at 500 invoices a month or 50,000. There is no token-volatility surprise when a vendor sends a 40-line invoice instead of a 4-line one. Volume discounts are available for higher throughput; <a href="https://www.sensible.so/pricing" style="color:var(--brand-magenta)">see pricing</a> or talk to our team for a volume quote.</p>'),
    faq('How does Sensible catch bad extractions before they reach the ledger?',
        '<p>Validation rules cross-check that line items sum to the subtotal, that tax matches the stated rate, and that the grand total reconciles. Discrepancies are flagged automatically with a confidence score, and low-confidence extractions can be routed to human review with thresholds you configure. Results are delivered by webhook or API.</p>'),
    faq('How accurate is the extraction?',
        '<p>Accuracy depends on document quality and configuration, so we don&rsquo;t quote a single flat number. What we can tell you is how the output is checked: schema enforcement, calculation validation and a confidence score on each field, so weak extractions are flagged instead of passed through silently. The best way to know is to run your own invoices, including the ugly ones, through it.</p>'),
    faq('How is invoice data secured, and how long is it retained?',
        '<p>Sensible is SOC 2 Type II certified and HIPAA compliant, with data encrypted in transit and at rest. Document data is stored indefinitely by default; custom retention policies are available, including same-day deletion.</p>'),
]
faqs_carry = []


FIELD_TABS = [
  ('header', 'Header', 9, [
    ('Invoice number','invoice_number','string','Kept exactly as printed. With vendor, date and total it forms a duplicate-check key in your system.',''),
    ('Invoice date','invoice_date','date','ISO 8601 value; the original text is preserved alongside it as <code>source</code>.',''),
    ('Due date','due_date','date','ISO 8601 value with the original text preserved.',''),
    ('PO number','po_number','string','Format-checked, and kept clean enough to match against the PO and goods receipt it references.','PO format'),
    ('Vendor name','vendor_name','string','Mapped to your schema whether the invoice says &ldquo;From&rdquo;, &ldquo;Billed by&rdquo; or &ldquo;Seller&rdquo;.',''),
    ('Vendor address','vendor_address','string','Captured as printed, from the header or the footer of the document.',''),
    ('Bill-to name','bill_to_name','string','The entity being billed, for entity and cost-center routing.',''),
    ('Bill-to address','bill_to_address','string','Captured as printed.',''),
    ('Payment terms','payment_terms','string','Terms as written (Net 30, 2/10 Net 30) so your system can compute the due date its own way.',''),
  ]),
  ('lines', 'Line items', 8, [
    ('Description','description','string','Multi-line descriptions are kept together as one row instead of splitting across lines.',''),
    ('Quantity','quantity','number','Parsed to a number; handles credit-memo negatives.',''),
    ('Unit price','unit_price','currency','Parsed to a number; the printed text is preserved in <code>source</code>.',''),
    ('Unit of measure','unit_of_measure','string','Hours, each, per diem or whatever the vendor prints, when the invoice carries one.',''),
    ('Discount','discount','currency','Row-level discount, when present.',''),
    ('Tax amount','tax_amount','currency','Row-level tax for invoices with varying tax codes.','Tax'),
    ('Extended amount','extended_amount','currency','The row total. Tables that run across page breaks are read as one table.','Subtotal'),
    ('SKU / part number','sku','string','Captured when present, so lines can be matched to PO lines.',''),
  ]),
  ('totals', 'Totals', 8, [
    ('Subtotal','subtotal','currency','Checked against the sum of the line items.','Subtotal'),
    ('Discount total','discount_total','currency','Document-level discount.',''),
    ('Tax total','tax_total','currency','Checked against the stated tax rate.','Tax'),
    ('Shipping / freight','shipping_freight','currency','Separated from the goods total so it does not distort the subtotal check.',''),
    ('Grand total','grand_total','currency','Must reconcile: subtotal + tax + shipping &minus; discount.','Total'),
    ('Amount paid','amount_paid','currency','For part-paid invoices and deposits.',''),
    ('Balance due','balance_due','currency','What is actually payable now.',''),
    ('Currency','currency','string','The currency printed on the document, so multi-currency AP does not guess.',''),
  ]),
]

def fields_section():
    tabs = ''.join(
        f'<button class="ft-tab" role="tab" aria-selected="{"true" if i==0 else "false"}" data-ft="{k}">{name}<span>{n}</span></button>'
        for i,(k,name,n,_) in enumerate(FIELD_TABS))
    panes = ''
    for i,(k,name,n,rows) in enumerate(FIELD_TABS):
        body = ''
        for f,key,typ,note,chk in rows:
            badge = f'<span class="ft-check">{chk}</span>' if chk else '<span class="ft-none">&mdash;</span>'
            body += (f'<div class="ft-row"><div class="ft-field">{f}</div><div class="ft-key"><code>{key}</code></div>'
                     f'<div class="ft-type"><span class="ft-t t-{typ}">{typ}</span></div><div class="ft-note">{note}</div>'
                     f'<div class="ft-chk">{badge}</div></div>')
        panes += (f'<div class="ft-pane{" active" if i==0 else ""}" id="ft-{k}" role="tabpanel">'
                  f'<div class="ft-row ft-head"><div>Field</div><div>Schema key</div><div>Type</div><div>How Sensible handles it</div><div>Validated in</div></div>{body}</div>')
    return f'''
  <section class="sec white" id="fields">
    <div class="container">
      <div class="sec-head">
        <span class="sec-eyebrow">What Sensible extracts</span>
        <h2 class="sec-h2">Every field typed, checked, and traceable</h2>
        <p class="sec-desc">Three buckets, 25 fields AP teams request most. Each comes back typed, keeps its printed text, and links to its source location on the page.</p>
      </div>
      <div class="ft-wrap">
        <div class="ft-tabs" role="tablist" aria-label="Field groups">{tabs}</div>
        <div class="ft-table">{panes}</div>
      </div>
      <div class="ft-schema">
        <div class="ft-schema-copy">
          <b>Your schema, not a fixed list.</b>
          <p>Every AP team&rsquo;s schema is different, so this list is a starting point that gets mapped to yours. Keys, names and structure follow your contract, and anything else your workflow needs is added in configuration.</p>
        </div>
        <div class="ft-schema-chips"><span class="lbl">Commonly added</span><ul class="field-list">{chips(['GL code','Cost center','Ship-to','Remit-to details','Vendor tax ID','Receipt / GRN number','Project code','Early-pay discount terms'])}</ul></div>
      </div>
    </div>
  </section>'''

body = f'''
{nav_html}

  <!-- 1 + 2. HERO: H1 + FRAMING beside the LIVE DEMO (first fold) -->
  <section class="ap-hero">
    <div class="container">
     <div class="ap-hero-grid">
      <div class="ap-hero-copy">
        <span class="eyebrow">Solutions &nbsp;/&nbsp; Accounts payable</span>
        <h1 class="ap-h1">Accounts payable automation, built on <em>extraction you can trust</em></h1>
        <p class="ap-frame">Sensible is the extraction layer under your AP workflow: schema-validated, traced to source coordinates, and scored for confidence, so your finance team can trust the data without checking it by hand.</p>
        <div class="ap-hero-actions">
          <a href="https://app.sensible.so/register/" class="btn btn-primary">Start free trial</a>
          <a href="https://www.sensible.so/meeting" class="btn btn-secondary">Book a demo</a>
        </div>
        <div class="ap-hero-note">14-day free trial · No credit card</div>
      </div>
      <div class="ap-hero-demo" id="demo">
        <div class="demo-tabs" role="tablist" aria-label="Sample AP documents">
          <button class="demo-tab" role="tab" aria-selected="true" data-pane="inv">Supplier invoice</button>
          <button class="demo-tab" role="tab" aria-selected="false" data-pane="po">Purchase order</button>
          <button class="demo-tab" role="tab" aria-selected="false" data-pane="cm">Credit memo</button>
        </div>
        <div class="demo-frame">{demo}
        </div>
        <p class="demo-caption">Hover a field to trace it to the source. Sample data; output is illustrative.</p>
      </div>
     </div>
      <div class="stats-row">
        <div class="stat hot"><b>75M+</b><span>documents processed</span></div>
        <div class="stat hot"><b>150+</b><span>library configurations, so your vendor formats have likely been seen before</span></div>
        <div class="stat"><b>Validated JSON</b><span>Schema-enforced output; every field matches your contract</span></div>
        <div class="stat"><b>Per-document</b><span>Predictable cost. No token-volatility surprises</span></div>
      </div>
    </div>
  </section>

  <!-- 3. TRUST STRIP -->
  {marq_html}


  <!-- 4. WHY HARD -->
  <section class="sec stone" id="why-hard">
    <div class="container">
      <div class="sec-head">
        <span class="sec-eyebrow">Why AP extraction is hard in production</span>
        <h2 class="sec-h2">The demo invoice is easy. Your AP inbox is not.</h2>
        <p class="sec-desc">Headers, totals, and line-item tables land somewhere new on every vendor&rsquo;s document. Hybrid extraction absorbs the variation, and deterministic validation re-checks the math before the data reaches your ledger.</p>
      </div>
      <div class="hard-grid">
        <article class="hard-card"><div class="hard-num">01</div><h3>Vendor format diversity</h3><p>QuickBooks exports, SAP invoices, handwritten bills, custom ERP outputs: each places fields differently. Hybrid extraction (LLM parsing plus SenseML rules) absorbs the variation instead of breaking on it.</p></article>
        <article class="hard-card"><div class="hard-num">02</div><h3>Line item table extraction</h3><p>Multi-page tables, merged cells, multi-line descriptions, varying tax codes. Quantity, unit price, tax and amount stay intact on every row, and page breaks are handled transparently.</p></article>
        <article class="hard-card"><div class="hard-num">03</div><h3>Calculation validation</h3><p>Do line items sum to the subtotal? Does the tax match the rate? Does the grand total reconcile? This is the check that catches a bad extraction before it reaches the ledger, not after.</p></article>
        <article class="hard-card ap"><div class="hard-num">04 <span class="hard-tag">AP-SPECIFIC</span></div><h3>PO and three-way-match readiness</h3><p>An invoice&rsquo;s PO number is only useful if it can be checked against the PO and goods receipt it references. Extraction has to preserve that reference cleanly enough to match on, not just capture it as a string.</p></article>
      </div>
    </div>
  </section>

  <!-- 5. FIELDS -->
  {fields_section()}

  <!-- 6. PIPELINE -->
  <section class="sec stone" id="how-it-works">
    <div class="container">
      <div class="sec-head">
        <span class="sec-eyebrow">How it works</span>
        <h2 class="sec-h2">A five-stage pipeline. Every field traceable.</h2>
        <p class="sec-desc">From a raw supplier document to schema-enforced JSON in your AP system, with a checkpoint at every stage.</p>
      </div>
      <div class="pipe-scope">
        <span class="pipe-scope-label">Sensible: the extraction layer</span>
        <div class="pipe-grid">
          <div class="pl-stage"><div class="pl-num">1</div><h3>Ingest</h3><p>PDF, scan, email attachment, or spreadsheet. Any source, no pre-sorting required.</p><div class="pl-io"><b>in</b> raw files, email, API upload<br><b>out</b> normalized pages</div></div>
          <div class="pl-stage"><div class="pl-num">2</div><h3>Classify</h3><p>Document type identified (invoice, PO, credit memo, remittance) before extraction runs.</p><div class="pl-io"><b>in</b> normalized pages<br><b>out</b> typed document</div></div>
          <div class="pl-stage"><div class="pl-num">3</div><h3>Extract</h3><p>Hybrid AI plus deterministic SenseML rules pull header, line item, and total fields regardless of layout.</p><div class="pl-io"><b>in</b> typed document<br><b>out</b> candidate fields</div></div>
          <div class="pl-stage"><div class="pl-num">4</div><h3>Validate</h3><p>Calculation checks run automatically: line items to subtotal, tax to rate, PO reference format. Discrepancies are flagged with a confidence score.</p><div class="pl-io"><b>in</b> candidate fields<br><b>out</b> checked fields + flags</div></div>
          <div class="pl-stage"><div class="pl-num">5</div><h3>Deliver</h3><p>Schema-enforced JSON, every field traced to page and bounding box, sent via webhook or pulled via API.</p><div class="pl-io"><b>in</b> checked fields<br><b>out</b> JSON to your system</div></div>
        </div>
      </div>
      <div class="pipe-handoff"><div class="stem"></div><div class="lbl">webhook · API</div><div class="stem"></div></div>
      <div class="pipe-down"><b>Your AP system, ERP, or matching engine</b><span>Three-way matching, approval routing, posting and payment stay here. Sensible hands over data you can trust; it does not run those steps.</span></div>
      <div class="trace-strip"><span class="tl">Every field is traceable</span><span><span class="k">total_due</span> → page <span class="v">1</span></span><span><span class="k">bbox</span> <span class="v">[412, 688, 540, 712]</span></span><span><span class="k">confidence</span> <span class="v">0.99</span></span><span><span class="k">source</span> <span class="v">"$15,091.75"</span></span></div>
    </div>
  </section>

  <!-- 7. VALIDATION -->
  <section class="sec white" id="validation">
    <div class="container">
      <div class="val-grid">
        <div class="val-copy">
          <span class="sec-eyebrow" style="text-align:left;margin-bottom:14px;display:block">Validation, not just extraction</span>
          <h2>Extraction alone isn&rsquo;t the hard part. Trusting the output is.</h2>
          <p>Any tool can return a number. The question your finance team asks is whether it&rsquo;s the right number. So Sensible checks the output the way an AP clerk would: do the line items sum to the subtotal, does the tax match the stated rate, does the grand total reconcile, is the PO reference in a valid format.</p>
          <p>When a check fails, the field is flagged with a confidence score and routed for review instead of flowing silently into your ledger.</p>
          <div class="val-quote">We don&rsquo;t publish a flat accuracy percentage. Accuracy depends on document quality and configuration, and a single number hides both.</div>
        </div>
        <div class="val-card">
          <div class="val-head"><span>Validation results</span><span>NB-2024-0418</span></div>
          <div class="val-row"><span class="val-ic ok">✓</span><div><b>Line items sum to subtotal</b><span class="d">5 lines add up to the stated subtotal</span></div><span class="val-res">$14,204.00</span></div>
          <div class="val-row"><span class="val-ic ok">✓</span><div><b>Tax matches rate</b><span class="d">6.25% of subtotal equals stated tax</span></div><span class="val-res">$887.75</span></div>
          <div class="val-row"><span class="val-ic ok">✓</span><div><b>Grand total reconciles</b><span class="d">Subtotal + tax − discount = total due</span></div><span class="val-res">$15,091.75</span></div>
          <div class="val-row"><span class="val-ic ok">✓</span><div><b>PO reference format</b><span class="d">Matches your PO number pattern</span></div><span class="val-res">PO-2024-0284</span></div>
          <div class="val-row flag"><span class="val-ic warn">!</span><div><b>Example of a flagged check</b><span class="d">Lines sum to $14,204.00 but subtotal reads $14,240.00, so the field is sent to review with a low-confidence score</span></div><span class="val-res">review</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. SELF-SERVE OR MANAGED -->
  <section class="sec stone" id="managed">
    <div class="container">
      <div class="managed">
        <span class="eyebrow">Self-serve or managed</span>
        <h2>Don&rsquo;t want to build the AP config yourself? <em>Our team can run the extraction backend for you.</em></h2>
        <p>Solutions engineers handle plan, build, deploy, and adjust on your behalf. You see clean JSON in your API response. Same engine as self-serve, with the configuration work outsourced.</p>
        <div class="m-steps">
          <div class="m-step"><i>01</i><b>Plan</b><span>Engineers review your samples and pick the right method</span></div>
          <div class="m-step"><i>02</i><b>Build</b><span>SenseML configs written from your samples</span></div>
          <div class="m-step"><i>03</i><b>Deploy</b><span>Same engine as self-serve, ready for production</span></div>
          <div class="m-step"><i>04</i><b>Adjust</b><span>Configs updated when formats shift or new edge cases appear</span></div>
          <div class="m-step"><i>05</i><b>Integrate</b><span>Help with custom integration into your downstream systems</span></div>
        </div>
        <div class="m-actions">
          <a class="m-btn p" href="https://www.sensible.so/managed-services">See managed services →</a>
          <a class="m-btn s" href="https://www.sensible.so/contact-us">Talk to our team</a>
        </div>
      </div>
    </div>
  </section>

  <!-- 9. SUPPORTED FORMATS -->
  <section class="sec white" id="formats">
    <div class="container">
      <div class="sec-head">
        <span class="sec-eyebrow">Supported formats</span>
        <h2 class="sec-h2">Any vendor, any accounting system, any country</h2>
        <p class="sec-desc">The extraction logic is explicit in SenseML, not hidden in prompt tuning, so new formats can be configured quickly and audited later.</p>
      </div>
      <div class="fmt-list">
        <div class="fmt-row"><h3>By source<small>accounting systems</small></h3><ul class="field-list">{chips(['QuickBooks','Xero','NetSuite','SAP','Oracle','FreshBooks','Wave','Custom / manual invoices'])}</ul></div>
        <div class="fmt-row"><h3>By type<small>invoice variants</small></h3><ul class="field-list">{chips(['Standard invoices','Credit memos','Debit notes','Proforma invoices','Recurring invoices','Construction progress billing'])}</ul></div>
        <div class="fmt-row"><h3>By AP document<small>for three-way matching</small></h3><ul class="field-list">{chips(['Purchase orders','Goods receipts','Remittance advices'])}</ul></div>
      </div>
      <p class="fmt-note">Three-way matching needs all three document types extracted consistently, so purchase orders and goods receipts run through the same schema-validated pipeline as invoices.</p>
    </div>
  </section>

  <!-- 10. FAQ -->
  <section class="faq-section" id="faq" style="background:var(--bg-stone-subtle)">
    <div class="container">
      <div class="sec-head">
        <span class="sec-eyebrow">Common questions</span>
        <h2 class="sec-h2">Answers for AP teams</h2>
        <p class="sec-desc">Straight answers on matching, duplicates, pricing, and where Sensible stops and your AP system starts.</p>
      </div>
      <div class="faq-container">
        {''.join(faqs_ap)}
      </div>
    </div>
  </section>

  <!-- 11. CLOSING CTA -->
  <section class="cta-banner">
    <div class="cta-inner">
      <h2 class="cta-h2">Turn your next invoice into JSON.</h2>
      <p class="cta-p">Bring the supplier invoice your team dreads. If it works on that one, you&rsquo;ll know.</p>
      <div class="cta-btns">
        <a href="https://app.sensible.so/register/" class="cta-btn-primary">Start free trial →</a>
        <a href="https://www.sensible.so/contact-us" class="cta-btn-secondary">Talk to our team</a>
      </div>
      <p class="cta-note">Free 14-day trial · No credit card required · Start extracting in minutes</p>
    </div>
  </section>

  {footer_html}

<script>
(function () {{
  var tabs = document.querySelectorAll('.demo-tab');
  tabs.forEach(function (t) {{
    t.addEventListener('click', function () {{
      tabs.forEach(function (x) {{ x.setAttribute('aria-selected', x === t ? 'true' : 'false'); }});
      document.querySelectorAll('.demo-pane').forEach(function (p) {{ p.classList.toggle('active', p.id === 'pane-' + t.dataset.pane); }});
    }});
  }});
  document.querySelectorAll('.ft-tab').forEach(function (t) {{
    t.addEventListener('click', function () {{
      document.querySelectorAll('.ft-tab').forEach(function (x) {{ x.setAttribute('aria-selected', x === t ? 'true' : 'false'); }});
      document.querySelectorAll('.ft-pane').forEach(function (p) {{ p.classList.toggle('active', p.id === 'ft-' + t.dataset.ft); }});
    }});
  }});
  function toggle(pane, f, on) {{
    pane.querySelectorAll('[data-f="' + f + '"]').forEach(function (el) {{ el.classList.toggle('hl', on); }});
  }}
  document.querySelectorAll('.demo-pane').forEach(function (pane) {{
    pane.addEventListener('mouseover', function (e) {{ var el = e.target.closest('[data-f]'); if (el) toggle(pane, el.dataset.f, true); }});
    pane.addEventListener('mouseout', function (e) {{ var el = e.target.closest('[data-f]'); if (el) toggle(pane, el.dataset.f, false); }});
  }});
}})();
</script>
'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Accounts Payable Automation: Invoice Data Extraction | Sensible</title>
  <meta name="description" content="Sensible is the extraction layer under your AP workflow: schema-validated invoice, PO and receipt data, traced to source coordinates and scored for confidence. Free 14-day trial."/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,300;0,400;0,500;1,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
  <style>
{base_css}
{marquee_css}
{sechead_css}
{faq_css}
{cta_footer_css}
{new_css}
  </style>
</head>
<body>
{body}
</body>
</html>
'''
open('accounts-payable.html', 'w').write(html)
print('wrote accounts-payable.html', len(html))
