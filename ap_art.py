"""Inline SVG art for the AP page. Line-art with a hard offset shadow (LlamaIndex-style),
in Sensible colors. Every SVG is small (<3KB) so it fits a Webflow Code Embed / DOM element."""

INK = '#1A1520'
SH = '#E6E6E9'
MAG = '#840055'
AMB = '#D88B1F'
MONO = "font-family=\"IBM Plex Mono, monospace\""


def _open(w, h, cls='ap-ill'):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'fill="none" stroke="{INK}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">')


def _doc(x, y, w, h, lines=3, shadow=True, stroke=INK, fill='#fff', cls=''):
    s = f'<rect x="{x+5}" y="{y+5}" width="{w}" height="{h}" rx="3" fill="{SH}" stroke="none"/>' if shadow else ''
    s += f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}"/>'
    for i in range(lines):
        yy = y + 12 + i * 8
        ww = w - 20 - (i % 2) * 14
        s += f'<path d="M{x+8} {yy}h{ww}" stroke-width="1.2" opacity=".55"/>'
    return s


def _tag(x, y, label, hot=False):
    w = len(label) * 5.6 + 12
    fill = MAG if hot else '#fff'
    col = '#fff' if hot else INK
    return (f'<g><rect x="{x+3}" y="{y+3}" width="{w}" height="15" fill="{SH}" stroke="none"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="15" fill="{fill}"/>'
            f'<text x="{x+6}" y="{y+11}" font-size="8" {MONO} fill="{col}" stroke="none" letter-spacing=".5">{label}</text></g>')


# ---------------------------------------------------------------- hero backdrop
def hero_rects():
    rects = [(600, -40, 420, 320), (470, 120, 400, 360), (330, 300, 390, 360), (170, 440, 380, 360), (-10, 560, 330, 300)]
    body = ''.join(
        f'<rect class="ap-hr" x="{x}" y="{y}" width="{w}" height="{h}" fill="rgba(255,255,255,.30)" stroke="#fff" stroke-width="2.5"/>'
        for x, y, w, h in rects)
    return (f'<svg class="ap-hero-art" viewBox="0 0 1000 760" preserveAspectRatio="xMaxYMid slice" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">{body}</svg>')


# ---------------------------------------------------------------- chaos -> order scene
SANS = "font-family=\"IBM Plex Sans, sans-serif\""
SERIF = "font-family=\"IBM Plex Serif, serif\""
MUTE = '#8B857B'


def _t(x, y, txt, size, fam=SANS, fill=INK, anchor='start', weight=400, ls=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" {fam} fill="{fill}" stroke="none" '
            f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}">{txt}</text>')


def _rows(x0, x1, y0, rows, step=10, size=6.5):
    out = ''
    for i, (d, amt) in enumerate(rows):
        y = y0 + i * step
        out += _t(x0, y, d, size) + _t(x1, y, amt, size, anchor='end', fam=MONO)
        out += f'<path d="M{x0} {y+3.5}H{x1}" stroke="#E6E6E9" stroke-width=".8"/>'
    return out


