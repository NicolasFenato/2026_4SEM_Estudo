# -*- coding: utf-8 -*-
from guide_builder import *

COLOR = "2E7D32"  # verde
TITLE = "Banco de Dados"
PROF = "Prof. Daniel S. Kaster · Departamento de Computação · UEL"
EXAM = "08/12/2026"
SOURCES = "Slides BD 06–08 (Algoritmos de processamento de consultas · Otimização de consultas · Transações: conceitos e teoria)"
TOPICS = ["Ordenação, seleção, junção, projeção, agregação", "Otimização de consultas", "Transações e ACID", "Problemas de concorrência", "Escalonamentos e serializabilidade"]
NOTE = "Os custos medem blocos de disco acessados (como nos slides). O slide 08 é em inglês (Elmasri & Navathe); aqui os termos aparecem em português com o original entre parênteses."

C = []

# =====================================================================
# 0. MAPA
# =====================================================================
C += [
    H1("Visão geral: do SQL ao disco, e do disco à consistência", numbered=False,
       intro="A disciplina responde a duas perguntas: como o SGBD executa uma consulta rápido? e como ele mantém os dados corretos com vários usuários ao mesmo tempo?"),
    T(["Parte", "Pergunta", "Ideia-chave", "Slide"],
      [["**Processamento de consultas**", "Que algoritmo executa cada operação (seleção, junção…) e quanto custa?", "Custo = **nº de blocos de disco** acessados", "06"],
       ["**Otimização de consultas**", "Entre as várias formas equivalentes de executar, qual escolher?", "Reescrita algébrica (regras) + estimativa de custo (estatísticas do catálogo)", "07"],
       ["**Transações**", "Como garantir que várias operações valham “tudo ou nada” e que usuários concorrentes não se atrapalhem?", "**ACID**, escalonamentos, **serializabilidade**", "08"]],
      widths=[3.6, 6.4, 5.4, 1.6], size=9.5),
    P("Fluxo de uma consulta no SGBD (visão completa dos slides): **Consulta em linguagem de alto nível → INTERPRETADOR** (leitura, parsing e validação) **→ OTIMIZADOR** (reescrita de consultas/algoritmos) "
      "**→ GERADOR DE CÓDIGO** (escolhe os algoritmos) **→ EXECUTOR → resultado**; e tudo sob o **processamento de transações**."),
    BOX("lembrete", "Como a prova costuma cobrar", [
        "- **Contas de custo** (blocos): ordenação externa, seleção (sequencial × binária × índice), junção (laços aninhados, índice, sort-merge, hash).",
        "- **Otimização**: aplicar as regras para montar a árvore otimizada; justificar a escolha de algoritmos com estatísticas.",
        "- **Transações**: decorar ACID; reconhecer problemas de concorrência; **testar serializabilidade** (grafo de precedência); níveis de isolamento.",
    ]),
]

# =====================================================================
# 1. ORDENAÇÃO
# =====================================================================
C += [
    H1("Processamento de consultas e ordenação",
       "Slide 06 (parte 1) · A base de custo e o algoritmo que mais aparece por baixo dos panos: a ordenação."),
    H2("Algoritmos e modelo de custo"),
    P("O gerador de código dispõe de algoritmos para cada operação: **ordenação, seleção, junção, projeção, operações de conjuntos e funções de agregação**. "
      "Em todos os slides, **o custo é o número de blocos (páginas) lidos/escritos no disco**, supondo que os dados são lidos do disco e que o resultado é materializado em disco (o processamento em memória é considerado desprezível)."),
    BOX("def", "Símbolos usados nas fórmulas (catálogo do SGBD)", [
        T(["Símbolo", "Significado"],
          [["**r**", "número de registros (tuplas) da relação"], ["**b**", "número de blocos da relação"], ["**Bfr** (bfr = B/R)", "fator de bloco: registros por bloco"],
           ["**x**", "número de níveis de um índice"], ["**b_leaf**", "blocos do nível folha (base) do índice"],
           ["**s**", "cardinalidade da seleção: nº de registros que satisfazem a condição (chave: s = 1)"], ["**sl** = s / r", "seletividade (chave: sl = 1/r)"],
           ["**b_buffer**", "blocos de buffer disponíveis em memória"]],
          widths=[3.6, 11], size=9.5),
    ]),
    BOX("lembrete", None, ["**b = ⌈ r / Bfr ⌉** (arredonde para cima). Ex.: 10.000 registros com Bfr = 5 ⇒ b = 2.000 blocos."]),
    H2("Ordenação: em memória × externa"),
    P("Ordenar é fundamental: **ORDER BY**, **junções** (sort-merge), **eliminação de duplicados** (DISTINCT, UNION…), agrupamentos. "
      "Se o arquivo **cabe na memória**, usa-se ordenação convencional (ex.: Quick Sort); se **não cabe**, usa-se **ordenação externa**, derivada do **merge sort**."),
    BOX("def", "Ordenação em memória", [
        "Lê todas as páginas, ordena no buffer. **Custo: C = b** (a ordenação na memória é irrelevante frente ao I/O).",
    ]),
    BOX("def", "Ordenação externa (sort-merge externo), com b_buffer blocos de memória", [
        "**1) Fase de ordenação (sorting):** enquanto não fim de arquivo, leia os próximos **b_buffer** blocos, ordene-os (como uma “parte”/*run*) e reescreva em outra área do disco.",
        "**2) Fase de intercalação (merge):** enquanto não ordenado, tome **b_buffer − 1** partes ordenadas, mescle-as usando 1 bloco do buffer para a saída e as demais para ler as partes, gravando o resultado.",
        "= C_{OrdExt} = 2 · ( b + b · log_{gm}(nr) )",
        "- **gm = b_buffer − 1**: **grau de merge** (quantas partes são mescladas por vez).",
        "- **nr = b / b_buffer**: número de partes ordenadas geradas no primeiro passo.",
        "- O termo b · log_{gm}(nr) = leituras/escritas dos **passes de merge**; o fator 2 conta **leitura + escrita**.",
    ]),
    BOX("exemplo", "Quantos passes? (b = 1.000 blocos, b_buffer = 11)", [
        "- Fase 1: partes de 11 blocos ⇒ **nr = ⌈1000/11⌉ = 91 partes**.",
        "- **gm = 10**. Passes de merge: ⌈log₁₀ 91⌉ = **2** (10¹ = 10 < 91 ≤ 10² = 100).",
        "- Custo = 2·(1000 + 1000·2) = **6.000 blocos** (com log real: 2·(1000 + 1000·1,96) ≈ 5.918). Em provas, siga a fórmula do enunciado; arredondar o nº de passes para cima é o que acontece na prática.",
    ]),
    BOX("insight", "Por que o custo cresce “quase” linearmente em b", [
        "O número de passes é **logarítmico** e, com bastante buffer, é 1 ou 2. Ordenar uma tabela gigante custa **poucas leituras completas** da tabela. Mais memória (b_buffer maior) ⇒ menos partes e **maior grau de merge** ⇒ menos passes.",
    ]),
    BOX("erro", None, [
        "- Esquecer que o **buffer inteiro** (b_buffer blocos) é usado na fase 1, mas na fase 2 um bloco vai para a **saída** (gm = b_buffer − 1).",
        "- Esquecer o fator **2** (leitura + escrita).",
        "- Confundir **nr** (nº de partes) com o nº de passes: os passes são o **logaritmo** de nr na base gm.",
    ]),
    BOX("resumo", None, [
        "- Custo em **blocos de disco**; b = ⌈r/Bfr⌉.",
        "- Ordenação em memória: b. Externa: **2·(b + b·log_{gm} nr)**, gm = b_buffer − 1, nr = b/b_buffer.",
    ]),
    EX([
        Q("Uma tabela tem 12.000 registros e Bfr = 20. Quantos blocos ocupa? Se couber em um buffer de 700 blocos, qual o custo da ordenação?",
          ["b = ⌈12000/20⌉ = **600 blocos**. Cabe no buffer (700 ≥ 600) ⇒ ordenação **em memória**: custo **= b = 600** blocos."]),
        Q("Uma relação de 1.000 blocos é ordenada externamente com 11 blocos de buffer. Calcule nr, gm e o custo.",
          ["nr = ⌈1000/11⌉ = 91; gm = 10; passes = ⌈log₁₀ 91⌉ = 2.",
           "C = 2 · (1000 + 1000 · 2) = **6.000 blocos**."]),
        Q("Por que o custo de ordenação externa diminui quando aumentamos o buffer?",
          "Com mais blocos de buffer, a fase 1 gera **menos partes (nr = b/b_buffer menor)** e o **grau de merge gm = b_buffer − 1 é maior**, o que reduz o número de passes de merge log_{gm}(nr) — logo, menos leituras/escritas."),
        Q("V ou F: (a) a ordenação externa deriva do merge sort; (b) se a relação cabe na memória, o custo de ordenar é b; (c) o grau de merge é igual ao tamanho do buffer.",
          "(a) **V**. (b) **V**. (c) **F** — gm = b_buffer − 1 (um bloco é reservado à saída)."),
    ]),
]

