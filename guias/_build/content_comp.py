# -*- coding: utf-8 -*-
from guide_builder import *

COLOR = "6A1B9A"  # roxo
TITLE = "Computabilidade e Decidibilidade"
PROF = "Prof. Dr. Gilberto Fernandes Jr. · 1COP030 · Departamento de Computação · UEL"
EXAM = "03/12/2026"
SOURCES = "Slides 08–13 (Máquina de Turing · Extensões · Decidibilidade · Computabilidade · Diagonalização · Redutibilidade)"
TOPICS = ["Máquina de Turing", "Extensões da MT", "Church-Turing e decidibilidade", "Problemas indecidíveis (ALG, Parada)", "Diagonalização e L_{D}", "Redutibilidade"]
NOTE = "Notação dos slides: ⊗ = marcador de início de fita, β = branco. Trechos “Além dos slides” trazem complementos da literatura (Sipser, Hopcroft)."

C = []

# =====================================================================
# 0. MAPA
# =====================================================================
C += [
    H1("Visão geral: a grande pergunta da disciplina", numbered=False,
       intro="Existe um algoritmo para resolver este problema? E, se não existir, como provar isso?"),
    P("Toda a matéria é um único argumento em seis passos. Se você entender a **cadeia lógica** abaixo, qualquer questão de prova encaixa em algum elo."),
    T(["#", "Passo", "Ideia central", "Slide"],
      [["1", "**Formalizar “algoritmo”**", "Máquina de Turing (MT): fita infinita + controle + função de transição", "08"],
       ["2", "**Testar a robustez do modelo**", "Extensões (várias fitas, não-determinismo…) **não** aumentam o poder: tese de Church-Turing", "09, 10"],
       ["3", "**Classificar problemas**", "Recursivo (decidível) ⊂ recursivamente enumerável (semidecidível) ⊂ todas as linguagens", "10, 11"],
       ["4", "**Mostrar que há o impossível**", "Contagem: há mais linguagens do que MTs; ALG e HALT não são decidíveis", "11, 12"],
       ["5", "**Exibir um problema concreto sem solução**", "Linguagem diagonal L_{D} (não-RE), via diagonalização de Cantor", "12"],
       ["6", "**Espalhar a impossibilidade**", "Redução: se A se reduz a B e A é indecidível, B é indecidível", "13"]],
      widths=[1, 5, 9.5, 1.5], align=["c", "l", "l", "c"], size=9.5),
    BOX("lembrete", "As 6 definições que valem pontos", [
        "- **MT-decidível (recursiva)**: existe MT que **sempre para**, respondendo SIM/NÃO. = *algoritmo*.",
        "- **MT-aceitável (RE)**: existe MT que **aceita** exatamente as cadeias da linguagem (pode **entrar em loop** nas outras). = *procedimento*.",
        "- Decidível ⇒ RE (a volta é falsa). L decidível ⇔ **L e seu complemento são RE**.",
        "- **A_{MT}** e **PARA_{MT}** (problema da parada) são **RE e indecidíveis**; **L_{D}** é **não-RE**.",
        "- **A ≤_{m} B**: se B decidível ⇒ A decidível; se A indecidível ⇒ B indecidível (**o sentido importa!**).",
    ]),
]

