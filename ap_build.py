#!/usr/bin/env python3
"""Builds the accounts-payable page.

Outputs
  ap/fragment.html       page body only (no nav/footer): what goes into Webflow as elements
  accounts-payable.html  standalone demo page = real nav + fragment + real CTA/footer + GSAP
"""
import re
from ap_art import hero_rects, chaos_scene, mini, pipe_ill, icon, schematic

src = open('index.html').read().split('\n')
L = lambda a, b: '\n'.join(src[a - 1:b])
full = '\n'.join(src)
css = open('ap/ap.css').read()
js = open('ap/ap.js').read()


# ============================================================ demo panes (source doc + JSON)
def jl(text, f=None):
    attr = f' data-f="{f}"' if f else ''
    return f'<span class="ap-jl"{attr}>{text}</span>'


K = lambda s: f'<span class="ap-jk">"{s}"</span>'
S = lambda s: f'<span class="ap-js">"{s}"</span>'
N = lambda s: f'<span class="ap-jn">{s}</span>'
C = lambda s: f'<span class="ap-jc">{s}</span>'


def fld(key, source, value, typ, f, comma=True, num=False):
    v = N(value) if num else S(value)
    return jl(f'  {K(key)}: {{ {K("source")}: {S(source)}, {K("value")}: {v}, {K("type")}: {S(typ)} }}{"," if comma else ""}', f)


def json_inv():
    return ''.join([
        jl('{'), jl(f'  {K("invoice_number")}: {S("NB-2024-0418")},', 'no'),
        jl(f'  {K("vendor")}: {S("Northbridge Studio LLC")},', 'vendor'),
        jl(f'  {K("bill_to")}: {S("Stillwater Robotics, Inc.")},', 'billto'),
        jl(f'  {K("po_number")}: {S("PO-2024-0284")},', 'po'),
        fld('issue_date', 'Apr 18, 2024', '2024-04-18', 'date', 'issue'),
        fld('due_date', 'May 18, 2024', '2024-05-18', 'date', 'due'),
        jl(f'  {K("payment_terms")}: {S("Net 30")},', 'terms'),
        jl(f'  {K("line_items")}: ['),
        jl(f'    {{ {K("description")}: {S("Strategy workshop facilitation")}, {K("qty")}: {N("2")}, {K("unit_price")}: {N("1850.00")}, {K("amount")}: {N("3700.00")} }},', 'li1'),
        jl(f'    {{ {K("description")}: {S("UX research interviews")}, {K("qty")}: {N("8")}, {K("unit_price")}: {N("425.00")}, {K("amount")}: {N("3400.00")} }},', 'li2'),
        jl(f'    {C("// + 3 more rows")}'), jl('  ],'),
        fld('subtotal', '$14,204.00', '14204.00', 'currency', 'sub', num=True),
        fld('tax_total', '$887.75', '887.75', 'currency', 'tax', num=True),
        jl(f'  {K("total_due")}: {{ {K("source")}: {S("$15,091.75")}, {K("value")}: {N("15091.75")}, {K("type")}: {S("currency")}, {K("confidence")}: {N("0.99")} }},', 'total'),
        jl(f'  {K("validation")}: {{', 'sub'),
        jl(f'    {K("line_items_sum_to_subtotal")}: {S("pass")}, {K("tax_matches_rate")}: {S("pass")},'),
        jl(f'    {K("total_reconciles")}: {S("pass")}, {K("po_reference_format")}: {S("pass")}'),
        jl('  }'), jl('}')])


def json_po():
    return ''.join([
        jl('{'), jl(f'  {K("po_number")}: {S("PO-2024-0284")},', 'po'),
        fld('order_date', 'Mar 28, 2024', '2024-03-28', 'date', 'odate'),
        jl(f'  {K("buyer")}: {S("Stillwater Robotics, Inc.")},', 'buyer'),
        jl(f'  {K("vendor")}: {S("Northbridge Studio LLC")},', 'vendor'),
        jl(f'  {K("payment_terms")}: {S("Net 30")},', 'terms'),
        jl(f'  {K("line_items")}: ['),
        jl(f'    {{ {K("description")}: {S("Strategy workshop facilitation")}, {K("qty")}: {N("2")}, {K("unit_price")}: {N("1850.00")}, {K("amount")}: {N("3700.00")} }},', 'li1'),
        jl(f'    {{ {K("description")}: {S("UX research interviews")}, {K("qty")}: {N("8")}, {K("unit_price")}: {N("425.00")}, {K("amount")}: {N("3400.00")} }},', 'li2'),
        jl(f'    {C("// + 3 more rows")}'), jl('  ],'),
        fld('subtotal', '$14,220.00', '14220.00', 'currency', 'sub', num=True),
        jl(f'  {K("total")}: {{ {K("source")}: {S("$14,220.00")}, {K("value")}: {N("14220.00")}, {K("type")}: {S("currency")}, {K("confidence")}: {N("0.99")} }},', 'total'),
        jl(f'  {K("validation")}: {{', 'sub'),
        jl(f'    {K("line_items_sum_to_subtotal")}: {S("pass")}, {K("total_reconciles")}: {S("pass")}'),
        jl('  }'), jl('}')])


