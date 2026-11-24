# -*- coding: utf-8 -*-
"""
Construtor compartilhado dos guias de estudo (python-docx).

Todos os guias usam exatamente este módulo -> mesmo estilo visual; só mudam
a cor-base e o conteúdo.

Conteúdo = lista de blocos criados pelas funções H1, H2, H3, P, B, N, BOX,
T, CODE, F, EX, SPACE, PB.

Marcação inline aceita em qualquer texto:
    **negrito**   *itálico*   `código`   _{subscrito}   ^{sobrescrito}

Convenções para listas de conteúdo dentro de caixas (BOX) e respostas:
    "- texto"   -> marcador          "-- texto" -> marcador de 2º nível
    "= texto"   -> fórmula centralizada
    "# texto"   -> subtítulo em negrito
    "> texto"   -> linha monoespaçada (pseudocódigo / tabela ASCII)
    outro texto -> parágrafo comum
    dict (bloco T/CODE/F) -> renderizado dentro da caixa
"""
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# --------------------------------------------------------------------------
# Blocos (DSL)
# --------------------------------------------------------------------------
def H1(text, intro=None, numbered=True): return {"t": "h1", "text": text, "intro": intro, "numbered": numbered}
def H2(text):                      return {"t": "h2", "text": text}
def H3(text):                      return {"t": "h3", "text": text}
def P(text):                       return {"t": "p", "text": text}
def B(items):                      return {"t": "bullets", "items": items}
def N(items):                      return {"t": "numbered", "items": items}
def BOX(kind, title=None, items=None):
    if isinstance(items, str):
        items = [items]
    return {"t": "box", "kind": kind, "title": title, "items": items or []}
def T(headers, rows, widths=None, align=None, size=10):
    return {"t": "table", "headers": headers, "rows": rows, "widths": widths, "align": align, "size": size}
def CODE(text, title=None):        return {"t": "code", "text": text.strip("\n"), "title": title}
def F(text):                       return {"t": "formula", "text": text}
def EX(items, title=None):         return {"t": "ex", "items": items, "title": title}
def Q(q, a, opts=None, table=None, code=None):
    return {"q": q, "a": a, "opts": opts, "table": table, "code": code}
def SPACE(pt=6):                   return {"t": "space", "pt": pt}
def PB():                          return {"t": "pagebreak"}


# --------------------------------------------------------------------------
# Cores
# --------------------------------------------------------------------------
def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _hex(rgb):
    return "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)

def mix(h, other, t):
    """t=0 -> h ; t=1 -> other"""
    a, b = _rgb(h), _rgb(other)
    return _hex([a[i] + (b[i] - a[i]) * t for i in range(3)])


# --------------------------------------------------------------------------
# Utilidades de XML
# --------------------------------------------------------------------------
PPR_AFTER_PBDR = ('w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap',
                  'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN',
                  'w:bidi', 'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind',
                  'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc',
                  'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
                  'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange')
PPR_AFTER_SHD = PPR_AFTER_PBDR[1:]

TCPR_AFTER_SHD = ('w:noWrap', 'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign',
                  'w:hideMark', 'w:headers', 'w:cellIns', 'w:cellDel', 'w:cellMerge', 'w:tcPrChange')
TCPR_AFTER_BORDERS = ('w:shd',) + TCPR_AFTER_SHD
TCPR_AFTER_MAR = ('w:textDirection', 'w:tcFitText', 'w:vAlign', 'w:hideMark', 'w:headers',
                  'w:cellIns', 'w:cellDel', 'w:cellMerge', 'w:tcPrChange')

TBLPR_AFTER_BORDERS = ('w:shd', 'w:tblLayout', 'w:tblCellMar', 'w:tblLook', 'w:tblCaption',
                       'w:tblDescription', 'w:tblPrChange')
TBLPR_AFTER_LAYOUT = ('w:tblCellMar', 'w:tblLook', 'w:tblCaption', 'w:tblDescription', 'w:tblPrChange')


def _replace_child(parent, tag, successors):
    old = parent.find(qn(tag))
    if old is not None:
        parent.remove(old)
    el = OxmlElement(tag)
    parent.insert_element_before(el, *successors)
    return el


