# -*- coding: utf-8 -*-
from guide_builder import *

COLOR = "1565C0"  # azul
TITLE = "Aprendizado de Máquina"
PROF = "Prof. Gustavo T. Naozuka · Ciência da Computação · UEL"
EXAM = "30/11/2026"
SOURCES = "Slides ML 01–06 (Árvores de decisão ID3/C4.5 · Perceptron · MLP · Regressão linear · K-means)"
TOPICS = ["Árvores de Decisão (ID3 e C4.5)", "Perceptron", "MLP e Backpropagation", "Regressão Linear", "K-means"]

C = []

# =====================================================================
# 0. MAPA DA DISCIPLINA
# =====================================================================
C += [
    H1("Visão geral: o mapa da matéria", numbered=False, intro=
       "Antes dos detalhes, entenda onde cada técnica se encaixa. Metade das dúvidas de prova some quando você sabe classificar o problema."),
    P("Todos os métodos desta prova aprendem **a partir de dados**. A primeira pergunta diante de qualquer problema é: "
      "*eu tenho rótulos (a resposta certa) nos dados de treino?*"),
    T(["Tipo de aprendizado", "Dados", "Saída", "Nesta prova"],
      [["**Supervisionado — classificação**", "Exemplos com rótulo (classe)", "Categoria (Sim/Não, A/B/C)", "Árvores de decisão (ID3, C4.5), Perceptron, MLP"],
       ["**Supervisionado — regressão**", "Exemplos com valor numérico alvo", "Número contínuo (preço, nota)", "Regressão linear simples e múltipla"],
       ["**Não supervisionado**", "Exemplos **sem** rótulo", "Estrutura/grupos nos dados", "K-means (agrupamento)"]],
      widths=[3.2, 3.6, 3.8, 5], size=9.5),
    BOX("insight", "Um fio condutor entre as seis aulas", [
        "- **Árvores:** o modelo é um conjunto de regras *se–então*; aprende dividindo os dados com uma métrica de *impureza* (entropia).",
        "- **Perceptron → MLP:** o modelo é uma função com *pesos*; aprende **corrigindo erros** (regra do Perceptron) ou **descendo o gradiente** (backpropagation).",
        "- **Regressão linear:** o modelo é uma reta/plano; aprende **minimizando a soma dos quadrados dos erros** (mínimos quadrados).",
        "- **K-means:** sem rótulos; aprende **minimizando a distância quadrática** dos pontos aos centroides.",
        "Repare: *aprender = escolher parâmetros que minimizam uma medida de erro/impureza.* Muda a medida e o método de busca, mas a ideia é a mesma.",
    ]),
    BOX("lembrete", None, [
        "A prova costuma cobrar **contas à mão** (entropia, ganho, razão de ganho, passos do Perceptron, forward pass, reta de mínimos quadrados, iteração do K-means) e **perguntas conceituais** "
        "(por que XOR não é linearmente separável? o que a poda faz? como escolher k?). Este guia treina os dois tipos.",
    ]),
]

# =====================================================================
# 1. ÁRVORES DE DECISÃO + ID3
# =====================================================================
C += [
    H1("Árvores de Decisão e o Algoritmo ID3",
       "Slide 01 · Modelo interpretável que aprende regras dividindo os dados em subconjuntos cada vez mais “puros”."),
    H2("O que é uma árvore de decisão"),
    P("Uma árvore de decisão é um modelo preditivo que mapeia observações sobre uma variável-alvo. Serve para **classificação** e para **regressão**. "
      "É popular porque é *interpretável*: dá para ler o caminho raiz → folha e entender **por que** o modelo previu aquilo. "
      "É também a base de métodos mais fortes, como **Random Forest** e **Gradient Boosting**."),
    T(["Componente", "O que é", "Analogia (jogo de 20 perguntas)"],
      [["**Nó raiz**", "Primeiro nó; contém todos os dados", "A primeira pergunta que você faz"],
       ["**Nó interno**", "Teste sobre um atributo", "“É maior que 1 m?”"],
       ["**Ramo**", "Cada resultado possível do teste", "As respostas “sim”/“não”"],
       ["**Folha**", "Classe final (decisão)", "O palpite final"]],
      widths=[3, 6.5, 7.5], size=10),
    H2("Como a árvore é construída (esqueleto recursivo)"),
    CODE("""função ConstruirÁrvore(dados)
  se todos os exemplos têm a MESMA classe:  retorne folha(classe)
  se não há atributos ou critério de parada: retorne folha(classe mais frequente)
  A ← melhor atributo para dividir dados
  nó ← nó de decisão em A
  para cada valor v de A:
      dados_v ← exemplos com A = v
      conectar ConstruirÁrvore(dados_v) ao nó pelo ramo v
  retorne nó""", "Pseudocódigo geral (slide 11)"),
    P("É um algoritmo **guloso (greedy), top-down e recursivo**: em cada nó escolhe o melhor atributo *naquele momento*, sem voltar atrás. "
      "A pergunta central de todo algoritmo de árvore é: **o que significa “melhor atributo”?**"),
    BOX("def", "Critérios de parada", [
        "- **Profundidade máxima** atingida;",
        "- **Quantidade mínima** de exemplos no nó;",
        "- **Homogeneidade**: (quase) todos os exemplos do nó são da mesma classe;",
        "- **Sem atributos** restantes para dividir.",
        "Servem para evitar árvores gigantes e favorecer a **generalização** para dados novos.",
    ]),
    BOX("intuicao", None, [
        "Dividir bem = produzir subconjuntos **mais homogêneos** que o conjunto original. "
        "Um nó com 7 “Sim” e 0 “Não” é ótimo (decisão óbvia); um nó com 4 “Sim” e 4 “Não” é inútil (moeda ao ar). "
        "A **impureza** mede o quão “misturadas” estão as classes. Métricas: **Ganho de Informação** (ID3), **Razão de Ganho** (C4.5), **Índice de Gini** (CART).",
    ]),
    H2("Regiões de decisão"),
    P("Cada nó interno define uma regra do tipo *atributo ≤ limiar*, que corta o espaço dos atributos com um **hiperplano paralelo a um eixo**. "
      "Resultado: o espaço é particionado em **regiões retangulares**, cada folha corresponde a uma região associada a uma classe. "
      "Quanto mais profunda a árvore, mais fragmentada (e mais propensa a overfitting) fica a partição."),
    BOX("insight", None, [
        "Como as fronteiras são “degraus” alinhados aos eixos, árvores têm dificuldade com fronteiras diagonais suaves (que um Perceptron faz com uma única reta). "
        "Em compensação, modelam **relações não lineares** e misturam atributos numéricos e categóricos sem precisar normalizar nada.",
    ]),
    H2("Entropia: medindo a incerteza"),
    BOX("def", "Entropia de um conjunto S", [
        "= Entropia(S) = − Σ_{i=1..c}  p_{i} · log_{2}(p_{i})",
        "- **S**: conjunto de exemplos no nó; **c**: número de classes; **p_{i}**: proporção de exemplos de S na classe *i*.",
        "- Convenção: 0 · log₂ 0 = 0.",
    ]),
    T(["Distribuição em S (binário)", "Entropia", "Interpretação"],
      [["[4+ , 0−]  ou  [0+ , 4−]", "**0**", "Conjunto puro — nenhuma incerteza"],
       ["[6+ , 2−]", "0,811", "Pouco misturado"],
       ["[9+ , 5−]  (Jogar Tênis)", "0,940", "Bem misturado"],
       ["[4+ , 4−]  (50 %/50 %)", "**1** (máximo p/ 2 classes)", "Incerteza máxima"]],
      widths=[6, 4, 7], align=["l", "c", "l"]),
    BOX("lembrete", None, [
        "Entropia **mínima = 0** (conjunto puro) e **máxima = log₂(c)** (classes igualmente prováveis). Para 2 classes o máximo é 1; para 4 classes equiprováveis, 2.",
        "Dica de cálculo: com a calculadora, log₂(x) = ln(x)/ln(2). Decore: log₂(2)=1, log₂(4)=2, log₂(8)=3, log₂(1/2)=−1.",
    ]),
    H2("Ganho de Informação e o algoritmo ID3"),
    BOX("def", "Ganho de Informação", [
        "= Ganho(S, A) = Entropia(S) − Σ_{v ∈ Valores(A)}  ( |S_{v}| / |S| ) · Entropia(S_{v})",
        "É a **redução esperada da entropia** ao dividir S pelo atributo A. O ID3 escolhe o atributo de **maior ganho**.",
    ]),
    P("**ID3 (Iterative Dichotomiser 3):** constrói a árvore recursiva e top-down; em cada nó calcula o ganho de todos os atributos *ainda disponíveis*, "
      "escolhe o maior, cria um ramo para cada valor e **remove o atributo** da lista nas chamadas recursivas. Para quando o nó é puro ou não restam atributos "
      "(neste caso, folha com a classe mais frequente)."),
    BOX("exemplo", "Jogar Tênis (14 dias: 9 Sim, 5 Não)", [
        "# 1) Entropia do conjunto",
        "= E(S) = −(9/14)·log₂(9/14) − (5/14)·log₂(5/14) ≈ 0,940",
        "# 2) Ganho da Umidade (Alta: 3 Sim e 4 Não; Normal: 6 Sim e 1 Não)",
        "= E(Alta) ≈ 0,985  ·  E(Normal) ≈ 0,591",
        "= Ganho(S, Umidade) = 0,940 − (7/14)·0,985 − (7/14)·0,591 ≈ 0,151",
        "# 3) Ganhos de todos os atributos",
        T(["Atributo", "Ganho"], [["**Tempo**", "**0,246**"], ["Umidade", "0,151"], ["Vento", "0,048"], ["Temperatura", "0,029"]],
          widths=[5, 3], align=["l", "c"], size=9.5),
        "# 4) Decisão",
        "O maior ganho é **Tempo** → vira a raiz. Ramos: Ensolarado (2 Sim, 3 Não), Nublado (4 Sim → folha pura), Chuvoso (3 Sim, 2 Não). Repete-se a recursão nos ramos impuros.",
    ]),
    BOX("exemplo", "Continuando o exemplo: por que a árvore final tem Umidade e Vento?", [
        "# Ramo Ensolarado (S = 2 Sim, 3 Não; E ≈ 0,971)",
        "- Umidade: Alta → 3 Não (puro); Normal → 2 Sim (puro). **Ganho = 0,971** (máximo possível, pois os dois ramos ficam puros).",
        "- Temperatura: ganho ≈ 0,571 · Vento: ganho ≈ 0,020.  → escolhe-se **Umidade**.",
        "# Ramo Chuvoso (S = 3 Sim, 2 Não; E ≈ 0,971)",
        "- Vento: Fraco → 3 Sim (puro); Forte → 2 Não (puro). **Ganho = 0,971** → escolhe-se **Vento**.",
        "# Árvore final",
        CODE("""Tempo?
 ├─ Ensolarado → Umidade?  Alta → Não   |  Normal → Sim
 ├─ Nublado    → Sim
 └─ Chuvoso    → Vento?    Fraco → Sim  |  Forte  → Não"""),
        "Note que **Temperatura não aparece**: nem todo atributo precisa entrar na árvore.",
    ]),
    BOX("erro", "Erros comuns no ID3", [
        "- Esquecer de **ponderar** pelo tamanho do subconjunto (|S_{v}|/|S|) ao somar as entropias dos ramos.",
        "- Calcular o ganho com a entropia **do pai errado**: a cada recursão, E(S) é a entropia do **subconjunto do nó atual**, não do conjunto inicial.",
        "- Reutilizar na recursão um atributo categórico já usado no caminho (o ID3 o **remove** da lista).",
        "- Achar que ganho alto = boa generalização. Um atributo do tipo “ID do cliente” tem ganho máximo e é completamente inútil (veja a Seção 2).",
        "- Esquecer que o ID3 **não trata atributos contínuos nem valores ausentes** e **não faz poda** — são justamente as melhorias do C4.5.",
    ]),
    BOX("extra", "ID3 × CART (contexto)", [
        "O slide cita o **Índice de Gini** como métrica do CART: Gini(S) = 1 − Σ p_{i}². Assim como a entropia, vale 0 para conjuntos puros e é máximo quando as classes são equiprováveis "
        "(0,5 para 2 classes). As duas métricas costumam escolher atributos parecidos; o foco da prova é a entropia.",
    ]),
    BOX("resumo", None, [
        "- Árvore = raiz, nós internos (testes), ramos, folhas (classes); construção **gulosa e recursiva**.",
        "- Impureza (entropia) mede a mistura de classes; **ganho = entropia antes − entropia ponderada depois**.",
        "- ID3: maior ganho; atributos categóricos; sem poda, sem contínuos, sem ausentes.",
    ]),
    EX([
        Q("Calcule a entropia de um conjunto com **[6+ , 2−]**, de outro com **[3+ , 3−]** e de outro com **[5+ , 0−]**.",
          ["Use E = −Σ p log₂ p.",
           "- [6+,2−]: −(6/8)log₂(6/8) − (2/8)log₂(2/8) = 0,311 + 0,5 = **0,811**.",
           "- [3+,3−]: **1** (50/50, incerteza máxima).",
           "- [5+,0−]: **0** (conjunto puro)."]),
        Q("Um conjunto S tem 8 exemplos (4 Sim e 4 Não). O atributo **X** gera os ramos a (3 Sim, 1 Não) e b (1 Sim, 3 Não). O atributo **Y** gera os ramos c (2 Sim, 0 Não) e d (2 Sim, 4 Não). "
          "Qual atributo o ID3 escolhe?",
          ["E(S) = 1.",
           "- X: E(a) = E(b) = E[3,1] = 0,811 → Ganho = 1 − (4/8)(0,811) − (4/8)(0,811) = **0,189**.",
           "- Y: E(c) = 0; E(d) = E[2,4] = 0,918 → Ganho = 1 − (2/8)(0) − (6/8)(0,918) = **0,311**.",
           "O ID3 escolhe **Y** (maior ganho). Observação: Y criou um ramo puro, o que ajuda muito."]),
        Q("Verdadeiro ou falso (justifique): (a) a entropia de um nó puro é 1; (b) o ID3 escolhe o atributo com **menor** ganho de informação; (c) o ID3 aceita diretamente atributos numéricos contínuos.",
          ["(a) **Falso** — nó puro tem entropia **0**; 1 é o máximo para 2 classes.",
           "(b) **Falso** — escolhe o de **maior** ganho (maior redução de incerteza).",
           "(c) **Falso** — o ID3 trabalha com atributos categóricos; o tratamento de contínuos (limiares) é uma melhoria do C4.5."]),
        Q("Na tabela Jogar Tênis, o ramo Nublado (4 Sim, 0 Não) virou folha “Sim” sem testar nenhum outro atributo. Qual critério de parada foi aplicado?",
          "Todos os exemplos do nó pertencem à **mesma classe** (nó puro, entropia 0). Não há ganho possível, então retorna-se uma folha com essa classe."),
        Q("Explique, com suas palavras, por que a árvore de decisão é considerada um algoritmo guloso e qual a consequência disso.",
          "Em cada nó ela escolhe o atributo que parece melhor **naquele passo** (maior ganho) e **nunca revisita** a escolha. "
          "Consequência: não há garantia de encontrar a **menor/ótima** árvore; árvores diferentes podem ser possíveis, e uma má escolha inicial persiste nos níveis abaixo."),
    ]),
]

