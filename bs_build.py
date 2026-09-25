#!/usr/bin/env python3
"""Builds the /doc-types/bank-statements page with a specialized Doc-Type structure.

Outputs:
  bs/fragment.html             Doc-type page body fragment
  bank-statements.html         Standalone demo page
  doc-types/bank-statements.html Subdirectory route
"""
import os
from bs_art import hero_rects, mini, icon, senseml_vs_llm_art

src = open('index.html').read().split('\n')
L = lambda a, b: '\n'.join(src[a - 1:b])
full = '\n'.join(src)
ap_css = open('ap/ap.css').read()
bs_css = open('bs/bs.css').read()
bs_js = open('bs/bs.js').read()

# ============================================================ FIELD DEFINITIONS
FIELD_TABS = [
    ('header', 'Header & Account', '01', 8, [
        ('Financial institution', 'institution_name', 'string', 'Identified and normalized across 150+ national, regional, and fintech banks.', ''),
        ('Account number', 'account_number', 'string', 'Masked or full account number; exact format kept for audit & deduplication.', ''),
        ('Routing / Sort code', 'routing_number', 'string', 'ABA 9-digit routing number, UK sort code, or SWIFT/BIC code.', 'ABA check'),
        ('Account holder name', 'account_holder_name', 'string', 'Legal business or individual entity name on record.', ''),
        ('Account holder address', 'account_holder_address', 'string', 'Street address and ZIP code as printed in the header.', ''),
        ('Statement start date', 'period_start_date', 'date', 'Normalized to ISO 8601, with raw printed text preserved as <code>source</code>.', ''),
        ('Statement end date', 'period_end_date', 'date', 'Normalized to ISO 8601, defining the exact accounting cycle.', ''),
        ('Account classification', 'account_type', 'string', 'Checking, savings, corporate treasury, money market, or credit facility.', ''),
    ]),
    ('txns', 'Transactions', '02', 8, [
        ('Posting date', 'posting_date', 'date', 'ISO 8601 date when the transaction officially settled on the ledger.', ''),
        ('Value / Effective date', 'value_date', 'date', 'Effective settlement date when distinguished by the bank.', ''),
        ('Description / Memo', 'description', 'string', 'Full multi-line narrative, counterparty name, and payment reference.', ''),
        ('Transaction type', 'transaction_type', 'string', 'Structured category: ACH, wire, check, card, fee, interest, or sweep.', ''),
        ('Amount', 'amount', 'currency', 'Signed numeric amount (positive credits, negative debits), keeping exact raw text.', 'Math sum'),
        ('Running balance', 'running_balance', 'currency', 'Account balance after line execution; verified sequentially across pages.', 'Balance check'),
        ('Check number', 'check_number', 'string', 'Check sequence number extracted from line description or dedicated column.', ''),
        ('Category / Counterparty', 'category', 'string', 'Automated transaction labeling (payroll, tax, merchant payout, SaaS, rent).', ''),
    ]),
    ('summary', 'Summary & Balances', '03', 7, [
        ('Beginning balance', 'beginning_balance', 'currency', 'Starting ledger balance; checked against prior period ending balance.', 'Reconciled'),
        ('Total deposits / additions', 'total_deposits', 'currency', 'Sum of all credits, wires in, and merchant payouts during the cycle.', 'Math check'),
        ('Total withdrawals / debits', 'total_withdrawals', 'currency', 'Sum of all debits, ACH withdrawals, and checks cleared.', 'Math check'),
        ('Interest & yield earned', 'interest_earned', 'currency', 'Yield, dividends, or interest credited during the statement period.', ''),
        ('Service fees & charges', 'total_fees', 'currency', 'Account maintenance fees, wire fees, and overdraft charges.', ''),
        ('Ending balance', 'ending_balance', 'currency', 'Closing ledger balance: must mathematically reconcile with beginning + credits − debits.', 'Reconciled'),
        ('Average daily balance', 'average_daily_balance', 'currency', 'Average ledger balance over the period, key for credit underwriting.', ''),
    ]),
]


def fields_block():
    tabs = ''.join(
        f'<button class="ap-ftab" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-ft="{k}">'
        f'<span class="n">{num}</span><span class="t">{name}</span><span class="c">{n}</span></button>'
        for i, (k, name, num, n, _) in enumerate(FIELD_TABS))
    panes = ''
    for i, (k, name, num, n, rows) in enumerate(FIELD_TABS):
        body = ''.join(
            f'<div class="ap-frow"><div class="ap-fname">{f}</div>'
            f'<div class="ap-fkey"><code>{key}</code><span class="ap-type t-{typ}">{typ}</span></div>'
            f'<div class="ap-fnote">{note}</div>'
            f'<div class="ap-fchk">{f"<span class=ap-chk>{chk}</span>" if chk else ""}</div></div>'
            for f, key, typ, note, chk in rows)
        panes += (f'<div class="ap-fpane{" on" if i == 0 else ""}" id="ap-f-{k}" role="tabpanel">'
                  f'<div class="ap-frow h"><div>Field</div><div>Schema key</div><div>How Sensible handles it</div><div>Validated in</div></div>{body}</div>')
    return tabs, panes