# =====================================================================
# 2. SELEÇÃO
# =====================================================================
C += [
    H1("Algoritmos de seleção",
       "Slide 06 (parte 2) · σ: filtrar tuplas. Pode reduzir muito o acesso a disco — se bem escolhido o algoritmo."),
    H2("Seletividade e estatísticas"),
    BOX("def", "Conceitos", [
        "- **s** (cardinalidade da seleção): nº de tuplas que satisfazem a condição.   - **sl = s / r** (seletividade): **fração** das tuplas que satisfazem. (Alguns autores definem sl = 1 − s/r: atenção ao enunciado.)",
        "- Estatísticas são guardadas **por atributo** no catálogo; exigem espaço, **manutenção periódica** (varreduras agendadas) e são consultadas na otimização.",
    ]),
    T(["Tipo de estatística", "Como estima s", "Prós / contras"],
      [["**Homogênea (uniforme)**", "**s = r / d** (d = nº de valores distintos). Para numéricos discretos: 1/(maior − menor). Intervalos: proporção da faixa", "Guarda poucos valores (distintos, mín, máx); fácil de manter; **estimativa em geral ruim** se a distribuição não for uniforme"],
       ["**Histograma**", "Conta quantas tuplas caem em cada “bin” (faixa)", "**Mais preciso**; usa mais espaço. Variações: **igual espaçamento** (equi-width) e **igual densidade** (agrupa bins de valores próximos)"],
       ["**Função de distribuição**", "Gaussiana, Poisson, χ²…; igualdade = valor da função; intervalo = **integral** (área sob a curva)", "Obtida por histograma + **curve fitting**"]],
      widths=[3.6, 7, 6.4], size=9),
    H2("Algoritmos de seleção e seus custos"),
    T(["Algoritmo", "Quando usar", "Custo (blocos)"],
      [["**S_{Seq}** — busca sequencial (*full table scan*)", "**Sempre** pode ser usada (só precisa do arquivo)", "**C = b**"],
       ["**S_{B.Bin}** — busca binária", "Arquivo **ordenado** pelo atributo da condição", "**C = log₂ b + s/Bfr − 1**"],
       ["**S_{Index_Clust}** — índice **clustering/primário** (B⁺)", "Existe índice clustering/primário no atributo (a relação está **ordenada** por ele)", "**C = x + s/Bfr**"],
       ["**S_{Index_Sec}** — índice **secundário** (B⁺)", "Existe índice secundário no atributo (relação **não** ordenada por ele)", "**C = x + b_leaf · (s/r) − 1 + s**"]],
      widths=[5.4, 6.8, 4.8], size=9.5),
    BOX("insight", "Lendo cada fórmula", [
        "- **Binária:** log₂ b acessos para achar o 1º bloco + os blocos adicionais com as s tuplas (**s/Bfr − 1**). Beneficia-se do **fator de bloco** porque tuplas consecutivas estão no mesmo bloco.",
        "- **Clustering:** x acessos descendo o índice + **s/Bfr blocos** de dados contíguos (a relação está ordenada pelo atributo).",
        "- **Secundário:** x níveis + folhas percorridas (b_leaf·s/r) − 1 + **até s acessos “aleatórios”** (cada tupla pode estar em um bloco diferente!). Por isso é bom só para **poucas tuplas**. "
        "Os **rids** recuperados no índice devem ser **ordenados** antes de acessar os blocos, para evitar acessos repetidos/desnecessários.",
    ]),
    BOX("lembrete", "Regra prática de decisão", [
        "Índice **secundário só vale a pena** quando a seleção é **bem seletiva** (poucas tuplas). Se s é grande (ex.: 90 % da tabela), **a varredura sequencial** (custo b) costuma ganhar do índice (custo ≈ s).",
    ]),
    H2("Condições conjuntivas e disjuntivas"),
    T(["Condição", "Estratégias"],
      [["**Conjuntiva (AND)**", "• **Varredura sequencial** (sempre possível).\n• **Um índice simples**: use o índice de **um** atributo da condição, recupere as tuplas e teste as outras condições **em memória** (sem custo de disco). C = custo do índice escolhido (com o s desse atributo).\n• **Índice composto**: transforma a conjunção em **chave de busca composta**. C = custo do índice composto (com s_conj).\n• **Interseção de ponteiros (rids)**: busca em **cada** índice (para na folha), **interseciona** os conjuntos de rids e só então acessa as tuplas: C = custo_índ₁ + custo_índ₂ + s_conj.".split("\n")],
       ["**Disjuntiva (OR)**", "Normalmente **varredura sequencial** (qualquer condição verdadeira inclui a tupla). Só se houver índice em **TODOS** os atributos da expressão: **união de ponteiros** (busca em cada índice, une os rids, acessa os dados): C = custo_índ₁ + … + custo_índₙ + s_disj."]],
      widths=[3.2, 13.8], size=9),
    BOX("exemplo", "Exemplo do slide: relação empregado", [
        "**Estatísticas:** r = 10.000, b = 2.000, Bfr = 5. Índice clustering em salário (x = 3, s = 20). Secundário em CPF (x = 4, s = 1). Secundário em dnum (x = 2, b_leaf = 4, d = 125 valores distintos). Secundário em sexo (x = 1, d = 2).",
        "- **s_dnum** = r/d = 10000/125 = **80**.  **s_sexo** = 10000/2 = **5.000**.",
        "- **Op1: CPF = ‘123456789’** → s = 1: Índice secundário: ≈ x + 1 = **~5 blocos** (vs 2.000 da sequencial).",
        "- **Op2: dnum = 5** → s = 80: C_{Index_Sec} = 2 + 4·(80/10000) − 1 + 80 ≈ **81** blocos (vs 2.000): índice ganha.",
        "- **Op3: dnum > 5** → quase todas as tuplas (≈ 9.600 se uniforme): índice custaria ≈ **9.600 blocos** > 2.000 ⇒ **varredura sequencial** é melhor!",
        "- **Op4: dnum = 5 AND salario > 3000 AND sexo = ‘f’:** alternativas: sequencial (2.000); índice simples em **dnum** (≈ 81), em **salário** (clustering) ou em **sexo** (≈ 5.000 — péssimo); ou **interseção de rids** dos três índices. O melhor, em geral, é usar o índice **mais seletivo** (dnum) e testar o resto em memória.",
    ]),
    BOX("erro", None, [
        "- Usar índice secundário para condição **pouco seletiva** (intervalos grandes, atributos com poucos valores, como sexo).",
        "- Esquecer que **busca binária** exige a relação **ordenada** pelo atributo da condição.",
        "- Aplicar **união de ponteiros** quando falta índice em algum atributo do OR (então é sequencial).",
        "- Calcular s para **desigualdade** com s = r/d (isso é para **igualdade**).",
    ]),
    BOX("resumo", None, [
        "- Sequencial: b · Binária: log₂b + s/Bfr − 1 · Clustering: x + s/Bfr · Secundário: x + b_leaf·s/r − 1 + s.",
        "- AND: um índice + filtro em memória, índice composto ou interseção de rids. OR: sequencial, ou união de rids se **todos** têm índice.",
    ]),
    EX([
        Q("Relação com r = 10.000, b = 2.000, Bfr = 5, ordenada por idade, com 20 tuplas em idade = 20. Estime o custo de: (a) sequencial; (b) busca binária; (c) índice clustering com x = 3.",
          ["(a) **2.000**.",
           "(b) ⌈log₂ 2000⌉ + s/Bfr − 1 = 11 + 20/5 − 1 = **14**.",
           "(c) x + s/Bfr = 3 + 4 = **7**."]),
        Q("Um atributo categórico tem 50 valores distintos em uma tabela de 10.000 tuplas (distribuição uniforme). Estime s e sl para uma igualdade.",
          "s = r/d = 10000/50 = **200**; sl = s/r = 200/10000 = **0,02 (2 %)**."),
        Q("Por que o índice secundário pode ser pior que a varredura sequencial quando a seleção devolve metade da relação?",
          "O custo do secundário tem a parcela **+ s**: cada uma das s tuplas pode exigir **um acesso a bloco diferente** (acesso aleatório). Se s ≈ r/2 > b, o custo passa do custo b da varredura sequencial, que lê cada bloco uma só vez."),
        Q("Explique a seleção conjuntiva por **interseção de ponteiros**.",
          "Para cada condição que tem índice, faz-se a busca **apenas no índice** (até a folha), obtendo o conjunto de **rids** que a satisfazem; **interseciona-se** os conjuntos; os rids que estão em todos satisfazem a conjunção e só então os **blocos de dados** são lidos. Custo ≈ custo dos índices + s_conj."),
        Q("V ou F: (a) a busca sequencial só funciona se houver índice; (b) a disjunção normalmente usa varredura sequencial; (c) o histograma costuma ser mais preciso que a estatística uniforme.",
          "(a) **F** — é sempre possível. (b) **V**. (c) **V**."),
    ]),
]