def json_cm():
    return ''.join([
        jl('{'), jl(f'  {K("credit_memo_number")}: {S("CM-2024-0031")},', 'no'),
        jl(f'  {K("original_invoice")}: {S("NB-2024-0418")},', 'ref'),
        jl(f'  {K("po_number")}: {S("PO-2024-0284")},', 'po'),
        fld('issue_date', 'May 2, 2024', '2024-05-02', 'date', 'issue'),
        jl(f'  {K("vendor")}: {S("Northbridge Studio LLC")},', 'vendor'),
        jl(f'  {K("reason")}: {S("Billable hours adjustment")},', 'reason'),
        jl(f'  {K("line_items")}: ['),
        jl(f'    {{ {K("description")}: {S("Account management: hours credited")}, {K("qty")}: {N("-2")}, {K("unit_price")}: {N("185.00")}, {K("amount")}: {N("-370.00")} }}', 'li1'),
        jl('  ],'),
        fld('subtotal', '−$370.00', '-370.00', 'currency', 'sub', num=True),
        fld('tax_total', '−$23.13', '-23.13', 'currency', 'tax', num=True),
        jl(f'  {K("total_credit")}: {{ {K("source")}: {S("−$393.13")}, {K("value")}: {N("-393.13")}, {K("type")}: {S("currency")}, {K("confidence")}: {N("0.98")} }},', 'total'),
        jl(f'  {K("validation")}: {{', 'sub'),
        jl(f'    {K("tax_matches_rate")}: {S("pass")}, {K("total_reconciles")}: {S("pass")},'),
        jl(f'    {K("references_known_invoice")}: {S("pass")}'),
        jl('  }'), jl('}')])


def doc_inv():
    return '''<div class="ap-doc">
<div class="ap-doc-top"><div data-f="vendor"><b>Northbridge Studio</b></div><div class="r"><b>INVOICE</b><span data-f="no">NB-2024-0418</span></div></div>
<dl class="ap-meta"><div><dt>Bill to</dt><dd data-f="billto">Stillwater Robotics, Inc.<br>2840 Innovation Way, Suite 410<br>Cambridge, MA 02142</dd></div>
<div class="g"><div><dt>Issue date</dt><dd data-f="issue">Apr 18, 2024</dd></div><div><dt>Due date</dt><dd data-f="due">May 18, 2024</dd></div><div><dt>PO #</dt><dd data-f="po">PO-2024-0284</dd></div><div><dt>Terms</dt><dd data-f="terms">Net 30</dd></div></div></dl>
<table class="ap-tbl"><tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
<tr data-f="li1"><td>Strategy workshop facilitation</td><td>2</td><td>$1,850.00</td><td>$3,700.00</td></tr>
<tr data-f="li2"><td>UX research interviews</td><td>8</td><td>$425.00</td><td>$3,400.00</td></tr>
<tr><td>Design system audit</td><td>1</td><td>$4,200.00</td><td>$4,200.00</td></tr>
<tr><td>Account management</td><td>12</td><td>$185.00</td><td>$2,220.00</td></tr>
<tr><td>Travel &amp; expenses</td><td>1</td><td>$684.00</td><td>$684.00</td></tr></table>
<div class="ap-tot"><div data-f="sub"><span>Subtotal</span><span>$14,204.00</span></div><div data-f="tax"><span>Sales tax (MA 6.25%)</span><span>$887.75</span></div><div class="g" data-f="total"><span>Total due</span><span>$15,091.75</span></div></div></div>'''