ftabs, fpanes = fields_block()

# ============================================================ CHALLENGES
CHALLENGES = [
    ('01', 'Multi-page transaction tables', 'Statements frequently span 10, 30, or 100+ pages with repeated headers, variable column widths, multi-line wire descriptions, and footnote breaks. Deterministic SenseML table anchors parse transactions continuously across breaks without losing row alignment.', 'tables', ''),
    ('02', 'Running balance arithmetic', 'Do all transaction credits and debits equal the stated period change? Does the running balance reconcile after every single row? Sensible re-calculates the ledger mathematically to catch OCR character misreads before they reach underwriting.', 'balance', ''),
    ('03', 'Tamper & layout anomaly signals', 'Detecting font inconsistencies, bounding box misalignments, suspicious metadata, and balance math contradictions that signal altered or fabricated statements before loans or credit lines are approved.', 'fraud', ''),
    ('04', 'Multi-account package splitting', 'Banks frequently bundle commercial checking, operating reserves, and money market schedules into a single PDF packet. Sensible isolates each account schedule and extracts them into discrete, cleanly keyed sub-ledgers.', 'multi_account', ''),
]
chal = ''.join(
    f'<div class="ap-cell" data-reveal><div class="ap-num">{n}{f"<span class=ap-tagline>{tg}</span>" if tg else ""}</div><h3>{t}</h3><p>{d}</p>{mini(m)}</div>'
    for n, t, d, m, tg in CHALLENGES)

# ============================================================ VALIDATION CHECKS
CHECKS = (
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Beginning balance matches statement</b><span class="d">Opening balance verified against account opening ledger</span></div><span class="res" data-count="124660.90">$124,660.90</span></div>'
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Transactions sum to period totals</b><span class="d">All 38 credits &amp; debits sum exactly to +$42,500.00 / &minus;$18,240.50</span></div><span class="res" data-count="24259.50">+$24,259.50</span></div>'
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Ending balance reconciles</b><span class="d">Beginning balance + total deposits &minus; total withdrawals = ending balance</span></div><span class="res" data-count="148920.40">$148,920.40</span></div>'
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Running balance continuous</b><span class="d">Every row balance equals previous row plus transaction amount</span></div><span class="res">38 / 38 rows pass</span></div>'
    '<div class="ap-check flag"><span class="ic">!</span><div><b>A check that fails</b><span class="d">Transactions sum to +$42,500.00 but summary header reads +$45,200.00 (transposition typo in document or altered PDF), flagged with 0.38 confidence and sent to underwriting review</span></div><span class="res">review flagged</span></div>')

# ============================================================ INSTITUTIONS MATRIX
BANKS = [
    ('JPMorgan Chase', 'Commercial checking, treasury services, sweep accounts, and credit facilities.', 'Top US Bank', 'us', 'v2.8 · Table Native'),
    ('Bank of America', 'Advantage business checking, preferred treasury, and CD statements.', 'Top US Bank', 'us', 'v2.6 · Anchored'),
    ('Wells Fargo', 'Commercial treasury management, analysis checking, and payroll reserves.', 'Top US Bank', 'us', 'v2.4 · Multi-page'),
    ('Citibank N.A.', 'Global transaction banking, multi-currency statements, and wire summaries.', 'Top US Bank', 'us', 'v2.5 · Native'),
    ('Silicon Valley Bank', 'Venture debt, startup checking, treasury yield, and FX wires.', 'Top US Bank', 'us', 'v2.9 · Verified'),
    ('Mercury', 'Modern tech checking, automated yield funds, and corp card sweeps.', 'Fintech & Neobank', 'fintech', 'v3.1 · API Ready'),
    ('Brex Treasury', 'Business account statements, rewards payouts, and cash reserves.', 'Fintech & Neobank', 'fintech', 'v2.2 · Verified'),
    ('Stripe Treasury', 'Merchant payouts, platform balance accounts, and dispute reserve statements.', 'Fintech & Neobank', 'fintech', 'v2.7 · Native'),
    ('Wise Business', 'Multi-currency balances, cross-border payments, and IBAN schedules.', 'Fintech & Neobank', 'fintech', 'v2.1 · Multi-currency'),
    ('Barclays UK', 'UK corporate checking, BACS schedules, sort code verification, and VAT statements.', 'International', 'intl', 'v2.3 · Sort code'),
    ('HSBC Global', 'International commercial banking, multi-currency ledgers, and trade finance.', 'International', 'intl', 'v2.0 · Global'),
    ('Royal Bank of Canada', 'Canadian commercial accounts, CAD/USD dual currency, and EFT statements.', 'International', 'intl', 'v2.5 · Dual CAD/USD'),
]
bank_cards = ''.join([
    f'<div class="bs-bank-card" data-category="{cat}">'
    f'<div class="bs-bank-top"><span class="bs-bank-name">{name}</span><span class="bs-bank-badge">{tag}</span></div>'
    f'<div class="bs-bank-meta">{meta}</div>'
    f'<div class="bs-bank-foot"><span>{badge}</span><span>100% test coverage</span></div>'
    f'</div>'
    for name, meta, tag, cat, badge in BANKS
])