# =====================================================================
# 3. JUNÇÃO
# =====================================================================
C += [
    H1("Algoritmos de junção",
       "Slide 06 (parte 3) · A operação mais custosa e mais frequente. Os quatro algoritmos e como comparar custos."),
    P("Tomamos a **equijoin** como exemplo (theta-joins e junções externas reaproveitam os algoritmos). A relação resultante tem tuplas que são a **concatenação** das de entrada (afeta o fator de bloco). "
      "Em junção **PK–FK**, a cardinalidade do resultado é **≤ a da relação do lado da FK** (igual se a FK não admitir nulos)."),
    T(["Sigla", "Algoritmo", "Ideia"],
      [["**J_{NL}**", "Laços aninhados (nested-loop)", "Itera as duas relações comparando"],
       ["**J_{Index}**", "Baseada em índice", "Para cada tupla da externa, busca no **índice** da interna"],
       ["**J_{SM}**", "Ordenação e intercalação (sort-merge)", "Ordena por atributos de junção e **intercala**"],
       ["**J_{Hash}**", "Baseada em hashing (hash join)", "Particiona por **função de hash** e junta buckets correspondentes"]],
      widths=[2.4, 6, 8.6], size=9.5),
    H2("Junção por laços aninhados (três variantes)"),
    T(["Variante", "Descrição", "Custo"],
      [["**Tupla-a-tupla**", "Para cada tupla r de R (externa), para cada tupla s de S (interna), testa", "r_outer · r_inner  (ou **b_outer + r_outer · b_inner** com cache de blocos)"],
       ["**Por blocos (v1)**", "Para cada **bloco** de R, para cada **bloco** de S, compara as tuplas dos dois blocos", "**b_outer + b_outer · b_inner**"],
       ["**Por blocos com buffer (v2)**", "Carrega **b_buffer − 2** blocos da externa na memória (numa estrutura de busca pelo atributo de junção); para cada bloco da interna, encontra os pares", "**b_outer + ⌈ b_outer / (b_buffer − 2) ⌉ · b_inner**"]],
      widths=[3.4, 8, 5.6], size=9),
    BOX("insight", "Escolha da relação externa e do buffer (slide: “Desempenho de JNL”)", [
        "- Com 1 bloco para a externa: b_R + b_R · b_S. Com (b_buffer − 2) blocos: b_R + ⌈b_R/(b_buffer − 2)⌉ · b_S.",
        "- A **menor** relação deve ser a **externa** (o termo multiplicativo é b_outer / (b_buffer − 2) × b_inner: quanto menor a externa, menos vezes se varre a interna). Se a **menor couber inteira** no buffer, o custo cai para **b_outer + b_inner**.",
    ]),
    H2("Junção baseada em índice"),
    P("Se existe índice no atributo de junção de **uma** das relações (a interna), para cada tupla da externa busca-se, **no índice**, as tuplas que casam. **C = b_outer + r_outer · custo_índice_inner**. "
      "É excelente quando a externa é pequena e o índice tem alta seletividade (ex.: chave primária)."),
    H2("Junção por ordenação e intercalação (sort-merge)"),
    B(["**Fase 1:** ordene R e S pelos atributos de junção **(se necessário)**.",
       "**Fase 2:** percorra as duas relações **uma única vez**, intercalando: se r < s avança r; se r > s avança s; se iguais, produz os pares (atenção a **valores repetidos**: reutiliza-se o grupo de S).",
       "**C = b_R + b_S** (+ custo das ordenações, se necessário). Se as relações **já estão ordenadas** pelo atributo (ou o índice clustering entrega a ordem), é muito barato."]),
    H2("Junção por hashing (hash join)"),
    B(["**Fase 1:** aplique a **mesma função de hash h** ao atributo de junção de **todas** as tuplas de R e de S, gravando-as em **buckets** (áreas) HR e HS. Chaves iguais caem no **mesmo bucket**.",
       "**Fase 2:** para cada **par de buckets correspondentes**, execute uma junção (laços aninhados) entre as tuplas dos dois buckets.",
       "**C = custo_hashing + custo_nested_loop_joins**, com **custo_hashing = 2·(b_R + b_S)** (ler e escrever os buckets). Se cada par de buckets cabe em memória, a fase 2 custa ≈ b_R + b_S (cada bloco é lido de novo uma vez)."]),
    BOX("def", "Qual usar? (regras de bolso)", [
        "- **Laços aninhados**: serve para **qualquer condição** (inclui theta-joins) e quando uma relação é **pequena** (cabe no buffer).",
        "- **Índice**: externa pequena + **índice na interna** (principalmente na chave).",
        "- **Sort-merge**: já ordenadas, ou quando o **resultado precisa vir ordenado**; só equijoin.",
        "- **Hash**: equijoin com relações grandes e sem índice/ordem.",
    ]),
    BOX("exemplo", "Exemplo do slide: empregado ⨝ departamento (CPF = CPFger)", [
        "**Dados:** b_buffer = 7; departamento: r = 50, **b = 10**; empregado: r = 6.000, **b = 2.000**; empregado tem índice secundário em CPF (x = 4); departamento tem índice secundário em CPFger (x = 2).",
        T(["Algoritmo", "Conta", "Custo (blocos)"],
          [["NL por blocos v1, **dep** externa", "10 + 10·2000", "**20.010**"],
           ["NL por blocos v1, **emp** externa", "2000 + 2000·10", "22.000"],
           ["NL com buffer v2, **dep** externa", "10 + ⌈10/5⌉·2000", "**4.010**"],
           ["NL com buffer v2, emp externa", "2000 + ⌈2000/5⌉·10", "6.000"],
           ["**Índice**, dep externa (índice em emp.CPF: ≈ x + 1 = 5)", "10 + 50·5", "**260** ← melhor"],
           ["Índice, emp externa (índice em dep: x + 1 = 3)", "2000 + 6000·3", "20.000"],
           ["Sort-merge (sem contar ordenações)", "10 + 2000", "2.010 (+ ordenar emp ≈ 20.000 com buffer 7)"],
           ["Hash", "2·(10 + 2000) + ≈ (10 + 2000)", "≈ 6.030"]],
          widths=[7, 5, 5], align=["l", "c", "c"], size=9),
        "**Lições:** (1) a **externa menor** vence; (2) **mais buffer** ajuda (20.010 → 4.010); (3) com índice na chave e externa pequena, a junção por índice é imbatível (260); (4) sort-merge **depende** de já estar ordenado.",
    ]),
    BOX("erro", None, [
        "- Escolher a relação **grande** como externa nos laços aninhados.",
        "- Esquecer de **somar a ordenação** no sort-merge quando as relações não estão ordenadas.",
        "- Usar hash join/sort-merge para **theta-join** (desigualdades): só servem para equijoin.",
        "- Esquecer o termo **b_outer** (leitura da externa) nas fórmulas de laços aninhados e de índice.",
        "- No v2 usar b_buffer em vez de **b_buffer − 2** (um bloco para a interna e um para a saída).",
    ]),
    BOX("resumo", None, [
        "- NL v1: b_o + b_o·b_i · NL v2: b_o + ⌈b_o/(b_buf−2)⌉·b_i · Índice: b_o + r_o·custo_índice · SM: b_R + b_S (+ordenação) · Hash: 2(b_R+b_S) + junção dos buckets.",
    ]),
    EX([
        Q("R tem 100 blocos e S tem 400 blocos. Calcule o custo do NL por blocos v1 com R externa e com S externa. Com buffer de 12 blocos (v2), idem.",
          ["v1: R externa: 100 + 100·400 = **40.100**; S externa: 400 + 400·100 = **40.400**.",
           "v2 (b_buffer − 2 = 10): R externa: 100 + ⌈100/10⌉·400 = **4.100**; S externa: 400 + ⌈400/10⌉·100 = **4.400**. Melhor: R (menor) como externa."]),
        Q("Em que situação o sort-merge join custa só b_R + b_S?",
          "Quando **as duas relações já estão ordenadas** pelos atributos de junção (ou uma estrutura como índice clustering entrega essa ordem), pois só resta a fase de intercalação, que lê cada bloco **uma vez**."),
        Q("Descreva as duas fases do hash join e o custo da primeira.",
          "**Fase 1:** a mesma função de hash é aplicada ao atributo de junção de todas as tuplas de R e S, gravando-as em buckets (tuplas com chaves iguais vão para o mesmo bucket). **Fase 2:** para cada par de buckets correspondentes, junta-se (laços aninhados). Custo do hashing = **2·(b_R + b_S)** (ler + escrever)."),
        Q("Dados A (20 blocos, r_A = 500) e B (5.000 blocos) com índice na chave de B (x = 3, busca por chave ≈ x + 1 = 4). Estime a junção por índice com A externa.",
          "C = b_A + r_A · custo_índice = 20 + 500·4 = **2.020 blocos** (versus 20 + ⌈20/5⌉·5000 = 20.020 com NL v2 e buffer 7: o índice é 10× melhor)."),
        Q("V ou F: (a) a junção por laços aninhados funciona com qualquer condição; (b) o hash join serve para theta-joins; (c) quanto menor a externa no NL por blocos, menor o custo.",
          "(a) **V**. (b) **F** — só equijoin. (c) **V**."),
    ]),
]