# =====================================================================
# 2. C4.5
# =====================================================================
C += [
    H1("Algoritmo C4.5: razão de ganho, contínuos, ausentes e poda",
       "Slides 01 (parte final) e 02 · O sucessor do ID3, projetado para corrigir os problemas práticos do ganho de informação."),
    H2("Principais melhorias sobre o ID3"),
    T(["Problema do ID3", "Solução do C4.5"],
      [["Ganho favorece atributos com **muitos valores**", "Usa a **Razão de Ganho** (ganho normalizado)"],
       ["Só atributos categóricos", "**Atributos contínuos** via limiares (cortes binários)"],
       ["Exemplos com valor faltando atrapalham", "**Valores ausentes**: distribuição proporcional (pesos fracionários)"],
       ["Overfitting (árvore completa decora o treino)", "**Poda pós-construção**"]],
      widths=[8, 9]),
    H2("Razão de Ganho (Gain Ratio)"),
    P("O ganho de informação tem um **viés**: um atributo com muitos valores (extremo: um “ID” único por exemplo) fragmenta o conjunto em muitos subconjuntos minúsculos e "
      "quase puros, ficando com ganho enorme sem ter poder preditivo. O C4.5 corrige penalizando divisões muito fragmentadas."),
    BOX("def", "Informação da Divisão e Razão de Ganho", [
        "= InfoDivisão(S, A) = − Σ_{v ∈ Valores(A)}  ( |S_{v}| / |S| ) · log_{2}( |S_{v}| / |S| )",
        "= RazãoGanho(S, A) = Ganho(S, A) / InfoDivisão(S, A)",
        "- **InfoDivisão** é a entropia da *distribuição dos exemplos pelos ramos* (ignora as classes!). Muitos ramos ⇒ InfoDivisão alta ⇒ razão menor.",
        "- O C4.5 escolhe o atributo de **maior Razão de Ganho**.",
    ]),
    BOX("exemplo", "Jogar Tênis no C4.5", [
        "# InfoDivisão da Umidade (7 Alta, 7 Normal)",
        "= InfoDivisão = −(7/14)log₂(7/14) − (7/14)log₂(7/14) = 1,000   →   Razão = 0,151 / 1,000 = **0,151**",
        T(["Atributo", "Ganho", "InfoDivisão", "Razão de Ganho"],
          [["**Tempo**", "0,246", "1,577", "**0,156**"], ["Temperatura", "0,029", "1,557", "0,019"],
           ["Umidade", "0,151", "1,000", "0,151"], ["Vento", "0,048", "0,985", "0,049"]],
          widths=[4, 3, 3.5, 4], align=["l", "c", "c", "c"], size=9.5),
        "Tempo continua sendo a raiz — mas repare que a razão (0,156) ficou bem mais próxima da Umidade (0,151): Tempo tem 3 valores e é penalizado pela InfoDivisão mais alta.",
    ]),
    BOX("insight", "Como ler a InfoDivisão", [
        "InfoDivisão não olha as classes: só *como os exemplos se espalham pelos ramos*. Dois ramos de tamanho igual → 1 bit. "
        "Quatorze ramos com 1 exemplo cada → log₂(14) ≈ 3,81 bits. Dividir por esse número derruba a razão de atributos “ID-like”.",
    ]),
    BOX("erro", "Armadilhas da razão de ganho", [
        "- A razão de ganho **atenua**, mas não elimina o viés. Exemplo: um atributo “Dia” (D1…D14) tem Ganho = 0,940 e InfoDivisão = log₂14 = 3,807 → Razão ≈ **0,247**, maior que a do Tempo (0,156)! "
        "Na prática, identificadores únicos devem ser **removidos** antes do treino.",
        "- InfoDivisão = 0 quando só há um ramo (divisão que não separa nada): a razão fica indefinida — evite dividir por atributos constantes.",
        "- Não confunda: **ganho** usa as classes; **InfoDivisão** não.",
    ]),
    BOX("extra", "Heurística do C4.5 original (Quinlan, 1993)", [
        "Para evitar que atributos com ganho minúsculo ganhem só porque a InfoDivisão também é minúscula, o C4.5 original considera apenas os atributos com **ganho ≥ média dos ganhos** e, entre eles, escolhe a maior razão. "
        "No Jogar Tênis a média é 0,1185; só Tempo (0,246) e Umidade (0,151) qualificam. Esse detalhe não está nos slides — conheça-o, mas na prova siga o roteiro dos slides (maior razão de ganho).",
    ]),

    H2("Atributos contínuos: encontrando o limiar"),
    P("Não dá para criar um ramo por valor numérico. O C4.5 transforma o atributo em um **teste binário**: A ≤ t ou A > t."),
    N(["**Ordene** os exemplos pelo valor do atributo A.",
       "**Candidatos a limiar:** para cada par consecutivo (a_{i}, a_{i+1}) com **classes diferentes**, t = (a_{i} + a_{i+1}) / 2.",
       "**Avalie cada t:** divida em A ≤ t e A > t e calcule a Razão de Ganho.",
       "**Escolha** o t⋆ de maior razão de ganho."]),
    BOX("exemplo", "Slide 02: 8 exemplos (5 Sim, 3 Não), E(S) ≈ 0,954", [
        "Ordenados: 22 Não · 24 Não · 27 Sim · 30 Sim · 34 Sim · 38 Não · 40 Sim · 42 Sim",
        "As classes mudam entre 24↔27, 34↔38 e 38↔40 → candidatos **25,5 · 36,0 · 39,0**.",
        "# Para t = 25,5",
        "- A ≤ 25,5 → {22, 24} = 2 Não → entropia 0.",
        "- A > 25,5 → {27, 30, 34, 38, 40, 42} = 5 Sim, 1 Não → entropia ≈ 0,650.",
        "= Ganho = 0,954 − (2/8)·0 − (6/8)·0,650 ≈ 0,467",
        "= InfoDivisão = −(2/8)log₂(2/8) − (6/8)log₂(6/8) ≈ 0,811   →   Razão ≈ 0,467/0,811 = **0,576**",
        T(["Limiar t", "Ganho", "InfoDivisão", "Razão de Ganho"],
          [["**25,5**", "0,467", "0,811", "**0,576**"], ["36,0", "0,003", "0,954", "0,003"], ["39,0", "0,204", "0,811", "0,252"]],
          widths=[4, 3, 3.5, 4], align=["c", "c", "c", "c"], size=9.5),
        "Melhor corte: **t⋆ = 25,5**. O nó gera a regra A ≤ 25,5 ⇒ Não; o ramo A > 25,5 ainda é misto e é **dividido novamente** (um mesmo atributo contínuo pode aparecer várias vezes no caminho!).",
    ]),
    BOX("insight", "Por que só testar pontos entre classes diferentes?", [
        "Entre dois valores vizinhos de **mesma** classe, mover o corte nunca melhora a pureza (só separa exemplos iguais uns dos outros). "
        "O ótimo sempre cai numa fronteira onde a classe muda — isso reduz muito o número de candidatos.",
    ]),
    BOX("erro", None, [
        "- Calcular o limiar como o **valor** de um dos exemplos em vez do **ponto médio**.",
        "- Considerar candidatos entre vizinhos da **mesma classe** (conta a mais, resposta igual).",
        "- Achar que um atributo contínuo, uma vez usado, sai da lista (diferente dos categóricos): ele pode ser **reutilizado** com outro limiar.",
    ]),

    H2("Valores ausentes"),
    P("O C4.5 **não descarta** exemplos com atributos faltantes. Na divisão por A, um exemplo com A = “?” é distribuído entre **todos** os ramos, "
      "com **peso proporcional** à frequência de cada valor entre os exemplos em que A é conhecido. Esses pesos fracionários entram nas contagens de entropia e ganho."),
    BOX("exemplo", "Slide 02: atributo Cor com um valor ausente", [
        "5 exemplos (3 Positivos, 2 Negativos): Cor = Vermelho (2), Azul (2), ? (1). Entre os conhecidos: 50 % Vermelho, 50 % Azul.",
        "- O exemplo “?” contribui **0,5** para o ramo Vermelho e **0,5** para o ramo Azul. Cada ramo fica com **2,5** exemplos ponderados.",
        "- Em cada ramo p₊ = 1,5/2,5 = 0,6 e p₋ = 0,4 → entropia ≈ 0,971.",
        "= Ganho(S, Cor) = 0,971 − (2,5/5)·0,971 − (2,5/5)·0,971 = **0**   (Cor não ajuda nesse exemplo)",
    ]),
    BOX("lembrete", None, ["Peso do ausente em um ramo = **frequência relativa do valor** entre os exemplos com o atributo conhecido. Os pesos de todos os ramos somam 1."]),

    H2("Poda (pruning): combatendo o overfitting"),
    P("Uma árvore crescida até o fim memoriza o treino (nós muito específicos, baixa generalização) — isso é **overfitting**. "
      "O C4.5 faz **poda pós-construção** (*post-pruning*): constrói a árvore completa e depois remove subárvores que não oferecem ganho estatístico real."),
    BOX("def", "Procedimento da poda (slides)", [
        "1) Para cada nó, estime a taxa de erro: **ê = e / N** (e = erros observados, N = exemplos no nó).",
        "2) Compare o erro **mantendo a subárvore** com o erro **se o nó virasse uma folha** (classe majoritária).",
        "3) Se a folha **não aumenta significativamente** o erro estimado → **pode** a subárvore (substitui por folha).",
    ]),
    BOX("exemplo", "Slide 02: duas decisões de poda", [
        "# Subárvore “Cor = Azul” (6 exemplos)",
        "- Mantida: Círculo (2 Neg, 1 Pos) erra 1; Quadrado (2 Neg) erra 0; Triângulo (1 Pos) erra 0 → 1/6 ≈ **0,17**.",
        "- Como folha “Negativo” (maioria): erra 2 (os 2 positivos) → 2/6 ≈ **0,33**.",
        "- 0,33 > 0,17 ⇒ **manter a subárvore**.",
        "# Subárvore “Cor = Vermelho” (5 exemplos)",
        "- Mantida: Círculo erra 0; Quadrado erra 1; Triângulo erra 1 → 2/5 = **0,4**.",
        "- Como folha “Positivo”: também 2 erros → 2/5 = **0,4**.",
        "- Erro igual (a subárvore não melhora nada) ⇒ **podar** (árvore mais simples com o mesmo erro).",
    ]),
    BOX("insight", "Princípio da navalha de Occam", [
        "Entre duas árvores com o mesmo erro, prefira a **menor**: ela generaliza melhor e é mais fácil de explicar. "
        "Note o detalhe do exemplo: no empate de erro, a poda acontece.",
    ]),
    BOX("extra", "Complemento: erro no treino × erro “pessimista”", [
        "A taxa ê = e/N do slide é calculada nos próprios dados de treino. O C4.5 real usa uma estimativa **pessimista** (limite superior de um intervalo de confiança do erro), o que torna a poda mais agressiva em nós pequenos. "
        "Para a prova, use o procedimento dos slides: comparar e/N da subárvore com e/N da folha.",
    ]),

    H2("Vantagens e desvantagens das árvores"),
    T(["Vantagens", "Desvantagens"],
      [["Intuitivas e **interpretáveis**", "Propensas a **overfitting**"],
       ["Pouco pré-processamento (sem normalização)", "**Instáveis**: pequena mudança nos dados pode mudar a árvore inteira"],
       ["Numéricos e categóricos", "Tendência a favorecer atributos com **muitos níveis**"],
       ["Modelam relações **não lineares**", "Podem ser ineficientes e **muito grandes**"],
       ["Base para Random Forest / Boosting", ""]],
      widths=[8.5, 8.5]),
    BOX("resumo", None, [
        "- C4.5 = ID3 + **razão de ganho** + **contínuos** (limiar = ponto médio entre classes diferentes) + **ausentes** (pesos fracionários) + **poda**.",
        "- Razão de ganho = ganho / InfoDivisão; penaliza atributos com muitos valores.",
        "- Poda: se erro(folha) ≤ erro(subárvore), substitui-se a subárvore pela folha.",
    ]),
    EX([
        Q("Para um conjunto de 14 exemplos, um atributo “ID” divide-o em 14 ramos de 1 exemplo cada. Calcule InfoDivisão, e a Razão de Ganho sabendo que o Ganho vale 0,940. O que isso ensina?",
          ["InfoDivisão = −14 · (1/14)·log₂(1/14) = log₂ 14 ≈ **3,807**.",
           "Razão = 0,940 / 3,807 ≈ **0,247**.",
           "Lição: a razão de ganho reduz muito o viés (de 0,940 para 0,247), mas ainda pode superar atributos legítimos (no Jogar Tênis, Tempo tem 0,156). Por isso IDs devem ser removidos dos dados."]),
        Q("Atributo contínuo A com os exemplos (valor, classe): (10,N) (15,N) (20,S) (25,S) (30,N) (35,S). Liste os limiares candidatos e determine o melhor pela razão de ganho. "
          "(Dica: E(S)=1.)",
          ["Classes mudam entre 15↔20, 25↔30 e 30↔35 → candidatos **17,5 · 27,5 · 32,5**.",
           T(["t", "Ganho", "InfoDiv.", "Razão"],
             [["17,5", "0,459", "0,918", "**0,500**"], ["27,5", "0,000", "0,918", "0,000"], ["32,5", "0,191", "0,650", "0,294"]],
             size=9.5),
           "Detalhe de t = 17,5: A ≤ 17,5 → {10N, 15N} (puro, E=0); A > 17,5 → {20S,25S,30N,35S} (3S,1N, E=0,811). Ganho = 1 − (4/6)(0,811) = 0,459; InfoDiv = E[2,4] = 0,918.",
           "Melhor: **t⋆ = 17,5** (regra A ≤ 17,5 ⇒ N)."]),
        Q("Em um nó com 10 exemplos, o atributo A tem 6 exemplos com A = a₁, 3 com A = a₂ e 1 com A = “?”. Com que peso o exemplo ausente entra em cada ramo, e quantos exemplos ponderados cada ramo recebe?",
          ["Conhecidos: 9 (6 de a₁ e 3 de a₂) → proporções 6/9 = 0,667 e 3/9 = 0,333.",
           "O ausente contribui **0,667** no ramo a₁ e **0,333** no ramo a₂.",
           "Ramo a₁: 6 + 0,667 = **6,667**; ramo a₂: 3 + 0,333 = **3,333** (soma = 10)."]),
        Q("Uma subárvore cobre 10 exemplos e comete 2 erros. Se substituída por uma folha com a classe majoritária, cometeria 3 erros. A subárvore deve ser podada? E se a folha cometesse 2 erros?",
          ["Subárvore: 2/10 = 0,20; folha: 3/10 = 0,30. A folha aumenta o erro → **não podar**.",
           "Se a folha também errasse 2 (0,20), o erro não aumenta → **podar** (árvore mais simples, mesmo erro)."]),
        Q("Marque V ou F: (a) o C4.5 usa o ganho de informação puro; (b) a poda é feita **antes** da construção da árvore; (c) um atributo contínuo pode aparecer mais de uma vez no mesmo caminho; "
          "(d) InfoDivisão depende das classes dos exemplos.",
          ["(a) **F** — usa a Razão de Ganho. (b) **F** — é *pós*-poda: poda-se a árvore já construída. "
           "(c) **V** — com limiares diferentes (ex.: A ≤ 25,5 e depois A ≤ 36). (d) **F** — depende só da distribuição dos exemplos pelos ramos."]),
    ]),
]