# ============================================================ USE CASES
USE_CASES = [
    ('SME Lending & MCA Underwriting', 'Calculate Debt Service Coverage Ratios (DSCR), monthly revenue velocity, average daily balances, and NSF instances directly from verified transaction feeds.', 'Lending & Credit', 'ledger'),
    ('Automated Bookkeeping & ERP Sync', 'Feed cleared transaction tables directly into NetSuite, QuickBooks, or Xero with continuous bank reconciliation and double-entry validation.', 'Accounting & ERP', 'flow'),
    ('Mortgage & Income Verification', 'Instantly verify borrower cash reserves, check deposit sourcing, and validate recurring payroll income without human line-item reviews.', 'Mortgage & VOI', 'shield'),
    ('Corporate Treasury & Liquidity', 'Consolidate multi-bank balances across dozens of institutions into a unified cash visibility ledger with automated sweep auditing.', 'Treasury Ops', 'bank'),
]
usecase_cards = ''.join([
    f'<div class="bs-usecase-card">'
    f'{icon(ic)}'
    f'<h3>{title}</h3>'
    f'<p>{desc}</p>'
    f'<span class="bs-usecase-tag">{tag}</span>'
    f'</div>'
    for title, desc, tag, ic in USE_CASES
])

# ============================================================ RELATED DOC TYPES
RELATED = [
    ('Tax Returns (1040 & 1120S)', 'Extract schedules, AGI, business income, and W-2 attachments with IRS schema mapping.', 'tax', 'tax-returns.html'),
    ('Pay Stubs & Earnings', 'Capture gross pay, net pay, YTD totals, tax withholdings, and employer metadata.', 'paystub', 'paystubs.html'),
    ('Balance Sheets & P&L', 'Parse financial statement tables, assets, liabilities, and revenue schedules.', 'pnl', 'financial-statements.html'),
    ('Accounts Payable Invoices', 'Extract vendor headers, multi-line item tables, and tax reconciliations.', 'invoice', 'accounts-payable.html'),
    ('ACORD Insurance Certificates', 'Extract policy limits, insured entities, carriers, and expiration dates.', 'acord', 'acord-certificates.html'),
]
related_cards = ''.join([
    f'<a class="bs-related-card" href="{url}">'
    f'{icon(ic)}'
    f'<h4>{title}</h4>'
    f'<p>{desc}</p>'
    f'<span class="bs-related-arrow">View Doc Type &rarr;</span>'
    f'</a>'
    for title, desc, ic, url in RELATED
])

# ============================================================ FAQS
FAQS = ''.join([
    f'<details class="ap-q" data-reveal open><summary>How does Sensible handle multi-page bank statements where tables span 20+ pages?<i>+</i></summary><div class="ap-q-a"><p>Sensible uses deterministic SenseML table definitions paired with layout-aware anchors. It recognizes column boundaries, multi-line transaction narratives, and page break headers, stitching rows together into a single continuous transaction array without skipping lines or misaligning debits and credits.</p></div></details>',
    f'<details class="ap-q" data-reveal><summary>How does arithmetic validation catch OCR errors and hallucinations?<i>+</i></summary><div class="ap-q-a"><p>Sensible executes automated math checks on every statement. It computes the delta between beginning balance and ending balance, sums all extracted credit and debit transactions, and checks that every single running balance row adds up. If an OCR misread turns a $1,200.00 charge into $1,700.00, the arithmetic mismatch is flagged immediately with an exact error breakdown and low confidence score.</p></div></details>',
    f'<details class="ap-q" data-reveal><summary>Can Sensible split statements that combine multiple accounts in one PDF?<i>+</i></summary><div class="ap-q-a"><p>Yes. Commercial banking statements frequently package checking, savings, payroll, and sweep accounts into a single file. Sensible classifies and partitions the document into individual account schedules, returning discrete JSON objects with their own account numbers, balance summaries, and transaction tables.</p></div></details>',
    f'<details class="ap-q" data-reveal><summary>Does Sensible support password-protected bank statements?<i>+</i></summary><div class="ap-q-a"><p>Yes. When submitting documents via the Sensible API, you can provide the document password in the request payload. Sensible unlocks the document in memory, processes the extraction, and ensures no unencrypted passwords or raw credentials are persisted.</p></div></details>',
    f'<details class="ap-q" data-reveal><summary>Can Sensible help detect altered or fraudulent bank statements?<i>+</i></summary><div class="ap-q-a"><p>Yes. Because Sensible verifies mathematical consistency across beginning balances, total deposits, total withdrawals, and running transaction rows, altered numbers (such as edited balances or injected deposits) immediately fail reconciliation. Additionally, Sensible exposes PDF metadata, font layout anomalies, and coordinate bounding boxes for every field so your risk engine can spot tampered documents.</p></div></details>',
    f'<details class="ap-q" data-reveal><summary>How is sensitive financial data protected, and what is your retention policy?<i>+</i></summary><div class="ap-q-a"><p>Sensible is SOC 2 Type II certified and HIPAA compliant. All document payloads and extracted data are encrypted with AES-256 in transit and at rest. We support configurable data retention policies, including zero-data retention (immediate purging after extraction) for regulated fintech and banking environments.</p></div></details>',
])