# =====================================================================
# 4. PROJEÇÃO, CONJUNTOS, AGREGAÇÃO
# =====================================================================
C += [
    H1("Projeção, eliminação de duplicados, operações de conjuntos e agregação",
       "Slide 06 (parte 4) · Os demais operadores da álgebra relacional."),
    H2("Eliminação de duplicados"),
    P("Usada no **DISTINCT** e em operações de conjunto que eliminam duplicados (**UNION, INTERSECT, EXCEPT**). Algoritmo clássico: **ordena** as tuplas e percorre, inserindo no resultado só as distintas. "
      "**C_{Elim_Dupl} = custo_ordenação + b**."),
    H2("Projeção (π)"),
    T(["Variação", "Característica", "Custo"],
      [["**Bag-based** (multiconjunto)", "**Não** elimina duplicados — coerente com a **SQL**", "**C = b**"],
       ["**Set-based** (conjunto)", "Elimina duplicados — coerente com o **modelo relacional**", "**C = b + (custo_ordenação(b′) + b′)**, b′ = nº de blocos após projetar"]],
      widths=[3.6, 7.4, 6], size=9.5),
    BOX("insight", "Atalho da projeção set-based", [
        "Se a projeção **inclui uma chave candidata** da relação de entrada, **não pode haver duplicados** ⇒ **pula-se a eliminação** e o custo é só b.",
    ]),
    H2("Operações de conjuntos"),
    B(["**Produto cartesiano**: laços aninhados.",
       "**União, interseção, diferença**: algoritmos **semelhantes ao sort-merge join** (ordenar e intercalar). Se tratadas como **conjunto (set-based)**, exigem eliminação de duplicados; se como **multiconjunto (bag-based)**, mantêm duplicados."]),
    H2("Funções de agregação"),
    T(["Algoritmo", "Descrição", "Custo"],
      [["**F_{Seq}** — varredura sequencial", "Percorre todas as tuplas (count, sum, avg, min, max)", "**b**"],
       ["**F_{Index}** — só pelo índice", "Quando o índice no atributo basta: **min/max** = folha mais à esquerda/direita; **count/avg/sum** com índice **denso** (fast-full scan das folhas)", "min/max: **x** (denso) ou **x + 1** (esparso); count/avg/sum: **b_leaf**"]],
      widths=[4.2, 8.4, 4.4], size=9.5),
    P("A agregação **indexada é rara**: normalmente a agregação está no **fim do plano**, quando já não há índices."),
    H3("Agregação com agrupamento (GROUP BY)"),
    T(["Método", "Como", "Custo", "Memória"],
      [["**Por ordenação**", "Ordena pelos atributos de agrupamento e calcula a agregação de cada grupo", "**custo_ordenação + b**", "Proporcional ao nº de **tuplas** (ordenação)"],
       ["**Estrutura auxiliar** (hash/árvore em memória)", "Varre sequencialmente e mantém **acumuladores por grupo** em memória", "**b**", "Proporcional ao nº de **grupos**"]],
      widths=[3.4, 6.2, 3.6, 3.8], size=9),
    BOX("erro", None, [
        "- Contar **custo de ordenação** na projeção **bag-based** (não há eliminação).",
        "- Esquecer a **dispensa da eliminação** quando a projeção inclui uma **chave candidata**.",
        "- Achar que agregação sempre usa índice.",
        "- O agrupamento por estrutura auxiliar só funciona se **o nº de grupos couber em memória**.",
    ]),
    BOX("resumo", None, [
        "- DISTINCT: ordena + varre. Projeção bag = b; set = b + (ord(b′) + b′). Conjuntos ≈ sort-merge. Agregação = b (sequencial). GROUP BY: ordenar (ord + b) ou acumuladores em memória (b).",
    ]),
    EX([
        Q("Uma relação tem b = 1.000 blocos. A projeção de 2 atributos (não chave) reduz para b′ = 250 blocos. Qual o custo da projeção set-based com buffer de 11 blocos? E se um dos atributos fosse a chave primária?",
          ["Ordenação externa de b′ = 250: nr = ⌈250/11⌉ = 23; gm = 10; passes = ⌈log₁₀ 23⌉ = 2 ⇒ 2·(250 + 250·2) = 1.500.",
           "C = b + (ord(b′) + b′) = 1.000 + (1.500 + 250) = **2.750**.",
           "Se a projeção inclui a **chave primária**, não há duplicados ⇒ **C = b = 1.000**."]),
        Q("Diferencie projeção bag-based e set-based e relacione com SQL e modelo relacional.",
          "**Bag-based** mantém duplicados (coerente com a **SQL**, que só elimina com DISTINCT); **set-based** elimina duplicados (coerente com o **modelo relacional**, em que relações são conjuntos)."),
        Q("Quais métodos existem para GROUP BY? Em que se diferenciam os requisitos de memória?",
          "**Por ordenação** (precisa ordenar a relação — memória proporcional ao nº de tuplas) e **por estrutura auxiliar** (acumuladores em memória por grupo — memória proporcional ao nº de **grupos**; custo b)."),
        Q("Como MAX(salario) pode ser calculado só com o índice?",
          "Com um índice **B⁺** em salario, o **maior valor** está na **folha mais à direita**: basta descer o índice (custo ≈ x se denso; x + 1 se esparso, pelo acesso ao registro) — sem ler o arquivo de dados todo."),
    ]),
]