# =====================================================================
# 3. NEURÔNIO E PERCEPTRON
# =====================================================================
C += [
    H1("Neurônio Artificial e Perceptron",
       "Slide 03 · O tijolo básico de toda rede neural e o mais simples classificador linear."),
    H2("Por que redes neurais? Modelos lineares × não lineares"),
    P("Redes neurais artificiais (RNAs) ganharam força por quatro fatores: **dados em grande escala**, **capacidade computacional**, **algoritmos e bibliotecas** prontos e a "
      "**aproximação universal** (veremos adiante). Aplicações: visão computacional (detecção, OCR), PLN (classificação de texto, tradução), séries temporais e sinais, saúde, finanças e engenharia."),
    T(["", "Modelos lineares (Perceptron)", "Modelos não lineares (redes multicamadas)"],
      [["Quando usar", "Relações ≈ lineares; pouca complexidade", "Padrões altamente não lineares/estruturados"],
       ["Dados", "Pouca quantidade", "Grande volume"],
       ["Vantagem", "Rápidos, simples, robustos, interpretáveis", "Maior capacidade e flexibilidade"],
       ["Custo", "Baixo", "Maior custo de treino e de ajuste (tuning)"]],
      widths=[3, 7, 7], size=9.5),
    H2("O neurônio artificial (McCulloch–Pitts, 1943)"),
    BOX("def", "Neurônio artificial", [
        "Unidade de cálculo que recebe o vetor de entradas **x**, faz uma **combinação linear** com pesos **w** e viés **b**, e passa o resultado por uma **função de ativação φ**:",
        "= ŷ = φ(z),     z = wᵀx + b,     x ∈ ℝ^{d}, w ∈ ℝ^{d}, b ∈ ℝ",
        "- **Pesos w**: importância de cada entrada. **Viés b**: desloca a fronteira de decisão (limiar de “disparo”).",
        "- **φ**: introduz **não linearidade**. Sem ela, empilhar neurônios seria equivalente a um único modelo linear.",
    ]),
    BOX("intuicao", None, [
        "Pense em um júri: cada entrada é um jurado, cada peso é o quanto você confia nele e o viés é o “nível de convencimento” mínimo para condenar. "
        "z soma os votos ponderados; a ativação decide a sentença.",
    ]),
    H3("Funções de ativação (propriedades pedidas na tabela do slide)"),
    T(["Ativação", "Propriedades"],
      [["**Degrau / Sinal**", "Decisão binária; **não diferenciável**; ideal ao Perceptron clássico, mas **inviável para métodos de gradiente**"],
       ["**Sigmoide** σ(z)=1/(1+e^{−z})", "Transição suave; saída em (0,1) com leitura de **probabilidade**; boa para saída binária; **satura** (gradientes pequenos nos extremos)"],
       ["**Tangente hiperbólica**", "Saída em (−1,1), centrada em zero; treina melhor que a sigmoide em redes multicamadas; também satura"],
       ["**ReLU** max(0,z)", "**Não satura** (para z>0); computacionalmente eficiente; favorece representações **esparsas**"],
       ["**Softplus** ln(1+e^{z})", "Versão **suave** da ReLU; gradiente estável; custo um pouco maior"]],
      widths=[4.5, 12.5], size=9.5),
    H2("O Perceptron: classificador linear"),
    BOX("def", "Modelo de decisão (binário)", [
        "= ŷ = sinal(z),     z = wᵀx + b,     ŷ ∈ {−1, +1}",
        "- Hipótese: as classes são separáveis por um **hiperplano** wᵀx + b = 0 (em ℝ², uma **reta**).",
        "- **w é normal (perpendicular) ao hiperplano** e define sua orientação; **b o desloca**.",
    ]),
    P("Exemplos: **AND** e **OR** são linearmente separáveis (uma reta separa os pontos +1 e −1), portanto um Perceptron os aprende. "
      "O **XOR** não é (veremos na Seção 4)."),
    T(["x₁", "x₂", "AND", "OR", "XOR"],
      [["0", "0", "−1", "−1", "−1"], ["0", "1", "−1", "+1", "+1"], ["1", "0", "−1", "+1", "+1"], ["1", "1", "+1", "+1", "−1"]],
      widths=[2, 2, 3, 3, 3], align=["c"] * 5),
    H2("Regra de aprendizado do Perceptron"),
    P("Rótulos em {−1,+1}. Se o exemplo está **certo**, y e z têm o mesmo sinal ⇒ **y·z > 0**. Se está **errado**, os sinais discordam ⇒ **y·z ≤ 0** ⇒ corrija os pesos:"),
    BOX("def", "Atualização (apenas em erro)", [
        "= w ← w + η · y · x          b ← b + η · y",
        "- **η > 0**: taxa de aprendizado.",
        "- Se y = +1 mas z ≤ 0: w ← w + ηx *aumenta* wᵀx, empurrando z para cima.",
        "- Se y = −1 mas z ≥ 0: w ← w − ηx *diminui* wᵀx, empurrando z para baixo.",
    ]),
    CODE("""w ← 0, b ← 0
para t = 1..T (épocas):
    embaralhe os exemplos;  erros ← 0
    para cada exemplo (xᵢ, yᵢ):
        z ← wᵀxᵢ + b
        se yᵢ·z ≤ 0:          # erro (inclui z = 0!)
            w ← w + η·yᵢ·xᵢ ;  b ← b + η·yᵢ ;  erros ← erros + 1
    se erros = 0: pare        # dados separados""", "Algoritmo online do Perceptron (slide 21)"),
    BOX("erro", "Pegadinhas clássicas", [
        "- A condição de erro é **y·z ≤ 0** — o caso **z = 0 conta como erro** (por isso, com w = 0 e b = 0, o 1º exemplo *sempre* atualiza).",
        "- A atualização é **só no erro**: exemplos classificados corretamente não mudam nada.",
        "- O viés é atualizado com **b ← b + η·y** (sem multiplicar por x).",
        "- Uma época “sem erros” é o critério de convergência; se os dados **não** forem separáveis, o algoritmo nunca zera os erros (use também um nº máximo de épocas T).",
    ]),
    BOX("def", "Bias trick", [
        "Incorpore o viés como um atributo constante: x̃ = [1 ; x], w̃ = [b ; w]. Então z̃ = w̃ᵀx̃ e a regra fica apenas w̃ ← w̃ + η·y·x̃. Mesma coisa, notação mais compacta (útil em código).",
    ]),
    BOX("exemplo", "Slide 03: três passos com η = 1, w = (0,0), b = 0", [
        "Exemplos em ordem: (1,1,+1), (0,1,−1), (1,0,−1).",
        "- **Passo 1:** x=(1,1), y=+1: z = 0 → y·z = 0 ≤ 0 → erro. w = (0,0)+1·(+1)·(1,1) = **(1,1)**; b = 0+1 = **1**.",
        "- **Passo 2:** x=(0,1), y=−1: z = (1,1)·(0,1)+1 = 2 → y·z = −2 ≤ 0 → erro. w = (1,1)−(0,1) = **(1,0)**; b = 1−1 = **0**.",
        "- **Passo 3:** x=(1,0), y=−1: z = (1,0)·(1,0)+0 = 1 → y·z = −1 ≤ 0 → erro. w = (1,0)−(1,0) = **(0,0)**; b = 0−1 = **−1**.",
        "Os pesos oscilaram: normal no começo do treino. Os dados são separáveis (reta x₁+x₂ = 1,5); com mais épocas converge (em nossa simulação, para w=(3,2), b=−4 após 10 épocas).",
    ]),
    H2("Teorema do Perceptron e hiperparâmetros"),
    BOX("def", "Teorema da convergência", [
        "Se os dados de treino são **linearmente separáveis**, o Perceptron (atualizando só em erros) **converge em um número finito de passos** para um hiperplano que separa corretamente todos os exemplos.",
        "Hipótese de separabilidade: existe (w⋆, b⋆) com yᵢ(w⋆ᵀxᵢ + b⋆) > 0 para todo i. **Se não houver separabilidade, pode não convergir.**",
    ]),
    T(["Hiperparâmetro", "Recomendação do slide"],
      [["Taxa de aprendizado η", "Testar {0,1; 0,5; 1,0} e ajustar pela estabilidade"],
       ["Nº de épocas T", "50 a 200 costumam bastar para observar a tendência"],
       ["Inicialização", "w = 0, b = 0 é aceitável no Perceptron clássico"],
       ["Embaralhamento", "A cada época: reduz o viés da ordem dos exemplos"],
       ["Padronização/Normalização", "Em geral melhora a estabilidade das atualizações"]],
      widths=[5, 12], size=9.5),
    BOX("insight", "Detalhe que cai em prova: η importa pouco aqui", [
        "Com w=0 e b=0 iniciais, multiplicar η por qualquer constante só **reescala** w e b; a fronteira (sinal de z) é a mesma. "
        "Por isso, no Perceptron clássico, η = 1 é um padrão razoável. Em redes treinadas por gradiente (Seção 5), η já é crítico.",
    ]),
    BOX("resumo", None, [
        "- Neurônio: **ŷ = φ(wᵀx + b)**. Perceptron: φ = sinal, saída ±1, fronteira linear.",
        "- Aprende **só em erro (y·z ≤ 0)**: w ← w + ηyx, b ← b + ηy. Converge **se separável**.",
        "- AND e OR são separáveis; **XOR não**.",
    ]),
    EX([
        Q("Dado um Perceptron com w = (2, −1) e b = −0,5, classifique x = (1,1), x = (0,1) e x = (1,0).",
          ["z = 2x₁ − x₂ − 0,5.",
           "- (1,1): z = 0,5 → **+1**.   - (0,1): z = −1,5 → **−1**.   - (1,0): z = 1,5 → **+1**."]),
        Q("Aplique **uma época** do Perceptron à função OR (rótulos −1,+1) com η = 1, w = (0,0), b = 0 e exemplos na ordem (0,0), (0,1), (1,0), (1,1). Dê w e b ao final.",
          ["- (0,0), y=−1: z=0 → y·z=0 ≤0 → erro: w=(0,0), b=−1.",
           "- (0,1), y=+1: z=−1 → y·z=−1 → erro: w=(0,1), b=0.",
           "- (1,0), y=+1: z=0 → erro: w=(1,1), b=1.",
           "- (1,1), y=+1: z=3 → y·z=3 > 0 → **ok**.",
           "Ao final da época 1: **w=(1,1), b=1**, com 3 erros (precisa de mais épocas). Continuando, o treino converge na época 6 com w=(2,2), b=−1 (verifique: (0,0)→z=−1⇒−1; os demais z>0 ⇒ +1)."]),
        Q("Marque V ou F: (a) o Perceptron sempre converge, para qualquer conjunto de dados; (b) a atualização acontece em todo exemplo, certo ou errado; (c) a função degrau não serve para métodos baseados em gradiente; "
          "(d) o viés b desloca a fronteira de decisão.",
          ["(a) **F** — só converge se for **linearmente separável**. (b) **F** — só atualiza quando y·z ≤ 0. "
           "(c) **V** — não é diferenciável. (d) **V** — sem b a fronteira passaria sempre pela origem."]),
        Q("Por que, com w=0 e b=0 iniciais, o primeiro exemplo apresentado sempre causa uma atualização?",
          "Porque z = 0 e y·z = 0 ≤ 0, e a regra considera erro todo caso y·z ≤ 0 (o empate conta como erro)."),
        Q("Por que a regra de atualização w ← w + ηyx “empurra” z na direção correta quando há erro com y = +1?",
          "Com o novo w' = w + ηx: z' = w'ᵀx + b' = z + η‖x‖² + η > z. O termo ‖x‖² ≥ 0 e η > 0 somam um valor positivo, aumentando z — aproximando-o do lado correto (positivo). Para y = −1 o raciocínio é simétrico (z diminui)."),
    ]),
]