# =====================================================================
# 1. MÁQUINA DE TURING
# =====================================================================
C += [
    H1("A Máquina de Turing",
       "Slide 08 · O modelo formal de algoritmo, proposto por Alan Turing em 1936 (cerca de 20 anos antes do primeiro computador digital)."),
    H2("A ideia: uma pessoa com lápis, borracha e papel infinito"),
    P("Turing formalizou a noção intuitiva de “efetivamente computável” imaginando uma pessoa que calcula com um instrumento de escrita e um apagador. "
      "O modelo é parecido com os computadores atuais: **fita** (memória/entrada/saída), **unidade de controle** (CPU, com um estado) e **programa** (função de transição)."),
    T(["Componente", "Papel", "Analogia"],
      [["**Fita**", "Dividida em **células**; dispositivo de **entrada, saída e memória**; infinita **à direita** (começa no marcador ⊗)", "Memória"],
       ["**Unidade de controle (UC)**", "Tem um **estado** corrente e uma **cabeça** que lê/escreve uma célula e se move L ou R", "CPU"],
       ["**Função de transição δ**", "A “programação”: dado (estado, símbolo lido) diz o que fazer", "Programa"]],
      widths=[4, 9.5, 3.5], size=9.5),
    H2("Definição formal"),
    BOX("def", "Máquina de Turing (slide 10)", [
        "= M = (Q, Σ, Γ, δ, q₀, β, F)",
        "- **Q**: conjunto **finito** de estados; **q₀ ∈ Q**: estado inicial.",
        "- **Γ**: alfabeto de **símbolos de fita**; **β ∈ Γ**: o símbolo **branco**. (O marcador de início de fita **⊗** também pertence a Γ.)",
        "- **Σ ⊆ Γ \\ {β}**: alfabeto de **entrada e saída** (não contém o branco).",
        "- **δ: Q × Γ → Q × Γ × {L, R}**: função de transição (parcial!).",
        "- **F ⊆ Q**: conjunto dos **estados finais** (de aceitação).",
    ]),
    BOX("def", "Como ler δ", [
        "= δ(qᵢ, a) = (qⱼ, b, x)      com  qᵢ, qⱼ ∈ Q ;  a, b ∈ Σ ∪ {β} ;  x ∈ {L, R}",
        "“No estado **qᵢ** lendo **a**: vá para **qⱼ**, **escreva b**, mova a cabeça para **x** (L = esquerda, R = direita)”.",
        "Três representações equivalentes: **(1) equações**, **(2) tabela** (|Q| linhas × |Γ| colunas, cada entrada é uma tripla) e **(3) diagrama de estados** (aresta de qᵢ a qⱼ rotulada **a/b, x**).",
    ]),
    BOX("erro", "Regras do marcador ⊗ (cai em prova)", [
        "- Se o símbolo lido é **diferente de ⊗**, o símbolo escrito **não pode ser ⊗** (⊗ só existe na 1ª célula).",
        "- Se a cabeça está em ⊗ (célula mais à esquerda), **só pode escrever ⊗ e não pode mover para a esquerda** (movimento inválido ⇒ a máquina para e **rejeita**).",
        "- δ pode ser **indefinida** para certos pares (estado, símbolo): a MT “**trava**” e para.",
    ]),
    H2("Computação, configurações e parada"),
    P("A computação começa no **estado inicial q₀**, com a **cabeça na célula mais à esquerda** (⊗) e a entrada w gravada à direita de ⊗. A cada passo aplica-se δ. "
      "Uma **configuração** é o “retrato” da máquina: **α q γ** — α é o que está à esquerda da cabeça, **q** o estado e **γ** o conteúdo **a partir da cabeça** (o 1º símbolo de γ é o que está sendo lido)."),
    BOX("exemplo", "Configurações da MT “Troca” (slide 08) com entrada abb", [
        CODE("""q₀⊗abbβ ⇒ ⊗q₁abbβ ⇒ ⊗bq₁bbβ ⇒ ⊗baq₁bβ ⇒ ⊗baaq₁β
        ⇒ ⊗baq₂aβ ⇒ ⊗bq₂aaβ ⇒ ⊗q₂baaβ   (configuração final)"""),
        "Em cada passo identifique α, q e γ. Ex.: em “⊗ba q₁ bβ”, α = ⊗ba, q = q₁, γ = bβ (a cabeça lê **b**).",
    ]),
    BOX("def", "Três condições de parada", [
        "1. **Estado final**: assume um estado de F ⇒ para e **aceita**.",
        "2. **Função indefinida** para (estado, símbolo) ⇒ para e **rejeita**.",
        "3. **Movimento inválido** (L estando em ⊗) ⇒ para e **rejeita**.",
        "Além disso, a MT pode **nunca parar** (loop infinito): nesse caso a entrada **não é aceita nem rejeitada**.",
    ]),
    H2("MT como reconhecedora e como computadora de funções"),
    B(["**Reconhecedora**: para uma entrada w, se para em estado ∈ F, w é **aceita/reconhecida**; se para em estado ∉ F, **rejeita**; se **nunca para**, w não é aceita nem rejeitada.",
       "M **reconhece** um conjunto X ⊆ Σ∗ se, para toda entrada, M **para** e aceita w ⇔ w ∈ X. (Σ∗ = fecho de Kleene: todas as palavras sobre Σ, incluindo a vazia.)",
       "**Computadora de função**: M **calcula** f: Σ∗ → Σ∗ se, para toda entrada w, M **para** e a saída (conteúdo da fita) é f(w)."]),
    H2("Exemplos resolvidos"),
    BOX("exemplo", "1) MT_bin_par: aceita binários pares", [
        "Q = {q₀, q₁, q₂}, Σ = {0,1}, F = {q₂}. A ideia: **ir até o fim** da entrada, **voltar uma célula** e testar o último bit (0 ⇒ par).",
        T(["Transição", "Significado"],
          [["δ(q₀, ⊗) = (q₀, ⊗, R)", "pula o marcador de início"], ["δ(q₀, 0) = (q₀, 0, R) · δ(q₀, 1) = (q₀, 1, R)", "anda para a direita sobre os bits"],
           ["δ(q₀, β) = (q₁, β, L)", "chegou ao fim: volta 1 célula"], ["δ(q₁, 0) = (q₂, 0, R)", "último bit **0** ⇒ estado final (**aceita**)"]],
          size=9.5, widths=[6, 5]),
        "Entrada **10**: q₀⊗10β ⇒ ⊗q₀10β ⇒ ⊗1q₀0β ⇒ ⊗10q₀β ⇒ ⊗1q₁0β ⇒ ⊗10q₂β (**aceita**).",
        "Entrada **11**: chega a ⊗1q₁1β; **δ(q₁, 1) é indefinida** ⇒ para e **rejeita**. Mesma coisa para 1011 e 101 (ímpares); 1010 e 10 são aceitas.",
    ]),
    BOX("exemplo", "2) MT “Troca” (computadora de função): troca a ↔ b e volta ao início", [
        T(["Q \\ Γ", "⊗", "a", "b", "β"],
          [["q₀", "q₁, ⊗, R", "–", "–", "–"], ["q₁", "–", "q₁, b, R", "q₁, a, R", "q₂, β, L"], ["q₂", "–", "q₂, a, L", "q₂, b, L", "–"]],
          align=["c"] * 5, size=9.5),
        "q₀ pula ⊗; q₁ vai **trocando** cada símbolo; ao ver β, q₂ **volta à esquerda** sem alterar até parar sobre ⊗ (sem transição ⇒ para). É uma **computadora de função**: o que importa é o **conteúdo final da fita**.",
    ]),
    BOX("exemplo", "3) Reconhecedora de {0ⁿ1ⁿ | n ≥ 0}", [
        "**Estratégia:** em cada rodada, marque um 0 (X), vá à direita marcar o 1 correspondente (Y), volte ao X mais à direita e repita. No fim, confira que **não sobraram 1’s**.",
        T(["Estado", "Transições", "Função"],
          [["q₀", "δ(q₀,⊗)=(q₀,⊗,R) · δ(q₀,β)=(q_f,β,R) · δ(q₀,0)=(q₁,X,R) · δ(q₀,Y)=(q₃,Y,R)", "Procura um 0 a marcar (ou passa para a verificação final)"],
           ["q₁", "δ(q₁,0)=(q₁,0,R) · δ(q₁,Y)=(q₁,Y,R) · δ(q₁,1)=(q₂,Y,L)", "Vai à direita, ignora 0 e Y, **marca o 1**"],
           ["q₂", "δ(q₂,Y)=(q₂,Y,L) · δ(q₂,0)=(q₂,0,L) · δ(q₂,X)=(q₀,X,R)", "Volta ao X mais à direita e recomeça"],
           ["q₃", "δ(q₃,Y)=(q₃,Y,R) · δ(q₃,β)=(q_f,β,R)", "Verifica que não há 1’s excedentes"]],
          size=9, widths=[1.6, 9.4, 6]),
        "Entrada **01**: ⊗01β → q₀ marca 0 (X) → q₁ lê 1, escreve Y, volta L → q₂ lê X → q₀ (R) lê Y → q₃ → lê β → **q_f (aceita)**.",
        "Entrada **011**: após marcar o primeiro par, q₀ lê o **1** que sobrou: **δ(q₀,1) indefinida** ⇒ para e **rejeita**. Entrada **vazia**: q₀ lê β ⇒ q_f ⇒ aceita (n = 0).",
    ]),
    BOX("exemplo", "4) Computadora da soma f(n₁, n₂) = n₁ + n₂ em notação unária", [
        "Entrada **1^{n₁} 0 1^{n₂}**, saída **1^{n₁+n₂}**. Exemplos dos slides: 111011 → 11111 (3+2); 1110111 → 111111 (3+3); “0” → β (0+0).",
        "**Ideia:** troque o separador **0 por 1** (agora há n₁+n₂+1 uns) e **apague um 1** (o último). Uma entrada sem separador (ex.: β) é rejeitada.",
    ]),
    BOX("insight", "Como projetar uma MT (receita dos slides)", [
        "(1) Resolva o problema **em linguagem natural** (algoritmo). (2) Pense em **como** a fita, a cabeça e os estados o executam (marcadores auxiliares, varreduras). "
        "(3) **Só depois** escreva a tabela/diagrama de δ. Estados = “o que a máquina está procurando agora”.",
    ]),
    BOX("erro", None, [
        "- Esquecer de **pular o ⊗** no início (δ(q₀, ⊗) = (q₀, ⊗, R)).",
        "- Esquecer que **“sem transição” = rejeitar** (não é erro de projeto: é a forma usual de rejeitar).",
        "- Confundir **aceitar** (para em F) com **parar** (pode parar rejeitando).",
        "- Em MT que **calcula função**, considerar a **aceitação**: o que vale é o conteúdo da fita ao parar.",
    ]),
    BOX("resumo", None, [
        "- MT = (Q, Σ, Γ, δ, q₀, β, F); δ: Q×Γ → Q×Γ×{L,R}, parcial. Fita infinita à direita, começa em ⊗.",
        "- Para: estado final (aceita), δ indefinida (rejeita), movimento inválido (rejeita); pode haver loop.",
        "- Reconhece linguagens ou calcula funções.",
    ]),
    EX([
        Q("Qual o conteúdo da fita e o estado final quando a MT “Troca” (tabela acima) processa a entrada **ba**?",
          ["Tape ⊗baβ. q₀⊗ → q₁ R; q₁ lê b → escreve a, R; q₁ lê a → escreve b, R; q₁ lê β → q₂, β, L; q₂ lê b → b, L; q₂ lê a → a, L; q₂ lê ⊗: sem transição ⇒ para.",
           "Fita final: **⊗abβ**, estado q₂ (a máquina **troca** os símbolos: ba → ab). Como q₂ não é final, não houve “aceitação”: é uma **computação de função**."]),
        Q("Use MT_bin_par e diga se aceita, rejeita ou entra em loop para as entradas **0**, **101**, **ε** (palavra vazia).",
          ["**0**: ⊗0β → … q₀ lê β → q₁, L → lê 0 → q₂ (final) ⇒ **aceita**.",
           "**101**: último bit 1: q₁ lê 1, **δ indefinida** ⇒ **rejeita**.",
           "**ε**: ⊗β → q₀ lê β → (q₁, β, L) volta para ⊗; **δ(q₁, ⊗) indefinida** ⇒ para e **rejeita**. Nenhuma entrada faz essa MT entrar em loop."]),
        Q("Faça o rastreamento de **0011** na MT de {0ⁿ1ⁿ}. Quais as quatro marcações que ocorrem na fita antes de aceitar?",
          ["⊗0011β → q₀: 0→X ⇒ ⊗X011; q₁ vai à direita (0 ignora), lê 1 → Y, L: ⊗X0Y1; q₂: 0 (L), X → q₀ (R): lê 0 → X: ⊗XXY1; q₁ ignora Y, lê 1 → Y, L: ⊗XXYY; q₂ ignora Y, vê X → q₀ (R) lê Y → q₃; q₃ ignora Y, lê β → **q_f: aceita**.",
           "Marcações: X, Y, X, Y (nessa ordem) — fita final ⊗XXYYβ."]),
        Q("Projete (descreva em alto nível e dê a tabela parcial) uma MT que **aceite as cadeias sobre {a,b} que terminam em a**.",
          ["Estados: q₀ (anda à direita), q₁ (volta 1 célula), q₂ (final). δ(q₀,⊗)=(q₀,⊗,R); δ(q₀,a)=(q₀,a,R); δ(q₀,b)=(q₀,b,R); δ(q₀,β)=(q₁,β,L); δ(q₁,a)=(q₂,a,R).",
           "(Mesmo desenho da MT_bin_par: o último símbolo decide.) Se o último for b, δ(q₁,b) é indefinida ⇒ rejeita."]),
        Q("V ou F: (a) δ é uma função total; (b) a MT pode escrever ⊗ em qualquer célula; (c) se a MT ficar em loop infinito, a entrada é rejeitada; (d) Σ não contém β.",
          "(a) **F** — é **parcial** (pode ser indefinida). (b) **F** — ⊗ só na 1ª célula. (c) **F** — loop = **nem aceita nem rejeita**. (d) **V**."),
    ]),
]