# =====================================================================
# 5. OTIMIZAÇÃO
# =====================================================================
C += [
    H1("Otimização de consultas",
       "Slide 07 · Como o SGBD escolhe, entre planos equivalentes, o mais barato."),
    H2("O otimizador no fluxo"),
    P("O **otimizador** recebe a árvore de consulta inicial (do interpretador) e gera uma **árvore equivalente** (mesmo resultado) mais eficiente. De forma didática há duas partes:"),
    T(["", "Otimização **lógica**", "Otimização **física**"],
      [["Objetivo", "Explorar **propriedades algébricas** das consultas relacionais (regras de equivalência)", "Identificar **quais algoritmos** executam cada operação de maneira mais eficiente"],
       ["Exemplo", "Empurrar seleções para baixo da árvore", "Escolher índice × varredura, tipo de junção"]],
      widths=[2.6, 7.2, 7.2], size=9.5),
    BOX("def", "Baseada em regras × baseada em custos", [
        "- **Baseada em regras (rule-based):** aplica **heurísticas** que, em geral, reduzem o custo (ex.: seleção antes de junção). Não olha estatísticas.",
        "- **Baseada em custos (cost-based):** aplica heurísticas **e estima o custo** de cada alternativa com **estatísticas do catálogo**, identificando o menor custo para **cada situação**. É uma **extensão** da baseada em regras.",
    ]),
    BOX("insight", "“Otimização” é um nome exagerado", [
        "Procura-se uma **melhora razoável**, não o ótimo: (1) o tempo para achar o plano ótimo pode **inviabilizar** a otimização; (2) o otimizador é um programa **limitado aos dados do catálogo** (estatísticas podem estar desatualizadas).",
    ]),
    P("**Componentes:** *gerador de planos lógicos* (a partir da **árvore canônica**, reescreve usando propriedades algébricas) e *avaliador de planos* (estima e compara custos, **consultando o catálogo/estatísticas**). Resultado: árvore “otimizada”."),
    H2("Regras de equivalência da álgebra relacional"),
    T(["#", "Regra", "Em símbolos"],
      [["R1", "**Cascateamento de σ**", "σ_{c₁ ∧ c₂ ∧ … ∧ cₙ}(R) ≡ σ_{c₁}(σ_{c₂}(…σ_{cₙ}(R)…))"],
       ["R2", "**Comutatividade de σ**", "σ_{c₁}(σ_{c₂}(R)) ≡ σ_{c₂}(σ_{c₁}(R))"],
       ["R3", "**Cascateamento de π**", "π_{L₁}(π_{L₂}(…π_{Lₙ}(R)…)) ≡ π_{L₁}(R)  (só a mais externa vale)"],
       ["R4", "**Comutatividade σ × π**", "π_{A₁…Aₙ}(σ_c(R)) ≡ σ_c(π_{A₁…Aₙ}(R))  — **só se c usa apenas atributos de A₁…Aₙ**"],
       ["R5", "**Comutatividade de ⋈ (e ×)**", "R ⋈_c S ≡ S ⋈_c R"],
       ["R6", "**Comutatividade de σ com ⋈ (ou ×, ∪, ∩, −)**", "σ_c(R ⋈ S) ≡ σ_c(R) ⋈ S  (c só com atributos de R);  ou, se c = c₁ ∧ c₂:  σ_{c₁}(R) ⋈ σ_{c₂}(S)"],
       ["R7", "**Comutatividade de π com ⋈ (ou ×)**", "π_L(R ⋈ S) ≡ π_L( π_{A…}(R) ⋈ π_{B…}(S) )  (cada lado mantém seus atributos de L **mais os de junção**)"],
       ["R8", "**Operações de conjunto**", "∪ e ∩ são **comutativas**; **− não é**"],
       ["R9", "**Associatividade de ⋈, ×, ∪, ∩**", "(R θ S) θ T ≡ R θ (S θ T)"],
       ["R10", "**σ + × → ⋈**", "σ_c(R × S) ≡ R ⋈_c S"]],
      widths=[1.1, 5.7, 10.2], align=["c", "l", "l"], size=9),
    H2("Algoritmo geral de otimização por regras"),
    P("**Fundamentos:** (1) aplicar **σ e π o mais cedo possível**, antes das operações binárias (que tendem a **multiplicar** os tamanhos de entrada); (2) **substituir** conjuntos de operações por operações equivalentes menos custosas; (3) definir **boa ordem** para as operações binárias."),
    N(["**Quebre** seleções conjuntivas em um **cascateamento** de seleções (R1).",
       "**Empurre as seleções** o mais para **baixo** possível na árvore (R2, R4, R6).",
       "**Reordene as folhas** de modo que as relações com as **seleções mais restritivas** sejam executadas **primeiro** (R5, R8, R9).",
       "**Troque** σ_c(R × S) por **R ⋈_c S** (R10).",
       "**Empurre as projeções** o mais para baixo possível (R3, R4, R7).",
       "**Identifique subárvores** que podem ser executadas por **um único algoritmo** (pipeline)."]),
    BOX("exemplo", "Exemplo dos slides: consulta sobre empregado, trab_em e projeto", [
        CODE("""SELECT e.nome
FROM empregado e, trab_em t, projeto p
WHERE p.pnome = 'aquarius' AND p.pnum = t.pnum
  AND e.CPF = t.CPF AND e.dt_nasc >= '1957-12-31';
(pnum, pnome e CPF são únicos)"""),
        "# Árvore canônica (inicial)",
        CODE("π_{e.nome}( σ_{pnome='aquarius' ∧ p.pnum=t.pnum ∧ e.CPF=t.CPF ∧ dt_nasc≥'1957-12-31'}( (e × t) × p ) )"),
        "# Aplicando o algoritmo",
        "- **Passos 1–2:** cascateia e empurra as seleções: σ_{pnome='aquarius'}(p) e σ_{dt_nasc≥…}(e) descem até as folhas.",
        "- **Passo 3:** a seleção **mais restritiva** é a de **projeto** (pnome único ⇒ **1 tupla**); a de dt_nasc é pouco seletiva. Logo a primeira junção deve ser **projeto ⨝ trab_em**.",
        "- **Passo 4:** produtos + seleções de igualdade viram **junções** (R10): ((σ(p) ⋈_{pnum} t) ⋈_{CPF} σ(e)).",
        "- **Passo 5:** projeções descem: p → π_{pnum}; t → π_{pnum, CPF}; e → π_{CPF, nome}.",
        CODE("π_{nome}( ( π_{pnum}(σ_{pnome='aquarius'}(p)) ⋈_{pnum} π_{pnum,CPF}(t) ) ⋈_{CPF} π_{CPF,nome}(σ_{dt_nasc≥'1957-12-31'}(e)) )"),
        "- **Passo 6:** juntas e projeções adjacentes podem ser executadas em **pipeline** por um único algoritmo.",
    ]),
    H2("Avaliador de planos: estatísticas do catálogo"),
    P("O custo considera: **acesso a disco** (prioridade dos SGBDs convencionais), comunicação, armazenamento temporário, processamento em memória e quantidade de memória. As estatísticas disponíveis:"),
    T(["Estatística", "Símbolo", "Estatística", "Símbolo"],
      [["Nº de registros", "r", "Nº de níveis do índice", "x"], ["Tamanho do registro", "R", "Nº de blocos folha do índice", "b_leaf"],
       ["Nº de blocos", "b", "Cardinalidade da seleção (chave s = 1)", "s"], ["Tamanho do bloco", "B", "Seletividade (chave 1/r)", "sl = s/r"],
       ["Fator de bloco", "bfr = B/R", "Nº de valores distintos, mín, máx, histogramas", "(por atributo)"]],
      widths=[4.2, 2.3, 7.2, 3.3], size=9.5),
    BOX("exemplo", "Exemplo baseado em custos (mesma consulta, com as estatísticas do slide)", [
        "**Dados do catálogo:** B = 1024 bytes; buffer de 5 blocos. empregado: r = 10.000; projeto: r = 250; trabalha_em: r = 500.000. Tamanhos: cpf 8, nome 80, salário 16, dt_nasc 8, endereço 200; pnum 8, pnome 40, plocalização 30; horas 4. "
        "Índices: emp_pkey_ix (cpf; x = 2; b_leaf = 40), emp_dt_nasc_ix (x = 2; 40), proj_pkey_ix (pnum; x = 2; 3), proj_pnome_ix (pnome; x = 2; 10), trab_pkey_ix (pnum, cpf; x = 3; 80). Histograma de dt_nasc: <1957: 1000; 1957–1980: 3000; 1980–1990: 4000; ≥1990: 2000.",
        "# Tamanhos (R, bfr, b) — valores aproximados",
        "- empregado: R = 312 ⇒ bfr = ⌊1024/312⌋ = 3 ⇒ **b ≈ 3.334**.  projeto: R = 78 ⇒ bfr = 13 ⇒ **b = 20**.  trabalha_em: R = 20 ⇒ bfr = 51 ⇒ **b ≈ 9.804**.",
        "# Seletividade das condições",
        "- **p.pnome = ‘aquarius’**: pnome é único ⇒ **s = 1** ⇒ por proj_pnome_ix: ≈ 2 + 10·(1/250) − 1 + 1 ≈ **3 blocos** (vs 20 da varredura).",
        "- **e.dt_nasc ≥ ‘1957-12-31’**: pelo histograma, ≈ 3000 + 4000 + 2000 = **9.000 tuplas (90 %)** ⇒ pouco seletiva. Pelo índice: ≈ 2 + 40·0,9 − 1 + 9000 ≈ **9.037** blocos > 3.334 ⇒ **varredura sequencial** (ou, melhor, **filtrar em memória** durante a junção).",
        "# Escolha do plano",
        "- Começar por **projeto** (1 tupla, 3 blocos). Juntar com trabalha_em usando o **índice composto (pnum, cpf)**: s = 500000/250 = 2.000 tuplas de trab_em para o pnum ⇒ ≈ 3 + 80·(2000/500000) − 1 + 2000 ≈ **2.002** blocos.",
        "- Para cada uma dessas ≈ 2.000 tuplas, buscar o empregado pelo **emp_pkey_ix** (cpf): ≈ x + 1 = **3** blocos cada ⇒ ≈ **6.000**; a condição de dt_nasc é testada **em memória**.",
        "- **Total ≈ 3 + 2.002 + 6.000 ≈ 8.000 blocos.** Alternativas que começam por empregado (3.334 blocos só para ler a tabela, mais junções com 500.000 tuplas de trabalha_em) custam **muito mais**.",
        "Conclusão: ordem **projeto → trabalha_em → empregado**, com **junções por índice** e filtros em memória. (Números aproximados; o importante é o **raciocínio**: seleção mais restritiva primeiro, índices onde há seletividade, varredura onde não há.)",
    ]),
    BOX("erro", None, [
        "- Aplicar R4 (trocar σ e π) quando a seleção usa **atributos que a projeção removeria**.",
        "- Dizer que “− (diferença)” é comutativa.",
        "- Empurrar **projeções** antes de uma junção **sem manter os atributos de junção**.",
        "- Esquecer que o otimizador **depende das estatísticas do catálogo** (podem estar desatualizadas).",
        "- Confundir **otimização lógica** (reescrita algébrica) com **física** (escolha de algoritmos).",
    ]),
    BOX("resumo", None, [
        "- Árvore canônica → (regras) → árvore otimizada → (custos) → plano físico.",
        "- Algoritmo: quebrar σ; empurrar σ; folhas mais restritivas primeiro; σ(×) → ⋈; empurrar π; agrupar subárvores em um algoritmo.",
        "- Rule-based = heurísticas; cost-based = heurísticas + estimativa com estatísticas.",
    ]),
    EX([
        Q("Por que as seleções devem ser aplicadas o mais cedo possível, antes das junções?",
          "Porque as operações binárias (junção, produto) tendem a **multiplicar** os tamanhos das entradas. Reduzir **cedo** o número de tuplas (e de atributos, com projeção) diminui o tamanho dos operandos e o custo de todas as operações seguintes."),
        Q("Aplique o algoritmo geral à consulta: SELECT d.dnome FROM departamento d, empregado e WHERE e.salario > 5000 AND e.dnum = d.dnum AND d.local = ‘Londrina’. Escreva a árvore otimizada.",
          ["Canônica: π_{dnome}(σ_{salario>5000 ∧ e.dnum=d.dnum ∧ local='Londrina'}(e × d)).",
           "Otimizada: π_{dnome}( π_{dnum,dnome}(σ_{local='Londrina'}(d)) ⋈_{dnum} π_{dnum}(σ_{salario>5000}(e)) ).",
           "Passos: quebrar a seleção, empurrar σ_{local} para d e σ_{salario} para e; × + igualdade → ⋈; projeções para baixo mantendo o atributo de junção dnum."]),
        Q("Qual a diferença entre otimização baseada em regras e em custos? Em qual delas o catálogo é indispensável?",
          "Em regras: heurísticas gerais, sem estimar custos. Em custos: aplica as heurísticas e **estima o custo** dos planos com **estatísticas do catálogo** (r, b, x, s, histogramas…) para escolher o menor. Portanto o catálogo é indispensável na baseada em **custos**."),
        Q("Marque V ou F: (a) σ_c(R ⋈ S) = σ_c(R) ⋈ S quando c usa só atributos de R; (b) a diferença de conjuntos é comutativa; (c) toda projeção pode ser empurrada para qualquer ponto da árvore; (d) o resultado da otimização deve ser equivalente à consulta original.",
          "(a) **V** (R6). (b) **F** (R8). (c) **F** — precisa manter os atributos necessários depois (junção e projeção final). (d) **V**."),
        Q("Dê dois motivos pelos quais “otimização” não é o termo mais adequado.",
          "(1) Encontrar o plano **ótimo** pode levar mais tempo que executar a consulta (impraticável); (2) o otimizador é um **programa limitado ao catálogo**: estatísticas imprecisas/desatualizadas levam a estimativas erradas. Busca-se uma melhora **razoável**, não a ótima."),
    ]),
]