# =====================================================================
# 4. XOR E MLP: FORWARD
# =====================================================================
C += [
    H1("XOR, Redes Multicamadas (MLP) e Forward Pass",
       "Slide 04 (1ª parte) · Por que uma camada não basta e como empilhar neurônios resolve o problema."),
    H2("O problema do XOR"),
    P("XOR devolve +1 quando as entradas **diferem**. Nenhuma reta separa os pontos (0,1),(1,0) de (0,0),(1,1) — é o contraexemplo clássico dos modelos lineares."),
    BOX("def", "Prova algébrica de que XOR não é linearmente separável", [
        "Suponha uma reta w₁x₁ + w₂x₂ + b com rótulos ±1. As quatro exigências:",
        "- (0,0) é −1:  **b < 0**",
        "- (1,1) é −1:  **w₁ + w₂ + b < 0**",
        "- (1,0) é +1:  **w₁ + b > 0**",
        "- (0,1) é +1:  **w₂ + b > 0**",
        "Somando as duas últimas: (w₁ + w₂) + 2b > 0. Mas a segunda diz (w₁ + w₂) + b < 0, e como b < 0 teríamos (w₁ + w₂) + 2b < (w₁ + w₂) + b < 0. **Contradição** ⇒ não existe tal reta.",
    ]),
    BOX("insight", "Como uma camada oculta resolve", [
        "XOR(x₁,x₂) = (x₁ ∨ x₂) ∧ ¬(x₁ ∧ x₂). OR, AND e NOT são separáveis. Uma **camada oculta** calcula funções linearmente separáveis simples (OR e AND, ou OR e NAND) e a **camada de saída** as combina. "
        "A camada oculta **transforma o espaço** de entrada num espaço onde o problema passa a ser separável.",
    ]),
    H2("Arquitetura da MLP"),
    P("Uma **Multilayer Perceptron** empilha camadas lineares intercaladas com ativações **não lineares**. Classificação pelo número de camadas ocultas:"),
    T(["Camadas ocultas", "Nome"],
      [["0", "Perceptron"], ["1", "MLP “raso”"], ["≥ 2", "MLP profundo / **Deep Neural Network (DNN)**"]],
      widths=[5, 8], align=["c", "l"]),
    BOX("def", "Teorema da Aproximação Universal", [
        "Um MLP com **uma camada oculta suficientemente larga** e ativação “adequada” pode aproximar **qualquer função contínua** com precisão arbitrária.",
        "- Consequência 1: redes com poucas camadas já são muito expressivas.",
        "- Consequência 2: redes mais **profundas** costumam atingir o mesmo resultado com **menos parâmetros** e reaproveitam características aprendidas nas camadas anteriores.",
        "- Cuidado: o teorema garante que a rede **existe**, não que o treino a **encontrará** nem quão larga ela precisa ser.",
    ]),
    BOX("erro", None, [
        "- Sem ativação não linear, **N camadas lineares ≡ 1 camada linear** (produto de matrizes é matriz). Profundidade só ajuda **com não linearidade**.",
        "- Usar **degrau** em MLP treinada por gradiente: derivada zero/indefinida ⇒ nada aprende. Por isso se usa sigmoide, tanh, ReLU…",
    ]),
    H2("Forward pass de uma MLP 2-2-1"),
    P("Entrada x ∈ ℝ², camada oculta com 2 neurônios (ativação φ) e saída com 1 neurônio (ativação g). Parâmetros: "
      "**W⁽¹⁾ ∈ ℝ^{2×2}, b⁽¹⁾ ∈ ℝ², W⁽²⁾ ∈ ℝ^{1×2}, b⁽²⁾ ∈ ℝ**. O índice ℓ indica a camada (1 = oculta, 2 = saída)."),
    BOX("def", "Passagem direta", [
        "= z⁽¹⁾ = W⁽¹⁾x + b⁽¹⁾          a⁽¹⁾ = φ(z⁽¹⁾)",
        "= z⁽²⁾ = W⁽²⁾a⁽¹⁾ + b⁽²⁾        ŷ = g(z⁽²⁾) ∈ (0,1)",
        "Escolhas típicas: φ = tanh ou σ na oculta; g = σ na saída (binária).",
    ]),
    H3("Funções de perda (custo)"),
    T(["Perda", "Por amostra", "Média (m amostras)", "Quando"],
      [["**MSE**", "L = ½ (ŷ − y)²", "J = (1/m) Σ L", "Regressão / qualquer saída numérica"],
       ["**Entropia cruzada binária (BCE)**", "L = −[ y·log ŷ + (1−y)·log(1−ŷ) ]", "J = (1/m) Σ L", "Classificação binária com sigmoide"]],
      widths=[3.5, 5.5, 3.5, 4.5], size=9.5),
    BOX("exemplo", "Slide 04: MLP 2-2-1 com sigmoides em tudo", [
        "Parâmetros fixos:  W⁽¹⁾ = [[1, −1], [1, 1]],  b⁽¹⁾ = (0, 0),  W⁽²⁾ = [3  −1],  b⁽²⁾ = 0,5.   Amostras: x⁽¹⁾=(1,0), y=1 e x⁽²⁾=(1,1), y=0.",
        "# Amostra 1: x = (1, 0)",
        "- z⁽¹⁾ = W⁽¹⁾x = (1, 1) → a⁽¹⁾ = σ(1,1) ≈ (0,7311 ; 0,7311)",
        "- z⁽²⁾ = 3·0,7311 − 1·0,7311 + 0,5 ≈ 1,9621 → ŷ = σ(1,9621) ≈ **0,8768**",
        "- MSE = ½(0,8768−1)² ≈ **0,0076**;  BCE = −log(0,8768) ≈ **0,1315**",
        "# Amostra 2: x = (1, 1)",
        "- z⁽¹⁾ = (0, 2) → a⁽¹⁾ ≈ (0,5000 ; 0,8808)",
        "- z⁽²⁾ = 3·0,5 − 0,8808 + 0,5 ≈ 1,1192 → ŷ ≈ **0,7538**",
        "- MSE = ½(0,7538)² ≈ **0,2841**;  BCE = −log(1−0,7538) ≈ **1,4018**",
        "# Perdas médias",
        "= J_MSE ≈ (0,0076 + 0,2841)/2 ≈ 0,1459          J_BCE ≈ (0,1315 + 1,4018)/2 ≈ 0,7666",
    ]),
    BOX("insight", "MSE × BCE: por que a BCE “pune” mais?", [
        "Na amostra 2 (y=0) a rede disse 0,75 de probabilidade de ser positivo: erro grave. MSE deu 0,28; BCE deu 1,40. "
        "A BCE cresce **sem limite** quando a rede erra com muita confiança (−log → ∞), ao passo que o MSE satura. "
        "Para classificação com sigmoide isso gera gradientes mais úteis (veja o insight da Seção 5).",
    ]),
    BOX("lembrete", None, [
        "- Contar parâmetros: camada com n_{in} entradas e n_{out} neurônios tem **n_{in}·n_{out} pesos + n_{out} vieses**. MLP 2-2-1: (2·2+2)+(2·1+1) = **9**.",
        "- Em ŷ = σ(z), a saída fica em (0,1): interprete como probabilidade da classe positiva; use limiar 0,5 para decidir.",
        "- Log da BCE: use o mesmo log (natural, em geral) em todas as contas — os slides usam ln.",
    ]),
    BOX("resumo", None, [
        "- XOR não é linearmente separável (prova por contradição); **uma camada oculta com não linearidade** resolve.",
        "- MLP: camadas lineares **+ ativações não lineares**; 1 camada oculta = raso, ≥2 = profundo; aproximação universal.",
        "- Forward: z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾; a⁽ˡ⁾ = φ(z⁽ˡ⁾). Perdas: MSE e BCE.",
    ]),
    EX([
        Q("Mostre que a rede abaixo resolve XOR com degrau (saída 0/1): neurônio h₁ = OR(x₁,x₂) com w=(1,1), b=−0,5; neurônio h₂ = NAND(x₁,x₂) com w=(−1,−1), b=1,5; saída = AND(h₁,h₂) com w=(1,1), b=−1,5. "
          "Verifique as quatro entradas.",
          ["Ativação degrau: saída 1 se z>0, senão 0.",
           T(["x₁x₂", "h₁ (OR)", "h₂ (NAND)", "z saída", "XOR"],
             [["00", "z=−0,5 → 0", "z=1,5 → 1", "0+1−1,5<0", "0"], ["01", "z=0,5 → 1", "z=0,5 → 1", "1+1−1,5>0", "1"],
              ["10", "1", "1", ">0", "1"], ["11", "z=1,5 → 1", "z=−0,5 → 0", "1+0−1,5<0", "0"]], size=9),
           "Produz 0,1,1,0 = XOR. Cada neurônio é linear; a **composição** em duas camadas é que resolve."]),
        Q("Considere a MLP 2-2-1 do slide (W⁽¹⁾=[[1,−1],[1,1]], b⁽¹⁾=0, W⁽²⁾=[3 −1], b⁽²⁾=0,5, sigmoides). Calcule ŷ e as perdas MSE e BCE da amostra x = (0,1), y = 1.",
          ["z⁽¹⁾ = W⁽¹⁾x = (−1 , 1) → a⁽¹⁾ = (σ(−1), σ(1)) = (0,2689 ; 0,7311).",
           "z⁽²⁾ = 3·0,2689 − 0,7311 + 0,5 = 0,5758 → **ŷ = σ(0,5758) ≈ 0,6401**.",
           "MSE = ½(0,6401 − 1)² ≈ **0,0648**;  BCE = −ln(0,6401) ≈ **0,4461**."]),
        Q("Quantos parâmetros treináveis tem uma MLP 4-5-3-1 (4 entradas, camadas ocultas com 5 e 3 neurônios, 1 saída)?",
          ["(4·5+5) + (5·3+3) + (3·1+1) = 25 + 18 + 4 = **47**."]),
        Q("Por que uma rede de 3 camadas **lineares** (sem ativação) não resolve XOR?",
          "A composição de transformações lineares é uma transformação linear: W₃(W₂(W₁x)) = (W₃W₂W₁)x. A rede inteira equivale a um único modelo linear, que não separa XOR. É a **não linearidade** das ativações que dá poder à profundidade."),
        Q("Marque a correta:",
          opts=["o teorema da aproximação universal garante que o treinamento sempre encontrará a rede ótima;",
                "uma MLP com 1 camada oculta é chamada de “rasa”;",
                "a BCE é indicada para regressão com saída em ℝ;",
                "o MSE é a única perda possível para o MLP."],
          a="**b).** a) falsa — garante existência, não que o treino a ache; c) falsa — BCE é para classificação binária com saída em (0,1); d) falsa — a BCE também é usada."),
    ]),
]