def doc_po():
    return '''<div class="ap-doc">
<div class="ap-doc-top"><div data-f="buyer"><b>Stillwater Robotics, Inc.</b></div><div class="r"><b>PURCHASE ORDER</b><span data-f="po">PO-2024-0284</span></div></div>
<dl class="ap-meta"><div><dt>Vendor</dt><dd data-f="vendor">Northbridge Studio LLC<br>114 Brattle Street<br>Cambridge, MA 02138</dd></div>
<div class="g"><div><dt>Order date</dt><dd data-f="odate">Mar 28, 2024</dd></div><div><dt>Terms</dt><dd data-f="terms">Net 30</dd></div><div><dt>Project</dt><dd>Phoenix Rebrand</dd></div></div></dl>
<table class="ap-tbl"><tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
<tr data-f="li1"><td>Strategy workshop facilitation</td><td>2</td><td>$1,850.00</td><td>$3,700.00</td></tr>
<tr data-f="li2"><td>UX research interviews</td><td>8</td><td>$425.00</td><td>$3,400.00</td></tr>
<tr><td>Design system audit</td><td>1</td><td>$4,200.00</td><td>$4,200.00</td></tr>
<tr><td>Account management</td><td>12</td><td>$185.00</td><td>$2,220.00</td></tr>
<tr><td>Travel &amp; expenses (NTE)</td><td>1</td><td>$700.00</td><td>$700.00</td></tr></table>
<div class="ap-tot"><div data-f="sub"><span>Subtotal</span><span>$14,220.00</span></div><div class="g" data-f="total"><span>Order total</span><span>$14,220.00</span></div></div></div>'''


def doc_cm():
    return '''<div class="ap-doc">
<div class="ap-doc-top"><div data-f="vendor"><b>Northbridge Studio</b></div><div class="r"><b>CREDIT MEMO</b><span data-f="no">CM-2024-0031</span></div></div>
<dl class="ap-meta"><div><dt>Credit to</dt><dd>Stillwater Robotics, Inc.<br>2840 Innovation Way, Suite 410</dd></div>
<div class="g"><div><dt>Issue date</dt><dd data-f="issue">May 2, 2024</dd></div><div><dt>Against invoice</dt><dd data-f="ref">NB-2024-0418</dd></div><div><dt>PO #</dt><dd data-f="po">PO-2024-0284</dd></div><div><dt>Reason</dt><dd data-f="reason">Hours adjustment</dd></div></div></dl>
<table class="ap-tbl"><tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
<tr data-f="li1"><td>Account management: hours credited</td><td>&minus;2</td><td>$185.00</td><td>&minus;$370.00</td></tr></table>
<div class="ap-tot"><div data-f="sub"><span>Subtotal</span><span>&minus;$370.00</span></div><div data-f="tax"><span>Sales tax (6.25%)</span><span>&minus;$23.13</span></div><div class="g" data-f="total"><span>Total credit</span><span>&minus;$393.13</span></div></div></div>'''


def drop_rate(h):
    h = h.replace('<th>Rate</th>', '')
    return re.sub(r'(<tr[^>]*><td>[^<]*</td><td>[^<]*</td>)<td>[^<]*</td>', r'\1', h)


def pane(pid, on, doc, endpoint, cap, body, n):
    doc = drop_rate(doc)
    return (f'<div class="ap-pane{" on" if on else ""}" id="ap-pane-{pid}" role="tabpanel">'
            f'<div class="ap-doccol"><div class="ap-cap">Source document</div>{doc}</div>'
            f'<div class="ap-jcol"><div class="ap-api"><span class="v">POST</span><span>{endpoint}</span><span class="ok">200 OK</span></div>'
            f'<div class="ap-json">{body}</div>'
            f'<div class="ap-jfoot"><span>{n} fields</span><span>every value traces to page + bounding box</span></div></div></div>')


demo = (pane('inv', True, doc_inv(), '/v0/extract/invoice', 'invoice', json_inv(), 14)
        + pane('po', False, doc_po(), '/v0/extract/purchase_order', 'po', json_po(), 9)
        + pane('cm', False, doc_cm(), '/v0/extract/credit_memo', 'cm', json_cm(), 10))