# =====================================================================
# 6. TRANSAÇÕES E ACID
# =====================================================================
C += [
    H1("Transações, escalonamentos e propriedades ACID",
       "Slide 08 (parte 1) · O mecanismo que dá “tudo ou nada” e isolamento em um banco compartilhado."),
    H2("Por que transações?"),
    P("Um banco de dados é um **recurso compartilhado** acessado por muitos usuários e processos **concorrentemente**. Sem controle surgem problemas por **concorrência** e por **falhas**. "
      "**Processamento de transações** = técnicas para gerenciar o banco em ambiente **concorrente multiusuário**. Sistemas **OLTP** (Online Transaction Processing) tratam milhares de transações por minuto e exigem **alta disponibilidade** e resposta rápida."),
    BOX("def", "Transação", [
        "**Unidade local de processamento do banco**: um programa em execução que inclui **uma ou mais operações de acesso** ao BD. Exemplo: transferir R$ 100 da conta corrente para a poupança.",
        "- **Operações características:** **leituras** (ex.: SELECT) e **escritas** (INSERT, UPDATE, DELETE).",
        "- Delimitada por **Begin_transaction** e **End_transaction**; termina em **Commit** (sucesso: resultados **permanentes**) ou **Abort/Rollback** (nada fica refletido no banco).",
    ]),
    H2("Modelo de processamento"),
    B(["O BD é uma coleção de **itens de dados** nomeados (a granularidade — campo, registro ou bloco — é irrelevante para a teoria).",
       "**read_item(X)**: acha o bloco que contém X → copia para um **buffer** da memória (se não estiver lá) → copia X do buffer para a variável do programa.",
       "**write_item(X)**: acha o bloco → carrega no buffer → copia X da variável do programa para o buffer → **grava o bloco no disco** (imediatamente ou, tipicamente, **mais tarde**).",
       "Leituras e escritas **levam tempo** — por isso transações concorrentes se entrelaçam."]),
    H3("Notação e escalonamentos (schedules)"),
    BOX("def", "Notação do slide", [
        "- **r_i(X)** = Tᵢ lê X · **w_i(X)** = Tᵢ escreve X · **c_i** = Tᵢ **commit** · **a_i** = Tᵢ **abort** (i = identificador da transação).",
        "- Ex.: T₁: r₁(X); w₁(X); r₁(Y); w₁(Y); — T₂: r₂(X); w₂(X);",
        "- **Escalonamento (schedule)** = **sequência de operações entrelaçadas** de várias transações. Ex.: S_a: r₁(X); r₂(X); w₁(X); r₁(Y); w₂(X); c₂; w₁(Y); a₁;",
        "- Modos de concorrência: **intercalado (interleaved)** em uma só CPU × **paralelo** em várias CPUs. A teoria básica assume **intercalação**.",
    ]),
    BOX("exemplo", "O que pode dar errado? (transferência bancária × saque)", [
        "T₁ (caixa 1): lê poupança; poupança −100; escreve; lê corrente; corrente +100; escreve.  T₂ (caixa 2): lê corrente; corrente −20; escreve; entrega R$ 20.",
        "- **Falha no meio de T₁** (depois de debitar a poupança e antes de creditar a corrente) ⇒ **dinheiro perdido**; se a escrita em disco não foi feita antes da falha ⇒ **atualizações perdidas**.",
        "- **Interferência:** se T₂ executar entre a leitura e a escrita de T₁ na conta corrente, o **saque de R$ 20 ou o depósito de R$ 100 é “perdido”** (a conta fica com valor incorreto).",
    ]),
    H2("Propriedades ACID"),
    T(["Propriedade", "Significado", "Quem garante"],
      [["**A**tomicidade", "A transação é **indivisível**: ou é executada **por completo** ou **não é executada** (nada)", "**Sistema de recuperação**"],
       ["**C**onsistência", "Uma execução correta leva o BD de um **estado consistente a outro** estado consistente", "**Sistema de restrições** do BD (e correção do programa)"],
       ["**I**solamento", "Embora concorrentes, as transações **parecem executar isoladas** (efeito final = como se cada uma fosse executada sozinha)", "**Controle de concorrência**"],
       ["**D**urabilidade", "Depois do **commit**, as mudanças **nunca podem ser perdidas** por falhas posteriores", "**Sistema de recuperação**"]],
      widths=[3.4, 8.8, 4.8], size=9.5),
    BOX("lembrete", "Decore a tríade “quem garante o quê”", [
        "**Consistência → restrições de integridade · Isolamento → controle de concorrência · Atomicidade + Durabilidade → recuperação.**",
    ]),
    BOX("erro", None, [
        "- Achar que **atomicidade** é sobre concorrência (é sobre **falhas**: tudo ou nada).",
        "- Confundir **consistência do BD** (restrições) com **consistência de leitura/isolamento**.",
        "- Esquecer que o **commit** é o ponto a partir do qual vale a **durabilidade**.",
        "- Dizer que a granularidade do item de dado (campo/registro/bloco) muda a teoria: **não muda**.",
    ]),
    BOX("resumo", None, [
        "- Transação = unidade lógica de trabalho com begin/end → commit ou abort.",
        "- Escalonamento = sequência entrelaçada de operações; notação r_i, w_i, c_i, a_i.",
        "- ACID: Atomicidade, Consistência, Isolamento, Durabilidade (com seus responsáveis).",
    ]),
    EX([
        Q("Associe cada propriedade ao mecanismo que a garante: (1) Atomicidade; (2) Consistência; (3) Isolamento; (4) Durabilidade — a) controle de concorrência; b) sistema de restrições/correção do programa; c) sistema de recuperação (atomicidade e durabilidade).",
          "(1)-c, (2)-b, (3)-a, (4)-c."),
        Q("Uma transação debita R$ 100 de A e credita R$ 100 em B. O sistema cai depois do débito e antes do crédito. Qual propriedade ACID está em jogo e o que o SGBD deve fazer na recuperação?",
          "**Atomicidade:** a transação não foi concluída (nem fez commit); o sistema de recuperação deve **desfazer (rollback)** o débito, deixando o BD como se a transação não tivesse ocorrido."),
        Q("Escreva a notação do schedule em que T₁ lê X, T₂ lê X, T₁ escreve X, T₂ escreve X e depois ambas fazem commit (T₁ primeiro).",
          "r₁(X); r₂(X); w₁(X); w₂(X); c₁; c₂;  (é o clássico “lost update”: veja a próxima seção)."),
        Q("V ou F: (a) após o commit, uma falha pode desfazer a transação; (b) OLTP exige alta disponibilidade e resposta rápida; (c) uma transação pode terminar em commit ou abort.",
          "(a) **F** — durabilidade. (b) **V**. (c) **V**."),
    ]),
]

# =====================================================================
# 7. PROBLEMAS DE CONCORRÊNCIA
# =====================================================================
C += [
    H1("Problemas de concorrência",
       "Slide 08 (parte 2) · Por que é preciso controlar como as transações se entrelaçam."),
    P("Para evitar problemas é necessário **restringir** o entrelaçamento. Os quatro problemas clássicos:"),
    T(["Problema", "Quando ocorre", "Exemplo do slide"],
      [["**Atualização perdida** (*lost update*)", "Duas transações **atualizam o mesmo item** mas ambas leram o **valor original** antes das atualizações", "X = 80. T₁: X := X − 5; T₂: X := X + 10. Ambas leem 80; T₁ grava 75; T₂ grava 90. Final **90** (ou 75), mas o correto é 80 − 5 + 10 = **85**"],
       ["**Leitura suja** (*dirty read*)", "T₂ **lê um item atualizado por T₁ ainda não confirmado**, e depois T₁ **aborta**, invalidando o valor lido", "T₁ grava X = 75 e depois aborta; T₂ leu 75, calculou 85 e gravou. Correto: **80 + 10 = 90**. T₂ também deve **abortar** (**rollback em cascata**)"],
       ["**Leituras inconsistentes** (*inconsistent reads / incorrect summary*)", "Uma transação lê valores que **não correspondem a um estado isolado** do BD", "T₂ calcula SUM(X₁,X₂,X₃) **enquanto** T₁ atualiza X₁ e X₃: soma 125 = mistura de antes/depois; correto: **120** (antes de T₁) ou **130** (depois)"],
       ["**Leitura não repetível** (*unrepeatable read*)", "Uma transação **lê o mesmo item duas vezes** e **outra transação o atualiza no meio**: obtém valores diferentes", "T₂ lê X = 80 (calcula Y), T₁ atualiza X = 75 e T₂ relê X = 75: **Z depende de dois valores diferentes de X**"]],
      widths=[3.6, 6.2, 7.2], size=9),
    BOX("def", "Quando há conflito?", [
        "Só importa a interação entre duas aplicações quando **uma lê enquanto a outra escreve** ou **ambas escrevem**. **Duas só-leituras não conflitam.**",
    ]),
    BOX("exemplo", "Lost update passo a passo (X = 80)", [
        T(["Passo", "T₁", "T₂", "X no BD"],
          [["1", "read_item(X) → 80", "", "80"], ["2", "X := X − 5 → 75", "", "80"], ["3", "", "read_item(X) → **80** (!)", "80"],
           ["4", "", "X := X + 10 → 90", "80"], ["5", "write_item(X) (75)", "", "75"], ["6", "", "write_item(X) (90)", "**90**"]],
          align=["c", "l", "l", "c"], size=9.5),
        "A atualização de T₁ (−5) foi **sobrescrita**. O valor 90 não corresponde a nenhuma execução serial (T₁;T₂ ou T₂;T₁ dariam **85**).",
    ]),
    BOX("insight", "Leitura suja ⇒ rollback em cascata", [
        "Se T₂ usa um dado “sujo” de T₁ e T₁ **aborta**, o que T₂ fez é **inválido** — T₂ deve ser desfeita também (e quem leu dados de T₂, e assim por diante: **efeito cascata**). "
        "Escalonamentos que **proíbem ler dados não confirmados** evitam cascata.",
    ]),
    BOX("erro", None, [
        "- Confundir **leitura suja** (dado não confirmado que depois some) com **leitura não repetível** (dado **confirmado** que **mudou** entre duas leituras).",
        "- Achar que leitura inconsistente envolve abort: é uma **visão mista** de antes e depois de outra transação.",
        "- Achar que **duas leituras** também podem conflitar (**não**).",
    ]),
    BOX("resumo", None, [
        "- Atualização perdida · Leitura suja · Leituras inconsistentes · Leitura não repetível.",
        "- Conflito = ≥ 1 escrita no mesmo item por transações diferentes.",
    ]),
    EX([
        Q("Identifique o problema: T₁ lê X (10), T₂ lê X (10), T₁ grava X = 15 (X := X + 5), T₂ grava X = 30 (X := X + 20). Qual o valor correto e qual o final?",
          "**Atualização perdida.** Correto: 10 + 5 + 20 = **35**. Final: **30** (a atualização de T₁ foi sobrescrita)."),
        Q("T₁ grava Y = 100 e ainda não faz commit; T₂ lê Y = 100 e grava Z = Y + 1; depois T₁ aborta. Que problema ocorreu e o que fazer?",
          "**Leitura suja**. T₂ usou um valor que nunca foi confirmado; deve sofrer **rollback em cascata** (e quem dependeu de T₂)."),
        Q("Em quais pares de operações de transações diferentes sobre o mesmo item há conflito? (r–r, r–w, w–r, w–w)",
          "**r–w, w–r e w–w** conflitam; **r–r não** conflita."),
        Q("Diferencie leitura não repetível de leitura suja.",
          "**Suja:** lê dado **não confirmado** que pode ser desfeito (abort). **Não repetível:** lê **duas vezes o mesmo item** e a segunda leitura difere porque **outra transação confirmou uma atualização** no meio."),
    ]),
]