# =====================================================================
# 5. BACKPROPAGATION
# =====================================================================
C += [
    H1("Backpropagation e Gradiente Descendente",
       "Slide 04 (2ª parte) · Como a rede aprende: calcular o quanto cada peso contribuiu para o erro e ajustá-lo."),
    H2("A ideia"),
    BOX("intuicao", None, [
        "Imagine descer uma montanha no nevoeiro: você sente a **inclinação** sob os pés (o gradiente) e dá um passo na direção que **desce**. "
        "O **gradiente descendente** faz isso com a perda J; o **backpropagation** é o método eficiente de calcular a inclinação em relação a *cada* peso, "
        "usando a **regra da cadeia** da saída para as camadas anteriores — reaproveitando contas já feitas.",
    ]),
    BOX("def", "Gradiente descendente", [
        "= W⁽ˡ⁾ ← W⁽ˡ⁾ − η · ∂J/∂W⁽ˡ⁾          b⁽ˡ⁾ ← b⁽ˡ⁾ − η · ∂J/∂b⁽ˡ⁾",
        "- **η** = taxa de aprendizado (learning rate). Muito grande: oscila/diverge. Muito pequeno: lento.",
        "- O sinal **menos**: andamos no sentido **contrário** ao gradiente, que é o de maior crescimento da perda.",
    ]),
    H2("Dedução (MSE + sigmoide na saída)"),
    P("Notação: δ⁽ˡ⁾ = ∂L/∂z⁽ˡ⁾ (o “erro” atribuído à camada ℓ). Derivadas úteis: **σ′(z) = σ(z)(1−σ(z))** e **tanh′(z) = 1 − tanh²(z)**."),
    BOX("def", "Camada de saída", [
        "= δ⁽²⁾ = (∂L/∂ŷ)(∂ŷ/∂z⁽²⁾) = (ŷ − y) · ŷ(1 − ŷ)",
        "= ∂L/∂W⁽²⁾ = δ⁽²⁾ (a⁽¹⁾)ᵀ          ∂L/∂b⁽²⁾ = δ⁽²⁾",
    ]),
    BOX("def", "Camada oculta (retropropagação do erro)", [
        "= δ⁽¹⁾ = ( (W⁽²⁾)ᵀ δ⁽²⁾ ) ⊙ φ′(z⁽¹⁾)",
        "= ∂L/∂W⁽¹⁾ = δ⁽¹⁾ xᵀ          ∂L/∂b⁽¹⁾ = δ⁽¹⁾",
        "⊙ é o **produto de Hadamard** (elemento a elemento): (A⊙B)_{ij} = A_{ij}·B_{ij}.",
    ]),
    BOX("insight", "Como ler: “o erro volta pelos mesmos pesos”", [
        "(W⁽²⁾)ᵀδ⁽²⁾ distribui o erro da saída de volta aos neurônios ocultos **proporcionalmente aos pesos que os ligam** à saída. "
        "Depois multiplica-se por φ′(z⁽¹⁾): se o neurônio oculto está saturado (φ′≈0), ele quase não recebe correção — é o problema do **gradiente que desaparece** da sigmoide/tanh.",
    ]),
    H3("Forma vetorizada (lote de m amostras)"),
    T(["Etapa", "Fórmula"],
      [["Forward", "Z⁽¹⁾ = W⁽¹⁾X + b⁽¹⁾1ₘᵀ,  A⁽¹⁾ = φ(Z⁽¹⁾),  Z⁽²⁾ = W⁽²⁾A⁽¹⁾ + b⁽²⁾1ₘᵀ,  Ŷ = g(Z⁽²⁾)"],
       ["Δ saída", "Δ⁽²⁾ = (Ŷ − Y) ⊙ Ŷ ⊙ (1 − Ŷ)"],
       ["Gradientes saída", "∂J/∂W⁽²⁾ = (1/m) Δ⁽²⁾ (A⁽¹⁾)ᵀ ;  ∂J/∂b⁽²⁾ = (1/m) Δ⁽²⁾ 1ₘ"],
       ["Δ oculta", "Δ⁽¹⁾ = ( (W⁽²⁾)ᵀ Δ⁽²⁾ ) ⊙ φ′(Z⁽¹⁾)"],
       ["Gradientes oculta", "∂J/∂W⁽¹⁾ = (1/m) Δ⁽¹⁾ Xᵀ ;  ∂J/∂b⁽¹⁾ = (1/m) Δ⁽¹⁾ 1ₘ"]],
      widths=[3.5, 13.5], size=9.5),
    CODE("""Para cada época:
  Para cada lote (X_b, Y_b):
     # Forward
     A⁽⁰⁾ ← X_b
     para ℓ = 1..L−1:  Z⁽ˡ⁾ ← W⁽ˡ⁾A⁽ˡ⁻¹⁾ + b⁽ˡ⁾ ;  A⁽ˡ⁾ ← φ(Z⁽ˡ⁾)
     Z⁽ᴸ⁾ ← W⁽ᴸ⁾A⁽ᴸ⁻¹⁾ + b⁽ᴸ⁾ ;  Ŷ ← g(Z⁽ᴸ⁾) ;  J ← PerdaMédia(Ŷ, Y_b)
     # Backward
     Δ⁽ᴸ⁾ ← DerivadaSaída(...)
     para ℓ = L−1..1:  Δ⁽ˡ⁾ ← ((W⁽ˡ⁺¹⁾)ᵀ Δ⁽ˡ⁺¹⁾) ⊙ φ′(Z⁽ˡ⁾)
     # Atualização
     para ℓ = 1..L:  W⁽ˡ⁾ ← W⁽ˡ⁾ − η·(1/m)Δ⁽ˡ⁾(A⁽ˡ⁻¹⁾)ᵀ ;  b⁽ˡ⁾ ← b⁽ˡ⁾ − η·(1/m)Δ⁽ˡ⁾1ₘ""", "Backpropagation com gradiente descendente em lotes (slide 38)"),
    BOX("erro", "Erros comuns", [
        "- Esquecer o fator **φ′(z)** (derivada da ativação) ao propagar o erro para a camada oculta.",
        "- Trocar a **ordem** dos produtos: ∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾ (a⁽ˡ⁻¹⁾)ᵀ — a ativação **da camada anterior**, não da atual.",
        "- Atualizar os pesos com **+η·gradiente** (sobe a perda!). É **−η·gradiente**.",
        "- Calcular δ da camada oculta com os pesos **já atualizados**. Calcule **todos os gradientes primeiro** e só depois atualize.",
        "- Inicializar todos os pesos iguais (simetria: neurônios ocultos aprendem a mesma coisa). Inicialize **aleatoriamente** (o Perceptron aceita zeros; a MLP não).",
        "- Confundir época (passada por **todo** o conjunto) com lote (subconjunto de m amostras usado em **uma** atualização).",
    ]),
    BOX("extra", "Com BCE + sigmoide o gradiente simplifica", [
        "Para L = BCE e ŷ = σ(z⁽²⁾), o fator ŷ(1−ŷ) **cancela** com o denominador da derivada da BCE e resulta δ⁽²⁾ = **ŷ − y**. "
        "Isso evita que o aprendizado “emperre” quando a saída está saturada e muito errada — uma razão prática de usar BCE em classificação. (Resultado padrão da literatura; os slides demonstram apenas o caso MSE.)",
    ]),
    BOX("exemplo", "Aplicando as fórmulas à amostra x=(0,1), y=1 (mesma rede do slide)", [
        "Do forward: a⁽¹⁾ = (0,2689 ; 0,7311), ŷ = 0,6401.",
        "- δ⁽²⁾ = (0,6401 − 1)·0,6401·(1 − 0,6401) = (−0,3599)(0,6401)(0,3599) ≈ **−0,0829**.",
        "- ∂L/∂W⁽²⁾ = δ⁽²⁾(a⁽¹⁾)ᵀ ≈ (−0,0223 ; −0,0606);  ∂L/∂b⁽²⁾ ≈ −0,0829.",
        "- δ⁽¹⁾ = ((W⁽²⁾)ᵀδ⁽²⁾) ⊙ a⁽¹⁾(1−a⁽¹⁾) = (3·(−0,0829) ; −1·(−0,0829)) ⊙ (0,1966 ; 0,1966) ≈ **(−0,0489 ; 0,0163)**.",
        "- ∂L/∂W⁽¹⁾ = δ⁽¹⁾xᵀ = [[0, −0,0489],[0, 0,0163]] (a coluna do x₁=0 zera!);  ∂L/∂b⁽¹⁾ = δ⁽¹⁾.",
        "# Passo com η = 0,5",
        "- W⁽²⁾: (3 ; −1) − 0,5·(−0,0223 ; −0,0606) = (**3,0111 ; −0,9697**);  b⁽²⁾ = 0,5 + 0,5·0,0829 = **0,5415**.",
        "Os pesos sobem onde era preciso aumentar ŷ (queremos ŷ→1). Sensato.",
    ]),
    BOX("resumo", None, [
        "- Aprender = **minimizar J** por gradiente descendente: W ← W − η·∂J/∂W.",
        "- Backprop = regra da cadeia: δ⁽ᴸ⁾ na saída, depois **δ⁽ˡ⁾ = (Wᵀδ⁽ˡ⁺¹⁾) ⊙ φ′(z⁽ˡ⁾)**, gradientes **δ·aᵀ** e **δ**.",
        "- σ′ = σ(1−σ); tanh′ = 1−tanh². Atualize **depois** de calcular todos os gradientes.",
    ]),
    EX([
        Q("Calcule σ′(z) para z = 0 e escreva tanh′(0). Por que esses valores explicam a importância de inicializar bem os pesos e o problema do gradiente que desaparece?",
          ["σ(0)=0,5 → σ′(0)=0,5·0,5 = **0,25** (é o **máximo** de σ′). tanh′(0) = 1 − 0 = **1**.",
           "Para |z| grande, σ′→0: o neurônio saturado quase não recebe gradiente e deixa de aprender; com várias camadas σ′ ≤ 0,25 é multiplicado repetidamente → gradientes minúsculos nas primeiras camadas."]),
        Q("Para a rede do slide e a amostra x=(0,1), y=1, ŷ=0,6401, calcule δ⁽²⁾ (MSE + sigmoide) e a atualização de b⁽²⁾ com η=0,5.",
          ["δ⁽²⁾ = (ŷ−y)·ŷ(1−ŷ) = (−0,3599)(0,6401)(0,3599) ≈ **−0,0829**.",
           "∂L/∂b⁽²⁾ = δ⁽²⁾ → b⁽²⁾ ← 0,5 − 0,5·(−0,0829) = **0,5415**. O viés aumenta, empurrando ŷ para 1."]),
        Q("Para a mesma amostra, calcule o primeiro componente de δ⁽¹⁾. Dados: W⁽²⁾=[3 −1], δ⁽²⁾=−0,0829, a⁽¹⁾=(0,2689 ; 0,7311).",
          ["[(W⁽²⁾)ᵀδ⁽²⁾]₁ = 3·(−0,0829) = −0,2487.",
           "φ′ do neurônio 1 = a₁(1−a₁) = 0,2689·0,7311 = 0,1966.",
           "δ⁽¹⁾₁ = −0,2487·0,1966 ≈ **−0,0489**."]),
        Q("Sobre o gradiente descendente: (a) com η muito grande, o que pode ocorrer? (b) o que significa uma “época”? (c) por que usamos lotes (batches)?",
          ["(a) A perda pode **oscilar ou divergir** (passos ultrapassam o mínimo). (b) Uma passada completa por **todo** o conjunto de treino. "
           "(c) Atualizar com subconjuntos de tamanho m é mais barato por passo e aproveita vetorização (matrizes), com ruído que muitas vezes ajuda a escapar de mínimos ruins."]),
        Q("Marque V/F: (a) no backprop, o erro é propagado da entrada para a saída; (b) o produto de Hadamard multiplica matrizes pela regra linhas×colunas; (c) ∂L/∂b⁽ˡ⁾ = δ⁽ˡ⁾.",
          ["(a) **F** — o erro é propagado da **saída para as camadas anteriores** (por isso “back”). (b) **F** — Hadamard é elemento a elemento. (c) **V**."]),
    ]),
]