# =====================================================================
# 2. EXTENSÕES
# =====================================================================
C += [
    H1("Extensões da Máquina de Turing e equivalência",
       "Slide 09 · Variações que facilitam o projeto de MTs — e que NÃO aumentam o poder computacional."),
    H2("Por que estender a MT?"),
    B(["Usar **recursos adicionais** facilita a construção de MTs para funções complexas (máquinas mais compactas, com menos estados/transições e menor overhead).",
       "**Evidência empírica do poder da MT**: as extensões comprovadamente **não alteram** o conjunto de funções computáveis — reforça a **Tese de Church**."]),
    T(["Extensão", "O que muda"],
      [["Fita infinita nos **dois lados**", "Sem marcador de início de fita"],
       ["Fita **bidimensional** (ou k-pistas)", "Grade em vez de linha"],
       ["**Várias fitas** (k fitas)", "Cada fita com sua cabeça; muito usada em projetos"],
       ["Cabeça que **não se move**", "Opção ‘ficar parada’ (S) além de L/R"],
       ["**Várias cabeças** de leitura/escrita", "Mais de uma cabeça sobre a mesma fita"],
       ["**Não-determinismo**", "δ vira uma **relação**: várias transições possíveis para (estado, símbolo)"],
       ["**Combinação** de quaisquer das anteriores", "—"]],
      widths=[6, 11], size=9.5),
    BOX("exemplo", "Vantagem de múltiplas fitas: {aⁿbⁿcⁿ | n ≥ 0}... usando 4 fitas", [
        "Slide: MT com **4 fitas**: fita 1 guarda a entrada (nunca alterada); fitas 2, 3, 4 **contam** os a’s, b’s e c’s, respectivamente (um símbolo por ocorrência). "
        "Ao fim, compara-se se os três contadores têm o **mesmo tamanho**. Resultado: **menos estados**, mais simplicidade e menos overhead que a MT de 1 fita.",
    ]),
    H2("Como provar equivalência"),
    N(["Mostrar que a **MT estendida pode ser simulada** por uma MT básica (construir a básica e provar que imita corretamente a extensão).",
       "O sentido contrário (a básica é um caso particular da estendida) é, em geral, **trivial**."]),
    T(["Teorema", "Enunciado (resumo)", "Como é simulado"],
      [["**1**", "Fita infinita nos 2 lados ≡ MT básica", "Células **pares** = parte direita; **ímpares** = parte esquerda; ⊗ marca a fronteira"],
       ["**2**", "Fita bidimensional (ou k-pistas) ≡ básica", "Linearização da grade / pistas como tuplas"],
       ["**3**", "k fitas ≡ básica", "Cada célula guarda uma **2k-upla**: k símbolos das fitas + k marcas de onde está cada cabeça"],
       ["**4**", "Cabeça sem movimento ≡ básica", "‘Ficar’ = mover R e depois L"],
       ["**5**", "Várias cabeças ≡ básica", "Marcadores de posição das cabeças"],
       ["**6**", "Toda linguagem aceita por MT **não-determinística** é aceita por uma **determinística**", "Simula **todas as ramificações** (busca em largura na árvore de computações)"]],
      widths=[1.6, 8, 7.4], align=["c", "l", "l"], size=9),
    BOX("insight", "O que o não-determinismo muda (e o que não muda)", [
        "Muda a **facilidade de projeto** e, em geral, o **tempo** (a simulação determinística pode ser exponencialmente mais lenta — esse é o coração de P × NP). "
        "**Não muda** o conjunto de linguagens **reconhecíveis** (Teorema 6). Como uma MT não-determinística pode terminar com resultados diferentes, só faz sentido vê-la como **reconhecedora de linguagens**, não como computadora de funções.",
    ]),
    BOX("erro", None, [
        "- Achar que uma extensão “resolve mais problemas”: **nenhuma** resolve. Ela só torna a MT **mais cômoda** (ou mais rápida).",
        "- Confundir **poder computacional** (o que se consegue calcular) com **eficiência** (quanto tempo/espaço leva).",
        "- Esquecer que a prova de equivalência tem **duas partes**: construir a MT básica **e** provar a correção da simulação.",
    ]),
    BOX("resumo", None, [
        "- Fitas extras, cabeças extras, fita bi-infinita, parada, bidimensional e não-determinismo ⇒ **todas equivalentes** à MT básica.",
        "- Prova: simulação da extensão pela básica. Evidência a favor da Tese de Church.",
    ]),
    EX([
        Q("Por que se diz que as extensões da MT corroboram a Tese de Church?",
          "Porque modelos mais ricos (várias fitas, não-determinismo, etc.) acabam computando **exatamente as mesmas funções** que a MT básica: o limite da computação não muda quando enriquecemos o modelo, o que sugere que a MT captura toda a noção intuitiva de algoritmo."),
        Q("Descreva como uma MT de **1 fita** simula uma MT de **3 fitas**.",
          "Cada célula da fita única guarda uma **6-upla**: 3 componentes com os símbolos das 3 fitas e 3 componentes marcando a **posição da cabeça** de cada fita. "
          "Para simular um passo, varre-se a fita para ler os 3 símbolos marcados, aplica-se a transição e varre-se de novo para atualizar símbolos e marcas."),
        Q("V ou F: (a) uma MT não-determinística reconhece linguagens que nenhuma MT determinística reconhece; (b) fita bidimensional é equivalente à fita simples; (c) uma MT com várias fitas pode ser mais rápida que uma de 1 fita.",
          "(a) **F** — Teorema 6. (b) **V** — Teorema 2. (c) **V** — ganha-se em eficiência/simplicidade, não em poder."),
        Q("Projete em alto nível uma MT de 4 fitas para {w ∈ {a,b,c}∗ | w é uma permutação de aⁿbⁿcⁿ, n ≥ 0}.",
          "Fita 1 = entrada; varrer w uma vez: para cada **a** acrescentar um símbolo na fita 2, para cada **b** na fita 3, para cada **c** na fita 4 (rejeitar se aparecer símbolo fora de {a,b,c}). "
          "Depois mover as cabeças das fitas 2, 3 e 4 juntas para a direita; **aceita** se as três chegam a β **simultaneamente** (mesmo tamanho), rejeita caso contrário."),
    ]),
]