LOGOS = ['vouch.svg', 'limit.png', 'ledgebrook.svg', 'obie.svg', 'neptune-flood.svg', 'insurance-quantified.svg',
         'lettuce.svg', 'founder-shield.svg', 'compscience.svg', 'inclined.png', 'sterlingrisk.png']
logo_imgs = ''.join(f'<img src="assets/logos/{f}" alt="">' for f in LOGOS * 2)

# ============================================================ FRAGMENT BUILD
fragment = f'''<div class="ap">

  <!-- 1. DOC-TYPE HERO: SPEC HEADER + INTERACTIVE PARSER WORKBENCH -->
  <section class="ap-hero" id="bs-hero">
    <div class="ap-hero-copy">
      <div class="bs-crumbs" data-hero>
        <a href="https://www.sensible.so">Home</a>
        <span class="sep">/</span>
        <a href="#bs-catalog">Document Types</a>
        <span class="sep">/</span>
        <span class="curr">Bank Statements</span>
      </div>
      <span class="ap-tag" data-hero>[ DOC TYPE · CONFIG LIBRARY ]</span>
      <h1 class="ap-h1">Bank statement extraction &amp; OCR API, <em>pre-configured for production</em></h1>
      <p class="ap-lede" data-hero>Extract schema-validated transaction schedules, account metadata, and reconciled ledger balances from multi-page PDFs with pre-built SenseML configurations.</p>
      
      <!-- Spec Chips -->
      <div class="bs-spec-grid" data-hero>
        <div class="bs-spec-card">
          <div class="bs-spec-label">Doc Type ID</div>
          <div class="bs-spec-val">bank_statement</div>
        </div>
        <div class="bs-spec-card">
          <div class="bs-spec-label">Prebuilt Library</div>
          <div class="bs-spec-val">150+ Financial Institutions</div>
        </div>
        <div class="bs-spec-card">
          <div class="bs-spec-label">Supported Formats</div>
          <div class="bs-spec-val">PDF (native/scan), TIFF, PNG</div>
        </div>
        <div class="bs-spec-card">
          <div class="bs-spec-label">Math Engine</div>
          <div class="bs-spec-val">Start + Credits &minus; Debits = End</div>
        </div>
      </div>

      <div class="ap-btns" data-hero>
        <a class="ap-btn p" href="https://app.sensible.so/register/">Test with your statement</a>
        <a class="ap-btn s" href="#bs-catalog">Browse 150+ bank configs</a>
      </div>
      <div class="ap-note" data-hero>14-day free trial · Instant API access · No credit card</div>
    </div>

    <div class="ap-hero-panel">
      {hero_rects()}
      
      <!-- INTERACTIVE DOCUMENT WORKBENCH -->
      <div class="bs-workbench">
        <!-- Top Toolbar -->
        <div class="bs-wb-bar">
          <div class="bs-wb-banks">
            <button class="bs-wb-bank-btn active" data-bank="chase">Chase Commercial</button>
            <button class="bs-wb-bank-btn" data-bank="bofa">Bank of America</button>
            <button class="bs-wb-bank-btn" data-bank="mercury">Mercury Treasury</button>
            <button class="bs-wb-bank-btn" data-bank="wells">Wells Fargo</button>
          </div>
          <div class="bs-wb-views">
            <button class="bs-wb-view-btn active" data-view="anatomy">Visual Anatomy</button>
            <button class="bs-wb-view-btn" data-view="json">Schema JSON</button>
            <button class="bs-wb-view-btn" data-view="senseml">SenseML Rule</button>
            <button class="bs-wb-view-btn" data-view="api">cURL</button>
          </div>
        </div>

        <!-- Workbench Content Area -->
        <div class="bs-wb-content">
          <!-- View 1: Visual Anatomy with Bounding Boxes -->
          <div class="bs-wb-panel active" id="bs-wb-panel-anatomy">
            <div class="bs-anatomy-split">
              <!-- Document Canvas -->
              <div class="bs-doc-view">
                <div class="bs-bbox-card active" id="bs-card-chase">
                  <!-- Header BBox -->
                  <div class="bs-bbox-box active" data-field="Header &amp; Institution" data-bbox="[32, 14, 480, 80]">
                    <span class="bs-bbox-badge ok">0.99 CONF</span>
                    <div style="font-weight:600;font-size:12px;">JPMorgan Chase Bank, N.A.</div>
                    <div style="color:#8B857B;font-size:10px;">Account: ...8842 &middot; Routing: 021000021 &middot; Period: Oct 01 - Oct 31, 2024</div>
                    <div style="color:#4A4540;font-size:10px;margin-top:2px;">Stillwater Robotics, Inc. &middot; Cambridge, MA</div>
                  </div>
                  <!-- Summary Balances BBox -->
                  <div class="bs-bbox-box" data-field="Summary Balances" data-bbox="[420, 110, 520, 190]">
                    <span class="bs-bbox-badge ok">MATH RECONCILED</span>
                    <div style="display:flex;justify-content:space-between;font-size:10px;">
                      <span>Beginning: <b>$124,660.90</b></span>
                      <span>Deposits (+12): <b style="color:#2E7B40">+$42,500.00</b></span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;margin-top:2px;">
                      <span>Withdrawals (-26): <b>&minus;$18,240.50</b></span>
                      <span>Ending: <b>$148,920.40</b></span>
                    </div>
                  </div>
                  <!-- Transactions Table BBox -->
                  <div class="bs-bbox-box" data-field="Transaction Schedule" data-bbox="[32, 210, 540, 680]">
                    <span class="bs-bbox-badge">TABLE &middot; 38 ROWS</span>
                    <table class="ap-tbl" style="margin-bottom:0;">
                      <tr><th>Date</th><th>Description</th><th>Amount</th><th>Running Bal</th></tr>
                      <tr><td>10/04</td><td>ACH Deposit: Stripe Payments Payout</td><td style="color:#2E7B40">+$42,500.00</td><td>$167,160.90</td></tr>
                      <tr><td>10/12</td><td>ACH Debit: Gusto Payroll Tax &amp; Salary</td><td>&minus;$15,120.50</td><td>$152,040.40</td></tr>
                      <tr><td>10/18</td><td>POS Purchase: AWS Cloud Infrastructure</td><td>&minus;$3,120.00</td><td>$148,920.40</td></tr>
                    </table>
                  </div>
                </div>
              </div>

              <!-- Real-time Field Inspector -->
              <div class="bs-side-inspector">
                <div class="bs-inspect-title"><span>Field Inspector</span><span style="color:var(--ap-ok)">LIVE AUDIT</span></div>
                <div class="bs-inspect-row"><span class="k">Selected Element</span><span class="v code" id="bs-ins-field">Header &amp; Institution</span></div>
                <div class="bs-inspect-row"><span class="k">Institution</span><span class="v" id="bs-ins-bank">JPMorgan Chase Bank, N.A.</span></div>
                <div class="bs-inspect-row"><span class="k">Account Number</span><span class="v code" id="bs-ins-acct">...8842</span></div>
                <div class="bs-inspect-row"><span class="k">Cycle Dates</span><span class="v" id="bs-ins-period">Oct 01, 2024 - Oct 31, 2024</span></div>
                <div class="bs-inspect-row"><span class="k">Ending Balance</span><span class="v code" id="bs-ins-ending">$148,920.40</span></div>
                <div class="bs-inspect-row"><span class="k">Confidence Score</span><span class="v ok">0.99 (99.8%)</span></div>
                <div class="bs-inspect-row"><span class="k">Bounding Box</span><span class="v code" id="bs-ins-bbox">[32, 14, 480, 80]</span></div>
                <div class="bs-inspect-row"><span class="k">Math Status</span><span class="v ok">Reconciled (0.00 delta)</span></div>
                <div style="margin-top:14px;padding:10px;background:var(--ap-soft);border-radius:4px;font-size:10px;color:var(--ap-body);">
                  Every extracted data point links directly to page coordinates for human-in-the-loop review.
                </div>
              </div>
            </div>
          </div>

          <!-- View 2: Schema JSON -->
          <div class="bs-wb-panel" id="bs-wb-panel-json">
            <div class="bs-code-panel">
<pre><code><span class="ap-jk">"account_metadata"</span>: &#123;
  <span class="ap-jk">"institution"</span>: <span class="ap-js">"JPMorgan Chase Bank, N.A."</span>,
  <span class="ap-jk">"account_number"</span>: <span class="ap-js">"...8842"</span>,
  <span class="ap-jk">"routing_number"</span>: <span class="ap-js">"021000021"</span>,
  <span class="ap-jk">"period_start"</span>: <span class="ap-js">"2024-10-01"</span>,
  <span class="ap-jk">"period_end"</span>: <span class="ap-js">"2024-10-31"</span>,
  <span class="ap-jk">"currency"</span>: <span class="ap-js">"USD"</span>
&#125;,
<span class="ap-jk">"balances"</span>: &#123;
  <span class="ap-jk">"beginning_balance"</span>: <span class="ap-jn">124660.90</span>,
  <span class="ap-jk">"total_deposits"</span>: <span class="ap-jn">42500.00</span>,
  <span class="ap-jk">"total_withdrawals"</span>: <span class="ap-jn">-18240.50</span>,
  <span class="ap-jk">"ending_balance"</span>: <span class="ap-jn">148920.40</span>,
  <span class="ap-jk">"reconciliation_delta"</span>: <span class="ap-jn">0.00</span>
&#125;,
<span class="ap-jk">"transactions"</span>: [
  &#123;
    <span class="ap-jk">"date"</span>: <span class="ap-js">"2024-10-04"</span>,
    <span class="ap-jk">"description"</span>: <span class="ap-js">"ACH Deposit: Stripe Payments Payout"</span>,
    <span class="ap-jk">"type"</span>: <span class="ap-js">"ACH"</span>,
    <span class="ap-jk">"amount"</span>: <span class="ap-jn">42500.00</span>,
    <span class="ap-jk">"running_balance"</span>: <span class="ap-jn">167160.90</span>,
    <span class="ap-jk">"bbox"</span>: [112, 210, 480, 18],
    <span class="ap-jk">"confidence"</span>: <span class="ap-jn">0.99</span>
  &#125;
]</code></pre>
            </div>
          </div>

          <!-- View 3: SenseML Configuration -->
          <div class="bs-wb-panel" id="bs-wb-panel-senseml">
            <div class="bs-code-panel">
<pre><code id="bs-code-senseml">&#123;
  <span class="ap-jk">"fields"</span>: [
    &#123;
      <span class="ap-jk">"id"</span>: <span class="ap-js">"transactions"</span>,
      <span class="ap-jk">"type"</span>: <span class="ap-js">"table"</span>,
      <span class="ap-jk">"method"</span>: &#123;
        <span class="ap-jk">"id"</span>: <span class="ap-js">"row"</span>,
        <span class="ap-jk">"stop"</span>: <span class="ap-js">"DAILY BALANCE SUMMARY"</span>,
        <span class="ap-jk">"columns"</span>: [
          &#123; <span class="ap-jk">"id"</span>: <span class="ap-js">"date"</span>, <span class="ap-jk">"type"</span>: <span class="ap-js">"date"</span> &#125;,
          &#123; <span class="ap-jk">"id"</span>: <span class="ap-js">"description"</span>, <span class="ap-jk">"type"</span>: <span class="ap-js">"string"</span> &#125;,
          &#123; <span class="ap-jk">"id"</span>: <span class="ap-js">"amount"</span>, <span class="ap-jk">"type"</span>: <span class="ap-js">"currency"</span> &#125;,
          &#123; <span class="ap-jk">"id"</span>: <span class="ap-js">"balance"</span>, <span class="ap-jk">"type"</span>: <span class="ap-js">"currency"</span> &#125;
        ]
      &#125;
    &#125;
  ]
&#125;</code></pre>
            </div>
          </div>

          <!-- View 4: cURL API Request -->
          <div class="bs-wb-panel" id="bs-wb-panel-api">
            <div class="bs-code-panel">
<pre><code><span class="ap-jc"># Direct Extraction Request via Sensible REST API</span>
curl -X POST https://api.sensible.so/v0/extract/bank_statement \
  -H <span class="ap-js">"Authorization: Bearer $SENSIBLE_API_KEY"</span> \
  -H <span class="ap-js">"Content-Type: application/pdf"</span> \
  -F <span class="ap-js">"file=@chase_commercial_oct2024.pdf"</span> \
  -F <span class="ap-js">"configuration_id=bank_statement/chase_v2"</span></code></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 2. STATS RIBBON + LOGOS -->
  <div class="ap-ribbon"><div class="ap-wrap"><div class="ap-ribbon-grid">
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">150+</p><p class="ap-ribbon-l">Pre-built bank configs</p></div>
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">75M+</p><p class="ap-ribbon-l">Documents processed</p></div>
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">SOC 2 + HIPAA</p><p class="ap-ribbon-l">Certified infrastructure</p></div>
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">0.00 Delta</p><p class="ap-ribbon-l">Ledger math verification</p></div>
  </div></div></div>
  <div class="ap-logos"><div class="ap-logos-cap">Trusted by fintechs and lenders turning complex financial documents into production data</div><div class="ap-logos-track">{logo_imgs}</div></div>

  <!-- 3. PRE-BUILT BANK CONFIGURATION CATALOG (150+ INSTITUTION MATRIX) -->
  <section class="ap-sec" id="bs-catalog">
    <div class="ap-wrap">
      <div class="ap-head ap-center" data-reveal>
        <span class="ap-kicker">Pre-built Config Library</span>
        <h2 class="ap-h2">Production configurations for 150+ financial institutions</h2>
        <p class="ap-lede">Tested across tens of millions of statements. Zero setup required for top national, commercial, and fintech banks.</p>
      </div>

      <!-- Filter Tabs -->
      <div class="bs-matrix-filters" data-reveal>
        <button class="bs-matrix-btn active" data-filter="all">All Institutions (150+)</button>
        <button class="bs-matrix-btn" data-filter="us">Top US Commercial</button>
        <button class="bs-matrix-btn" data-filter="fintech">Fintech &amp; Neobanks</button>
        <button class="bs-matrix-btn" data-filter="intl">International &amp; Global</button>
      </div>

      <!-- Grid of Bank Cards -->
      <div class="bs-bank-grid" data-reveal>
        {bank_cards}
      </div>
    </div>
  </section>

  <!-- 4. SENSEML VS PURE LLM PARSING (WHY DETERMINISTIC RULES MATTER) -->
  <section class="ap-sec ap-band" id="bs-comparison">
    <div class="ap-wrap">
      <div class="ap-head ap-center" data-reveal>
        <span class="ap-kicker">Under the Hood</span>
        <h2 class="ap-h2">Why financial statements need <em>SenseML deterministic rules</em></h2>
        <p class="ap-lede">LLM-only parsers suffer from token limits, hallucinate pennies in balances, and skip lines on 50-page PDFs. Sensible combines layout-aware anchors with ledger arithmetic.</p>
      </div>

      <div class="bs-cmp-wrap" data-reveal>
        <div class="bs-cmp-list">
          <div class="bs-cmp-item">
            <span class="bullet">1</span>
            <div>
              <b>Zero Hallucinated Pennies</b>
              <p>Numbers are pulled from raw coordinate boxes and validated mathematically. If a digit doesn&rsquo;t sum, it is flagged immediately.</p>
            </div>
          </div>
          <div class="bs-cmp-item">
            <span class="bullet">2</span>
            <div>
              <b>Continuous Multi-Page Table Anchors</b>
              <p>SenseML table methods track table headers across page boundaries without dropping rows on multi-page statements.</p>
            </div>
          </div>
          <div class="bs-cmp-item">
            <span class="bullet">3</span>
            <div>
              <b>Exact Audit Trails to Source Coordinates</b>
              <p>Every single transaction row retains its exact bounding box and page index for compliance audits.</p>
            </div>
          </div>
        </div>

        <div style="text-align:center;">
          {senseml_vs_llm_art()}
        </div>
      </div>
    </div>
  </section>

  <!-- 5. FOUR PRODUCTION CHALLENGES -->
  <section class="ap-sec" id="bs-challenges">
    <div class="ap-wrap ap-head ap-center" data-reveal>
      <span class="ap-kicker">Production Reliability</span>
      <h2 class="ap-h2">Where bank statement parsing breaks in production</h2>
      <p class="ap-lede">Multi-page splits, altered balances, and combined statements break generic OCR tools. Here is how Sensible solves them.</p>
    </div>
    <div class="ap-grid ap-g4">{chal}</div>
  </section>

  <!-- 6. DOCUMENT ANATOMY & EXTRACTED FIELDS EXPLORER -->
  <section class="ap-sec" id="bs-fields">
    <div class="ap-wrap"><div class="ap-fields">
      <div class="ap-fields-nav" data-reveal>
        <span class="ap-kicker">Data Dictionary</span>
        <h2 class="ap-h2">The extracted schema</h2>
        <p class="ap-lede">Structured specifically for credit underwriting, cash flow modeling, and accounting reconciliation. Every field comes strictly typed with bounding box coordinates.</p>
        <div class="ap-ftabs" role="tablist" aria-label="Field groups">{ftabs}</div>
      </div>
      <div data-reveal>
        {fpanes}
        <div class="ap-more"><b>Custom schema extensions available.</b><span>Commonly added downstream: NSF/overdraft flags, recurring payroll tags, merchant payout classification, and check image extraction.</span></div>
      </div>
    </div></div>
  </section>

  <!-- 7. VALIDATION & RECONCILIATION ENGINE -->
  <section class="ap-sec ap-band" id="bs-validation">
    <div class="ap-wrap">
      <div class="ap-val">
        <div data-reveal>
          <span class="ap-kicker">Automated Reconciliation</span>
          <h2 class="ap-h2">How the ledger math gets checked</h2>
          <p class="ap-lede">A single OCR typo in a transaction amount ruins downstream debt-to-income and cash flow modeling. Sensible executes strict mathematical verification on every document: beginning balance + credits &minus; debits must equal ending balance, and running balances are checked row-by-row.</p>
        </div>
        <div class="ap-checks"><div class="ap-checks-h"><span>Reconciliation status</span><span>CHASE-...8842</span></div>{CHECKS}</div>
      </div>
      <div class="ap-quote">
        <div><span class="ap-kicker">Our position</span></div>
        <blockquote><p class="ap-qtext">We don&rsquo;t publish a flat accuracy percentage. Financial statements demand exact mathematical reconciliation, not probabilistic guesses.</p><cite>Sensible</cite></blockquote>
      </div>
    </div>
  </section>

  <!-- 8. DOWNSTREAM USE CASES -->
  <section class="ap-sec" id="bs-usecases">
    <div class="ap-wrap">
      <div class="ap-head ap-center" data-reveal>
        <span class="ap-kicker">Use Cases</span>
        <h2 class="ap-h2">Built for high-volume financial workflows</h2>
        <p class="ap-lede">Delivering verified financial feeds directly to underwriting models, ERPs, and risk engines.</p>
      </div>
      <div class="bs-usecase-grid" data-reveal>
        {usecase_cards}
      </div>
    </div>
  </section>

  <!-- 9. DEVELOPER QUICKSTART (API & SDKs) -->
  <section class="ap-sec ap-band" id="bs-quickstart">
    <div class="ap-wrap">
      <div class="ap-head ap-center" data-reveal>
        <span class="ap-kicker">Developer Integration</span>
        <h2 class="ap-h2">Integrate in minutes with REST API &amp; SDKs</h2>
        <p class="ap-lede">Send documents directly via API or webhook and receive normalized JSON in sub-second response times.</p>
      </div>

      <div class="bs-api-box" data-reveal>
        <div class="bs-api-nav">
          <button class="bs-api-tab active" data-lang="curl">cURL</button>
          <button class="bs-api-tab" data-lang="python">Python SDK</button>
          <button class="bs-api-tab" data-lang="node">Node.js SDK</button>
          <button class="bs-api-tab" data-lang="webhook">Webhook Payload</button>
        </div>
        <div class="bs-api-code active" id="bs-code-curl">
<pre><code># Extract structured bank statement data via REST API
curl -X POST https://api.sensible.so/v0/extract/bank_statement \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/pdf" \
  --data-binary "@statement.pdf"</code></pre>
        </div>
        <div class="bs-api-code" id="bs-code-python">
<pre><code>import sensible
from sensible import SensibleClient

client = SensibleClient(api_key="YOUR_API_KEY")

# Extract bank statement
response = client.extract(
    document_type="bank_statement",
    file=open("statement.pdf", "rb")
)

print(f"Ending Balance: {{response.parsed_document['balances']['ending_balance']}}")
print(f"Total Transactions: {{len(response.parsed_document['transactions'])}}")</code></pre>
        </div>
        <div class="bs-api-code" id="bs-code-node">
<pre><code>import {{ SensibleSDK }} from "sensible-api";
import fs from "fs";

const sensible = new SensibleSDK({{ apiKey: process.env.SENSIBLE_API_KEY }});

const result = await sensible.extract({{
  documentType: "bank_statement",
  file: fs.createReadStream("statement.pdf")
}});

console.log("Reconciled Balance:", result.parsed_document.balances.ending_balance);</code></pre>
        </div>
        <div class="bs-api-code" id="bs-code-webhook">
<pre><code>{{
  "event": "extraction.completed",
  "document_id": "doc_8f921a48c90b",
  "document_type": "bank_statement",
  "status": "SUCCESS",
  "validation_passed": true,
  "data_url": "https://api.sensible.so/v0/documents/doc_8f921a48c90b/output"
}}</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- 10. RELATED DOC TYPES CROSS-NAVIGATION -->
  <section class="ap-sec" id="bs-related">
    <div class="ap-wrap">
      <div class="ap-head ap-center" data-reveal>
        <span class="ap-kicker">Document Type Library</span>
        <h2 class="ap-h2">Explore related financial document types</h2>
        <p class="ap-lede">Sensible supports hundreds of structured and unstructured document types across lending, insurance, and accounting.</p>
      </div>
      <div class="bs-related-grid" data-reveal>
        {related_cards}
      </div>
    </div>
  </section>

  <!-- 11. FAQ -->
  <section class="ap-sec ap-band" id="bs-faq">
    <div class="ap-wrap"><div class="ap-faq">
      <div class="ap-faq-head" data-reveal>
        <span class="ap-kicker">Common questions</span>
        <h2 class="ap-h2">Questions from engineering &amp; risk teams</h2>
        <p class="ap-lede">Multi-page tables, fraud checks, math validation, and data security.</p>
      </div>
      <div class="ap-faq-list">{FAQS}</div>
    </div></div>
  </section>

</div>'''

