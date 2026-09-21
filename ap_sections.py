"""Middle sections of accounts-payable.html (why hard -> FAQ), laid out as editorial
split / ruled-list sections instead of centered heading + card grids."""


def rule(num, title, text, tag=''):
    t = f' <span class="rl-tag">{tag}</span>' if tag else ''
    return (f'<div class="rl-item"><span class="rl-num">{num}</span>'
            f'<div><h3>{title}{t}</h3><p>{text}</p></div></div>')


def mid_sections(fields_html, faqs_html):
    hard = ''.join([
        rule('01', 'Vendor format diversity',
             'QuickBooks exports, SAP invoices, handwritten bills, custom ERP outputs: each one places fields '
             'somewhere different. Hybrid extraction (LLM parsing plus SenseML rules) absorbs the variation '
             'instead of breaking on it.'),
        rule('02', 'Line item table extraction',
             'Multi-page tables, merged cells, multi-line descriptions and varying tax codes. Quantity, unit '
             'price, tax and amount stay attached to the right row, and page breaks are handled without you '
             'noticing them.'),
        rule('03', 'Calculation validation',
             'Do the line items sum to the subtotal? Does the tax match the rate? Does the grand total '
             'reconcile? This check catches a bad extraction before it reaches the ledger, not after.'),
        rule('04', 'PO and three-way-match readiness',
             'An invoice&rsquo;s PO number is only useful if it can be checked against the PO and goods receipt '
             'it references. Extraction has to keep that reference clean enough to match on, not just capture '
             'it as a string.', 'AP-specific'),
    ])

    stages = [
        ('01', 'Ingest', 'PDF, scan, email attachment or spreadsheet. Any source, no pre-sorting.',
         ('in', 'files, email, API'), ('out', 'normalized pages')),
        ('02', 'Classify', 'Document type identified (invoice, PO, credit memo, remittance) before extraction runs.',
         ('in', 'normalized pages'), ('out', 'typed document')),
        ('03', 'Extract', 'Hybrid AI plus deterministic SenseML rules pull header, line item and total fields, '
                          'whatever the layout.',
         ('in', 'typed document'), ('out', 'candidate fields')),
        ('04', 'Validate', 'Calculation checks run automatically: line items to subtotal, tax to rate, PO '
                           'reference format. Discrepancies get a confidence score.',
         ('in', 'candidate fields'), ('out', 'checked fields + flags')),
        ('05', 'Deliver', 'Schema-enforced JSON, every field traced to page and bounding box, sent by webhook '
                          'or pulled by API.',
         ('in', 'checked fields'), ('out', 'JSON to your system')),
    ]
    rail = ''.join(
        f'<div class="rail-cell"><span class="rl-num">{n}</span><h3>{t}</h3><p>{d}</p>'
        f'<div class="rail-io"><b>{i[0]}</b> {i[1]}<br><b>{o[0]}</b> {o[1]}</div></div>'
        for n, t, d, i, o in stages)

    checks = (
        '<div class="val-row"><span class="val-ic ok">&#10003;</span><div><b>Line items sum to subtotal</b>'
        '<span class="d">5 lines add up to the stated subtotal</span></div><span class="val-res">$14,204.00</span></div>'
        '<div class="val-row"><span class="val-ic ok">&#10003;</span><div><b>Tax matches rate</b>'
        '<span class="d">6.25% of the subtotal equals the stated tax</span></div><span class="val-res">$887.75</span></div>'
        '<div class="val-row"><span class="val-ic ok">&#10003;</span><div><b>Grand total reconciles</b>'
        '<span class="d">Subtotal + tax &minus; discount = total due</span></div><span class="val-res">$15,091.75</span></div>'
        '<div class="val-row"><span class="val-ic ok">&#10003;</span><div><b>PO reference format</b>'
        '<span class="d">Matches your PO number pattern</span></div><span class="val-res">PO-2024-0284</span></div>'
        '<div class="val-row flag"><span class="val-ic warn">!</span><div><b>A check that fails</b>'
        '<span class="d">Lines sum to $14,204.00 but the subtotal reads $14,240.00, so the field is flagged with a '
        'low confidence score and sent to review</span></div><span class="val-res">review</span></div>')

    mg = ''.join(rule(n, t, d) for n, t, d in [
        ('01', 'Plan', 'Engineers review your samples and pick the right method.'),
        ('02', 'Build', 'SenseML configs written from your samples.'),
        ('03', 'Deploy', 'Same engine as self-serve, ready for production.'),
        ('04', 'Adjust', 'Configs updated when formats shift or new edge cases appear.'),
        ('05', 'Integrate', 'Help with custom integration into your downstream systems.'),
    ])

    def dl(label, sub, items):
        return (f'<div class="dl-row"><div class="dl-k"><h3>{label}</h3><span>{sub}</span></div>'
                f'<p class="dl-v">{" <i>&middot;</i> ".join("<span>" + x + "</span>" for x in items)}</p></div>')

    fmt = ''.join([
        dl('By source', 'accounting systems',
           ['QuickBooks', 'Xero', 'NetSuite', 'SAP', 'Oracle', 'FreshBooks', 'Wave', 'Custom / manual invoices']),
        dl('By type', 'invoice variants',
           ['Standard invoices', 'Credit memos', 'Debit notes', 'Proforma invoices', 'Recurring invoices',
            'Construction progress billing']),
        dl('By AP document', 'for three-way matching', ['Purchase orders', 'Goods receipts', 'Remittance advices']),
    ])

    return f'''
  <!-- 4. WHY HARD -->
  <section class="sec white" id="why-hard">
    <div class="container sp-split">
      <div class="sp-split-head">
        <span class="sp-kicker">Why AP extraction is hard in production</span>
        <h2 class="sp-h2">Where invoice extraction breaks in production</h2>
        <p class="sp-lede">Headers, totals and line-item tables land somewhere different on every vendor&rsquo;s document. Hybrid extraction handles the variation, and validation re-checks the math before anything reaches your ledger.</p>
      </div>
      <div class="rl-list">{hard}</div>
    </div>
  </section>

  <!-- 5. FIELDS -->
  {fields_html}

  <!-- 6. PIPELINE -->
  <section class="sec white" id="how-it-works">
    <div class="container">
      <div class="head-row">
        <div><span class="sp-kicker">How it works</span><h2 class="sp-h2">How an invoice moves through Sensible</h2></div>
        <p class="sp-lede">Five stages, and every field keeps its page and bounding box all the way through.</p>
      </div>
      <div class="rail">{rail}</div>
      <div class="rail-scope"><span class="bar"></span><span class="lbl">Sensible: the extraction layer</span><span class="bar"></span></div>
      <div class="handoff">
        <span class="hk">Then</span>
        <p>Webhook or API into your AP system, ERP or matching engine. Three-way matching, approval routing, posting and payment happen there. Sensible hands over data you can trust; it doesn&rsquo;t run those steps.</p>
      </div>
      <div class="trace-line"><span class="tl">Every field is traceable</span><span><span class="k">total_due</span> &rarr; page <span class="v">1</span></span><span><span class="k">bbox</span> <span class="v">[412, 688, 540, 712]</span></span><span><span class="k">confidence</span> <span class="v">0.99</span></span><span><span class="k">source</span> <span class="v">&quot;$15,091.75&quot;</span></span></div>
    </div>
  </section>

  <!-- 7. VALIDATION -->
  <section class="sec white" id="validation">
    <div class="container sp-split">
      <div class="sp-split-head">
        <span class="sp-kicker">Validation, not just extraction</span>
        <h2 class="sp-h2">How the numbers get checked</h2>
        <p class="sp-lede">Getting a number out of a PDF is the easy part. The question your finance team asks is whether it&rsquo;s the right number, so Sensible checks each invoice the way an AP clerk would.</p>
        <p class="sp-lede sp-lede-2">When a check fails, the field is flagged with a confidence score and can be routed for review instead of flowing into your ledger.</p>
        <p class="val-note">We don&rsquo;t publish a flat accuracy percentage. Accuracy depends on document quality and configuration, and a single number hides both.</p>
      </div>
      <div class="val-plain"><div class="val-plain-head"><span>Validation results</span><span>NB-2024-0418</span></div>{checks}</div>
    </div>
  </section>

  <!-- 8. SELF-SERVE OR MANAGED -->
  <section class="sec white" id="managed">
    <div class="container sp-split">
      <div class="sp-split-head">
        <span class="sp-kicker">Self-serve or managed</span>
        <h2 class="sp-h2">Don&rsquo;t want to build the AP config yourself? <em>Our team can run the extraction backend for you.</em></h2>
        <p class="sp-lede">Solutions engineers handle plan, build, deploy and adjust on your behalf. You see clean JSON in your API response. Same engine as self-serve, with the configuration work done for you.</p>
        <div class="m-actions mg-actions">
          <a class="m-btn p" href="https://www.sensible.so/managed-services">See managed services &rarr;</a>
          <a class="m-btn s" href="https://www.sensible.so/contact-us">Talk to our team</a>
        </div>
      </div>
      <div class="rl-list">{mg}</div>
    </div>
  </section>

  <!-- 9. SUPPORTED FORMATS -->
  <section class="sec white" id="formats">
    <div class="container sp-split">
      <div class="sp-split-head">
        <span class="sp-kicker">Supported formats</span>
        <h2 class="sp-h2">Any vendor, any accounting system, any country</h2>
        <p class="sp-lede">The extraction logic is written out in SenseML rather than buried in prompts, so a new format can be added and reviewed. Three-way matching needs all three document types extracted the same way, so purchase orders and goods receipts run through the same pipeline as invoices.</p>
      </div>
      <div class="dl-list">{fmt}</div>
    </div>
  </section>

  <!-- 10. FAQ -->
  <section class="sec white faq-section" id="faq">
    <div class="container sp-split">
      <div class="sp-split-head">
        <span class="sp-kicker">Common questions</span>
        <h2 class="sp-h2">Questions from AP teams</h2>
        <p class="sp-lede">Matching, duplicates, pricing, and where Sensible stops and your AP system starts.</p>
      </div>
      <div class="faq-plain">{faqs_html}</div>
    </div>
  </section>

'''