# =====================================================================
# 6. REGRESSÃO LINEAR
# =====================================================================
C += [
    H1("Regressão Linear Simples e Múltipla",
       "Slide 05 · Prever valores contínuos com uma reta (ou plano) ajustada pelo método dos mínimos quadrados."),
    H2("Fundamentos: classificação × regressão"),
    P("**Classificação** prevê uma categoria; **regressão** prevê um **valor contínuo** (preço, faturamento, tamanho de tumor). Modelo geral:"),
    F("y = f(x₁, x₂, …, xₙ) + ε"),
    P("**y**: variável dependente (resposta) · **x₁…xₙ**: variáveis independentes (preditoras/explicativas) · **ε**: erro (diferença entre o real e o previsto). "
      "Exemplo: prever o preço de uma casa (y) pela área construída (x). A regressão também pode ser **não linear** (ex.: modelos de crescimento tumoral exponencial, logístico, von Bertalanffy)."),
    H2("Regressão linear simples"),
    BOX("def", "Modelo", [
        "= y = β₀ + β₁x + ε",
        "- **β₀ (intercepto)**: valor esperado de y quando x = 0. **β₁ (coeficiente angular)**: variação esperada em y por unidade a mais de x.",
        "- **ε**: erro aleatório (o que a reta não explica).",
    ]),
    H3("Método dos Mínimos Quadrados (MQO)"),
    P("Resíduo de cada ponto: **eᵢ = yᵢ − (β₀ + β₁xᵢ)**. Escolhemos β₀, β₁ que minimizam a **soma dos quadrados dos resíduos**:"),
    F("S(β₀, β₁) = Σ eᵢ² = Σ (yᵢ − β₀ − β₁xᵢ)²"),
    P("Derivando em β₀ e β₁ e igualando a zero obtém-se o sistema (equações normais):"),
    F("Σyᵢ = nβ₀ + β₁Σxᵢ          Σxᵢyᵢ = β₀Σxᵢ + β₁Σxᵢ²"),
    BOX("def", "Solução fechada", [
        "= β₁ = Σ (xᵢ − x̄)(yᵢ − ȳ) / Σ (xᵢ − x̄)²          β₀ = ȳ − β₁·x̄",
        "- A reta **sempre passa pelo ponto das médias (x̄, ȳ)** (consequência de β₀ = ȳ − β₁x̄).",
        "- S é **quadrática**, logo **convexa**: qualquer ponto crítico é **mínimo global** (um paraboloide).",
    ]),
    BOX("intuicao", "Por que elevar ao quadrado?", [
        "Erros positivos e negativos se cancelariam na soma simples; o quadrado os torna todos positivos, **pune desproporcionalmente erros grandes** e torna S diferenciável com solução em fórmula fechada.",
    ]),
    BOX("exemplo", "Slide 05: horas de estudo (x) × nota (y)", [
        T(["x (horas)", "1", "2", "3", "4", "5"], [["y (nota)", "2", "3", "5", "4", "6"]], align=["c"] * 6, size=9.5),
        "- x̄ = (1+2+3+4+5)/5 = **3**;  ȳ = (2+3+5+4+6)/5 = **4**.",
        "- Σ(xᵢ−x̄)(yᵢ−ȳ) = (−2)(−2)+(−1)(−1)+0·1+(1)(0)+(2)(2) = 4+1+0+0+4 = **9**;  Σ(xᵢ−x̄)² = 4+1+0+1+4 = **10**.",
        "- β₁ = 9/10 = **0,9**;  β₀ = 4 − 0,9·3 = **1,3**.",
        "= ŷ = 1,3 + 0,9x",
        "Interpretação: cada hora extra de estudo aumenta, em média, 0,9 ponto na nota; β₀=1,3 é a nota esperada com 0 hora (extrapolação a tomar com cuidado).",
        "# Qualidade do ajuste (complemento)",
        "- Resíduos eᵢ = (−0,2 ; −0,1 ; 1,0 ; −0,9 ; 0,2): **somam zero** (propriedade do MQO com intercepto). SSE = 1,9;  SST = Σ(yᵢ−ȳ)² = 10;  R² = 1 − 1,9/10 = **0,81**.",
    ]),
    BOX("extra", "R² (coeficiente de determinação)", [
        "R² = 1 − SSE/SST é a fração da variância de y explicada pelo modelo (0 a 1). Não aparece nos slides, mas é a métrica mais comum para “quão boa é a reta”. "
        "Cuidado: R² sempre sobe ao acrescentar variáveis; não prova que o modelo é bom (overfitting!).",
    ]),
    H2("Regressão linear múltipla"),
    BOX("def", "Modelo e forma matricial", [
        "= y = β₀ + β₁x₁ + β₂x₂ + … + β_{p}x_{p} + ε",
        "= y = Xβ + ε",
        "- **y ∈ ℝ^{n×1}** (respostas); **X ∈ ℝ^{n×(p+1)}** (preditores **com uma coluna de 1s** para o intercepto); **β ∈ ℝ^{(p+1)×1}**; **ε ∈ ℝ^{n×1}**.",
    ]),
    BOX("def", "Equação normal (MQO matricial)", [
        "= β̂ = (XᵀX)⁻¹ Xᵀ y",
        "- Exige **det(XᵀX) ≠ 0**, isto é, XᵀX **invertível**: as colunas de X devem ser **linearmente independentes** (sem colinearidade perfeita) e n ≥ p+1.",
    ]),
    BOX("lembrete", "Interpretação dos coeficientes (cai em prova!)", [
        "- **β₀**: valor esperado de y quando **todos** os xⱼ = 0 (muitas vezes só interpretação matemática).",
        "- **βⱼ**: variação média em y quando xⱼ aumenta 1 unidade, **mantendo as demais variáveis constantes** (*ceteris paribus*).",
    ]),
    BOX("exemplo", "Slide 05: preço (mil R$) × área (m²) e quartos", [
        T(["Área x₁", "Quartos x₂", "Preço y"], [["50", "1", "200"], ["60", "2", "250"], ["80", "3", "310"]], align=["c"] * 3, size=9.5),
        "= X = [[1,50,1],[1,60,2],[1,80,3]],   y = (200, 250, 310)ᵀ",
        "= XᵀX = [[3, 190, 6],[190, 12500, 410],[6, 410, 14]],   Xᵀy = (760, 49800, 1630)ᵀ",
        "= (XᵀX)⁻¹ = [[69, −2, 29],[−2, 0,06, −0,9],[29, −0,9, 14]]",
        "= β̂ = (XᵀX)⁻¹Xᵀy = (110 ; 1 ; 40)",
        "= ŷ = 110 + x₁ + 40x₂",
        "- β̂₁ = 1: cada m² a mais soma R$ 1.000 (mantendo quartos fixos). β̂₂ = 40: cada quarto a mais soma R$ 40.000 (mantendo a área).",
        "- Previsão para 70 m² e 2 quartos: 110 + 70 + 80 = **260** → R$ 260.000.",
    ]),
    BOX("insight", "Atenção: este exemplo se ajusta perfeitamente", [
        "São 3 pontos e 3 parâmetros (β₀,β₁,β₂): o sistema é exato e os resíduos são **todos zero**. Isso é um alerta de **overfitting**: com n = p+1 qualquer ruído seria “decorado”. "
        "Na prática, n deve ser **muito maior** que p+1.",
    ]),
    BOX("erro", None, [
        "- Esquecer a **coluna de 1s** em X (o modelo ficaria sem intercepto).",
        "- Trocar a ordem em β̂ = (XᵀX)⁻¹Xᵀy (as dimensões não fecham se errar).",
        "- Interpretar βⱼ sem a cláusula “mantendo as demais constantes”.",
        "- Usar preditores **colineares** (ex.: área em m² e em pés²): XᵀX singular → sem solução única.",
        "- Extrapolar a reta muito além da faixa dos dados.",
        "- **Correlação não é causalidade**: o coeficiente descreve associação nos dados.",
    ]),
    BOX("resumo", None, [
        "- Simples: ŷ = β₀ + β₁x; **β₁ = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²**, **β₀ = ȳ − β₁x̄**; a reta passa por (x̄, ȳ).",
        "- Múltipla: **β̂ = (XᵀX)⁻¹Xᵀy**, com X contendo coluna de 1s; XᵀX deve ser invertível.",
        "- Minimiza a **soma dos quadrados dos resíduos**; a função é convexa (mínimo global).",
    ]),
    EX([
        Q("Dados (x,y) = (1,3), (2,5), (3,7), (4,8). Ajuste a reta de MQO e preveja y para x = 5.",
          ["x̄ = 2,5; ȳ = 5,75.",
           "Σ(x−x̄)(y−ȳ) = (−1,5)(−2,75)+(−0,5)(−0,75)+(0,5)(1,25)+(1,5)(2,25) = 4,125+0,375+0,625+3,375 = **8,5**;  Σ(x−x̄)² = 2,25+0,25+0,25+2,25 = **5**.",
           "β₁ = 8,5/5 = **1,7**;  β₀ = 5,75 − 1,7·2,5 = **1,5** → ŷ = 1,5 + 1,7x.",
           "Para x=5: ŷ = 1,5 + 8,5 = **10**."]),
        Q("Para o ajuste do exercício anterior, calcule os resíduos e verifique que somam zero. Calcule também SSE e R².",
          ["ŷ = 3,2 ; 4,9 ; 6,6 ; 8,3 → resíduos e = −0,2 ; 0,1 ; 0,4 ; −0,3 → **soma = 0**.",
           "SSE = 0,04+0,01+0,16+0,09 = **0,30**.  SST = Σ(y−5,75)² = 7,5625+0,5625+1,5625+5,0625 = 14,75.",
           "R² = 1 − 0,30/14,75 ≈ **0,98** (ajuste muito bom)."]),
        Q("No modelo múltiplo do slide (ŷ = 110 + x₁ + 40x₂, preço em mil R$), qual o preço estimado de uma casa com 100 m² e 3 quartos? Interprete β₂.",
          ["ŷ = 110 + 100 + 40·3 = **330** → R$ 330.000.",
           "β₂ = 40: aumento médio de R$ 40.000 por quarto adicional, **mantendo a área constante**."]),
        Q("Explique por que (XᵀX) precisa ser invertível e dê um exemplo de situação em que não é.",
          "A solução β̂ = (XᵀX)⁻¹Xᵀy exige a inversa. XᵀX não é invertível quando as colunas de X são linearmente dependentes (**colinearidade**), por exemplo se x₂ = 2·x₁ para todas as amostras, "
          "ou há menos amostras que parâmetros (n < p+1). Então há infinitas soluções de MQO."),
        Q("Marque V/F: (a) o MQO minimiza a soma dos resíduos (sem quadrado); (b) a reta de MQO passa por (x̄, ȳ); (c) β₀ sempre tem interpretação prática; (d) a função S(β₀,β₁) é convexa.",
          ["(a) **F** — minimiza a soma dos **quadrados**. (b) **V**. (c) **F** — se x=0 estiver fora da faixa dos dados é só matemática. (d) **V** — logo todo ponto crítico é mínimo global."]),
    ]),
]