# =====================================================================
# 3. CHURCH-TURING E DECIDIBILIDADE
# =====================================================================
C += [
    H1("Tese de Church-Turing, decidibilidade e hierarquia de linguagens",
       "Slide 10 · O que significa “existir um algoritmo” e como classificar linguagens."),
    H2("Hipótese (tese) de Church-Turing"),
    BOX("def", "Enunciado", [
        "“A capacidade de computação representada pela Máquina de Turing é o **limite máximo** que pode ser atingido por qualquer dispositivo de computação.”",
        "**Noção intuitiva de algoritmo = algoritmos de Máquina de Turing.**",
        "- Como “algoritmo” é uma noção **intuitiva**, a tese **não é demonstrável** (é uma **hipótese/tese**, assumida verdadeira em toda a Ciência da Computação).",
    ]),
    BOX("insight", "Consequência prática", [
        "Qualquer linguagem de programação (Pascal, C, Python…) computa **as mesmas funções** que a MT. Se algo não é computável em C, não é computável em nenhuma outra linguagem. Por isso as provas deste curso escrevem **pseudocódigo** em vez de tabelas de MT.",
    ]),
    H2("Problemas de decisão como linguagens"),
    P("Um **problema de decisão** tem só respostas **SIM/NÃO**. Formaliza-se como **pertinência**: “a cadeia w pertence à linguagem L ⊆ Σ∗?” (L = conjunto das instâncias SIM). "
      "Assim, “existe um algoritmo para o problema?” vira **“existe uma MT para esta linguagem?”**"),
    BOX("def", "Como demonstrar existência ou inexistência de algoritmo", [
        "- **Existe** (decidível): **projetar uma MT que sempre para**, para qualquer entrada.",
        "- **Não existe** (indecidível): **prova por contradição / diagonalização de Cantor** ou **prova por redução**.",
    ]),
    H2("Decidibilidade × aceitabilidade"),
    T(["", "MT-**decidível** (recursiva)", "MT-**aceita** (RE)"],
      [["Definição", "Existe MT que **para sempre**: SIM se w ∈ L, **NÃO** se w ∉ L", "Existe MT que para com **SIM** se w ∈ L (se w ∉ L, **pode rejeitar ou entrar em loop**)"],
       ["Equivale a", "**Algoritmo**", "**Procedimento**"],
       ["Força", "Mais forte", "Mais fraca"]],
      widths=[3, 7, 7], size=9.5),
    BOX("def", "Linguagens associadas a uma MT M (todas ⊆ Σ∗)", [
        "- **ACEITA(M) = L(M)**: palavras para as quais M **para em estado final**.",
        "- **REJEITA(M)**: palavras para as quais M **para em estado não final**.",
        "- **LOOP(M)**: palavras para as quais M **processa indefinidamente**.",
        "Propriedades: ACEITA ∪ REJEITA ∪ LOOP = Σ∗ e **as três são disjuntas** (duas a duas). Complemento de ACEITA = REJEITA ∪ LOOP; complemento de REJEITA = ACEITA ∪ LOOP; complemento de LOOP = ACEITA ∪ REJEITA.",
    ]),
    BOX("lembrete", "Duas armadilhas de nomenclatura", [
        "- **Complemento de L(M) NÃO é REJEITA(M)** (falta o LOOP!). Só coincidem se M for um decisor (LOOP = ∅).",
        "- **Decidível = recursiva**; **aceitável = recursivamente enumerável (RE)**; ambos termos aparecem na prova.",
    ]),
    H2("Resultados básicos"),
    N(["**Teorema 1:** toda linguagem MT-decidível é MT-aceita. (A volta é **falsa**: A_{MT} é aceitável mas não decidível.)",
       "**Teorema 2:** se L é decidível, seu complemento **L̄ = Σ∗ − L** também é decidível. *Prova:* use o decisor de L e **troque** as respostas SIM/NÃO.",
       "**Propriedade 2:** **L é recursiva ⇔ L e L̄ são ambas RE.** (⇒ imediato. ⇐: rode as duas MTs **em paralelo**; exatamente uma vai aceitar; se for a de L, responda SIM; se for a de L̄, NÃO.)",
       "**Propriedade 3:** Recursivas ⊊ RE (a inclusão é **própria**: existe RE não recursiva, ex.: A_{MT})."]),
    H2("Hierarquia de linguagens e de problemas"),
    T(["Classe de problemas", "Classe de linguagens", "Existe MT que…"],
      [["**Solucionável** (decidível, totalmente solucionável)", "**Recursiva**", "aceita a linguagem **e para com toda entrada**"],
       ["**Parcialmente solucionável** (semidecidível, computável)", "**Recursivamente enumerável (RE)**", "**aceita** a linguagem; pode entrar em loop nas instâncias negativas"],
       ["**Não-solucionável** (indecidível)", "**Não recursiva**", "se existir MT que a aceite, ela **entra em loop** em alguma instância negativa (ou nem existe MT)"],
       ["**Totalmente insolúvel** (não computável)", "**Não-RE**", "**nenhuma** MT aceita a linguagem"]],
      widths=[5.2, 4.6, 7.2], size=9.5),
    CODE("""┌──────────────────────────────────────────────┐
│  Não-RE   (totalmente insolúveis)            │
│   ┌──────────────────────────────────────┐   │
│   │  RE (parcialmente solucionáveis)     │   │
│   │   ┌──────────────────────────┐       │   │
│   │   │  Recursivas (decidíveis) │       │   │
│   │   └──────────────────────────┘       │   │
│   │   Indecidíveis mas RE: A_MT, PARA_MT │   │
│   └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘""", "Mapa mental (Recursivas ⊂ RE ⊂ todas as linguagens)"),
    BOX("exemplo", "Onde cada exemplo dos slides mora", [
        "- **Recursivas (decidíveis):** {aⁿ | n ≥ 0}, as linguagens **regulares**, as **livres de contexto** (reconhecidas por autômato com pilha, determinístico ou não) e as **sensíveis ao contexto**, como {aⁿbⁿcⁿ | n ≥ 0} — estas **exigem uma MT**, mas a MT sempre para.",
        "- **RE e não recursiva (indecidíveis, mas semidecidíveis):** **A_{MT} = {⟨M,w⟩ | M aceita w}** e **PARA_{MT}**. Segundo o slide, “só esta é exclusivamente RE”.",
        "- **Não-RE:** a linguagem diagonal **L_{D}** (Seção 5) e o complemento de A_{MT}.",
    ]),
    BOX("erro", None, [
        "- Dizer “decidível = RE”: decidível ⊂ RE, **próprio**.",
        "- Dizer que “indecidível ⇒ não computável”: **A_{MT} e PARA_{MT} são indecidíveis e, ainda assim, RE (semidecidíveis/computáveis)**; **só L_{D} é não-RE**.",
        "- Esquecer que um **decisor** nunca entra em loop; um **reconhecedor** pode.",
    ]),
    BOX("resumo", None, [
        "- Church-Turing: algoritmo intuitivo = MT (tese, não teorema). Problema ↔ linguagem.",
        "- Decidível (recursiva) ⊊ RE ⊊ todas. L recursiva ⇔ L e L̄ RE. Decidível fechado por complemento.",
        "- ACEITA, REJEITA, LOOP particionam Σ∗.",
    ]),
    EX([
        Q("Uma MT M tem ACEITA(M) = {w | w termina em 0}, REJEITA(M) = {w | w termina em 1} e LOOP(M) = {ε}. M é um decisor? Qual a linguagem L(M)? O complemento de L(M) é REJEITA(M)?",
          ["**M não é decisor** (LOOP(M) ≠ ∅, ε faz M entrar em loop).",
           "L(M) = ACEITA(M) = {w | w termina em 0}.",
           "O complemento de L(M) é REJEITA(M) ∪ LOOP(M) = {w | termina em 1} ∪ {ε} — **não** é só REJEITA(M)."]),
        Q("Prove que, se L é decidível, então Σ∗ − L é decidível.",
          "Seja M um decisor de L. Construa M′ igual a M, mas que **inverte as respostas**: aceita quando M rejeita e rejeita quando M aceita. Como M sempre para, M′ sempre para e aceita exatamente as cadeias fora de L."),
        Q("Se L e L̄ são ambas RE, mostre que L é decidível.",
          "Sejam M₁ que aceita L e M₂ que aceita L̄. Construa M que, dada w, **simula M₁ e M₂ em paralelo** (alternando passos). Para toda w, **exatamente uma** das duas aceita (w ∈ L ou w ∈ L̄). Se M₁ aceita, M aceita; se M₂ aceita, M rejeita. M sempre para ⇒ decide L."),
        Q("Classifique cada afirmação como V ou F: (a) toda linguagem recursiva é RE; (b) toda linguagem RE é recursiva; (c) o complemento de uma linguagem recursiva é recursivo; (d) o complemento de uma linguagem RE é sempre RE.",
          "(a) **V**. (b) **F** (A_{MT}). (c) **V**. (d) **F** (o complemento de A_{MT} é não-RE; se ambos fossem RE, A_{MT} seria recursiva)."),
        Q("Que tipo de MT é preciso para provar que uma linguagem é **decidível**? E para provar que é **apenas RE**?",
          "Para **decidível**: uma MT que **sempre para** (decisor) aceitando exatamente a linguagem. Para **RE**: basta uma MT que **aceite** a linguagem (pode entrar em loop nas cadeias fora dela). Para mostrar que **não é decidível**, é preciso uma prova por contradição/diagonalização ou por redução."),
    ]),
]