# ============================================================ section content
FIELD_TABS = [
    ('header', 'Header', '01', 9, [
        ('Invoice number', 'invoice_number', 'string', 'Kept as printed; part of a duplicate-check key in your system.', ''),
        ('Invoice date', 'invoice_date', 'date', 'ISO 8601 value, with the printed text kept as <code>source</code>.', ''),
        ('Due date', 'due_date', 'date', 'ISO 8601 value, printed text kept.', ''),
        ('PO number', 'po_number', 'string', 'Format-checked and clean enough to match a PO and receipt.', 'PO format'),
        ('Vendor name', 'vendor_name', 'string', 'Mapped from &ldquo;From&rdquo;, &ldquo;Billed by&rdquo;, &ldquo;Seller&rdquo; and the like.', ''),
        ('Vendor address', 'vendor_address', 'string', 'As printed, from the header or footer.', ''),
        ('Bill-to name', 'bill_to_name', 'string', 'The billed entity, for routing.', ''),
        ('Bill-to address', 'bill_to_address', 'string', 'As printed.', ''),
        ('Payment terms', 'payment_terms', 'string', 'As written (Net 30, 2/10 Net 30).', ''),
    ]),
    ('lines', 'Line items', '02', 8, [
        ('Description', 'description', 'string', 'Multi-line descriptions stay in one row.', ''),
        ('Quantity', 'quantity', 'number', 'Parsed to a number; credit-memo negatives handled.', ''),
        ('Unit price', 'unit_price', 'currency', 'A number, with the printed text kept as <code>source</code>.', ''),
        ('Unit of measure', 'unit_of_measure', 'string', 'Hours, each, per diem: whatever is printed.', ''),
        ('Discount', 'discount', 'currency', 'Row-level, when present.', ''),
        ('Tax amount', 'tax_amount', 'currency', 'Row-level tax for mixed tax codes.', 'Tax'),
        ('Extended amount', 'extended_amount', 'currency', 'The row total. Tables across page breaks read as one.', 'Subtotal'),
        ('SKU / part number', 'sku', 'string', 'When present, so lines can match PO lines.', ''),
    ]),
    ('totals', 'Totals', '03', 8, [
        ('Subtotal', 'subtotal', 'currency', 'Checked against the sum of the lines.', 'Subtotal'),
        ('Discount total', 'discount_total', 'currency', 'Document-level discount.', ''),
        ('Tax total', 'tax_total', 'currency', 'Checked against the stated tax rate.', 'Tax'),
        ('Shipping / freight', 'shipping_freight', 'currency', 'Kept apart from goods so the subtotal check stays clean.', ''),
        ('Grand total', 'grand_total', 'currency', 'Must reconcile: subtotal + tax + shipping &minus; discount.', 'Total'),
        ('Amount paid', 'amount_paid', 'currency', 'For part-paid invoices and deposits.', ''),
        ('Balance due', 'balance_due', 'currency', 'What is actually payable now.', ''),
        ('Currency', 'currency', 'string', 'As printed, so multi-currency AP does not guess.', ''),
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

STAGES = [
    ('01', 'Ingest', 'PDF, scan, email attachment or spreadsheet. Any source, no pre-sorting.', 'in files, email, API', 'out normalized pages'),
    ('02', 'Classify', 'Document type identified (invoice, PO, credit memo, remittance) before extraction runs.', 'in normalized pages', 'out typed document'),
    ('03', 'Extract', 'Hybrid AI plus deterministic SenseML rules pull header, line item and total fields, whatever the layout.', 'in typed document', 'out candidate fields'),
    ('04', 'Validate', 'Calculation checks run automatically: line items to subtotal, tax to rate, PO reference format. Discrepancies get a confidence score.', 'in candidate fields', 'out checked fields + flags'),
    ('05', 'Deliver', 'Schema-enforced JSON, every field traced to page and bounding box, sent by webhook or pulled by API.', 'in checked fields', 'out JSON to your system'),
]


def io(a, b):
    return f'<div class="ap-io"><b>{a.split(" ", 1)[0]}</b> {a.split(" ", 1)[1]}<br><b>{b.split(" ", 1)[0]}</b> {b.split(" ", 1)[1]}</div>'


cards = ''.join(
    f'<div class="ap-card" data-reveal><div class="art">{pipe_ill(i + 1)}</div><div class="ap-num">{n}</div><h3>{t}</h3><p>{d}</p>{io(a, b)}</div>'
    for i, (n, t, d, a, b) in enumerate(STAGES))

CHALLENGES = [
    ('01', 'Vendor format diversity', 'QuickBooks exports, SAP invoices, handwritten bills, custom ERP outputs: each one places fields somewhere different. Hybrid extraction (LLM parsing plus SenseML rules) absorbs the variation instead of breaking on it.', 'formats', ''),
    ('02', 'Line item table extraction', 'Multi-page tables, merged cells, multi-line descriptions and varying tax codes. Quantity, unit price, tax and amount stay attached to the right row, and page breaks are handled without you noticing them.', 'tables', ''),
    ('03', 'Calculation validation', 'Do the line items sum to the subtotal? Does the tax match the rate? Does the grand total reconcile? This check catches a bad extraction before it reaches the ledger, not after.', 'calc', ''),
    ('04', 'PO and three-way-match readiness', 'An invoice&rsquo;s PO number is only useful if it can be checked against the PO and goods receipt it references. Extraction has to keep that reference clean enough to match on, not just capture it as a string.', 'po', 'AP-specific'),
]
chal = ''.join(
    f'<div class="ap-cell" data-reveal><div class="ap-num">{n}{f"<span class=ap-tagline>{tg}</span>" if tg else ""}</div><h3>{t}</h3><p>{d}</p>{mini(m)}</div>'
    for n, t, d, m, tg in CHALLENGES)

CHECKS = (
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Line items sum to subtotal</b><span class="d">5 lines add up to the stated subtotal</span></div><span class="res" data-count="14204">$14,204.00</span></div>'
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Tax matches rate</b><span class="d">6.25% of the subtotal equals the stated tax</span></div><span class="res" data-count="887.75">$887.75</span></div>'
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>Grand total reconciles</b><span class="d">Subtotal + tax &minus; discount = total due</span></div><span class="res" data-count="15091.75">$15,091.75</span></div>'
    '<div class="ap-check"><span class="ic">&#10003;</span><div><b>PO reference format</b><span class="d">Matches your PO number pattern</span></div><span class="res">PO-2024-0284</span></div>'
    '<div class="ap-check flag"><span class="ic">!</span><div><b>A check that fails</b><span class="d">Lines sum to $14,204.00 but the subtotal reads $14,240.00, so the field is flagged with a low confidence score and sent to review</span></div><span class="res">review</span></div>')

MANAGED = [
    ('01', 'Plan', 'Engineers review your samples and pick the right method.', 'plan'),
    ('02', 'Build', 'SenseML configs written from your samples.', 'build'),
    ('03', 'Deploy', 'Same engine as self-serve, ready for production.', 'deploy'),
    ('04', 'Adjust', 'Configs updated when formats shift or new edge cases appear.', 'adjust'),
    ('05', 'Integrate', 'Help with custom integration into your downstream systems.', 'link'),
]
mgd = ''.join(f'<div class="ap-cell" data-reveal><div class="ap-num">{n}</div>{icon(ic)}<h3>{t}</h3><p>{d}</p></div>' for n, t, d, ic in MANAGED)


def dots(items):
    return ' <i>&middot;</i> '.join(f'<span style="white-space:nowrap">{x}</span>' for x in items)


FORMATS = [
    ('ledger', 'By source', dots(['QuickBooks', 'Xero', 'NetSuite', 'SAP', 'Oracle', 'FreshBooks', 'Wave', 'Custom / manual invoices'])),
    ('stack', 'By invoice type', dots(['Standard invoices', 'Credit memos', 'Debit notes', 'Proforma invoices', 'Recurring invoices', 'Construction progress billing'])),
    ('po', 'Purchase orders', 'Extracted against the same schema as the invoices that reference them, so the two can be compared field for field.'),
    ('box', 'Goods receipts', 'Received quantities captured in the same shape, so invoice lines can be matched against what actually arrived.'),
    ('remit', 'Remittance advices', 'Payment references pulled out so they can be tied back to open invoices.'),
    ('file', 'File formats', dots(['PDF (native or scanned)', 'Word', 'XLSX / XLS / CSV', 'JPEG / PNG', 'TIFF', 'Email bodies with attachments'])),
]
fmt = ''.join(f'<div class="ap-cell" data-reveal>{icon(ic)}<h3>{t}</h3><p class="ap-plain">{d}</p></div>' for ic, t, d in FORMATS)


def faq(q, a, o=False):
    return f'<details class="ap-q" data-reveal{" open" if o else ""}><summary>{q}<i>+</i></summary><div class="ap-q-a">{a}</div></details>'


FAQS = ''.join([
    faq('Does Sensible do invoice-to-PO-to-receipt three-way matching itself?', '<p>No. Sensible is the extraction layer. It reads the invoice, the purchase order and the goods receipt, and captures the reference fields that tie them together (PO number, line quantities, unit prices, totals) in a consistent, schema-validated shape. The matching logic itself, including tolerances and exception handling, lives downstream in your AP system, ERP or matching engine.</p>', True),
    faq('Can Sensible flag likely duplicate invoices?', '<p>Not as a built-in feature. Sensible&rsquo;s validation rules run against one document at a time, and spotting a duplicate needs a comparison across documents you have already processed.</p><p>What Sensible does give you is a reliable duplicate key on every invoice: vendor, invoice number, invoice date and grand total, extracted the same way each time. Checking that key against your history belongs in your AP system or ERP. If you want that wired in as part of the pipeline, our managed-services team can help with the integration.</p>'),
    faq('How does per-document pricing work for high-volume AP teams?', '<p>Sensible prices per document, not per token, so cost is predictable at 500 invoices a month or 50,000. There is no token-volatility surprise when a vendor sends a 40-line invoice instead of a 4-line one. Volume discounts are available for higher throughput; <a href="https://www.sensible.so/pricing">see pricing</a> or talk to our team for a volume quote.</p>'),
    faq('How does Sensible catch bad extractions before they reach the ledger?', '<p>Validation rules cross-check that line items sum to the subtotal, that tax matches the stated rate, and that the grand total reconciles. Discrepancies are flagged automatically with a confidence score, and low-confidence extractions can be routed to human review with thresholds you configure. Results are delivered by webhook or API.</p>'),
    faq('How accurate is the extraction?', '<p>Accuracy depends on document quality and configuration, so we don&rsquo;t quote a single flat number. What we can tell you is how the output is checked: schema enforcement, calculation validation and a confidence score on each field, so weak extractions are flagged instead of passed through silently. The best way to know is to run your own invoices, including the ugly ones, through it.</p>'),
    faq('How is invoice data secured, and how long is it retained?', '<p>Sensible is SOC 2 Type II certified and HIPAA compliant, with data encrypted in transit and at rest. Document data is stored indefinitely by default; custom retention policies are available, including same-day deletion.</p>'),
])

LOGOS = ['vouch.svg', 'limit.png', 'ledgebrook.svg', 'obie.svg', 'neptune-flood.svg', 'insurance-quantified.svg',
         'lettuce.svg', 'founder-shield.svg', 'compscience.svg', 'inclined.png', 'sterlingrisk.png']
logo_imgs = ''.join(f'<img src="assets/logos/{f}" alt="">' for f in LOGOS * 2)

# ============================================================ fragment (what goes into Webflow)
fragment = f'''<div class="ap">

  <!-- 1. HERO: H1 + framing beside the live demo (first fold) -->
  <section class="ap-hero" id="ap-hero">
    <div class="ap-hero-copy">
      <span class="ap-tag" data-hero>[ Accounts payable ]</span>
      <h1 class="ap-h1">Accounts payable automation, built on <em>extraction you can trust</em></h1>
      <p class="ap-lede" data-hero>Sensible is the extraction layer under your AP workflow: schema-validated, traced to source coordinates, and scored for confidence, so your finance team can trust the data without checking it by hand.</p>
      <div class="ap-btns" data-hero>
        <a class="ap-btn p" href="https://app.sensible.so/register/">Start free trial</a>
        <a class="ap-btn s" href="https://www.sensible.so/meeting">Book a demo</a>
      </div>
      <div class="ap-note" data-hero>14-day free trial · No credit card</div>
    </div>
    <div class="ap-hero-panel">
      {hero_rects()}
      <div class="ap-demo-wrap">
        <div class="ap-demo-tabs" role="tablist" aria-label="Sample AP documents">
          <button class="ap-demo-tab" role="tab" aria-selected="true" data-pane="inv">Supplier invoice</button>
          <button class="ap-demo-tab" role="tab" aria-selected="false" data-pane="po">Purchase order</button>
          <button class="ap-demo-tab" role="tab" aria-selected="false" data-pane="cm">Credit memo</button>
        </div>
        <div class="ap-demo">{demo}</div>
        <p class="ap-demo-note">Hover a field to trace it to the source. Sample data; output is illustrative.</p>
      </div>
    </div>
  </section>

  <!-- 2. STATS RIBBON (same component as the sensible.so homepage) + LOGOS -->
  <div class="ap-ribbon"><div class="ap-wrap"><div class="ap-ribbon-grid">
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">75M+</p><p class="ap-ribbon-l">documents processed</p></div>
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">150+</p><p class="ap-ribbon-l">library configurations</p></div>
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">SOC 2 + HIPAA</p><p class="ap-ribbon-l">independently audited</p></div>
    <div class="ap-ribbon-cell"><p class="ap-ribbon-v">No credit card</p><p class="ap-ribbon-l">14-day free trial</p></div>
  </div></div></div>
  <!-- WEBFLOW: swap for the existing customer-logo strip component -->
  <div class="ap-logos"><div class="ap-logos-cap">Trusted by teams turning documents into production data</div><div class="ap-logos-track">{logo_imgs}</div></div>

  <!-- 3. CHAOS -> ONE SCHEMA -->
  <section class="ap-sec" id="ap-why">
    <div class="ap-wrap">
      <div class="ap-chaos">
        <div class="ap-chaos-copy">
          <span class="ap-kicker">Why AP extraction is hard</span>
          <h2 class="ap-h2">Every vendor invoices differently. Your ledger needs one format.</h2>
          <ul class="ap-bullets">
            <li>Each supplier lays out fields in its own way</li>
            <li>Line-item tables run across pages, merge cells and wrap descriptions</li>
            <li>Totals that don&rsquo;t add up reach the ledger unchecked</li>
            <li>A PO number captured as a string can&rsquo;t be matched to its receipt</li>
          </ul>
          <div class="ap-btns"><a class="ap-btn s" href="#ap-how">See how it works</a></div>
        </div>
        <div class="ap-chaos-stage">{chaos_scene()}<div class="ap-chaos-label"><span class="a">Vendor chaos</span><span class="b">One schema</span></div></div>
      </div>
    </div>
  </section>

  <!-- 4. FOUR CHALLENGES -->
  <section class="ap-sec" id="ap-hard">
    <div class="ap-wrap ap-head ap-center" data-reveal>
      <span class="ap-kicker">Why AP extraction is hard in production</span>
      <h2 class="ap-h2">Where invoice extraction breaks in production</h2>
      <p class="ap-lede">Headers, totals and line-item tables land somewhere different on every vendor&rsquo;s document. Hybrid extraction handles the variation, and validation re-checks the math before anything reaches your ledger.</p>
    </div>
    <div class="ap-grid ap-g4">{chal}</div>
  </section>

  <!-- 5. FIELDS -->
  <section class="ap-sec" id="ap-fields">
    <div class="ap-wrap"><div class="ap-fields">
      <div class="ap-fields-nav" data-reveal>
        <span class="ap-kicker">What Sensible extracts</span>
        <h2 class="ap-h2">The fields we extract</h2>
        <p class="ap-lede">Grouped the way AP teams ask for them. Each field comes back typed, keeps the text as printed, and points to where it sits on the page.</p>
        <div class="ap-ftabs" role="tablist" aria-label="Field groups">{ftabs}</div>
        <div class="ap-schem-wrap">{schematic()}</div>
      </div>
      <div data-reveal>
        {fpanes}
        <div class="ap-more"><b>Your schema, not a fixed list.</b><span>Every AP team&rsquo;s schema is different, so this is a starting point mapped to yours. Commonly added: GL code, cost center, ship-to, remit-to details, vendor tax ID, GRN number, project code, early-pay terms.</span></div>
      </div>
    </div></div>
  </section>

  <!-- 6. HOW IT WORKS -->
  <section class="ap-sec ap-band" id="ap-how">
    <div class="ap-wrap">
      <div class="ap-head ap-center" data-reveal>
        <span class="ap-kicker">How it works</span>
        <h2 class="ap-h2">How an invoice moves through Sensible</h2>
        <p class="ap-lede">Five stages, and every field keeps its page and bounding box all the way through.</p>
      </div>
      <div class="ap-cards">{cards}</div>
      <div class="ap-scope"><i></i><span>Sensible: the extraction layer</span><i></i></div>
      <div class="ap-then" data-reveal><span class="k">Then</span><p>Webhook or API into your AP system, ERP or matching engine. Three-way matching, approval routing, posting and payment happen there. Sensible hands over data you can trust; it doesn&rsquo;t run those steps.</p></div>
      <div class="ap-trace" data-reveal><span class="tl">Every field is traceable</span><span><span class="k">total_due</span> &rarr; page <span class="v">1</span></span><span><span class="k">bbox</span> <span class="v">[412, 688, 540, 712]</span></span><span><span class="k">confidence</span> <span class="v">0.99</span></span><span><span class="k">source</span> <span class="v">&quot;$15,091.75&quot;</span></span></div>
    </div>
  </section>

  <!-- 7. VALIDATION + POSITION -->
  <section class="ap-sec" id="ap-validation">
    <div class="ap-wrap">
      <div class="ap-val">
        <div data-reveal>
          <span class="ap-kicker">Validation, not just extraction</span>
          <h2 class="ap-h2">How the numbers get checked</h2>
          <p class="ap-lede">Getting a number out of a PDF is the easy part. The question your finance team asks is whether it&rsquo;s the right number, so Sensible checks each invoice the way an AP clerk would. When a check fails, the field is flagged with a confidence score and can be routed for review instead of flowing into your ledger.</p>
        </div>
        <div class="ap-checks"><div class="ap-checks-h"><span>Validation results</span><span>NB-2024-0418</span></div>{CHECKS}</div>
      </div>
      <div class="ap-quote">
        <div><span class="ap-kicker">Our position</span></div>
        <blockquote><p class="ap-qtext">We don&rsquo;t publish a flat accuracy percentage. Accuracy depends on document quality and configuration, and a single number hides both.</p><cite>Sensible</cite></blockquote>
      </div>
    </div>
  </section>

  <!-- 8. SELF-SERVE OR MANAGED -->
  <section class="ap-sec ap-mgd" id="ap-managed">
    <div class="ap-wrap ap-head ap-center" data-reveal>
      <span class="ap-kicker">Self-serve or managed</span>
      <h2 class="ap-h2">Don&rsquo;t want to build the AP config yourself? <em>Our team can run the extraction backend for you.</em></h2>
      <p class="ap-lede">Solutions engineers handle plan, build, deploy and adjust on your behalf. You see clean JSON in your API response. Same engine as self-serve, with the configuration work done for you.</p>
      <div class="ap-btns"><a class="ap-btn p" href="https://www.sensible.so/managed-services">See managed services</a><a class="ap-btn s" href="https://www.sensible.so/contact-us">Talk to our team</a></div>
    </div>
    <div class="ap-grid ap-g5">{mgd}</div>
  </section>

  <!-- 9. SUPPORTED FORMATS -->
  <section class="ap-sec" id="ap-formats">
    <div class="ap-wrap ap-head ap-center" data-reveal>
      <span class="ap-kicker">Supported formats</span>
      <h2 class="ap-h2">Any vendor, any accounting system, any country</h2>
      <p class="ap-lede">The extraction logic is written out in SenseML rather than buried in prompts, so a new format can be added and reviewed.</p>
    </div>
    <div class="ap-grid ap-g3">{fmt}</div>
  </section>

  <!-- 10. FAQ -->
  <section class="ap-sec" id="ap-faq">
    <div class="ap-wrap"><div class="ap-faq">
      <div class="ap-faq-head" data-reveal>
        <span class="ap-kicker">Common questions</span>
        <h2 class="ap-h2">Questions from AP teams</h2>
        <p class="ap-lede">Matching, duplicates, pricing, and where Sensible stops and your AP system starts.</p>
      </div>
      <div class="ap-faq-list">{FAQS}</div>
    </div></div>
  </section>

</div>'''

open('ap/fragment.html', 'w').write(fragment)

# ============================================================ standalone demo page
base_css = L(20, 249)                                # tokens, reset, nav, buttons (existing site CSS)
cta_footer_css = L(998, 1160)                        # closing CTA + footer (existing site CSS)
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
  <title>Accounts Payable Automation: Invoice Data Extraction | Sensible</title>
  <meta name="description" content="Sensible is the extraction layer under your AP workflow: schema-validated invoice, PO and receipt data, traced to source coordinates and scored for confidence. Free 14-day trial."/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,300;0,400;0,500;1,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
  <script>document.documentElement.classList.add('ap-js')</script>
  <style>
{base_css}
{cta_footer_css}
{site_extra}
{css}
  </style>
</head>
<body>
{nav_html}
{fragment}
{cta_html}
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script>
{js}
</script>
</body>
</html>
'''
open('accounts-payable.html', 'w').write(page)
print('fragment', len(fragment), 'css', len(css), 'js', len(js), 'page', len(page))