def chaos_doc(v, name, num, total, rows):
    """One vendor invoice. Three layouts on purpose: fields sit in different places per vendor."""
    W, H = 172, 122
    s = f'<rect width="{W}" height="{H}" rx="3" fill="#fff"/>'
    if v == 0:      # header left, total bottom-right
        s += _t(10, 18, name, 9, SERIF, weight=500) + _t(162, 17, 'INVOICE', 6.5, MONO, anchor='end', ls=1.4)
        s += _t(162, 26, num, 5.5, MONO, MUTE, 'end')
        s += f'<path d="M10 33H162" stroke-width=".9" opacity=".5"/>'
        s += _t(10, 43, 'DESCRIPTION', 5, MONO, MUTE, ls=.6) + _t(162, 43, 'AMOUNT', 5, MONO, MUTE, 'end', ls=.6)
        s += _rows(10, 162, 54, rows)
        s += _t(10, 106, 'TOTAL DUE', 5.5, MONO, MUTE, ls=.6)
        s += _t(156, 106, total, 8, MONO, INK, 'end', 600)
        tx, ty, tw, th = 100, 94, 64, 17
    elif v == 1:    # big title, boxed table, total bottom-left
        s += _t(10, 24, 'Invoice', 15, SERIF, weight=500) + _t(10, 35, name, 6.5, SANS, MUTE)
        s += _t(162, 18, num, 5.5, MONO, MUTE, 'end') + _t(162, 27, 'Net 30', 5.5, MONO, MUTE, 'end')
        s += f'<rect x="10" y="42" width="152" height="46" rx="2" stroke-width=".9" opacity=".6"/>'
        s += f'<path d="M10 53H162M10 64H162M10 75H162M118 42V88" stroke-width=".7" opacity=".45"/>'
        for i, (d, amt) in enumerate(rows):
            y = 50 + i * 11
            s += _t(14, y, d, 6) + _t(158, y, amt, 5.8, MONO, anchor='end')
        s += _t(14, 103, 'Amount due', 6, SANS, MUTE) + _t(14, 114, total, 9, MONO, INK, weight=600)
        tx, ty, tw, th = 10, 96, 70, 22
    else:           # centered vendor, total top-right, lines below
        s += _t(86, 16, name, 9, SERIF, anchor='middle', weight=500)
        s += _t(10, 40, 'Ref ' + num, 5.5, MONO, MUTE)
        s += _t(162, 39, total, 8, MONO, INK, 'end', 600) + _t(162, 32, 'TOTAL', 5, MONO, MUTE, 'end', ls=.6)
        s += f'<path d="M10 47H162" stroke-width=".9" opacity=".5"/>'
        s += _rows(10, 162, 58, rows, step=11)
        s += _t(10, 112, 'Payable within 30 days', 5.5, SANS, MUTE)
        tx, ty, tw, th = 108, 24, 58, 19
    s += (f'<rect class="ap-cs-hl" x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="2" fill="rgba(132,0,85,.08)" '
          f'stroke="{MAG}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    return s


def chaos_scene():
    defs = ('<defs><linearGradient id="apg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{MAG}"/><stop offset="1" stop-color="#F89C2A"/></linearGradient></defs>')
    scatter = [(-150, -70, -18), (150, -90, 20), (-130, 60, 14), (120, 50, -22), (-80, 140, -26), (140, 120, 30)]
    docs = [
        ('Northbridge Studio', 'NB-2024-0418', '$15,091.75', [('Strategy workshop', '3,700.00'), ('UX research', '3,400.00'), ('Design audit', '4,200.00')]),
        ('Halden &amp; Co.', 'HC-88213', '$8,940.00', [('Freight', '2,100.00'), ('Handling', '640.00'), ('Insurance', '6,200.00')]),
        ('Kite Freight', '#4471', 'USD 1,205.50', [('Pallets x4', '480.00'), ('Fuel surcharge', '95.50'), ('Delivery', '630.00')]),
        ('ACME Supply', 'AS-1029', '$3,317.20', [('Materials', '1,900.00'), ('Tooling', '1,200.00'), ('Tax', '217.20')]),
        ('Orrin Labs', 'OL-5560', '$22,480.00', [('Assay panel', '9,600.00'), ('Sample prep', '4,880.00'), ('Rush fee', '8,000.00')]),
        ('Bellweather LLC', 'BW-0317', '$640.00', [('Hosting', '400.00'), ('Support', '190.00'), ('Domain', '50.00')]),
    ]
    out = ['<svg class="ap-chaos-svg" viewBox="36 8 438 522" xmlns="http://www.w3.org/2000/svg" '
           'fill="none" stroke="url(#apg)" stroke-width="1.4" aria-hidden="true" focusable="false">', defs]
    n = 0
    for j in range(3):
        for i in range(2):
            bx, by = 56 + i * 212, 28 + j * 152
            dx, dy, rot = scatter[n]
            name, num, total, rows = docs[n]
            out.append(f'<g transform="translate({bx} {by})"><g class="ap-cs" data-dx="{dx}" data-dy="{dy}" data-r="{rot}">'
                       f'{chaos_doc(n % 3, name, num, total, rows)}</g></g>')
            n += 1
    out.append('</svg>')
    return ''.join(out)


# ---------------------------------------------------------------- 4 challenge mini illustrations (200x120)
def mini(kind):
    s = _open(200, 120, 'ap-mini')
    if kind == 'formats':
        s += _doc(8, 14, 54, 74, 0) + '<rect x="14" y="20" width="22" height="8" fill="#fff"/><rect class="m1" x="36" y="66" width="20" height="8" fill="rgba(132,0,85,.15)" stroke="' + MAG + '"/>'
        s += _doc(72, 14, 54, 74, 0) + '<rect x="78" y="20" width="22" height="8" fill="#fff"/><rect class="m2" x="80" y="60" width="20" height="8" fill="rgba(132,0,85,.15)" stroke="' + MAG + '"/>'
        s += _doc(136, 14, 54, 74, 0) + '<rect x="142" y="20" width="22" height="8" fill="#fff"/><rect class="m3" x="164" y="22" width="20" height="8" fill="rgba(132,0,85,.15)" stroke="' + MAG + '"/>'
        s += f'<path d="M20 44h30M20 52h24M84 40h30M84 48h22M148 44h30M148 52h26" stroke-width="1.1" opacity=".5"/>'
    elif kind == 'tables':
        s += _doc(14, 10, 78, 92, 0) + _doc(104, 10, 78, 92, 0)
        s += '<path d="M22 24h62M22 36h62M22 48h62M22 60h62M22 72h62M22 24v48M50 24v48M84 24v48" stroke-width="1.1" opacity=".55"/>'
        s += '<path d="M112 24h62M112 36h62M112 48h62M112 24v24M140 24v24M174 24v24" stroke-width="1.1" opacity=".55"/>'
        s += f'<path d="M92 56h12" stroke="{MAG}" stroke-dasharray="2 3"/><rect class="m1" x="22" y="48" width="28" height="12" fill="rgba(132,0,85,.15)" stroke="{MAG}"/>'
    elif kind == 'calc':
        s += _doc(30, 8, 100, 104, 0)
        s += '<path d="M42 26h50M42 40h50M42 54h50" stroke-width="1.2" opacity=".55"/><path d="M100 26h18M100 40h18M100 54h18" stroke-width="1.6"/>'
        s += '<path d="M42 68h76" stroke-width="1.6"/>'
        s += f'<path class="m1" d="M100 84h18" stroke="{MAG}" stroke-width="2"/><path d="M42 84h34" stroke-width="1.2" opacity=".55"/>'
        s += f'<circle class="m2" cx="158" cy="64" r="20" fill="#fff" stroke="{MAG}"/><path d="M148 64l7 7 13-14" stroke="{MAG}" stroke-width="2"/>'
    else:  # po
        s += _doc(10, 12, 50, 64, 2) + _doc(75, 44, 50, 64, 2) + _doc(140, 12, 50, 64, 2)
        s += _tag(14, 18, 'PO', True) if False else ''
        s += f'<text x="20" y="66" font-size="9" {MONO} stroke="none" fill="{INK}">PO</text><text x="86" y="98" font-size="9" {MONO} stroke="none" fill="{INK}">GRN</text><text x="150" y="66" font-size="9" {MONO} stroke="none" fill="{INK}">INV</text>'
        s += f'<path class="m1" d="M60 56C68 56 68 70 75 70M125 70C132 70 132 56 140 56" stroke="{MAG}" stroke-width="1.6" stroke-dasharray="3 3"/>'
    return s + '</svg>'


# ---------------------------------------------------------------- pipeline illustrations (240x170)
def pipe_ill(n):
    s = _open(240, 170, 'ap-ill')
    if n == 1:
        s += _doc(70, 20, 90, 86, 3) + _doc(52, 34, 90, 86, 3) + _doc(34, 48, 90, 86, 4)
        s += _tag(150, 30, 'PDF') + _tag(158, 62, 'SCAN') + _tag(150, 96, 'XLSX') + _tag(30, 138, 'EMAIL')
        s += f'<path class="ap-draw" pathLength="1" d="M120 148v10M112 152l8 8 8-8" stroke="{MAG}" stroke-width="1.8"/>'
    elif n == 2:
        s += _doc(76, 30, 88, 100, 4)
        s += _tag(84, 42, 'INVOICE', True)
        s += _tag(10, 34, 'PO') + _tag(146, 140, 'CREDIT MEMO') + _tag(8, 110, 'REMITTANCE')
        s += f'<path class="ap-draw" pathLength="1" d="M34 49C50 49 60 56 78 62M180 140C176 132 170 128 164 124M52 114C64 112 70 104 78 100" stroke-dasharray="3 3" opacity=".6"/>'
    elif n == 3:
        s += _doc(20, 18, 110, 130, 0)
        s += '<path d="M30 34h50M30 46h74M30 58h60M30 100h74M30 112h60" stroke-width="1.1" opacity=".45"/>'
        s += f'<rect class="ap-draw" pathLength="1" x="26" y="28" width="60" height="14" stroke="{MAG}" stroke-dasharray="3 3"/>'
        s += f'<rect class="ap-draw" pathLength="1" x="26" y="52" width="76" height="14" stroke="{MAG}" stroke-dasharray="3 3"/>'
        s += f'<rect class="ap-draw" pathLength="1" x="76" y="122" width="48" height="16" stroke="{MAG}" stroke-dasharray="3 3"/>'
        s += f'<path d="M130 36h30M130 60h30M130 130h30" stroke="{MAG}" stroke-width="1.2"/>'
        s += _tag(162, 28, 'VENDOR') + _tag(162, 52, 'DATE') + _tag(162, 122, 'TOTAL', True)
    elif n == 4:
        s += _doc(28, 18, 150, 118, 0)
        for i, (lab, ok) in enumerate([('SUM', 1), ('TAX', 1), ('TOTAL', 1), ('PO', 0)]):
            y = 32 + i * 26
            s += f'<path d="M40 {y+6}h70" stroke-width="1.1" opacity=".5"/>'
            col = MAG if ok else AMB
            s += f'<circle class="ap-draw" pathLength="1" cx="150" cy="{y+4}" r="9" fill="#fff" stroke="{col}"/>'
            s += (f'<path d="M145 {y+4}l4 4 7-8" stroke="{col}" stroke-width="1.8"/>' if ok else
                  f'<path d="M150 {y-1}v6M150 {y+9}v.5" stroke="{col}" stroke-width="1.8"/>')
        s += f'<text x="188" y="60" font-size="10" {MONO} fill="{INK}" stroke="none">0.99</text>'
    else:
        s += f'<rect x="24" y="24" width="112" height="86" rx="3" fill="{SH}" stroke="none" transform="translate(5 5)"/><rect x="24" y="24" width="112" height="86" rx="3" fill="#fff"/>'
        s += f'<text x="34" y="46" font-size="10" {MONO} fill="{MAG}" stroke="none">{{</text><text x="46" y="62" font-size="8" {MONO} fill="{INK}" stroke="none">"total": 15091.75</text><text x="46" y="76" font-size="8" {MONO} fill="{INK}" stroke="none">"po": "PO-0284"</text><text x="34" y="96" font-size="10" {MONO} fill="{MAG}" stroke="none">}}</text>'
        s += f'<path class="ap-draw" pathLength="1" d="M136 66h34M162 58l8 8-8 8" stroke="{MAG}" stroke-width="1.8"/>'
        s += _tag(176, 40, 'WEBHOOK') + _tag(176, 92, 'API')
        s += f'<rect x="170" y="128" width="62" height="26" rx="3" fill="#fff" stroke-dasharray="3 3"/><text x="178" y="145" font-size="8" {MONO} fill="{INK}" stroke="none">AP SYSTEM</text>'
        s += f'<path d="M204 100v24M198 118l6 6 6-6" stroke-width="1.2" stroke-dasharray="3 3"/>'
    return s + '</svg>'


# ---------------------------------------------------------------- 48px line icons
def icon(name):
    p = {
        'ledger': '<rect x="8" y="6" width="32" height="36" rx="2"/><path d="M8 16h32M8 26h32M18 6v36"/>',
        'stack': '<rect x="14" y="6" width="26" height="32" rx="2"/><path d="M10 12v30h26M20 16h14M20 24h14M20 32h8"/>',
        'po': '<rect x="10" y="8" width="28" height="34" rx="2"/><path d="M18 8V5h12v3M16 20h16M16 27h16M16 34h9"/>',
        'box': '<path d="M24 5l17 9v20L24 43 7 34V14z"/><path d="M7 14l17 9 17-9M24 23v20"/>',
        'remit': '<rect x="6" y="12" width="36" height="26" rx="2"/><path d="M6 14l18 13 18-13"/>',
        'file': '<path d="M12 5h17l9 9v29H12z"/><path d="M29 5v9h9M18 24h14M18 31h14M18 38h8"/>',
        'plan': '<circle cx="21" cy="21" r="11"/><path d="M29 29l12 12M16 21h10M21 16v10"/>',
        'build': '<path d="M18 12L6 24l12 12M30 12l12 12-12 12M27 8l-6 32"/>',
        'deploy': '<path d="M24 6c8 6 11 14 9 24H15c-2-10 1-18 9-24zM15 30l-6 8 9-2M33 30l6 8-9-2"/><circle cx="24" cy="20" r="3"/>',
        'adjust': '<path d="M8 14h32M8 24h32M8 34h32"/><circle cx="16" cy="14" r="4" fill="#fff"/><circle cx="32" cy="24" r="4" fill="#fff"/><circle cx="20" cy="34" r="4" fill="#fff"/>',
        'link': '<circle cx="12" cy="24" r="6"/><circle cx="36" cy="12" r="6"/><circle cx="36" cy="36" r="6"/><path d="M18 22l12-8M18 26l12 8"/>',
    }[name]
    return (f'<svg class="ap-icon" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="{INK}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{p}</svg>')


# ---------------------------------------------------------------- invoice schematic for the fields explorer
def schematic():
    def lines(x, y, n, w=150, step=9, op=.5):
        return ''.join(f'<path d="M{x} {y + i * step}h{w - (i % 3) * 22}" stroke-width="1.1" opacity="{op}"/>' for i in range(n))
    s = _open(230, 300, 'ap-schem')
    s += f'<rect x="19" y="13" width="200" height="278" rx="3" fill="{SH}" stroke="none"/><rect x="14" y="8" width="200" height="278" rx="3" fill="#fff"/>'
    # header
    s += '<g class="rg rg-header"><rect class="bg" x="22" y="16" width="184" height="70" rx="2"/>'
    s += f'<text x="30" y="34" font-size="10" {SERIF} fill="{INK}" stroke="none" font-weight="500">Vendor name</text>'
    s += f'<text x="198" y="34" font-size="7" {MONO} fill="{INK}" stroke="none" text-anchor="end" letter-spacing="1.4">INVOICE</text>'
    s += lines(30, 44, 3, 96) + f'<path d="M150 44h48M150 53h48M150 62h48" stroke="{MAG}" stroke-width="1.4" opacity=".7"/>'
    s += f'<text x="30" y="80" font-size="6" {MONO} fill="{MAG}" stroke="none" letter-spacing=".8" class="lb">HEADER · 9 FIELDS</text></g>'
    # line items
    s += '<g class="rg rg-lines"><rect class="bg" x="22" y="96" width="184" height="112" rx="2"/>'
    s += '<path d="M30 112h168M30 128h168M30 144h168M30 160h168M30 176h168M30 112V176M112 112V176M150 112V176" stroke-width=".9" opacity=".45"/>'
    s += lines(34, 121, 1, 60) + lines(34, 137, 1, 50) + lines(34, 153, 1, 64) + lines(34, 169, 1, 44)
    s += f'<text x="30" y="202" font-size="6" {MONO} fill="{MAG}" stroke="none" letter-spacing=".8" class="lb">LINE ITEMS · 8 FIELDS</text></g>'
    # totals
    s += '<g class="rg rg-totals"><rect class="bg" x="22" y="216" width="184" height="62" rx="2"/>'
    s += '<path d="M116 228h82M116 240h82M116 252h82" stroke-width="1.1" opacity=".5"/><path d="M116 262h82" stroke-width="1.6"/>'
    s += f'<text x="30" y="272" font-size="6" {MONO} fill="{MAG}" stroke="none" letter-spacing=".8" class="lb">TOTALS · 8 FIELDS</text></g>'
    return s + '</svg>'