# =====================================================================
# 4. COMPUTABILIDADE E PROBLEMAS INDECIDÍVEIS
# =====================================================================
C += [
    H1("Computabilidade e problemas indecidíveis: ALG e o problema da parada",
       "Slide 11 · Existem problemas sem solução algorítmica — e podemos prová-lo."),
    H2("Problema de decisão e classes de solucionabilidade"),
    P("Um problema de decisão cujas instâncias têm resposta SIM/NÃO é representado pela linguagem das instâncias SIM. Exemplo: “o binário é par?” ⇔ w ∈ L = {0, 10, 100, 110, 1000, …}. "
      "Se existe MT que sempre para e decide, M **decide** o problema e existe **algoritmo**. Exemplo clássico: **primalidade** — testar todos os fatores não triviais mostra que existe método (eficiência é outra questão)."),
    BOX("def", "Resumo das classes", [
        "- **Decidível / solucionável** ⇔ linguagem **recursiva**.",
        "- **Semidecidível / parcialmente solucionável / computável** ⇔ **RE** (para qualquer algoritmo que o resolva parcialmente e não é decidível, existe ao menos uma entrada que o faz **processar indefinidamente**).",
        "- **Indecidível** ⇔ não recursiva. **Totalmente insolúvel** ⇔ **não-RE** (nem solução parcial).",
        "- Todo solucionável é parcialmente solucionável; existem não solucionáveis que têm solução parcial; existem completamente insolúveis.",
    ]),
    BOX("insight", "Por que estudar o que não tem solução?", [
        "Para saber **quando parar de procurar** o algoritmo geral e **simplificar o problema**; para entender **limites** da computação; e porque um problema insolúvel conhecido serve de **ponto de partida para provar que outros também são** (princípio da **redução**).",
    ]),
    H2("Funções computáveis e a tese de Church"),
    P("Uma função é **computável** ⇔ existe MT que a compute. As **funções não computáveis** são aquelas para as quais nenhum procedimento efetivo pode ser formulado — logo **nenhum programa** de computador as calcula. "
      "Pela tese de Church, vale para **qualquer linguagem de programação**."),
    H2("Problema 1: a função ALG (“este procedimento é um algoritmo?”)"),
    P("Existe um procedimento **ALG(p)** que devolve true se p é um **algoritmo** (para em **todas** as entradas) e false caso contrário? **Não.** Prova por contradição, por **diagonalização/auto-referência**:"),
    CODE("""procedure Problema();
begin
   while ALG(Problema) do nil      { passa o próprio código de Problema }
end;""", "Procedimento “maldoso” construído a partir de ALG"),
    N(["Suponha que **Problema é algoritmo** ⇒ ALG(Problema) = **true** ⇒ o while **nunca termina** ⇒ Problema **não** é algoritmo. **Contradição.**",
       "Suponha que **Problema não é algoritmo** ⇒ ALG(Problema) = **false** ⇒ o while termina ⇒ Problema **é** algoritmo. **Contradição.**",
       "Logo **ALG não pode existir**."]),
    H2("Problema 2: o Problema da Parada (HALT)"),
    P("Existe um procedimento **HALT(p, x)** que devolve true se p **para** com a entrada x e false se p **não para**? **Não.**"),
    CODE("""procedure PROC(x: integer);
begin
   while HALT(PROC, x) do nil
end;""", "Mesmo truque: PROC usa HALT contra si mesmo"),
    B(["Se **PROC para** com x ⇒ HALT(PROC,x) = true ⇒ o while **não termina** ⇒ PROC não para. **Contradição.**",
       "Se **PROC não para** com x ⇒ HALT = false ⇒ o while termina ⇒ PROC para. **Contradição.** ⇒ **HALT não existe.**"]),
    BOX("lembrete", "Como reconhecer a estrutura da prova (serve para qualquer ‘não existe’)", [
        "1) **Suponha** que o procedimento existe. 2) Use-o para construir um programa **que se contradiz quando recebe a si mesmo** como entrada. 3) Mostre as **duas** hipóteses (para / não para) levando à contradição. 4) Conclua que o procedimento **não pode existir**.",
    ]),
    H2("Propriedades de procedimentos: decidível, não-decidível, semidecidível"),
    P("**Problema** e **propriedade** são duas formas de falar da mesma coisa. Uma propriedade P é **decidível** se existe algoritmo que, dado um procedimento, devolve **true** se tem P e **false** se não tem."),
    B(["**Decidíveis:** “um autômato finito reconhece uma linguagem regular”; “duas linguagens regulares são equivalentes”.",
       "**Teorema 1:** a propriedade “**para para toda entrada**” (isto é, “**é algoritmo**”) é **não-decidível** (se fosse decidível, seria o ALG que já provamos não existir).",
       "**Cuidado:** o teorema fala do caso **geral**. Para um programa específico (ex.: algoritmo de Euclides) **é possível** decidir que para. O que **não existe** é um algoritmo para **todo** programa p e entrada x.",
       "**Corolário:** se P é não-decidível, **¬P** também é não-decidível (se ¬P fosse decidível, inverta a resposta do decisor para decidir P). Logo “não para para alguma entrada” e “**não para para a entrada x**” são não-decidíveis."]),
    BOX("def", "Semi-decidibilidade", [
        "P é **semi-decidível** se existe procedimento que, dado proc, **responde true** quando proc tem P (mas **pode não terminar** quando não tem). Decidível ⇒ semi-decidível.",
        "- **Teorema 2:** “**para para a entrada x**” é semi-decidível (basta **executar** proc(x); se terminar, devolva true).",
        "- **Teorema 3:** **P e ¬P semi-decidíveis ⇒ P decidível** (execute os dois em **paralelo**; um deles responde true: se foi o de P, devolva true; se foi o de ¬P, devolva false).",
    ]),
    BOX("insight", "O corolário mais importante", [
        "“Para para x” é semi-decidível, mas **não** decidível. Se ¬“para para x” (“**não para**”) fosse semi-decidível, pelo Teorema 3 “para” seria decidível — falso. "
        "Logo, “**não para para x**” **não é sequer semi-decidível** (é a propriedade **não-RE**). *Aceitar que algo termina é fácil (espere); provar que algo **nunca** termina é impossível em geral.*",
    ]),
    BOX("extra", "Outros problemas indecidíveis citados", [
        "Problema das **palavras em grupos finitamente apresentados**; **ambiguidade** e equivalência de **gramáticas livres de contexto**; o problema de **planejamento de passagens aéreas** com tarifas (versão do slide). "
        "Fora dos slides, mas clássico: o **Teorema de Rice** diz que **toda propriedade não trivial do comportamento (da linguagem) de uma MT é indecidível** (ex.: “aceita a cadeia vazia?”, “aceita alguma cadeia?”, “aceita linguagem regular?”).",
    ]),
    BOX("erro", None, [
        "- Achar que “indecidível” significa que **nenhuma instância** pode ser decidida: indecidível = **não há algoritmo geral**; casos particulares podem ser resolvidos.",
        "- Confundir **semidecidível** com “quase decidível”: semidecidível significa que **só o SIM é garantido**.",
        "- Esquecer a **simetria**: P decidível ⇔ ¬P decidível; mas P semi-decidível ⇏ ¬P semi-decidível.",
    ]),
    BOX("resumo", None, [
        "- ALG e HALT não existem (prova por **auto-referência** / diagonalização).",
        "- P decidível ⇒ ¬P decidível. P semidec. e ¬P semidec. ⇒ P decidível.",
        "- “Para para x” é semidecidível mas não decidível; “**não para para x**” não é sequer semidecidível.",
    ]),
    EX([
        Q("Qual a diferença entre uma propriedade ser decidível e ser semi-decidível? Dê um exemplo de cada tipo (da parada).",
          "**Decidível:** o algoritmo **sempre** responde true/false. **Semi-decidível:** o procedimento responde **true** se a propriedade vale, mas pode **não terminar** se não vale. "
          "Exemplo: “para para a entrada x” é **semi-decidível** (simule); “o número é primo” é **decidível**."),
        Q("Refaça a prova de que HALT não existe, passo a passo, sem consultar as anotações.",
          ["Suponha HALT(p, x) que devolve true ⇔ p para com x. Defina PROC(x) = “while HALT(PROC, x) do nil”.",
           "Se PROC(x) para ⇒ HALT(PROC,x)=true ⇒ o laço nunca termina ⇒ PROC(x) não para. Contradição.",
           "Se PROC(x) não para ⇒ HALT(PROC,x)=false ⇒ o laço termina ⇒ PROC(x) para. Contradição. Logo HALT não existe."]),
        Q("A propriedade “o programa para para a entrada x” é semi-decidível. O que se pode concluir sobre “o programa **não** para para x”? Justifique com o Teorema 3.",
          "Se “não para” fosse semi-decidível, pelo Teorema 3 (P e ¬P semi-decidíveis ⇒ P decidível) “para” seria decidível, contradição com o problema da parada. Logo “**não para**” não é sequer semi-decidível."),
        Q("Marque V ou F: (a) se um problema é indecidível, nenhum programa específico dele pode ser analisado; (b) ALG existe se limitarmos aos programas em Pascal; (c) o corolário diz que se P é não-decidível, ¬P é não-decidível; (d) o Problema da Parada é semi-decidível.",
          "(a) **F** — instâncias particulares podem ser decididas. (b) **F** — Church: vale para qualquer linguagem. (c) **V**. (d) **V**."),
        Q("Por que a função ALG é considerada “diagonalização”?",
          "Porque se aplica o procedimento a **si mesmo** (Problema recebe seu próprio código) e a resposta é **invertida** — o mesmo esquema da diagonal de Cantor: constrói-se um objeto que **difere de cada item da lista justamente na posição diagonal**."),
    ]),
]