def ppr_border(pPr, sides):
    """sides: dict side -> (sz_eighths_pt, color_hex, space_pt)"""
    pbdr = _replace_child(pPr, 'w:pBdr', PPR_AFTER_PBDR)
    for side in ('top', 'left', 'bottom', 'right'):
        if side in sides:
            sz, color, space = sides[side]
            e = OxmlElement(f'w:{side}')
            e.set(qn('w:val'), 'single')
            e.set(qn('w:sz'), str(sz))
            e.set(qn('w:space'), str(space))
            e.set(qn('w:color'), color)
            pbdr.append(e)


def ppr_shade(pPr, fill):
    shd = _replace_child(pPr, 'w:shd', PPR_AFTER_SHD)
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)


def cell_shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = _replace_child(tcPr, 'w:shd', TCPR_AFTER_SHD)
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)


def cell_borders(cell, spec):
    """spec: dict side -> (sz, color) ou None para 'nil'"""
    tcPr = cell._tc.get_or_add_tcPr()
    b = _replace_child(tcPr, 'w:tcBorders', TCPR_AFTER_BORDERS)
    for side in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement(f'w:{side}')
        v = spec.get(side)
        if v is None:
            e.set(qn('w:val'), 'nil')
        else:
            e.set(qn('w:val'), 'single')
            e.set(qn('w:sz'), str(v[0]))
            e.set(qn('w:space'), '0')
            e.set(qn('w:color'), v[1])
        b.append(e)