# =====================================================================
# 7. K-MEANS
# =====================================================================
C += [
    H1("Agrupamento de Dados e Algoritmo K-means",
       "Slide 06 · Aprendizado **não supervisionado**: descobrir grupos quando não há rótulos."),
    H2("Aprendizado não supervisionado e tarefas"),
    P("Muitas vezes não temos rótulos (rotular é caro e demorado). No aprendizado não supervisionado buscamos **estrutura ou padrões** nos dados sem rótulos. Três tarefas principais:"),
    T(["Tarefa", "Objetivo", "Algoritmos citados"],
      [["**Sumarização**", "Condensar a informação preservando a estrutura essencial", "PCA, SVD, Autoencoders, NMF"],
       ["**Associação**", "Descobrir itens/atributos que ocorrem juntos com frequência (cesta de compras)", "Apriori, FP-Growth"],
       ["**Agrupamento (clustering)**", "Particionar em grupos: objetos do mesmo grupo similares entre si e diferentes dos outros grupos", "K-means, DBSCAN, hierárquico…"]],
      widths=[3.6, 8.4, 5], size=9.5),
    H2("Similaridade e tipos de agrupamento"),
    BOX("def", "Métricas de distância (entre xᵢ e xⱼ com n atributos)", [
        "= Euclidiana: d₂ = √( Σ_k (x_{ik} − x_{jk})² )          Manhattan: d₁ = Σ_k |x_{ik} − x_{jk}|",
        "= Minkowski: d_{p} = ( Σ_k |x_{ik} − x_{jk}|^{p} )^{1/p}          Cosseno: d_{cos} = 1 − (xᵢ·xⱼ)/(‖xᵢ‖‖xⱼ‖)",
        "Minkowski generaliza: p=1 → Manhattan; p=2 → Euclidiana. A escolha da métrica **influencia o resultado**.",
    ]),
    BOX("lembrete", "Padronize os dados!", [
        "Se um atributo tem escala muito maior (ex.: “valor médio por compra” de 75 a 320 vs. “compras por mês” de 0,8 a 5), ele **domina a distância**. "
        "Na prática normalize/padronize antes de usar K-means.",
    ]),
    T(["Baseado em", "Metodologia", "Algoritmos"],
      [["Centroide", "Proximidade ao centroide", "K-means, K-means++, K-medoids"],
       ["Conectividade", "Proximidade entre clusters", "Agrupamento hierárquico"],
       ["Densidade", "Regiões densas separadas por regiões ralas", "DBSCAN, OPTICS, HDBSCAN"],
       ["Grafos", "Distância em grafos", "Propagação de afinidade, espectral"],
       ["Distribuição", "Prob. de pertencer à mesma distribuição", "Modelos de mistura gaussiana"]],
      widths=[3.2, 8, 5.8], size=9.5),
    P("Características desejáveis dos clusters: **coesão** (elementos do mesmo cluster bem próximos), **separação** (clusters distintos bem afastados), **formato** (esféricos no K-means; arbitrários no DBSCAN) e "
      "**tamanho/densidade** (cada algoritmo lida de um jeito)."),
    H2("O algoritmo K-means"),
    P("Particiona os dados em **k clusters disjuntos**; cada cluster é representado pelo seu **centroide** (média dos pontos). Objetivo (função de custo):"),
    BOX("def", "Função objetivo", [
        "= J = Σ_{i=1..k} Σ_{x ∈ Cᵢ} ‖x − μ_{i}‖²",
        "- k = nº de clusters (definido **pelo usuário**); C_{i} = pontos do cluster i; μ_{i} = centroide do cluster i. Queremos centroides que minimizem J (o mesmo que o **WCSS**).",
    ]),
    CODE("""Entrada: dados X, k, nº máx. de iterações T, tolerância ε
1. Inicialize aleatoriamente os k centroides
2. Para t = 1..T:
     a) Atribua cada ponto ao centroide MAIS PRÓXIMO (distância euclidiana)
     b) Atualize cada centroide como a MÉDIA dos pontos atribuídos
     c) Se ‖μᵢ⁽ᵗ⁾ − μᵢ⁽ᵗ⁻¹⁾‖ < ε para todo i: pare""", "Algoritmo (slide 26)"),
    BOX("insight", "Dois passos que se alternam: “atribuir” e “atualizar”", [
        "Cada passo **nunca aumenta** J: atribuir ao centroide mais próximo reduz as distâncias; trocar o centroide pela média também (a média minimiza a soma das distâncias quadráticas). "
        "Como há finitas partições possíveis, o algoritmo **converge** — mas para um **mínimo local**, que depende da inicialização.",
    ]),
    BOX("exemplo", "Slide 06: segmentando clientes de academia (k = 2)", [
        T(["Cliente", "1", "2", "3", "4", "5", "6", "7", "8"],
          [["IMC", "24", "27", "23", "30", "22", "33", "31", "29"], ["Freq. semanal", "2", "3", "1", "5", "2", "6", "5", "4"]],
          align=["l"] + ["c"] * 8, size=9),
        "Centroides iniciais: **μ₁ = (26 ; 4,5)** e **μ₂ = (32,5 ; 4)**.",
        "# Iteração 1 — atribuição (distâncias euclidianas)",
        "- d(1,μ₁)=3,20 · d(1,μ₂)=8,73 → C₁;  cliente 2: 1,80 vs 5,59 → C₁;  3: 4,61 vs 9,96 → C₁;",
        "- 4: 4,03 vs 2,69 → **C₂**;  5: 4,72 vs 10,69 → C₁;  6: 7,16 vs 2,06 → **C₂**;  7: 5,03 vs 1,80 → **C₂**;  8: 3,04 vs 3,50 → **C₁**.",
        "= C₁ = {1, 2, 3, 5, 8},   C₂ = {4, 6, 7}",
        "# Iteração 1 — atualização",
        "= μ₁ = ((24+27+23+22+29)/5 ; (2+3+1+2+4)/5) = (25,0 ; 2,4)          μ₂ = ((30+33+31)/3 ; (5+6+5)/3) = (31,3 ; 5,3)",
        "# Iteração 2 (complemento: o slide mostra a figura final sem detalhar)",
        "- Cliente 8 = (29,4): d(8,μ₁)=4,31 e d(8,μ₂)=2,69 → **muda para C₂**. Demais permanecem.",
        "= μ₁ = (24 ; 2)          μ₂ = (30,75 ; 5)          J = 26,75",
        "- Iteração 3: nada muda → **convergiu**. Clusters finais: C₁ = {1, 2, 3, 5} (IMC baixo, pouca frequência) e C₂ = {4, 6, 7, 8} (IMC alto, mais frequência).",
    ]),
    BOX("lembrete", None, [
        "Critério de parada típico: **nenhum ponto muda de cluster** (equivalente a centroides parados) **ou** movimento < ε **ou** T iterações. "
        "Na prova, lembre que **uma iteração = atribuição + atualização**, e que pode ser preciso mais de uma para convergir.",
    ]),
    H2("Vantagens, limitações e erros"),
    T(["Vantagens", "Limitações"],
      [["Simples e **rápido** para bases grandes", "**Sensível aos centroides iniciais** (diferentes inicializações → resultados diferentes; mínimo local)"],
       ["Eficiente com clusters **esféricos** e de tamanho similar", "**Difícil escolher k**"],
       ["", "Ruim para clusters de **formato não esférico** ou **tamanhos variados**"],
       ["", "Afetado por **outliers** (a média é sensível a valores extremos)"]],
      widths=[8, 9], size=9.5),
    BOX("erro", None, [
        "- Achar que K-means encontra **o** agrupamento ótimo: encontra um **ótimo local**.",
        "- Confundir K-means (não supervisionado; agrupa) com **KNN** (supervisionado; classifica).",
        "- Esquecer de **normalizar** atributos em escalas diferentes.",
        "- Usar o **centroide como ponto da base**: o centroide é uma média e pode nem ser um dado real (K-medoids usa pontos reais).",
        "- Interpretar os números dos clusters (“cluster 1”, “2”) como ordem ou ranking: são apenas rótulos arbitrários.",
        "- Esquecer que k é definido **antes** de rodar o algoritmo.",
    ]),
    BOX("extra", "K-means++ (citado na tabela do slide)", [
        "Variante que escolhe os centroides iniciais de modo **espalhado** (o próximo centroide é sorteado com probabilidade proporcional ao quadrado da distância ao centroide mais próximo já escolhido). "
        "Reduz a sensibilidade à inicialização. Prática comum: rodar o K-means várias vezes e ficar com o menor J.",
    ]),
    H2("Escolhendo o número de clusters k"),
    P("k é um **hiperparâmetro**: um k inadequado divide incorretamente os dados ou perde informação. Há dois métodos heurísticos nos slides."),
    BOX("def", "Método do Cotovelo (Elbow)", [
        "1) Calcule o **WCSS** = Σ_i Σ_{x∈C_i} ‖x − μ_i‖² para vários k (é o próprio J).",
        "2) Plote **WCSS × k**.   3) Procure o ponto onde a redução do WCSS **fica menos acentuada** (o “cotovelo”).   4) Esse k é o sugerido.",
        "- WCSS **sempre diminui** com k crescente (com k = n vale 0): por isso não se escolhe o menor WCSS, e sim o cotovelo.",
    ]),
    BOX("def", "Coeficiente de Silhueta", [
        "= s(i) = ( b(i) − a(i) ) / max{ a(i), b(i) }",
        "- **a(i)**: distância **média** do ponto i aos demais pontos do **seu** cluster (coesão): a(i) = (1/(|C_i|−1)) Σ_{j∈C_i, j≠i} d(i,j).",
        "- **b(i)**: **menor** distância média de i aos pontos de **outro** cluster (separação): b(i) = min_{C_ℓ ≠ C_i} (1/|C_ℓ|) Σ_{j∈C_ℓ} d(i,j).",
        "- **s(i) ≈ 1**: boa separação · **s(i) ≈ 0**: sobreposição entre clusters · **s(i) < 0**: ponto provavelmente no cluster errado.",
        "- Escolha o **k que maximiza a silhueta média** s̄ = (1/n) Σ s(i).",
    ]),
    T(["", "Cotovelo", "Silhueta"],
      [["Natureza", "Visual, intuitivo", "Quantitativa (coesão e separação)"],
       ["Ponto fraco", "Subjetivo (onde exatamente é o cotovelo?)", "Mais custosa (distâncias entre pares)"],
       ["Quando ajuda", "Curva com “dobra” clara", "Casos ambíguos, mais confiável"]],
      widths=[3, 7, 7], size=9.5),
    BOX("exemplo", "Silhueta em 1D: clusters C₁ = {1, 2} e C₂ = {8, 9, 10}", [
        "- Ponto 2 (em C₁): a = |2−1| = 1;  b = média(|2−8|,|2−9|,|2−10|) = (6+7+8)/3 = 7 → s = (7−1)/7 = **0,857**.",
        "- Ponto 8 (em C₂): a = (|8−9|+|8−10|)/2 = 1,5;  b = média(|8−1|,|8−2|) = 6,5 → s = (6,5−1,5)/6,5 = **0,769**.",
        "Valores próximos de 1 ⇒ agrupamento bom.",
    ]),
    BOX("resumo", None, [
        "- Clustering = não supervisionado; K-means minimiza J = ΣΣ‖x−μ‖² alternando **atribuir ao mais próximo** e **recalcular médias**.",
        "- Sensível à inicialização, a outliers e ao k; bom para clusters esféricos.",
        "- Escolha de k: **cotovelo** (WCSS×k) e **silhueta** (maximizar s̄).",
    ]),
    EX([
        Q("Dados a = (1, 2) e b = (4, 6), calcule as distâncias Euclidiana, de Manhattan e de Minkowski com p = 3.",
          ["Diferenças: (3, 4).",
           "- Euclidiana: √(9+16) = **5**.   - Manhattan: 3+4 = **7**.   - Minkowski p=3: (27+64)^{1/3} = 91^{1/3} ≈ **4,50**."]),
        Q("Execute o K-means em 1D com k = 2 sobre os pontos {1, 2, 4, 11, 12} com centroides iniciais μ₁ = 1 e μ₂ = 4. Mostre as iterações até convergir e calcule J final.",
          ["**Iteração 1 (atribuição):** 1→μ₁(0 vs 3); 2→μ₁(1 vs 2); 4→μ₂(3 vs 0); 11 e 12→μ₂. C₁={1,2}, C₂={4,11,12}.",
           "**Atualização:** μ₁ = 1,5;  μ₂ = (4+11+12)/3 = 9.",
           "**Iteração 2:** o ponto 4: |4−1,5| = 2,5 < |4−9| = 5 → **vai para C₁**. C₁={1,2,4}, C₂={11,12}. Atualização: μ₁ = 7/3 ≈ 2,33; μ₂ = 11,5.",
           "**Iteração 3:** nenhuma mudança → convergiu.",
           "J = (1−2,33)²+(2−2,33)²+(4−2,33)² + (11−11,5)²+(12−11,5)² = 1,78+0,11+2,78+0,25+0,25 ≈ **5,17**."]),
        Q("Calcule a silhueta do ponto 4 do exercício anterior no agrupamento final (C₁={1,2,4}, C₂={11,12}).",
          ["a(4) = (|4−1|+|4−2|)/2 = 2,5.  b(4) = (|4−11|+|4−12|)/2 = 7,5.",
           "s = (7,5 − 2,5)/7,5 = **0,667**. Positivo e razoável: o ponto está bem no seu cluster, mas é o mais “distante” dele."]),
        Q("Uma curva de WCSS × k dá: k=1→500; k=2→220; k=3→90; k=4→75; k=5→68; k=6→63. Qual k sugere o método do cotovelo? Por que não escolher k = 6, que tem o menor WCSS?",
          ["O **cotovelo** está em **k = 3**: a queda de k=2→3 é grande (130) e a partir daí as quedas são pequenas (15, 7, 5).",
           "O WCSS **sempre** decresce com k (chega a 0 com k = n); escolher o menor WCSS levaria a k excessivo (overfitting, clusters sem significado). Procura-se o ponto de **retorno decrescente**."]),
        Q("Marque V/F: (a) K-means exige rótulos; (b) o resultado pode depender dos centroides iniciais; (c) a silhueta s(i) < 0 sugere que i está no cluster errado; (d) K-means lida bem com clusters não esféricos de formatos arbitrários.",
          ["(a) **F** — é não supervisionado. (b) **V** (mínimo local). (c) **V**. (d) **F** — para formatos arbitrários use DBSCAN (densidade)."]),
        Q("Você tem uma base de clientes sem rótulo e quer perfis para campanhas. Qual a abordagem? Descreva os passos e dois cuidados.",
          ["Agrupamento com K-means: (1) escolher atributos (ex.: compras/mês, valor médio, % devoluções) e **padronizá-los**; (2) escolher k (cotovelo/silhueta); (3) rodar K-means (várias inicializações); "
           "(4) **interpretar** os centroides como perfis (ex.: “frequente de ticket baixo”, “raro de ticket alto”). Cuidados: escalas diferentes e outliers distorcem as distâncias; k é uma decisão do analista."]),
    ]),
]