# =====================================================================
# 5. DIAGONALIZAÇÃO
# =====================================================================
C += [
    H1("Diagonalização de Cantor e a linguagem diagonal",
       "Slide 12 · Comparar o “tamanho” de conjuntos infinitos e exibir uma linguagem que NENHUMA MT reconhece."),
    H2("Comparando conjuntos: emparelhamento"),
    P("Para conjuntos finitos, contamos. Para infinitos, **Cantor** propôs: A e B têm o **mesmo tamanho** se existe um **emparelhamento** (correspondência um-a-um, uma **bijeção**) entre eles — sem contar."),
    BOX("def", "Contável (enumerável)", [
        "- Um conjunto infinito A é **enumerável/contável** se existe uma correspondência de A com os **naturais ℕ**. Caso contrário, é **incontável**.",
        "- Um conjunto qualquer é **contável** se é **finito** ou tem o mesmo tamanho que ℕ.",
    ]),
    BOX("exemplo", "Contáveis, apesar da intuição", [
        "- **Pares:** f(n) = 2n emparelha ℕ com {2, 4, 6, …}. Apesar de ser subconjunto próprio de ℕ, tem o **mesmo tamanho**!",
        "- **Racionais ℚ:** monte uma matriz infinita M_{ij} = i/j e percorra-a em **diagonais** (zigue-zague), numerando cada fração nova (1º, 2º, …) ⇒ ℚ ↔ ℕ (Sipser, p. 187).",
        "- **Σ∗** (todas as cadeias de um alfabeto) é contável: enumere por **tamanho crescente e ordem lexicográfica** (Σ={0,1}: ε, 0, 1, 00, 01, 10, 11, 000, …).",
    ]),
    H2("Os reais são incontáveis (a prova de Cantor)"),
    N(["**Suponha** que existe uma correspondência f entre ℕ e os reais (uma lista infinita f(1), f(2), f(3), …, cada um com sua expansão decimal).",
       "**Construa** um real x cujo **n-ésimo dígito decimal difere do n-ésimo dígito de f(n)** (ex.: se for 1 troque por 4, etc.).",
       "Então x **não é** f(1) (difere no 1º dígito), **não é** f(2) (difere no 2º)… x ≠ f(n) para todo n.",
       "Mas x é real e **ficou fora da lista**: contradição. Logo **ℝ é incontável**."]),
    BOX("intuicao", "Por que a “diagonal”?", [
        "Se você escrever a lista como uma tabela, os dígitos que você **modifica** estão na **diagonal**. O número novo é o “anti-diagonal”: por construção difere de toda linha.",
    ]),
    H2("Há mais linguagens (problemas) do que MTs (algoritmos)"),
    B(["**O conjunto de todas as MTs é contável:** toda MT pode ser **codificada** por uma cadeia ⟨M⟩ ∈ Σ∗; Σ∗ é contável; logo as MTs podem ser enumeradas.",
       "**O conjunto de todas as linguagens é incontável** (prova por diagonalização, abaixo).",
       "Cada MT reconhece **uma única** linguagem ⇒ **existem linguagens (problemas) que nenhuma MT (algoritmo) reconhece.**"]),
    BOX("exemplo", "Diagonalização em linguagens (slide)", [
        "Suponha uma enumeração L₁, L₂, L₃, … de todas as linguagens e uma lista w₁, w₂, … de cadeias. Tabela: célula (i, j) = **1 se wⱼ ∈ Lᵢ**.",
        T(["", "w₁", "w₂", "w₃", "w₄"],
          [["L₁", "**1**", "0", "0", "1"], ["L₂", "0", "**0**", "1", "0"], ["L₃", "1", "0", "**0**", "1"], ["L₄", "1", "1", "0", "**1**"], ["**L_{d}**", "0", "1", "1", "0"]],
          align=["c"] * 5, size=9.5),
        "L_{d} = **complemento da diagonal** (a diagonal é 1,0,0,1 ⇒ L_{d} = 0,1,1,0). L_{d} difere de **cada** Lᵢ na coluna i ⇒ **não está na lista** ⇒ a lista não era completa ⇒ **o conjunto de linguagens é incontável.**",
    ]),
    H2("A linguagem diagonal L_{D}: um problema concreto não-RE"),
    P("Resta exibir **uma** linguagem concreta que nenhuma MT reconhece. Para isso, **codifique** MTs como cadeias binárias: cada MT T tem um **índice/nome ⟨T⟩ ∈ {0,1}∗** (cadeias que não codificam MT valem por convenção como uma MT trivial que aceita ∅)."),
    BOX("def", "Matriz do argumento diagonal e a definição de L_{D}", [
        "- **W_{ij} = 1** se a MT Mᵢ **aceita** a cadeia wⱼ (wⱼ ∈ L(Mᵢ)); **W_{ij} = 0** caso contrário. Linhas = MTs (Mᵢ ∈ ℕ), colunas = cadeias (wⱼ ∈ ℕ). **Observe: as MTs são, elas próprias, cadeias das colunas** (wᵢ = ⟨Mᵢ⟩).",
        "= L_{D} = { ⟨Mᵢ⟩ : W_{ii} = 0 }",
        "Os slides dizem: “**Mᵢ que rejeita o próprio código está em L_{D}**”. Tecnicamente W_{ii} = 0 significa **M não aceita** ⟨M⟩ (rejeita **ou entra em loop**): L_{D} = {⟨M⟩ | M **não aceita** ⟨M⟩}. Com “só rejeita” a linguagem seria RE; é o “**não aceita**” que a torna não-RE.",
    ]),
    BOX("def", "Teorema: L_{D} é não-RE", [
        "**Prova (por contradição):** suponha L_{D} ∈ RE. Então existe MT **M_d** com L(M_d) = L_{D}. Seja k = ⟨M_d⟩ (M_d é uma linha da tabela). Considere a cadeia k:",
        "- Se **k ∈ L_{D}** ⇒ W_{kk} = 0 ⇒ M_d **não aceita** k ⇒ **k ∉ L(M_d) = L_{D}**. Contradição.",
        "- Se **k ∉ L_{D}** ⇒ W_{kk} = 1 ⇒ M_d **aceita** k ⇒ **k ∈ L(M_d) = L_{D}**. Contradição.",
        "Logo **M_d não existe** ⇒ **L_{D} é não-RE** (e portanto **indecidível**: nem semidecidível).",
    ]),
    BOX("insight", "Por que isso importa", [
        "L_{D} é o **primeiro problema concreto não-RE**. É a “semente” de tudo que vem depois: com **redução** a partir de L_{D} provam-se outros problemas não-RE (Seção 6). "
        "Também mostra a **mesma estrutura** das provas de ALG e HALT: aplicar algo a **si mesmo** e inverter a resposta.",
    ]),
    BOX("erro", None, [
        "- Confundir **contável** com **finito**: ℕ, ℤ, ℚ, pares, Σ∗ são infinitos **contáveis**.",
        "- Dizer que ℝ é contável “porque é infinito como ℕ”: **nem todo infinito é do mesmo tamanho**.",
        "- Na diagonal, esquecer de **complementar** a diagonal (a diagonal igual ao original **estaria** na lista).",
        "- Confundir a matriz **W** (indexada por MTs e cadeias) com a de linguagens (indexada por linguagens e cadeias).",
    ]),
    BOX("resumo", None, [
        "- Contável ⇔ bijeção com ℕ. ℕ, pares, ℚ, Σ∗, o conjunto das MTs: contáveis. ℝ e o conjunto de todas as linguagens: **incontáveis**.",
        "- Diagonalização: construir um objeto que difere do n-ésimo da lista no n-ésimo ponto.",
        "- L_{D} = {⟨M⟩ | M não aceita ⟨M⟩} é **não-RE**.",
    ]),
    EX([
        Q("Mostre que o conjunto ℤ dos inteiros é contável exibindo uma enumeração ℕ → ℤ.",
          "f(n) = n/2 se n é par; f(n) = −(n+1)/2 se n é ímpar. Isto gera 0, −1, 1, −2, 2, −3, 3, … : cada inteiro aparece **exatamente uma vez**, logo é uma bijeção. ℤ é contável."),
        Q("Dada a tabela (linha i = linguagem Lᵢ, coluna j = cadeia wⱼ; 1 = wⱼ ∈ Lᵢ) com L₁ = 1 1 0 0; L₂ = 0 1 0 1; L₃ = 1 0 0 0; L₄ = 1 1 1 0, determine a linguagem diagonal L_{d} e verifique que ela difere de cada Lᵢ.",
          ["Diagonal: (L₁,w₁)=1, (L₂,w₂)=1, (L₃,w₃)=0, (L₄,w₄)=0. Complemento: **L_{d} = 0 0 1 1**.",
           "L_{d} difere de L₁ em w₁ (0 ≠ 1), de L₂ em w₂ (0 ≠ 1), de L₃ em w₃ (1 ≠ 0) e de L₄ em w₄ (1 ≠ 0). Logo L_{d} ∉ {L₁…L₄}."]),
        Q("Por que “existem mais linguagens do que MTs” leva à conclusão de que há problemas indecidíveis?",
          "O conjunto de MTs é **contável** e cada MT reconhece **uma** linguagem; portanto no máximo **uma quantidade contável** de linguagens é reconhecível. O conjunto de **todas** as linguagens é **incontável**, então sobram linguagens que **nenhuma MT** reconhece (e, a fortiori, nenhuma decide)."),
        Q("Na prova de que L_{D} é não-RE, explique por que k = ⟨M_d⟩ gera contradição nos dois casos.",
          "Se k ∈ L_{D}, então por definição M_d **não aceita** k (W_{kk} = 0), logo k ∉ L(M_d) = L_{D} — absurdo. Se k ∉ L_{D}, então W_{kk} = 1, ou seja, M_d aceita k e k ∈ L(M_d) = L_{D} — absurdo. A hipótese de que M_d existe é falsa."),
        Q("V ou F: (a) o conjunto das MTs é incontável; (b) ℚ é contável; (c) L_{D} é RE, mas não recursiva; (d) cada MT tem um índice binário ⟨M⟩.",
          "(a) **F** — contável. (b) **V**. (c) **F** — L_{D} é **não-RE**. (d) **V**."),
    ]),
]

