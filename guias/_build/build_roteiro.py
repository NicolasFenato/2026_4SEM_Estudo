# -*- coding: utf-8 -*-
"""Gera o Roteiro de Estudos (DOCX). Depois: docx2pdf.ps1 ../Roteiro_de_Estudos.docx"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from guide_builder import (add_runs, cell_shade, cell_borders, cell_margins, table_borders, table_fixed,
                           style_font, ppr_border, row_flags, mix, add_field, _run, EMOJI)

BASE = "37474F"   # cinza-azulado neutro do documento
D = {  # disciplina -> (nome curto, cor)
    "ML": ("Machine Learning", "1565C0"),
    "RD": ("Redes", "C62828"),
    "CG": ("Comp. Gráfica", "6D4C41"),
    "CP": ("Computabilidade", "6A1B9A"),
    "BD": ("Banco de Dados", "2E7D32"),
}
ABBR = {"ML": "ML", "RD": "Redes", "CG": "CG", "CP": "Comput.", "BD": "BD"}
EXAM = {"ML": "30/11 (seg)", "RD": "30/11 (seg)", "CG": "01/12 (ter)", "CP": "03/12 (qui)", "BD": "08/12 (ter)"}

# (dia_semana, data, [(disc, texto, minutos)], meta, prova)
DAYS = [
    ("Terça", "24/11", [
        ("ML", "Guia ML · Seção 1 — Árvores de decisão e ID3 (leitura + exercícios)", 75),
        ("ML", "Guia ML · Seção 2 — C4.5: razão de ganho e atributos contínuos (refaça as contas à mão)", 105)],
     "Calcular entropia, ganho e razão de ganho sem consultar; achar o melhor limiar de um atributo contínuo.", None),
    ("Quarta", "25/11", [
        ("ML", "Guia ML · Seção 2 (cont.) — valores ausentes, poda e exercícios", 60),
        ("ML", "Guia ML · Seção 3 — Neurônio e Perceptron (simule 1 época à mão)", 90),
        ("ML", "Revisão relâmpago: refazer 3 contas de ganho/razão sem olhar o gabarito", 30)],
     "Decidir poda por erro e/ou limiar; aplicar a regra do Perceptron (y·z ≤ 0) em um exemplo.", None),
    ("Quinta", "26/11", [
        ("ML", "Guia ML · Seção 4 — XOR, MLP e forward pass (calcule ŷ, MSE e BCE)", 90),
        ("ML", "Guia ML · Seção 5 — Backpropagation e gradiente descendente (δ⁽²⁾, δ⁽¹⁾, atualização)", 90)],
     "Fazer o forward de uma MLP 2-2-1 e um passo de backprop com os números do slide.", None),
    ("Sexta", "27/11", [
        ("ML", "Guia ML · Seção 6 — Regressão linear simples e múltipla (β₁, β₀ e (XᵀX)⁻¹Xᵀy)", 75),
        ("ML", "Guia ML · Seção 7 — K-means (itere à mão) e escolha de k (cotovelo/silhueta)", 90),
        ("ML", "Ler a Cola (Seção 8) e anotar os 12 erros mais comuns", 15)],
     "Ajustar uma reta de mínimos quadrados; fazer 2 iterações de K-means; calcular uma silhueta.", None),
    ("Sábado", "28/11", [
        ("ML", "Revisão ativa: refaça os exercícios das Seções 1–5 SEM olhar o gabarito; anote os erros", 120),
        ("RD", "Guia Redes · Seções 1–3 — introdução, camadas OSI/TCP-IP, nível físico", 75),
        ("RD", "Guia Redes · Seção 4 — Enlace e Ethernet (CSMA/CD, quadro 802.3, switch × hub × roteador, VLAN)", 75)],
     "Dizer em que camada está cada equipamento/protocolo; números do quadro Ethernet de cabeça.", None),
    ("Domingo", "29/11", [
        ("ML", "Revisão das Seções 6–7 + mini-simulado final do guia (Seção 8)", 60),
        ("RD", "Guia Redes · Seções 5–6 — rede/roteamento e TCP/IP (faça as contas de sub-rede à mão)", 60),
        ("RD", "Guia Redes · Seções 7–8 — gerência (FCAPS, SNMP, SLA) e segurança; ler a Cola", 30),
        ("CG", "Guia CG · Seção 1 — Transformações 3D e composição (matrizes, pivô, ordem T·R·S)", 75),
        ("CG", "Guia CG · Seção 2 — Objetos 3D, malhas e arquivo .obj", 45)],
     "Redes: máscara/CIDR e portas dominados. CG: aplicar T, E, Rx/Ry/Rz e rotação em torno de pivô.", None),
    ("Segunda", "30/11", [
        ("ML", "ANTES DA PROVA — Cola do ML (Seção 8): fórmulas e erros comuns", 15),
        ("RD", "ANTES DA PROVA — Cola de Redes (Seção 9)", 15),
        ("CG", "Guia CG · Seção 3 — Projeções e câmera (eye/look/up → u,v,n; Model·View·Projection)", 75),
        ("CG", "Guia CG · Seção 4 — Cenas e pipeline gráfico (ordem das etapas)", 45),
        ("CG", "Guia CG · Seção 5 — Iluminação (Lambert, especular, ambiente, flat × smooth)", 60)],
     "Depois das provas: projetar um ponto em perspectiva; ordenar o pipeline; calcular I_d e r.", "PROVAS: Machine Learning + Redes"),
    ("Terça", "01/12", [
        ("CG", "ANTES DA PROVA — Cola de CG (Seção 6) + mini-simulado do guia", 60),
        ("CP", "Guia Computabilidade · Seção 1 — Máquina de Turing (rastreie MT_bin_par e {0ⁿ1ⁿ} à mão)", 90),
        ("CP", "Guia Computabilidade · Seção 2 — Extensões da MT e equivalência", 45)],
     "Depois da prova: escrever a definição formal da MT e as 3 condições de parada de cabeça.", "PROVA: Computação Gráfica"),
    ("Quarta", "02/12", [
        ("CP", "Guia Computabilidade · Seção 3 — Church-Turing, decidível × aceitável, hierarquia", 75),
        ("CP", "Guia Computabilidade · Seção 4 — ALG, problema da parada e semidecidibilidade", 75),
        ("CP", "Guia Computabilidade · Seção 5 — Diagonalização de Cantor e L_D", 75),
        ("CP", "Refazer à mão as provas de HALT e de L_D (sem consultar)", 30)],
     "Explicar por que HALT não existe e por que L_D é não-RE; classificar linguagens (recursiva/RE/não-RE).", None),
    ("Quinta", "03/12", [
        ("CP", "ANTES DA PROVA — Guia Computabilidade · Seção 6 — Redutibilidade (direção da redução!)", 75),
        ("CP", "ANTES DA PROVA — Cola + mini-simulado do guia", 45),
        ("BD", "Depois da prova: Guia BD · visão geral + Seção 1 (ordenação em memória × externa)", 60)],
     "Fazer uma redução por mapeamento e dizer o que se conclui (decidível/indecidível).", "PROVA: Computabilidade"),
    ("Sexta", "04/12", [
        ("BD", "Guia BD · Seção 2 — Algoritmos de seleção (sequencial, binária, clustering, secundário; AND/OR)", 75),
        ("BD", "Guia BD · Seção 3 — Junção (NL tupla/bloco v1/v2, índice, sort-merge, hash)", 90),
        ("BD", "Refazer 3 contas de custo sem olhar o gabarito", 15)],
     "Calcular custos de seleção e de junção (NL v1/v2) e escolher o melhor algoritmo.", None),
    ("Sábado", "05/12", [
        ("BD", "Exercícios da Seção 3 (junção) + contas do exemplo empregado ⨝ departamento", 30),
        ("BD", "Guia BD · Seção 4 — Projeção, duplicados, conjuntos e agregação", 45),
        ("BD", "Guia BD · Seção 5 — Otimização de consultas (regras R1–R10, algoritmo geral, exemplo)", 105),
        ("BD", "Refazer: otimizar uma consulta nova (árvore canônica → otimizada)", 30)],
     "Montar a árvore otimizada de uma consulta; justificar o plano com estatísticas.", None),
    ("Domingo", "06/12", [
        ("BD", "Guia BD · Seção 6 — Transações, escalonamentos e ACID", 60),
        ("BD", "Guia BD · Seção 7 — Problemas de concorrência (lost update, dirty read…)", 45),
        ("BD", "Guia BD · Seção 8 — Serializabilidade (grafo de precedência), view, SQL e níveis de isolamento", 90)],
     "Montar o grafo de precedência de qualquer escalonamento e dizer se é serializável.", None),
    ("Segunda", "07/12", [
        ("BD", "Revisão: refazer as contas de custo (ordenação, seleção, junção, projeção)", 75),
        ("BD", "Revisão: grafos de precedência + tabela de isolamento", 45),
        ("BD", "Cola + mini-simulado do guia (Seção 9)", 45)],
     "Zero dúvida nas fórmulas; erros do caderno de erros revisados.", None),
    ("Terça", "08/12", [
        ("BD", "ANTES DA PROVA — Cola + 5 exercícios relâmpago (1 de cada tema) e revisão do caderno de erros", 120)],
     "Entrar na prova com as fórmulas de custo e o teste de serializabilidade automáticos.", "PROVA: Banco de Dados"),
]


def fmt(m):
    h, mi = divmod(m, 60)
    if h and mi: return f"{h}h{mi:02d}"
    if h: return f"{h}h"
    return f"{mi} min"


def gap(doc, pt=3):
    g = doc.add_paragraph()
    g.paragraph_format.space_after = Pt(0)
    g.paragraph_format.space_before = Pt(0)
    g.paragraph_format.line_spacing = Pt(pt)
    return g


def lighter(c, t=0.88):
    return mix(c, "FFFFFF", t)


doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(1.8)
sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.6)
sec.footer_distance = Cm(0.7)
st = doc.styles
style_font(st["Normal"], "Calibri", 10.5)
st["Normal"].paragraph_format.space_after = Pt(4)
st["Normal"].paragraph_format.line_spacing = 1.1
style_font(st["Heading 1"], "Calibri", 17, True, BASE)
st["Heading 1"].paragraph_format.space_before = Pt(14)
st["Heading 1"].paragraph_format.space_after = Pt(6)
st["Heading 1"].paragraph_format.keep_with_next = True
ppr_border(st["Heading 1"].element.get_or_add_pPr(), {"bottom": (12, BASE, 4)})

# rodapé
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_runs(fp, "Roteiro de Estudos · 24/11 a 08/12/2026 · página ", color="777777", size=8.5)
for r in add_field(fp, "PAGE", "1"):
    r.font.size = Pt(8.5); r.font.color.rgb = RGBColor.from_string("777777")

W = 17.4  # largura útil em cm

# ------------------------------------------------------------------ título
t = doc.add_table(rows=1, cols=1)
table_borders(t, None); table_fixed(t)
c = t.rows[0].cells[0]
c.width = Cm(W)
cell_shade(c, BASE); cell_margins(c, 260, 260, 360, 360)
p = c.paragraphs[0]
add_runs(p, "ROTEIRO DE ESTUDOS", color="CFD8DC", size=10.5, bold=True)
p.paragraph_format.space_after = Pt(4)
p = c.add_paragraph()
add_runs(p, "Provas do 2º bimestre — 24/11 a 08/12", color="FFFFFF", size=22, bold=True)
p.paragraph_format.space_after = Pt(4)
p.paragraph_format.line_spacing = 1.0
total_all = sum(m for d in DAYS for (_, _, m) in d[2])
p = c.add_paragraph()
add_runs(p, f"15 dias · mínimo de 2h por dia · {fmt(total_all)} planejadas no total · começando hoje (terça, 24/11)",
         color="ECEFF1", size=11)
doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ------------------------------------------------------------------ provas e carga
p = doc.add_paragraph(style="Heading 1")
add_runs(p, "Visão geral")
sums = {k: 0 for k in D}
for d in DAYS:
    for (k, _, m) in d[2]:
        sums[k] += m
order = ["ML", "RD", "CG", "CP", "BD"]
exam_rows = [
    ("ML", "Segunda, 30/11", "6 dias", "Mais cálculos à mão (ganho, Perceptron, backprop, K-means). Peso alto."),
    ("RD", "Segunda, 30/11", "6 dias", "Prova fácil, objetiva e de pouco peso: estudo enxuto (guia resumido)."),
    ("CG", "Terça, 01/12", "7 dias", "Matrizes, câmera, pipeline e iluminação. Menor volume de conteúdo."),
    ("CP", "Quinta, 03/12", "9 dias", "Conceitual e de provas (HALT, L_D, reduções): precisa de tempo para refazer as demonstrações."),
    ("BD", "Terça, 08/12", "14 dias", "Contas de custo + otimização + serializabilidade. Maior folga: estudar por último."),
]
tb = doc.add_table(rows=1 + len(exam_rows), cols=5)
table_borders(tb, "CFD8DC", 4); table_fixed(tb); tb.alignment = WD_TABLE_ALIGNMENT.CENTER
widths = [3.6, 3.0, 2.0, 2.2, 6.6]
heads = ["Disciplina", "Prova", "Faltam", "Horas", "Observação"]
for j, h in enumerate(heads):
    cc = tb.rows[0].cells[j]; cc.width = Cm(widths[j]); cell_shade(cc, BASE); cell_margins(cc, 60, 60, 100, 100)
    add_runs(cc.paragraphs[0], h, bold=True, color="FFFFFF", size=9.5)
    cc.paragraphs[0].paragraph_format.space_after = Pt(0)
for i, (k, ex, falta, obs) in enumerate(exam_rows, 1):
    name, col = D[k]
    vals = [None, ex, falta, fmt(sums[k]), obs]
    for j in range(5):
        cc = tb.rows[i].cells[j]; cc.width = Cm(widths[j]); cell_margins(cc, 60, 60, 100, 100)
        cc.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if j == 0:
            cell_shade(cc, lighter(col, 0.85)); cell_borders(cc, {"left": (36, col)})
            add_runs(cc.paragraphs[0], name, bold=True, color=mix(col, "000000", 0.25), size=10)
        else:
            add_runs(cc.paragraphs[0], vals[j], size=9.5, bold=(j == 1))
        cc.paragraphs[0].paragraph_format.space_after = Pt(0)
        cc.paragraphs[0].paragraph_format.line_spacing = 1.05

doc.add_paragraph().paragraph_format.space_after = Pt(2)
p = doc.add_paragraph()
add_runs(p, "**Lógica do roteiro:** estudar na ordem das provas — ML primeiro (6 dias, conteúdo mais pesado), Redes enxuto no fim de semana (prova fácil), "
            "Computação Gráfica no domingo e na segunda, Computabilidade entre as provas de CG e a sua, e **BD por último**, com a maior folga de calendário. "
            "Como ML e Redes caem no mesmo dia, o sábado e o domingo têm blocos de Redes; a segunda-feira à tarde já volta para CG.", size=10)

# ------------------------------------------------------------------ calendário
p = doc.add_paragraph(style="Heading 1")
add_runs(p, "Calendário")
weeks = [
    [("23", None, True), ("24", 0, False), ("25", 1, False), ("26", 2, False), ("27", 3, False), ("28", 4, False), ("29", 5, False)],
    [("30", 6, False), ("01", 7, False), ("02", 8, False), ("03", 9, False), ("04", 10, False), ("05", 11, False), ("06", 12, False)],
    [("07", 13, False), ("08", 14, False), ("", None, True), ("", None, True), ("", None, True), ("", None, True), ("", None, True)],
]
cal = doc.add_table(rows=1 + len(weeks), cols=7)
table_borders(cal, "FFFFFF", 12); table_fixed(cal); cal.alignment = WD_TABLE_ALIGNMENT.CENTER
dn = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
cw = W / 7
for j in range(7):
    cc = cal.rows[0].cells[j]; cc.width = Cm(cw); cell_shade(cc, BASE); cell_margins(cc, 40, 40, 80, 80)
    pp = cc.paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER; pp.paragraph_format.space_after = Pt(0)
    add_runs(pp, dn[j], bold=True, color="FFFFFF", size=9)
for wi, wk in enumerate(weeks, 1):
    for j, (num, idx, blank) in enumerate(wk):
        cc = cal.rows[wi].cells[j]; cc.width = Cm(cw); cell_margins(cc, 50, 50, 70, 70)
        row = cal.rows[wi]
        if blank:
            cell_shade(cc, "ECEFF1")
            if num:
                add_runs(cc.paragraphs[0], num, color="90A4AE", size=9); cc.paragraphs[0].paragraph_format.space_after = Pt(0)
            continue
        day = DAYS[idx]
        mins = sum(m for _, _, m in day[2])
        cell_shade(cc, "FFEBEE" if day[4] else "F5F7F8")
        pp = cc.paragraphs[0]; pp.paragraph_format.space_after = Pt(1)
        add_runs(pp, num, bold=True, size=11, color=BASE)
        add_runs(pp, f"   {fmt(mins)}", size=8.5, color="607D8B")
        agg = {}
        for k, _, m in day[2]:
            agg[k] = agg.get(k, 0) + m
        for k, m in agg.items():
            q = cc.add_paragraph(); q.paragraph_format.space_after = Pt(0); q.paragraph_format.line_spacing = 1.0
            add_runs(q, "■ ", color=D[k][1], size=8.5)
            add_runs(q, f"{ABBR[k]} {fmt(m)}", size=8, color="37474F")
        if day[4]:
            q = cc.add_paragraph(); q.paragraph_format.space_before = Pt(2); q.paragraph_format.space_after = Pt(0)
            who = {"30/11": "ML + REDES", "01/12": "CG", "03/12": "COMPUT.", "08/12": "BD"}[day[1]]
            add_runs(q, "PROVA " + who, bold=True, size=8, color="C62828")
        cc.paragraphs[0].paragraph_format.keep_with_next = True
        row_flags(row, cant_split=True)

# ------------------------------------------------------------------ dia a dia
p = doc.add_paragraph(style="Heading 1")
p.paragraph_format.page_break_before = True
add_runs(p, "Dia a dia")
p = doc.add_paragraph()
add_runs(p, "Cada bloco indica a **seção do guia** correspondente e o tempo sugerido. Dentro de cada bloco: leia a seção (≈ 30 %), faça os exercícios **sem olhar o gabarito** (≈ 50 %) "
            "e confira/anote os erros (≈ 20 %). Blocos marcados **ANTES DA PROVA** devem ser feitos antes do horário da prova; ajuste se o horário real for diferente.", size=9.5, color="455A64")
dt = doc.add_table(rows=len(DAYS), cols=3)
table_borders(dt, "CFD8DC", 4); table_fixed(dt); dt.alignment = WD_TABLE_ALIGNMENT.CENTER
cws = [2.6, 10.4, 4.4]
for i, (wd, dt_, tasks, goal, exam) in enumerate(DAYS):
    row = dt.rows[i]
    row_flags(row, cant_split=True)
    mins = sum(m for _, _, m in tasks)
    a, b, c3 = row.cells
    for cc, w in zip((a, b, c3), cws):
        cc.width = Cm(w); cell_margins(cc, 70, 70, 100, 100); cc.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    fill = "FFEBEE" if exam else ("F5F7F8" if i % 2 == 0 else "FFFFFF")
    for cc in (a, b, c3):
        cell_shade(cc, fill)
    cell_borders(a, {"left": (36, "C62828" if exam else BASE), "top": (4, "CFD8DC"), "bottom": (4, "CFD8DC"), "right": (4, "CFD8DC")})
    pa = a.paragraphs[0]; pa.paragraph_format.space_after = Pt(0)
    add_runs(pa, dt_, bold=True, size=16, color=BASE)
    q = a.add_paragraph(); q.paragraph_format.space_after = Pt(2)
    add_runs(q, wd, size=9.5, color="607D8B")
    q = a.add_paragraph(); q.paragraph_format.space_after = Pt(0)
    add_runs(q, fmt(mins), bold=True, size=11, color="37474F")
    first = True
    if exam:
        pp = b.paragraphs[0]; first = False
        pp.paragraph_format.space_after = Pt(3)
        add_runs(pp, "🎯 " + exam, bold=True, size=10.5, color="C62828")
    for (k, txt, m) in tasks:
        pp = b.paragraphs[0] if first else b.add_paragraph()
        first = False
        pp.paragraph_format.space_after = Pt(3)
        pp.paragraph_format.left_indent = Cm(0.45)
        pp.paragraph_format.first_line_indent = Cm(-0.45)
        add_runs(pp, "■ ", color=D[k][1], size=10)
        add_runs(pp, txt, size=9.5)
        add_runs(pp, f"  ({fmt(m)})", size=9, color="78909C", bold=True)
    pg = c3.paragraphs[0]; pg.paragraph_format.space_after = Pt(2)
    add_runs(pg, "META DO DIA", size=7.5, bold=True, color="78909C")
    q = c3.add_paragraph(); q.paragraph_format.space_after = Pt(0)
    add_runs(q, goal, size=9, color="37474F")

# ------------------------------------------------------------------ método e plano B
p = doc.add_paragraph(style="Heading 1")
p.paragraph_format.page_break_before = True
add_runs(p, "Como estudar cada bloco")
steps = [
    ("1. Leia ativamente (≈ 30 %)", "Leia a seção do guia e grife só as caixas **Lembrete para a prova** e **Erro comum**. Não copie texto: se precisar anotar, anote fórmulas e pegadinhas."),
    ("2. Exercícios sem olhar (≈ 50 %)", "Resolva os exercícios de revisão **no papel**, antes de abrir o gabarito comentado. É aqui que a matéria fixa. Nas contas (ganho, custo de junção, matrizes), refaça até acertar sem consultar."),
    ("3. Caderno de erros (≈ 20 %)", "Para cada erro, escreva **a causa** (fórmula errada? sinal? direção da redução?). Revise esse caderno todo dia nos primeiros 10 min e na véspera de cada prova."),
]
for h, t_ in steps:
    tbx = doc.add_table(rows=1, cols=1); table_borders(tbx, None); table_fixed(tbx)
    cc = tbx.rows[0].cells[0]; cc.width = Cm(W); cell_shade(cc, "ECEFF1"); cell_borders(cc, {"left": (36, BASE)}); cell_margins(cc, 90, 90, 180, 140)
    add_runs(cc.paragraphs[0], h, bold=True, color=BASE, size=11)
    cc.paragraphs[0].paragraph_format.space_after = Pt(2)
    q = cc.add_paragraph(); q.paragraph_format.space_after = Pt(0)
    add_runs(q, t_, size=10)
    gap(doc, 4)
p = doc.add_paragraph()
add_runs(p, "**Ritmo:** blocos de 50 min + 10 min de pausa; água e movimento nas pausas; durma pelo menos 7 h nas vésperas de prova. "
            "Nas vésperas, **não aprenda matéria nova**: só cola, caderno de erros e mini-simulado.", size=10)

p = doc.add_paragraph(style="Heading 1")
add_runs(p, "“Estou pronto” quando você consegue…")
ready = {
    "ML": ["calcular entropia, ganho, razão de ganho e o melhor limiar contínuo; decidir uma poda;",
           "simular épocas do Perceptron; fazer forward e um passo de backprop (δ⁽²⁾, δ⁽¹⁾); ajustar uma reta e fazer K-means à mão."],
    "RD": ["dizer em qual camada atua cada equipamento/protocolo; números do quadro Ethernet; calcular máscara/sub-redes;",
           "TCP × UDP e portas; FCAPS, SLA e SNMP; CIA e principais ataques/defesas."],
    "CG": ["aplicar T, E, R e rotação em torno de pivô na ordem certa; ler um .obj;",
           "projeção em perspectiva; n, u, v da câmera; ordem do pipeline; Lambert e especular; flat × smooth."],
    "CP": ["definir MT e rastrear exemplos; classificar linguagens (recursiva/RE/não-RE);",
           "reproduzir as provas de HALT e L_D; fazer uma redução por mapeamento na **direção certa**."],
    "BD": ["calcular custos de ordenação, seleção e junção e escolher o melhor algoritmo; otimizar uma consulta aplicando R1–R10;",
           "ACID, problemas de concorrência, grafo de precedência e níveis de isolamento."],
}
for k in order:
    name, col = D[k]
    tbx = doc.add_table(rows=1, cols=2); table_borders(tbx, None); table_fixed(tbx)
    a, b = tbx.rows[0].cells
    a.width, b.width = Cm(3.4), Cm(W - 3.4)
    cell_shade(a, col); cell_shade(b, lighter(col, 0.93)); cell_margins(a, 80, 80, 120, 100); cell_margins(b, 80, 80, 140, 120)
    add_runs(a.paragraphs[0], name, bold=True, color="FFFFFF", size=10); a.paragraphs[0].paragraph_format.space_after = Pt(0)
    a.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for n, line in enumerate(ready[k]):
        q = b.paragraphs[0] if n == 0 else b.add_paragraph()
        q.paragraph_format.space_after = Pt(1)
        add_runs(q, "✔ " + line, size=9.5)
    gap(doc, 4)

p = doc.add_paragraph(style="Heading 1")
add_runs(p, "Se o tempo apertar (plano B)")
B = [
    "**Atrasou um dia?** Corte primeiro o que é de menor peso: Redes §7–§8 (gerência e segurança) e exercícios extras de CG §2 (.obj). Nunca corte a revisão ativa de ML nem as demonstrações de Computabilidade.",
    "**Prioridade dentro de cada guia:** caixas “Lembrete para a prova”, exercícios de revisão e Cola. As caixas “Além dos slides” são opcionais.",
    "**Sobrou tempo?** Refaça o mini-simulado de cada guia cronometrado (1h) e releia o caderno de erros.",
    "**Horário das provas diferente?** Mantenha a ordem dos blocos e mova só os marcados ANTES DA PROVA para a noite anterior.",
]
for line in B:
    q = doc.add_paragraph(); q.paragraph_format.left_indent = Cm(0.5); q.paragraph_format.first_line_indent = Cm(-0.4)
    q.paragraph_format.space_after = Pt(3)
    add_runs(q, "• " + line, size=10)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Roteiro_de_Estudos.docx")
doc.save(out)
print(os.path.abspath(out), "total", fmt(total_all), {k: fmt(v) for k, v in sums.items()})
for d in DAYS:
    mm = sum(m for _, _, m in d[2])
    assert mm >= 120, (d[1], mm)