# =====================================================================
# 8. COLA
# =====================================================================
C += [
    H1("Cola de última hora e erros mais comuns",
       "Releia esta seção na véspera e no dia da prova."),
    H2("Fórmulas-chave em uma página"),
    T(["Tema", "Fórmula / regra"],
      [["Entropia", "E(S) = −Σ pᵢ log₂ pᵢ   (0 = puro; máx. log₂ c)"],
       ["Ganho (ID3)", "Ganho(S,A) = E(S) − Σ (|S_v|/|S|)·E(S_v)"],
       ["Razão de ganho (C4.5)", "InfoDiv = −Σ (|S_v|/|S|) log₂(|S_v|/|S|);  Razão = Ganho / InfoDiv"],
       ["Limiar contínuo", "t = (aᵢ + aᵢ₊₁)/2 entre vizinhos de **classes diferentes**; escolher maior razão"],
       ["Ausentes (C4.5)", "peso do ausente no ramo = freq. relativa do valor entre os conhecidos"],
       ["Poda", "podar se erro(folha) ≤ erro(subárvore);  ê = e/N"],
       ["Neurônio", "ŷ = φ(wᵀx + b)"],
       ["Perceptron", "erro se y·z ≤ 0;  w ← w + ηyx;  b ← b + ηy;  converge só se separável"],
       ["Forward MLP", "z⁽ˡ⁾ = W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾;  a⁽ˡ⁾ = φ(z⁽ˡ⁾)"],
       ["Perdas", "MSE: ½(ŷ−y)²;  BCE: −[y ln ŷ + (1−y) ln(1−ŷ)]"],
       ["Derivadas", "σ′ = σ(1−σ);  tanh′ = 1 − tanh²"],
       ["Backprop", "δ⁽ᴸ⁾ = (ŷ−y)ŷ(1−ŷ) (MSE+σ);  δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾ᵀδ⁽ˡ⁺¹⁾) ⊙ φ′(z⁽ˡ⁾);  ∂L/∂W = δ·aᵀ;  ∂L/∂b = δ"],
       ["Gradiente desc.", "θ ← θ − η ∂J/∂θ"],
       ["Reg. simples", "β₁ = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²;  β₀ = ȳ − β₁x̄"],
       ["Reg. múltipla", "β̂ = (XᵀX)⁻¹Xᵀy  (X com coluna de 1s)"],
       ["K-means", "J = ΣΣ‖x−μ‖²;  atribuir ao mais próximo → recalcular médias"],
       ["Escolha de k", "Cotovelo: WCSS×k;  Silhueta: s = (b−a)/max(a,b), maximizar a média"]],
      widths=[4, 13], size=9.5),
    H2("Os 12 erros que mais custam pontos"),
    N(["Entropia de nó **puro** = 0 (e não 1).",
       "No ganho, **ponderar** cada ramo por |S_v|/|S|.",
       "Usar a entropia do **subconjunto atual** em cada recursão (não do conjunto inicial).",
       "C4.5 escolhe por **razão de ganho**, não por ganho.",
       "Limiar = **ponto médio** entre vizinhos de classes **diferentes**.",
       "Perceptron: **z = 0 conta como erro**; atualiza **só** em erro; b ← b + ηy.",
       "XOR não é linearmente separável; MLP precisa de **ativação não linear**.",
       "Backprop: **não esquecer φ′(z)**; usar a(ℓ−1) no ∂L/∂W; calcular todos os gradientes antes de atualizar; sinal **−η**.",
       "Regressão: coluna de 1s em X; interpretar βⱼ com “demais variáveis constantes”.",
       "K-means: **uma iteração = atribuir + atualizar**; só termina quando nada muda.",
       "K-means é **não supervisionado**; k é escolhido pelo usuário; sensível a inicialização e outliers.",
       "WCSS sempre cai ao aumentar k — procure o **cotovelo**, não o mínimo."]),
    H2("Mini-simulado final (misto)"),
    EX([
        Q("Associe: (1) ID3; (2) C4.5; (3) Perceptron; (4) MLP; (5) K-means; (6) Regressão linear — a: aprende por gradiente com camadas ocultas; b: ganho de informação, só categóricos; "
          "c: razão de ganho e poda; d: agrupa sem rótulos; e: classificador linear com regra de correção de erro; f: mínimos quadrados.",
          "(1)-b, (2)-c, (3)-e, (4)-a, (5)-d, (6)-f."),
        Q("Um colega diz: “Vou usar um Perceptron para o problema XOR, só aumentando as épocas.” Responda.",
          "Não adianta: XOR não é linearmente separável, e o teorema do Perceptron só garante convergência para dados separáveis. Com mais épocas ele continuará oscilando. Solução: MLP com ao menos 1 camada oculta e ativação não linear."),
        Q("Classifique cada problema em supervisionado (classificação/regressão) ou não supervisionado e proponha um algoritmo desta disciplina: (a) prever o preço de um carro; "
          "(b) dizer se um e-mail é spam; (c) separar clientes em perfis sem rótulos; (d) decidir se concede crédito a partir de histórico e renda, com regras legíveis.",
          ["(a) supervisionado — **regressão linear**.  (b) supervisionado/classificação — **MLP** (ou árvore).  (c) **não supervisionado — K-means**.  (d) classificação interpretável — **árvore de decisão (C4.5)**."]),
    ], title="Exercícios — Mini-simulado"),
]