# =====================================================================
# 6. REDUTIBILIDADE
# =====================================================================
C += [
    H1("Redutibilidade",
       "Slide 13 · A ferramenta para espalhar (in)decidibilidade de um problema para outro."),
    H2("A ideia de redução"),
    P("**Reduzir A a B** (A → B) é converter o problema A em B: **se tenho solução para B, tenho solução para A** (uso a solução de B como sub-rotina). "
      "Logo **resolver A não é mais difícil que resolver B** (B é “pelo menos tão difícil quanto” A)."),
    BOX("def", "Consequências (decore!)", [
        "Se **A é redutível a B**:",
        "- **B decidível ⇒ A decidível.**",
        "- **A indecidível ⇒ B indecidível.**   (← a principal ferramenta para provar indecidibilidade)",
        "- **A decidível NÃO implica B decidível.**   - **B indecidível NÃO implica A indecidível.**",
    ]),
    BOX("exemplo", "A analogia do sorvete (slide)", [
        "A = “conseguir R$ 2,00 para uma casquinha”; B = “criar uma start-up e virar bilionário”. A se reduz a B (se sei ser bilionário, sei comprar a casquinha). "
        "Isso mostra que B é **pelo menos tão difícil** quanto A — **não** que A seja tão difícil quanto B.",
        "Outro exemplo: A = “o aluno passou em todas as disciplinas?”; B = “o aluno vai se formar?”. B **precisa** de A: se A é NÃO ⇒ B é NÃO; se B é SIM ⇒ A é SIM. Mas A = SIM não decide B (faltam outros requisitos), e B = NÃO não diz nada sobre A.",
    ]),
    BOX("erro", "O erro nº 1 da matéria: inverter o sentido", [
        "Para provar que **B é indecidível**, reduza de um problema **A já sabidamente indecidível PARA B** (A ≤ B). Reduzir B → A (**ao contrário**) **não prova nada**! "
        "Memorize: “**indecidível entra à esquerda, o novo problema à direita**”.",
    ]),
    H2("Exemplo 1: A_{MT} → PARA_{MT} (Redução de Turing)"),
    P("Definições: **A_{MT} = {⟨M,w⟩ | M é MT e M aceita w}** (aceitação) e **PARA_{MT} = {⟨M,w⟩ | M é MT e M para sobre w}** (problema da parada). A_{MT} é indecidível (e RE). Prove que PARA_{MT} é indecidível:"),
    CODE("""Suponha que a MT R decide PARA_MT.
Construa S que decide A_MT, sobre a entrada <M,w>:
 1. Rode R sobre <M,w>.                    (R decide se M PARA)
 2. Se R rejeita: M não para ⇒ M não aceita w ⇒ rejeite <M,w>.
 3. Se R aceita: M para ⇒ simule M sobre w até parar (termina!).
 4. Se M aceitou: aceite <M,w>;  se M rejeitou: rejeite <M,w>.
Se R existisse, S decidiria A_MT — contradição (A_MT é indecidível).
Logo PARA_MT é indecidível.""", "Prova por contradição (slide)"),
    P("Observe: **R é usada como sub-rotina** e ainda se faz **uma simulação adicional** — esse tipo de redução mais geral chama-se **Redução de Turing**."),
    H2("Redutibilidade por mapeamento (≤ₘ)"),
    BOX("def", "Definição formal", [
        "Uma função **f: Σ∗ → Σ∗** é **computável** se existe uma MT que, para toda entrada w, **para** com f(w) na fita.",
        "= A ≤_{m} B  ⇔  existe f computável tal que  ∀w ∈ Σ∗:   w ∈ A  ⇔  f(w) ∈ B",
        "f é a **redução** de A para B: **instâncias SIM de A ↦ instâncias SIM de B; instâncias NÃO de A ↦ instâncias NÃO de B.** (Preserva as duas coisas!)",
    ]),
    BOX("exemplo", "Exemplo numérico do slide", [
        "A = números **pares**; B = **múltiplos de 4**; f(n) = **2n**.",
        T(["n", "n ∈ A?", "f(n) = 2n", "f(n) ∈ B?"], [["2", "SIM", "4", "SIM"], ["3", "NÃO", "6", "NÃO"], ["4", "SIM", "8", "SIM"], ["5", "NÃO", "10", "NÃO"]],
          align=["c"] * 4, size=9.5),
        "n ∈ A ⇔ 2n ∈ B (n é par ⇔ 2n é múltiplo de 4) ⇒ **A ≤_{m} B**.",
    ]),
    BOX("def", "Teoremas da redução por mapeamento", [
        "- **Se A ≤_{m} B e B é decidível, então A é decidível.** (Decisor de A: calcule f(w), rode o decisor de B.)",
        "- **Corolário: se A ≤_{m} B e A é indecidível, então B é indecidível.**",
        "- (Máquina de redução, versão do slide, com L_A ≤ L_B): **(a)** L_B recursiva ⇒ L_A recursiva; **(b)** L_B RE ⇒ L_A RE; **(c)** L_A não recursiva ⇒ L_B não recursiva; **(d)** **L_A não-RE ⇒ L_B não-RE** (c e d são as contrapositivas de a e b).",
    ]),
    CODE("""Para provar que B é indecidível (receita):
 1. Assuma, por contradição, que B é decidível por uma MT R.
 2. Escolha um problema A CONHECIDO indecidível.
 3. Mostre A ≤m B: construa a MT que computa f (instância de A -> instância de B).
 4. Então S = "Sobre w: calcule f(w); rode R sobre f(w); aceite se R aceitar, rejeite se rejeitar"
    decide A.  CONTRADIÇÃO.  Logo B é indecidível.""", "Receita de prova"),
    BOX("exemplo", "Exemplo 2: A_{MT} ≤ₘ PARA_{MT} por mapeamento", [
        "A função f leva ⟨M, w⟩ a ⟨M′, w⟩, onde **M′** é uma máquina construída a partir de M: **M′ = “Sobre a entrada x: (1) rode M sobre x; (2) se M aceita, aceite; (3) se M rejeita, ENTRE EM LOOP.”**",
        T(["Caso", "M sobre w", "⟨M,w⟩ ∈ A_{MT}?", "M′ sobre w", "⟨M′,w⟩ ∈ PARA_{MT}?"],
          [["1", "aceita", "SIM", "para (aceita)", "SIM"], ["2", "rejeita", "NÃO", "loop (forçado)", "NÃO"], ["3", "loop", "NÃO", "loop (da simulação)", "NÃO"]],
          align=["c"] * 5, size=9),
        "SIM ↔ SIM e NÃO ↔ NÃO ⇒ ⟨M,w⟩ ∈ A_{MT} ⇔ ⟨M′,w⟩ ∈ PARA_{MT}. **M′ é necessária** porque, numa MT, **rejeitar = parar**; no mapeamento precisamos transformar “rejeita” em “não para”.",
    ]),
    BOX("extra", "Padrão para outras reduções (ex.: prove que B = {⟨M⟩ | M aceita ε} é indecidível)", [
        "Reduza A_{MT} a B: f(⟨M,w⟩) = ⟨M′⟩, onde **M′ ignora sua entrada e simula M sobre w** (aceita se M aceitar w). Então M aceita w ⇔ M′ aceita **ε** (aceita toda entrada). "
        "A construção “**M′ ignora a entrada, simula M sobre w**” é a ferramenta clássica e aparece em muitas reduções (veja também o Teorema de Rice).",
    ]),
    BOX("erro", None, [
        "- **Direção da redução** (o item de maior risco).",
        "- Esquecer de provar que **f é computável** (a MT que calcula f deve **sempre parar**).",
        "- Esquecer que f deve valer nos **dois sentidos** (⇔): SIM→SIM **e** NÃO→NÃO.",
        "- Usar redução para provar **decidibilidade** apontando uma solução de A para B (sentido errado): para decidir A, reduza A **para** um B já decidível.",
        "- Confundir redução de **Turing** (sub-rotina, resposta de R pode ser usada de qualquer forma) com redução por **mapeamento** (uma conversão f, uma única consulta, resposta idêntica).",
    ]),
    BOX("resumo", None, [
        "- A ≤ B: solução de B resolve A. B decidível ⇒ A decidível; A indecidível ⇒ B indecidível.",
        "- Mapeamento: f computável com w ∈ A ⇔ f(w) ∈ B. Receita: assumir B decidível, reduzir de um A indecidível, contradição.",
        "- A_{MT} ≤ PARA_{MT} usa M′ que entra em loop quando M rejeita.",
    ]),
    EX([
        Q("Seja A ≤ₘ B. Classifique: (a) se B é decidível, então A é decidível; (b) se A é indecidível, então B é indecidível; (c) se A é decidível, então B é decidível; (d) se B é indecidível, então A é indecidível; (e) se B é RE, então A é RE; (f) se A não é RE, então B não é RE.",
          "(a) **V**; (b) **V**; (c) **F**; (d) **F**; (e) **V**; (f) **V** (contrapositiva de e). Observe que só valem as implicações “de B para A” para propriedades **positivas** (decidível, RE) e “de A para B” para propriedades **negativas** (indecidível, não-RE)."),
        Q("Sejam A = {w ∈ {0,1}∗ | w começa com 0} e B = {w ∈ {0,1}∗ | w termina com 1}. Mostre que A ≤ₘ B definindo f.",
          "f(w) = **“1”** se w começa com 0 (primeiro símbolo = 0) e f(w) = **“0”** caso contrário (inclusive w = ε). f é computável (olha o 1º símbolo e escreve 1 ou 0). "
          "Então w ∈ A ⇔ f(w) = 1 ∈ B (termina com 1) e w ∉ A ⇔ f(w) = 0 ∉ B. Logo A ≤ₘ B."),
        Q("A = números pares, B = múltiplos de 4. Para cada candidato a f diga se é redução válida de A a B (se não, dê contraexemplo): (a) f(n) = n; (b) f(n) = 2n; (c) f(n) = 4.",
          ["(a) **Inválida:** n = 2 ∈ A mas f(2) = 2 ∉ B.",
           "(b) **Válida:** n par ⇔ 2n múltiplo de 4.",
           "(c) **Inválida:** n = 3 ∉ A, mas f(3) = 4 ∈ B (a constante 4 mapeia tudo para uma instância SIM)."]),
        Q("Sabemos que L_{D} é não-RE. Se L_{D} ≤ₘ L, o que se conclui sobre L?",
          "Pela contrapositiva de “L RE ⇒ L_{D} RE”: como L_{D} **não é RE**, **L também não é RE** (nem decidível, nem semidecidível)."),
        Q("Prove que B = {⟨M⟩ | M aceita a cadeia vazia ε} é indecidível, reduzindo A_{MT} a B. (Dica do slide: M′ ignora a própria entrada e simula M sobre w.)",
          ["Suponha R decide B. Defina S sobre ⟨M, w⟩: **(1)** construa M′ = “sobre qualquer entrada x: ignore x, simule M sobre w; se M aceita, aceite; se rejeita, rejeite”. **(2)** Rode R sobre ⟨M′⟩ e responda o que R responder.",
           "M′ aceita ε ⇔ M aceita w. Logo S decide A_{MT}, o que é impossível. Portanto B é **indecidível**.",
           "(f(⟨M,w⟩) = ⟨M′⟩ é computável: só escreve o código de M′ a partir de M e w.)"]),
        Q("Descreva por que, na prova de A_{MT} ≤ PARA_{MT} via mapeamento, a máquina M′ precisa entrar em loop quando M rejeita.",
          "Porque, numa MT, **rejeitar é parar**. Se M′ também parasse ao rejeitar, o caso “M rejeita w” (resposta NÃO em A_{MT}) viraria “M′ para” (resposta SIM em PARA_{MT}), quebrando a equivalência. Forçando o loop, “não aceita” vira “não para” e a correspondência SIM↔SIM, NÃO↔NÃO fica correta."),
    ]),
]