def cell_margins(cell, top=100, bottom=100, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    m = _replace_child(tcPr, 'w:tcMar', TCPR_AFTER_MAR)
    for side, val in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        e = OxmlElement(f'w:{side}')
        e.set(qn('w:w'), str(val))
        e.set(qn('w:type'), 'dxa')
        m.append(e)


def table_borders(table, color=None, sz=4):
    tblPr = table._tbl.tblPr
    b = _replace_child(tblPr, 'w:tblBorders', TBLPR_AFTER_BORDERS)
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{side}')
        if color is None:
            e.set(qn('w:val'), 'nil')
        else:
            e.set(qn('w:val'), 'single')
            e.set(qn('w:sz'), str(sz))
            e.set(qn('w:space'), '0')
            e.set(qn('w:color'), color)
        b.append(e)


def table_fixed(table):
    tblPr = table._tbl.tblPr
    lay = _replace_child(tblPr, 'w:tblLayout', TBLPR_AFTER_LAYOUT)
    lay.set(qn('w:type'), 'fixed')


def row_flags(row, header=False, cant_split=False):
    trPr = row._tr.get_or_add_trPr()
    if cant_split:
        trPr.append(OxmlElement('w:cantSplit'))
    if header:
        trPr.append(OxmlElement('w:tblHeader'))


def style_font(style, name, size=None, bold=None, color=None, italic=None):
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        rfonts.attrib.pop(qn(a), None)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rfonts.set(qn(a), name)
    if size is not None:
        style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    if color is not None:
        style.font.color.rgb = RGBColor.from_string(color)
        c = rpr.find(qn('w:color'))
        if c is not None:
            for a in ('w:themeColor', 'w:themeShade', 'w:themeTint'):
                c.attrib.pop(qn(a), None)


def add_field(paragraph, instr, placeholder=""):
    runs = []
    r = paragraph.add_run()
    f = OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'), 'begin'); r._r.append(f); runs.append(r)
    r = paragraph.add_run()
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr; r._r.append(it); runs.append(r)
    r = paragraph.add_run()
    f = OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'), 'separate'); r._r.append(f); runs.append(r)
    r = paragraph.add_run(placeholder); runs.append(r)
    r = paragraph.add_run()
    f = OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'), 'end'); r._r.append(f); runs.append(r)
    return runs


# --------------------------------------------------------------------------
# Marcação inline
# --------------------------------------------------------------------------
TOKEN = re.compile(r'(\*\*.+?\*\*|`[^`]+`|_\{[^}]*\}|\^\{[^}]*\}|\*[^*\s][^*]*?\*)')
MONO = "Consolas"
MATH = "Cambria Math"
EMOJI = "Segoe UI Emoji"


def add_runs(p, text, bold=False, italic=False, color=None, size=None, font=None,
             sub=False, sup=False):
    for part in TOKEN.split(text):
        if not part:
            continue
        kw = dict(bold=bold, italic=italic, color=color, size=size, font=font, sub=sub, sup=sup)
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            kw["bold"] = True
            add_runs(p, part[2:-2], **kw)
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            kw["font"] = MONO
            _run(p, part[1:-1], **kw)
        elif part.startswith("_{") and part.endswith("}"):
            kw["sub"] = True
            _run(p, part[2:-1], **kw)
        elif part.startswith("^{") and part.endswith("}"):
            kw["sup"] = True
            _run(p, part[2:-1], **kw)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            kw["italic"] = True
            add_runs(p, part[1:-1], **kw)
        else:
            _run(p, part, **kw)


def _run(p, text, bold=False, italic=False, color=None, size=None, font=None, sub=False, sup=False):
    r = p.add_run(text)
    if bold:
        r.bold = True
    if italic:
        r.italic = True
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    if size:
        r.font.size = Pt(size)
    if font:
        r.font.name = font
        rpr = r._r.get_or_add_rPr()
        rf = rpr.find(qn('w:rFonts'))
        rf.set(qn('w:eastAsia'), font)
        rf.set(qn('w:cs'), font)
    if sub:
        r.font.subscript = True
    if sup:
        r.font.superscript = True
    return r


# --------------------------------------------------------------------------
# Construtor
# --------------------------------------------------------------------------
PAGE_W_CM = 21.0
MARGIN_CM = 2.0
BODY_W_CM = PAGE_W_CM - 2 * MARGIN_CM   # 17 cm


class Guide:
    def __init__(self, key, title, color, professor, exam_date, sources,
                 subtitle="Guia de estudos · Prova do 2º bimestre", note=None, topics=None):
        self.key = key
        self.title = title
        self.subtitle = subtitle
        self.base = color.upper()
        self.dark = mix(self.base, "000000", 0.35)
        self.light = mix(self.base, "FFFFFF", 0.88)
        self.lighter = mix(self.base, "FFFFFF", 0.94)
        self.mid = mix(self.base, "FFFFFF", 0.55)
        self.professor = professor
        self.exam_date = exam_date
        self.sources = sources
        self.note = note
        self.topics = topics or []
        self.h1n = 0
        self.h2n = 0
        self.exn = 0
        self.BOX = {
            "def":      ("📘", "Definição",              self.light,  self.base,  self.dark),
            "insight":  ("💡", "Insight",                self.light,  self.base,  self.dark),
            "intuicao": ("🧠", "Intuição",               self.light,  self.base,  self.dark),
            "erro":     ("⚠️", "Erro comum",             "FFF3E0",    "E65100",   "BF360C"),
            "lembrete": ("📌", "Lembrete para a prova",  "FFF8E1",    "F9A825",   "8D6E00"),
            "exemplo":  ("🧪", "Exemplo resolvido",      "F5F5F5",    "757575",   "424242"),
            "extra":    ("🔎", "Além dos slides",        "EEF2F5",    "607D8B",   "37474F"),
            "resumo":   ("🧾", "Resumo da seção",        self.lighter, self.base, self.dark),
            "gabarito": ("✅", "Gabarito comentado",     self.lighter, self.dark, self.dark),
        }

    # ---------------- estilos ----------------
    def _setup(self):
        doc = Document()
        sec = doc.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        for side in ("left_margin", "right_margin"):
            setattr(sec, side, Cm(MARGIN_CM))
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(1.8)
        sec.header_distance = Cm(0.9)
        sec.footer_distance = Cm(0.8)
        sec.different_first_page_header_footer = True

        st = doc.styles
        style_font(st["Normal"], "Calibri", 11)
        pf = st["Normal"].paragraph_format
        pf.space_after = Pt(6)
        pf.line_spacing = 1.15

        style_font(st["Heading 1"], "Calibri", 22, True, self.base)
        h1 = st["Heading 1"].paragraph_format
        h1.space_before, h1.space_after = Pt(0), Pt(14)
        h1.keep_with_next = True
        h1.page_break_before = True
        ppr_border(st["Heading 1"].element.get_or_add_pPr(), {"bottom": (18, self.base, 6)})

        style_font(st["Heading 2"], "Calibri", 14, True, self.dark)
        h2 = st["Heading 2"].paragraph_format
        h2.space_before, h2.space_after = Pt(16), Pt(8)
        h2.keep_with_next = True
        h2pPr = st["Heading 2"].element.get_or_add_pPr()
        ppr_border(h2pPr, {"left": (36, self.base, 8)})
        ppr_shade(h2pPr, self.lighter)

        style_font(st["Heading 3"], "Calibri", 12, True, self.base)
        h3 = st["Heading 3"].paragraph_format
        h3.space_before, h3.space_after = Pt(12), Pt(4)
        h3.keep_with_next = True

        for name in ("List Bullet", "List Bullet 2"):
            style_font(st[name], "Calibri", 11)
            st[name].paragraph_format.space_after = Pt(3)
        for name in ("TOC 1", "TOC 2"):
            try:
                s = st[name]
            except KeyError:
                s = st.add_style(name, 1)
            style_font(s, "Calibri", 11 if name == "TOC 1" else 10.5,
                       bold=(name == "TOC 1"), color=self.dark if name == "TOC 1" else "333333")
            s.paragraph_format.space_after = Pt(2 if name == "TOC 2" else 4)
            s.paragraph_format.space_before = Pt(6 if name == "TOC 1" else 0)
            if name == "TOC 2":
                s.paragraph_format.left_indent = Cm(0.6)
        self.doc = doc

    def _header_footer(self):
        sec = self.doc.sections[0]
        hp = sec.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        add_runs(hp, f"Guia de Estudos  ·  ", color="777777", size=9)
        add_runs(hp, self.title, color=self.base, size=9, bold=True)
        ppr_border(hp._p.get_or_add_pPr(), {"bottom": (6, self.mid, 4)})

        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(fp, "Página ", color="777777", size=9)
        for r in add_field(fp, "PAGE", "1"):
            r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(self.base); r.bold = True
        add_runs(fp, " de ", color="777777", size=9)
        for r in add_field(fp, "NUMPAGES", "1"):
            r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string("777777")

    # ---------------- capa + sumário ----------------
    def _cover(self):
        doc = self.doc
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_borders(t, None)
        c = t.rows[0].cells[0]
        c.width = Cm(BODY_W_CM)
        t.rows[0].height = Cm(10.5)
        t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        cell_shade(c, self.base)
        cell_margins(c, 400, 400, 500, 500)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = c.paragraphs[0]
        add_runs(p, "GUIA DE ESTUDOS", color=self.light, size=12, bold=True)
        p.paragraph_format.space_after = Pt(18)
        p = c.add_paragraph()
        add_runs(p, self.title, color="FFFFFF", size=34, bold=True)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.0
        p = c.add_paragraph()
        add_runs(p, self.subtitle, color=self.light, size=14)
        p.paragraph_format.space_after = Pt(26)
        p = c.add_paragraph()
        ppr_border(p._p.get_or_add_pPr(), {"top": (8, self.light, 10)})
        add_runs(p, self.professor, color="FFFFFF", size=11, bold=True)
        p = c.add_paragraph()
        add_runs(p, f"Prova: {self.exam_date}", color="FFFFFF", size=11)

        doc.add_paragraph().paragraph_format.space_after = Pt(10)

        # ficha
        info = [("Material-base", self.sources)]
        if self.topics:
            info.append(("Conteúdo", " · ".join(self.topics)))
        if self.note:
            info.append(("Observação", self.note))
        t = doc.add_table(rows=len(info), cols=2)
        table_borders(t, None)
        table_fixed(t)
        for i, (k, v) in enumerate(info):
            a, b = t.rows[i].cells
            a.width, b.width = Cm(3.6), Cm(BODY_W_CM - 3.6)
            for cc in (a, b):
                cell_borders(cc, {"bottom": (4, self.mid)})
                cell_margins(cc, 80, 80, 100, 100)
            add_runs(a.paragraphs[0], k.upper(), color=self.base, bold=True, size=9)
            add_runs(b.paragraphs[0], v, size=10)
            for cc in (a, b):
                cc.paragraphs[0].paragraph_format.space_after = Pt(0)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        p = doc.add_paragraph()
        add_runs(p, "Como usar este guia", bold=True, color=self.dark, size=13)
        p.paragraph_format.space_after = Pt(4)
        p = doc.add_paragraph()
        add_runs(p, "Cada seção segue o roteiro *intuição → definição → exemplo → armadilhas* e termina com "
                    "**exercícios de revisão** e **gabarito comentado**. Tente resolver antes de olhar a resposta. "
                    "As caixas coloridas sinalizam o tipo de informação:", size=10)
        legend = [
            ("def", "conceitos e fórmulas oficiais"),
            ("insight", "o “porquê” por trás do conteúdo"),
            ("erro", "pegadinhas e confusões frequentes"),
            ("lembrete", "o que memorizar para a prova"),
            ("exemplo", "contas passo a passo"),
            ("extra", "complementos externos aos slides"),
        ]
        t = doc.add_table(rows=2, cols=3)
        table_borders(t, None)
        table_fixed(t)
        for i, (kind, desc) in enumerate(legend):
            icon, name, fill, border, tcol = self.BOX[kind]
            cc = t.rows[i // 3].cells[i % 3]
            cc.width = Cm(BODY_W_CM / 3)
            cell_shade(cc, fill)
            cell_borders(cc, {"left": (24, border), "top": (12, "FFFFFF"), "bottom": (12, "FFFFFF"),
                              "right": (36, "FFFFFF")})
            cell_margins(cc, 60, 60, 120, 80)
            p = cc.paragraphs[0]
            _run(p, icon + " ", font=EMOJI, size=10)
            add_runs(p, name, bold=True, color=tcol, size=10)
            p.paragraph_format.space_after = Pt(0)
            p2 = cc.add_paragraph()
            add_runs(p2, desc, size=9, color="555555")
            p2.paragraph_format.space_after = Pt(0)

        # sumário
        p = doc.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)
        p = doc.add_paragraph()
        add_runs(p, "Sumário", bold=True, color=self.base, size=22)
        ppr_border(p._p.get_or_add_pPr(), {"bottom": (18, self.base, 6)})
        p.paragraph_format.space_after = Pt(12)
        p = doc.add_paragraph()
        add_field(p, 'TOC \\o "1-2" \\h \\z \\u',
                  "Sumário — clique com o botão direito e escolha “Atualizar campo”.")

    # ---------------- renderização ----------------
    def _para(self, cont):
        """Novo parágrafo no container; reaproveita o 1º parágrafo vazio de células."""
        if hasattr(cont, "_fresh") and cont._fresh:
            cont._fresh = False
            return cont.paragraphs[0]
        return cont.add_paragraph()

    def _spacer(self, cont, pt=4):
        if cont is not self.doc:
            pt = min(pt, 3)
        p = self._para(cont)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = Pt(pt)
        return p

    def _new_cell(self, cell):
        cell._fresh = True
        return cell

    def render(self, cont, blk, in_box=False):
        t = blk["t"]
        if t == "h1":
            if blk.get("numbered", True):
                self.h1n += 1
            self.h2n = 0
            self.exn = 0
            p = self.doc.add_paragraph(style="Heading 1")
            add_runs(p, f"{self.h1n}. {blk['text']}" if blk.get("numbered", True) else blk["text"])
            self._unnum = not blk.get("numbered", True)
            if blk.get("intro"):
                p = self.doc.add_paragraph()
                add_runs(p, blk["intro"], italic=True, color="555555")
        elif t == "h2":
            self.h2n += 1
            p = self.doc.add_paragraph(style="Heading 2")
            add_runs(p, blk['text'] if getattr(self, "_unnum", False) else f"{self.h1n}.{self.h2n}  {blk['text']}")
        elif t == "h3":
            p = self._para(cont)
            p.style = self.doc.styles["Heading 3"]
            add_runs(p, blk["text"])
        elif t == "p":
            p = self._para(cont)
            add_runs(p, blk["text"])
            if in_box:
                p.paragraph_format.space_after = Pt(3)
        elif t == "bullets":
            self._bullets(cont, blk["items"], 1, in_box)
        elif t == "numbered":
            for i, it in enumerate(blk["items"], 1):
                p = self._para(cont)
                pf = p.paragraph_format
                pf.left_indent = Cm(0.8)
                pf.first_line_indent = Cm(-0.6)
                pf.tab_stops.add_tab_stop(Cm(0.8))
                pf.space_after = Pt(3)
                add_runs(p, f"{i}.\t", bold=True, color=self.base)
                add_runs(p, it)
        elif t == "box":
            self._box(cont, blk)
        elif t == "table":
            self._table(cont, blk, in_box)
        elif t == "code":
            self._code(cont, blk, in_box)
        elif t == "formula":
            self._formula(cont, blk["text"])
        elif t == "ex":
            self._exercises(blk)
        elif t == "space":
            self._spacer(cont, blk["pt"])
        elif t == "pagebreak":
            p = self._para(cont)
            p.add_run().add_break(WD_BREAK.PAGE)
        else:
            raise ValueError(t)

    def _bullets(self, cont, items, level, in_box):
        for it in items:
            if isinstance(it, (list, tuple)):
                head, subs = it[0], it[1]
                self._bullets(cont, [head], level, in_box)
                self._bullets(cont, subs, level + 1, in_box)
                continue
            p = self._para(cont)
            p.style = self.doc.styles["List Bullet" if level == 1 else "List Bullet 2"]
            add_runs(p, it)
            p.paragraph_format.space_after = Pt(2 if in_box else 3)

    def _formula(self, cont, text):
        p = self._para(cont)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        add_runs(p, text, font=MATH, size=11.5, color="1A1A1A")

    def _items(self, cell, items):
        """Renderiza a lista de itens (strings com prefixo ou blocos) dentro de uma célula."""
        for it in items:
            if isinstance(it, dict):
                self.render(cell, it, in_box=True)
                continue
            if it.startswith("-- "):
                p = self._para(cell)
                p.style = self.doc.styles["List Bullet 2"]
                add_runs(p, it[3:])
                p.paragraph_format.space_after = Pt(2)
            elif it.startswith("- "):
                p = self._para(cell)
                p.style = self.doc.styles["List Bullet"]
                add_runs(p, it[2:])
                p.paragraph_format.space_after = Pt(2)
            elif it.startswith("= "):
                self._formula(cell, it[2:])
            elif it.startswith("# "):
                p = self._para(cell)
                add_runs(p, it[2:], bold=True)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.keep_with_next = True
            elif it.startswith("> "):
                p = self._para(cell)
                add_runs(p, it[2:], font=MONO, size=9.5)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
            else:
                p = self._para(cell)
                add_runs(p, it)
                p.paragraph_format.space_after = Pt(3)

    def _box(self, cont, blk, width_cm=None):
        icon, name, fill, border, tcol = self.BOX[blk["kind"]]
        title = blk["title"]
        t = cont.add_table(rows=1, cols=1)
        if cont is self.doc:
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_borders(t, None)
        table_fixed(t)
        cell = self._new_cell(t.rows[0].cells[0])
        cell.width = Cm(width_cm or (BODY_W_CM if cont is self.doc else BODY_W_CM - 1.2))
        cell_shade(cell, fill)
        cell_borders(cell, {"left": (36, border)})
        cell_margins(cell, 110, 110, 200, 180)
        p = self._para(cell)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        _run(p, icon + "  ", font=EMOJI, size=11)
        add_runs(p, name.upper() if not title else name.upper() + "  ·  ", bold=True, color=tcol, size=9)
        if title:
            add_runs(p, title, bold=True, color=tcol, size=11)
        self._items(cell, blk["items"])
        if cont is self.doc:
            self._spacer(self.doc, 8)

    def _table(self, cont, blk, in_box=False):
        headers, rows = blk["headers"], blk["rows"]
        ncol = len(headers) if headers else len(rows[0])
        total = BODY_W_CM if cont is self.doc else BODY_W_CM - 1.8
        widths = blk["widths"] or [total / ncol] * ncol
        s = sum(widths)
        widths = [w * total / s for w in widths]
        align = blk["align"] or ["l"] * ncol
        size = blk["size"]
        nrows = len(rows) + (1 if headers else 0)
        t = cont.add_table(rows=nrows, cols=ncol)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_borders(t, "BFBFBF", 4)
        table_fixed(t)
        AL = {"l": WD_ALIGN_PARAGRAPH.LEFT, "c": WD_ALIGN_PARAGRAPH.CENTER, "r": WD_ALIGN_PARAGRAPH.RIGHT}
        r0 = 0
        if headers:
            row = t.rows[0]
            row_flags(row, header=True, cant_split=True)
            for j, h in enumerate(headers):
                c = row.cells[j]
                c.width = Cm(widths[j])
                cell_shade(c, self.base)
                cell_margins(c, 60, 60, 90, 90)
                c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = c.paragraphs[0]
                p.alignment = AL[align[j]] if align[j] != "l" else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.keep_with_next = True
                add_runs(p, h, bold=True, color="FFFFFF", size=size)
            r0 = 1
        for i, rv in enumerate(rows):
            row = t.rows[r0 + i]
            row_flags(row, cant_split=True)
            for j in range(ncol):
                val = rv[j] if j < len(rv) else ""
                c = row.cells[j]
                c.width = Cm(widths[j])
                if i % 2 == 1:
                    cell_shade(c, self.lighter)
                elif in_box:
                    cell_shade(c, "FFFFFF")
                cell_margins(c, 50, 50, 90, 90)
                c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                lines = val if isinstance(val, list) else [val]
                for k, line in enumerate(lines):
                    p = c.paragraphs[0] if k == 0 else c.add_paragraph()
                    p.alignment = AL[align[j]]
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.05
                    if i == 0 and len(rows) > 1:
                        p.paragraph_format.keep_with_next = True
                    add_runs(p, str(line), size=size)
        self._spacer(cont, 8)

    def _code(self, cont, blk, in_box=False):
        t = cont.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_borders(t, None)
        table_fixed(t)
        cell = self._new_cell(t.rows[0].cells[0])
        cell.width = Cm(BODY_W_CM if cont is self.doc else BODY_W_CM - 1.8)
        cell_shade(cell, "F7F7F7" if not in_box else "FFFFFF")
        cell_borders(cell, {"left": (18, self.mid), "top": (4, "E0E0E0"), "bottom": (4, "E0E0E0"),
                            "right": (4, "E0E0E0")})
        cell_margins(cell, 80, 80, 160, 120)
        if blk.get("title"):
            p = self._para(cell)
            add_runs(p, blk["title"], bold=True, color=self.dark, size=9)
            p.paragraph_format.space_after = Pt(2)
        for line in blk["text"].split("\n"):
            p = self._para(cell)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            add_runs(p, line if line else " ", font=MONO, size=9.5)
        self._spacer(cont, 8)

    def _exercises(self, blk):
        self.exn = 0
        doc = self.doc
        p = doc.add_paragraph(style="Heading 3")
        _run(p, "✍️  ", font=EMOJI)
        add_runs(p, blk.get("title") or f"Exercícios de revisão — Seção {self.h1n}")
        ppr_border(p._p.get_or_add_pPr(), {"top": (6, self.mid, 6)})
        for q in blk["items"]:
            self.exn += 1
            q["_id"] = f"{self.h1n}.{self.exn}"
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = Cm(1.1)
            pf.first_line_indent = Cm(-1.1)
            pf.tab_stops.add_tab_stop(Cm(1.1))
            pf.space_after = Pt(4)
            pf.keep_with_next = bool(q.get("opts") or q.get("table") or q.get("code"))
            add_runs(p, f"Q{q['_id']}\t", bold=True, color=self.base)
            add_runs(p, q["q"])
            if q.get("table"):
                h, rows = q["table"][0], q["table"][1]
                self._table(doc, {"headers": h, "rows": rows, "widths": None, "align": ["c"] * len(h or rows[0]),
                                  "size": 9.5})
            if q.get("code"):
                self._code(doc, {"text": q["code"].strip("\n"), "title": None})
            for k, o in enumerate(q.get("opts") or []):
                p = doc.add_paragraph()
                pf = p.paragraph_format
                pf.left_indent = Cm(1.8)
                pf.first_line_indent = Cm(-0.6)
                pf.tab_stops.add_tab_stop(Cm(1.8))
                pf.space_after = Pt(1)
                add_runs(p, f"{'abcdefgh'[k]})\t", bold=True, color=self.dark)
                add_runs(p, o)
            if q.get("opts"):
                self._spacer(doc, 4)
        # gabarito
        items = []
        for q in blk["items"]:
            ans = q["a"] if isinstance(q["a"], list) else [q["a"]]
            first = True
            for a in ans:
                if first and isinstance(a, str) and not a[:2] in ("- ", "= ", "# ", "> ", "--"):
                    items.append(f"**Q{q['_id']} —** " + a)
                else:
                    if first:
                        items.append(f"# Q{q['_id']}")
                    items.append(a)
                first = False
        self._box(doc, {"kind": "gabarito", "title": f"Seção {self.h1n}", "items": items})

    # ---------------- API ----------------
    def build(self, content, out_path):
        self._setup()
        self._header_footer()
        self._cover()
        for blk in content:
            self.render(self.doc, blk)
        self.doc.save(out_path)
        return out_path