# =====================================================================
# 8. SERIALIZABILIDADE
# =====================================================================
C += [
    H1("Escalonamentos seriais, serializabilidade e isolamento no SQL",
       "Slide 08 (parte 3) · A teoria que diz quais entrelaçamentos são aceitáveis."),
    H2("Escalonamento serial × serializável"),
    BOX("def", "Definições", [
        "- **Serial:** **não há entrelaçamento**: todas as operações de cada transação são executadas **consecutivamente**. **Qualquer escalonamento serial é correto** (cada transação, sozinha, leva de um estado consistente a outro).",
        "- Problema: serial é **inviável por desempenho** (transações longas bloqueiam as outras; durante um I/O o sistema não pode trocar de transação). Solução: **permitir entrelaçamento aceitável**.",
        "- **Serializável:** escalonamento **equivalente a algum escalonamento serial** das mesmas transações. É aceitável porque deixa o BD como uma execução serial.",
        "- Com **n transações** há **n!** escalonamentos seriais; **todos são corretos, mas podem dar resultados diferentes** (a correção é do ponto de vista do BD).",
        "- **Meta do controle de concorrência:** produzir escalonamentos **serializáveis**.",
    ]),
    BOX("exemplo", "Correto “do ponto de vista do BD” (slides 25–26)", [
        "T₁: aplicar juros de 5 % em S. T₂: sacar R$ 100 de S. S = 1.000.",
        "- T₂ antes de T₁: S = 900 → 900 + 5 % = **945**.   - T₁ antes de T₂: S = 1050 → −100 = **950**.",
        "**Ambos** são estados válidos do banco, ainda que diferentes. Se a aplicação exige uma ordem específica, isso é uma **regra de negócio** a ser implementada pela aplicação.",
    ]),
    H2("Equivalência de escalonamentos"),
    T(["Tipo", "Definição"],
      [["**Equivalência de resultado**", "Produzem o **mesmo estado final** do BD — pode ser **acidental** (não serve de critério geral)"],
       ["**Equivalência de conflito**", "A **ordem relativa de quaisquer duas operações em conflito é a mesma** nos dois escalonamentos"],
       ["**Equivalência de visão** (*view*)", "Cada leitura lê o **resultado da mesma escrita** nos dois escalonamentos (e a **última escrita** de cada item é a mesma)"]],
      widths=[4.6, 12.4], size=9.5),
    BOX("def", "Operações em conflito (no escalonamento S)", [
        "Duas operações **conflitam** se (1) pertencem a **transações diferentes**, (2) acessam o **mesmo item X** e (3) **pelo menos uma é write(X)**.",
    ]),
    H2("Serializabilidade por conflito: o grafo de precedência"),
    BOX("def", "Teste (grafo de serialização)", [
        "1. **Nó** para cada transação Tᵢ.",
        "2. **Aresta Tᵢ → Tⱼ** se alguma operação de Tᵢ aparece **antes** de uma operação **em conflito** de Tⱼ.",
        "3. **S é serializável por conflito ⇔ o grafo não tem ciclos.** Se acíclico, uma **ordenação topológica** do grafo dá um escalonamento serial equivalente.",
    ]),
    BOX("exemplo", "Aplicando o teste", [
        "**S₁ = r₁(X); r₂(X); w₁(X); w₂(X)** (lost update):",
        "- r₂(X) antes de w₁(X) ⇒ **T₂ → T₁**; r₁(X) antes de w₂(X) ⇒ **T₁ → T₂**; w₁(X) antes de w₂(X) ⇒ T₁ → T₂.  **Ciclo T₁ ⇄ T₂ ⇒ NÃO serializável.**",
        "**S₂ = r₁(X); w₁(X); r₂(X); w₂(X); r₁(Y); w₁(Y)**:",
        "- Conflitos em X: w₁(X)→r₂(X), w₁(X)→w₂(X), r₁(X)→w₂(X): todos **T₁ → T₂**. Y: só T₁.  **Grafo T₁ → T₂ (acíclico) ⇒ serializável**, equivalente ao serial **T₁; T₂**.",
        "**S₃ = r₁(A); w₂(A); r₂(B); w₃(B); r₃(C); w₁(C)**:",
        "- r₁(A)→w₂(A): T₁ → T₂; r₂(B)→w₃(B): T₂ → T₃; r₃(C)→w₁(C): T₃ → T₁.  **Ciclo T₁ → T₂ → T₃ → T₁ ⇒ NÃO serializável.**",
    ]),
    BOX("insight", "Como montar o grafo sem se perder", [
        "Percorra o escalonamento **item por item**. Para cada item X, liste as operações em ordem e, para **cada par** (anterior, posterior) com **transações diferentes e pelo menos uma escrita**, desenhe a aresta **da transação da operação anterior para a da posterior**. Leituras consecutivas **não** geram aresta.",
    ]),
    H2("Serializabilidade de visão (view)"),
    B(["S é **view-serializável** se é **view-equivalente** a algum escalonamento serial S′: **(1)** toda leitura rᵢ(X) lê o valor escrito pela **mesma escrita** (ou o valor original) em S e S′; **(2)** a **última escrita** de cada item em S é a mesma em S′.",
       "Teste: **enumerar os escalonamentos seriais** (n!) e verificar as duas condições.",
       "É **sensível a escritas cegas** (*blind writes*: escrever sem ler antes). **Conflito-serializável ⇒ view-serializável**, mas **não o contrário**; os dois coincidem se **não há escritas cegas** (*constrained write assumption*)."]),
    BOX("exemplo", "Exemplo do slide: view-serializável mas não conflito-serializável", [
        "T₁: r(X); w(X). T₂: w(X). T₃: w(X). Escalonamento: **r₁(X); w₂(X); w₁(X); w₃(X)**.",
        "- **Conflito:** r₁(X) antes de w₂(X) ⇒ T₁ → T₂; w₂(X) antes de w₁(X) ⇒ T₂ → T₁ ⇒ **ciclo ⇒ não é conflito-serializável**.",
        "- **View:** equivalente ao serial **T₁; T₂; T₃**: r₁(X) lê o valor original nos dois; a **última escrita** (w₃) é a mesma. ⇒ **view-serializável** (as escritas de T₂ e T₁ são “cegas”/sobrescritas por T₃).",
    ]),
    H2("Transações no SQL"),
    B(["Em geral **não há** `BEGIN TRANSACTION` obrigatório, mas toda transação deve ter um **fim explícito: COMMIT ou ROLLBACK**.",
       "**Transações aninhadas** (iniciadas dentro do escopo de outra) são implementadas de formas diferentes em cada SGBD. **Savepoints** permitem **rollback parcial**."]),
    CODE("""START TRANSACTION;
INSERT INTO table1 VALUES (1);
SAVEPOINT savepoint1;
INSERT INTO table1 VALUES (2);
ROLLBACK TO SAVEPOINT savepoint1;   -- desfaz só o INSERT 2
INSERT INTO table1 VALUES (3);
COMMIT;                             -- persiste o 1º e o 3º inserts""", "Savepoint (slide)"),
    H3("Níveis de isolamento do SQL"),
    P("Dependem de três problemas possíveis: **leitura suja**, **leitura não repetível** e **fantasmas** (*phantoms*: novas tuplas que passam a satisfazer a condição de uma consulta repetida)."),
    T(["Nível de isolamento", "Leitura suja", "Leitura não repetível", "Fantasma"],
      [["**READ UNCOMMITTED**", "Sim", "Sim", "Sim"], ["**READ COMMITTED**", "**Não**", "Sim", "Sim"],
       ["**REPEATABLE READ**", "**Não**", "**Não**", "Sim"], ["**SERIALIZABLE**", "**Não**", "**Não**", "**Não**"]],
      widths=[5.4, 3.4, 4.4, 3.8], align=["l", "c", "c", "c"], size=10),
    P("“Sim” = o problema **pode ocorrer** naquele nível. Níveis **mais altos** = mais isolamento (e, em geral, menos concorrência/desempenho)."),
    BOX("def", "Isolamento por snapshot (*snapshot isolation*)", [
        "Usado em alguns SGBDs comerciais: a transação **vê os valores confirmados** dos itens **no instante em que começou** (um “instantâneo” do banco). **Garante que o problema dos fantasmas não ocorre.**",
    ]),
    BOX("erro", None, [
        "- Dizer que **serial = serializável**: serial é **sem entrelaçamento**; serializável é **equivalente** a um serial (pode ter entrelaçamento).",
        "- Esquecer a condição **“pelo menos uma é escrita”** para conflito (r–r **não** conflita).",
        "- Em ciclos: o grafo **precisa ser acíclico**; um único ciclo já reprova.",
        "- Trocar o sentido das arestas: vai da transação da operação **anterior** para a **posterior**.",
        "- Ler a tabela de isolamento ao contrário: “Sim” = a anomalia **é permitida**.",
        "- Achar que view-serializável ⇒ conflito-serializável (o inverso é que vale).",
    ]),
    BOX("resumo", None, [
        "- Serial = sem entrelaçamento (sempre correto). Serializável = equivalente a algum serial (n! possíveis).",
        "- Conflito: transações diferentes, mesmo item, ≥1 escrita. Teste: **grafo sem ciclos** ⇒ serializável por conflito.",
        "- View-serializabilidade é mais geral (considera escritas cegas). SQL: COMMIT/ROLLBACK, SAVEPOINT; 4 níveis de isolamento; snapshot evita fantasmas.",
    ]),
    EX([
        Q("Para o escalonamento S = r₁(X); w₁(X); r₂(X); w₂(X); r₂(Y); w₂(Y); r₁(Y); w₁(Y), construa o grafo de precedência e diga se é serializável por conflito.",
          ["Em **X**: w₁(X)→r₂(X) e w₁(X)→w₂(X) ⇒ **T₁ → T₂**.",
           "Em **Y**: r₂(Y)→w₁(Y), w₂(Y)→r₁(Y) e w₂(Y)→w₁(Y) ⇒ **T₂ → T₁**.",
           "Ciclo **T₁ ⇄ T₂** ⇒ **não é serializável por conflito**."]),
        Q("S = r₁(A); w₁(A); r₂(A); w₂(B); r₃(B); w₃(A). Qual o grafo? Se acíclico, dê um escalonamento serial equivalente.",
          ["A: w₁(A)→r₂(A): T₁ → T₂; w₁(A)→w₃(A): T₁ → T₃; r₂(A)→w₃(A): T₂ → T₃.  B: w₂(B)→r₃(B): T₂ → T₃.",
           "Arestas: T₁→T₂, T₁→T₃, T₂→T₃. **Sem ciclos** ⇒ serializável. Ordem topológica: **T₁; T₂; T₃**."]),
        Q("Quantos escalonamentos seriais existem para 4 transações? Todos produzem o mesmo resultado?",
          "**4! = 24**. Todos são **corretos**, mas **não necessariamente iguais** (como 945 × 950 no exemplo dos juros)."),
        Q("Por que o escalonamento r₁(X); w₂(X); w₁(X); w₃(X) é view-serializável mas não conflito-serializável?",
          "Conflito: r₁(X)→w₂(X) (T₁→T₂) e w₂(X)→w₁(X) (T₂→T₁): ciclo. View: equivale ao serial T₁;T₂;T₃: r₁(X) lê o valor original nos dois e a **última escrita é w₃(X)**. As escritas de T₁ e T₂ são **cegas** e sobrescritas por T₃."),
        Q("Marque a correta sobre níveis de isolamento: (a) READ COMMITTED permite leitura suja; (b) REPEATABLE READ elimina leitura suja e não repetível, mas pode ter fantasmas; (c) SERIALIZABLE permite fantasmas; (d) READ UNCOMMITTED evita todos os problemas.",
          opts=["READ COMMITTED permite leitura suja.", "REPEATABLE READ elimina leitura suja e não repetível, mas ainda permite fantasmas.",
                "SERIALIZABLE permite fantasmas.", "READ UNCOMMITTED evita todos os problemas."],
          a="**b).** a) falsa — READ COMMITTED **evita** leitura suja; c) falsa — SERIALIZABLE evita todos; d) falsa — READ UNCOMMITTED permite os três."),
        Q("O que faz o ROLLBACK TO SAVEPOINT savepoint1 no exemplo dos slides, e quais inserts permanecem após o COMMIT?",
          "Desfaz tudo o que foi feito **depois** do savepoint (o INSERT do valor 2) sem encerrar a transação. Após o COMMIT permanecem os inserts de **1** e de **3**."),
    ]),
]