# =====================================================================
# 7. COLA
# =====================================================================
C += [
    H1("Cola de última hora e erros comuns", "Releia na véspera."),
    H2("Definições em uma página"),
    T(["Conceito", "Lembrar"],
      [["MT", "M = (Q, Σ, Γ, δ, q₀, β, F); δ: Q×Γ → Q×Γ×{L,R} parcial; fita à direita, ⊗ = início; configuração α q γ"],
       ["Parada", "estado final = aceita; δ indefinida = rejeita; movimento inválido = rejeita; ou LOOP (nem aceita nem rejeita)"],
       ["Extensões", "multifita, 2D, bi-infinita, sem movimento, multicabeça, não-determinismo ⇒ **todas equivalentes** à MT básica"],
       ["Church-Turing", "algoritmo intuitivo = MT (tese, não demonstrável)"],
       ["Decidível", "MT que **sempre para** = recursiva = algoritmo"],
       ["Aceitável", "MT que aceita (pode loop) = RE = procedimento"],
       ["ACEITA/REJEITA/LOOP", "particionam Σ∗; complemento de ACEITA = REJEITA ∪ LOOP"],
       ["Fechamento", "Decidível: fechada por complemento. RE: **não** (em geral)"],
       ["L recursiva", "⇔ L e L̄ são RE"],
       ["Hierarquia", "Recursivas ⊊ RE ⊊ todas as linguagens (não-RE existem)"],
       ["ALG, HALT", "não existem; provas por auto-referência"],
       ["PARA_MT, A_MT", "indecidíveis mas RE (semidecidíveis)"],
       ["L_D", "{⟨M⟩ | M não aceita ⟨M⟩} é não-RE"],
       ["Contagem", "MTs contáveis, linguagens incontáveis ⇒ há problemas sem algoritmo"],
       ["P e ¬P", "P semidec. e ¬P semidec. ⇒ P decidível. “não para” não é semidecidível"],
       ["Redução", "A ≤ B: B decidível⇒A decidível; A indecidível⇒B indecidível; **indecidível à esquerda**"],
       ["Mapeamento", "f computável (sempre para); w ∈ A ⇔ f(w) ∈ B (SIM↔SIM, NÃO↔NÃO)"]],
      widths=[3.8, 13.2], size=9.5),
    H2("Os 10 erros que mais custam pontos"),
    N(["Esquecer de **pular ⊗** e de tratar o **movimento inválido** em ⊗.",
       "Confundir **rejeitar** (parar fora de F) com **loop** (nunca parar).",
       "Dizer que complemento de L(M) é REJEITA(M) (falta **LOOP**).",
       "Achar que extensões da MT aumentam o poder computacional.",
       "**Decidível ≠ RE**: recursiva ⊊ RE; RE **não** é fechada pelo complemento.",
       "Provas de “não existe”: esquecer de mostrar **os dois casos** (para / não para).",
       "Inverter a **direção da redução** (a boa é: indecidível → novo problema).",
       "Esquecer de provar que f é **computável** e vale **⇔** (SIM→SIM e NÃO→NÃO).",
       "Confundir PARA_MT (parada, **RE**) com L_D (**não-RE**).",
       "Chamar ℝ (ou o conjunto de linguagens) de contável; ou chamar o conjunto de MTs de incontável."]),
    H2("Mini-simulado final"),
    EX([
        Q("Associe: (1) decidível; (2) semidecidível; (3) não-RE — com: a) A_{MT}; b) L_{D}; c) {aⁿbⁿ | n ≥ 0}.",
          "(1)-c; (2)-a; (3)-b."),
        Q("Um colega diz: “O problema da parada é indecidível, então nenhum programa pode ser verificado por um compilador.” Responda.",
          "Falso: indecidível significa que **não existe algoritmo geral** para **todo** programa e entrada. Casos particulares (e muitas classes restritas) são decidíveis; por exemplo, o algoritmo de Euclides sempre para; e o problema da parada é **semi-decidível** (simule e espere). Compiladores usam análises aproximadas ou restritas."),
        Q("Dado A ≤ₘ B, A indecidível. O que pode ser concluído de B? E se fosse B ≤ₘ A, com A indecidível?",
          "De A ≤ₘ B com A indecidível: **B é indecidível**. De B ≤ₘ A com A indecidível: **nada se conclui** (B poderia até ser decidível; A é que pode ser “mais difícil”)."),
        Q("Esboce uma prova de que “M para para alguma entrada” **não** é decidível usando redução de PARA_{MT}.",
          "Dada ⟨M,w⟩, construa M′ = “ignore a entrada e simule M sobre w”. M′ para para **alguma** (na verdade, toda) entrada ⇔ M para sobre w. Logo PARA_{MT} ≤ₘ (propriedade “para para alguma entrada”); como PARA_{MT} é indecidível, a propriedade é indecidível."),
    ], title="Exercícios — Mini-simulado"),
]