open('bs/fragment.html', 'w').write(fragment)

# ============================================================ STANDALONE PAGE BUILD
base_css = L(20, 249)
cta_footer_css = L(998, 1160)
nav_html = full[full.index('<!-- Navbar -->'):full.index('<!-- 1. HERO FOLD')]
cta_html = full[full.index('<section class="cta-banner">'):full.index('</footer>') + len('</footer>')]
site_extra = '''
    @media (max-width: 991px) { .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px 24px; } }
    @media (max-width: 860px) { .navbar-inner { height: 60px; } .nav-links { display: none; } .nav-cta-group { display: none !important; } .mobile-toggle { display: block; } }
    @media (max-width: 767px) { .container { padding: 0 20px; } .cta-h2 { font-size: 28px; } .cta-banner { padding: 56px 24px; }
      .footer { padding: 64px 0 40px; } .footer-grid { grid-template-columns: 1fr; gap: 40px; padding-bottom: 40px; } .footer-bottom { flex-direction: column; align-items: flex-start; } }
    @media (max-width: 480px) { .nav-logo img { height: 22px !important; } }
    .sensible-font { font-family: 'Matter SQ', var(--font-sans); font-weight: 500; }
'''

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Bank Statement Extraction &amp; OCR API | Sensible Document Types</title>
  <meta name="description" content="Pre-built SenseML configurations for extracting multi-page bank statements across 150+ institutions. Automated ledger arithmetic, running balance checks, and bounding box coordinates."/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:wght@300;400;500&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
  <script>document.documentElement.classList.add('ap-js')</script>
  <style>
{base_css}
{cta_footer_css}
{site_extra}
{ap_css}
{bs_css}
  </style>
</head>
<body>
{nav_html}
{fragment}
{cta_html}
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script>
{bs_js}
</script>
</body>
</html>
'''

open('bank-statements.html', 'w').write(page)
os.makedirs('doc-types', exist_ok=True)
page_nested = page.replace('src="assets/', 'src="../assets/').replace("url('assets/", "url('../assets/")
open('doc-types/bank-statements.html', 'w').write(page_nested)
print('Generated: bs/fragment.html, bank-statements.html, doc-types/bank-statements.html')