# =====================================================================
# 9. COLA
# =====================================================================
C += [
    H1("Cola de última hora e erros comuns", "Releia na véspera."),
    H2("Fórmulas e regras em uma página"),
    T(["Tema", "Lembrar"],
      [["Blocos", "b = ⌈r / Bfr⌉; custo = **blocos de disco**"],
       ["Ordenação externa", "C = 2·(b + b·log_{gm} nr); gm = b_buffer − 1; nr = b / b_buffer"],
       ["Seleção", "Seq = b · Bin = log₂b + s/Bfr − 1 · Clustering = x + s/Bfr · Secundário = x + b_leaf·s/r − 1 + s"],
       ["Estatística uniforme", "s = r / d; sl = s / r"],
       ["AND / OR", "AND: índice simples + filtro, índice composto, interseção de rids · OR: sequencial (ou união de rids se **todos** indexados)"],
       ["Junção NL", "v1: b_o + b_o·b_i · v2: b_o + ⌈b_o/(b_buf − 2)⌉·b_i (externa = menor)"],
       ["Junção índice / SM / hash", "b_o + r_o·custo_índice · b_R + b_S (+ord.) · 2(b_R + b_S) + buckets"],
       ["Projeção", "bag = b · set = b + (ord(b′) + b′) · chave incluída ⇒ sem eliminação"],
       ["Agregação", "Seq = b · min/max pelo índice = x (+1) · GROUP BY: ord + b ou acumuladores (b)"],
       ["Regras", "R1/R2 σ · R3/R4 π · R5 ⋈ comutativa · R6 σ×⋈ · R7 π×⋈ · R8 ∪∩ comutam, − não · R9 associativas · R10 σ(×) = ⋈"],
       ["Algoritmo geral", "quebrar σ → empurrar σ → folhas mais restritivas → σ(×)→⋈ → empurrar π → agrupar subárvores"],
       ["ACID", "Atomicidade, Consistência, Isolamento, Durabilidade (recuperação, restrições, concorrência, recuperação)"],
       ["Problemas", "Atualização perdida · Leitura suja · Leituras inconsistentes · Leitura não repetível (+ fantasmas)"],
       ["Conflito", "transações diferentes + mesmo item + ≥ 1 escrita"],
       ["Serializabilidade", "grafo Tᵢ→Tⱼ (op. anterior → op. posterior); **sem ciclo** ⇒ serializável; n! seriais"],
       ["Isolamento SQL", "RU (3 problemas) · RC (sem suja) · RR (sem suja/não repetível) · SERIALIZABLE (nenhum)"]],
      widths=[3.8, 13.2], size=9.5),
    H2("Os 10 erros que mais custam pontos"),
    N(["Esquecer o fator **2** (leitura + escrita) e **gm = b_buffer − 1** na ordenação externa.",
       "Usar **índice secundário** para seleções pouco seletivas (a varredura pode ser melhor).",
       "Trocar **b_buffer** por **b_buffer − 2** nos laços aninhados v2 (e a externa deve ser a **menor**).",
       "Esquecer a **ordenação** no sort-merge quando a relação não está ordenada.",
       "Hash join/sort-merge para **theta-join**.",
       "Projeção set-based: esquecer o atalho da **chave candidata**.",
       "Otimização: empurrar π removendo **atributos de junção**.",
       "**Atomicidade/Durabilidade = recuperação**; Isolamento = concorrência; Consistência = restrições.",
       "Grafo: aresta **da operação anterior para a posterior**; **um ciclo** já reprova.",
       "Tabela de isolamento: “Sim” significa que a anomalia **pode ocorrer**."]),
    H2("Mini-simulado final"),
    EX([
        Q("Tabela T: r = 20.000, Bfr = 10, ordenada por código, com índice clustering em código (x = 3). Consulta: código BETWEEN 100 AND 150, retornando 50 tuplas. Estime o custo da sequencial, da busca binária e do índice clustering.",
          ["b = 2.000. Sequencial: **2.000**. Binária: ⌈log₂ 2000⌉ + 50/10 − 1 = 11 + 5 − 1 = **15**. Clustering: 3 + 50/10 = **8**.",
           "Melhor: **índice clustering (8 blocos)**."]),
        Q("A (10 blocos) ⨝ B (800 blocos) por NL com buffer de 8 blocos. Calcule os custos com A externa e com B externa.",
          ["b_buffer − 2 = 6. A externa: 10 + ⌈10/6⌉·800 = 10 + 2·800 = **1.610**.",
           "B externa: 800 + ⌈800/6⌉·10 = 800 + 134·10 = **2.140**. Melhor: A (menor) como externa."]),
        Q("Dê um escalonamento de duas transações que seja serializável (com entrelaçamento) e um que não seja, justificando pelo grafo.",
          ["Serializável: r₁(X); r₂(Y); w₁(X); w₂(Y) — itens diferentes ⇒ sem conflitos ⇒ sem arestas ⇒ equivalente a T₁;T₂ ou T₂;T₁.",
           "Não serializável: r₁(X); r₂(X); w₁(X); w₂(X) — arestas T₂→T₁ e T₁→T₂ ⇒ ciclo (lost update)."]),
        Q("Explique, com suas palavras, as quatro propriedades ACID com um exemplo de transferência bancária.",
          "**Atomicidade:** o débito e o crédito acontecem **ambos ou nenhum**. **Consistência:** o saldo total do banco continua correto (regras/restrições respeitadas) antes e depois. **Isolamento:** outra transação que consulta os saldos não vê um estado “meio transferido”. **Durabilidade:** depois do commit, a transferência não se perde mesmo que o sistema caia."),
    ], title="Exercícios — Mini-simulado"),
]
