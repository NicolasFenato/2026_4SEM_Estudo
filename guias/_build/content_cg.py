# -*- coding: utf-8 -*-
from guide_builder import *

COLOR = "6D4C41"  # marrom
TITLE = "Computação Gráfica"
PROF = "Prof. José Luis Seixas Junior · Ciência da Computação · UEL"
EXAM = "01/12/2026"
SOURCES = "Slides CG 07–10 (Transformações 3D e Mesh · Projeções e Câmera · Cenas e Pipeline · Iluminação)"
TOPICS = ["Transformações 3D", "Objetos 3D e malhas (.obj)", "Projeções e câmera", "Composição de cenas e pipeline", "Iluminação e shading"]
NOTE = "Referências dos slides: Hill (Computer Graphics Using OpenGL) e Shreiner et al. (OpenGL Programming Guide). Contas conferidas em Python."

C = []

# =====================================================================
# 0. MAPA
# =====================================================================
C += [
    H1("Visão geral: do objeto à imagem", numbered=False,
       intro="Os quatro conjuntos de slides contam uma única história: como transformar números (vértices) em uma imagem na tela."),
    P("Pense na **fotografia de uma maquete**: você (1) **modela** os objetos, (2) **posiciona** cada objeto no cenário (transformações), (3) escolhe onde **colocar a câmera** e como ela “enxerga” (projeção), "
      "(4) **acende as luzes** e define os materiais (iluminação) e (5) a placa gráfica transforma tudo em pixels (pipeline)."),
    T(["Etapa", "Pergunta que responde", "Ferramenta matemática", "Slides"],
      [["**Modelar**", "Qual a forma do objeto?", "Vértices, arestas, faces, malha (mesh), arquivo `.obj`", "07"],
       ["**Transformar**", "Onde ele está, quão grande, para onde aponta?", "Matrizes 4×4 em coordenadas homogêneas: T, E, R", "07"],
       ["**Ver**", "De onde e como a câmera olha?", "Matriz de visão (eye, look, up) e de projeção (paralela/perspectiva)", "08"],
       ["**Compor e processar**", "Como a cena vira imagem?", "Pipeline: modelagem → transformações → projeção/clipping → rasterização → fragmentos → testes → framebuffer", "09"],
       ["**Iluminar**", "Que cor tem cada ponto?", "Reflexão: Lambert (difusa), especular, ambiente; flat × smooth shading", "10"]],
      widths=[2.8, 4.7, 7, 2.5], size=9.5),
    BOX("lembrete", "O que mais cai (a partir da estrutura dos slides)", [
        "- **Matrizes**: escrever e **aplicar** T, E, Rx, Ry, Rz; **ordem da composição**; rotação em torno de um ponto (pivô).",
        "- **.obj**: saber ler vértices, normais e faces (índices começam em **1**).",
        "- **Perspectiva × paralela**; câmera: **eye, look, up** → vetores **u, v, n**; **ModelView** e a cadeia **P_clip = M_proj · M_view · M_model · P**.",
        "- **Pipeline**: a ordem e o papel de cada etapa (clipping, rasterização, testes de profundidade…).",
        "- **Iluminação**: fórmulas de **Lambert** e **especular**, papel da luz ambiente, **GL_FLAT × GL_SMOOTH**.",
    ]),
]

# =====================================================================
# 1. TRANSFORMAÇÕES 3D
# =====================================================================
C += [
    H1("Transformações geométricas 3D e composição",
       "Slide 07 (parte 1) · Mover, esticar e girar objetos usando matrizes 4×4."),
    H2("Por que coordenadas homogêneas?"),
    P("Um ponto 3D (x, y, z) é representado como o vetor coluna **[x y z 1]ᵀ** (coordenadas **homogêneas**). O “1” extra permite que a **translação** — que é uma soma — também seja escrita como **multiplicação de matriz**. "
      "Assim, **toda** transformação (translação, escala, rotação) vira uma matriz 4×4, e uma sequência delas vira **uma única matriz** (o produto das matrizes)."),
    BOX("insight", "O ganho prático", [
        "Em vez de aplicar 3 transformações a milhões de vértices, multiplica-se as 3 matrizes **uma vez** e aplica-se a matriz resultante a cada vértice (é o que a GPU faz).",
    ]),
    H2("As três transformações básicas"),
    BOX("def", "Translação  P′ = T(Δx, Δy, Δz) · P", [
        CODE("""[x']   [1 0 0 Δx] [x]        x' = x + Δx
[y'] = [0 1 0 Δy] [y]   ⇔    y' = y + Δy
[z']   [0 0 1 Δz] [z]        z' = z + Δz
[1 ]   [0 0 0 1 ] [1]"""),
    ]),
    BOX("def", "Escala  P′ = E(Ex, Ey, Ez) · P", [
        CODE("""[x']   [Ex 0  0  0] [x]        x' = x·Ex
[y'] = [0  Ey 0  0] [y]   ⇔    y' = y·Ey
[z']   [0  0  Ez 0] [z]        z' = z·Ez
[1 ]   [0  0  0  1] [1]"""),
        "A escala é feita **em relação à origem**: se o objeto não está na origem, ele também **se afasta/aproxima** dela (veja pivô).",
    ]),
    BOX("def", "Rotações (ângulo α; sentido anti-horário visto com o observador no eixo positivo)", [
        T(["Rotação em Z", "Rotação em X", "Rotação em Y"],
          [[["`│ cos α   −sen α    0       0   │`", "`│ sen α   cos α     0       0   │`", "`│   0       0       1       0   │`", "`│   0       0       0       1   │`"],
            ["`│   1       0       0       0   │`", "`│   0     cos α   −sen α    0   │`", "`│   0     sen α   cos α     0   │`", "`│   0       0       0       1   │`"],
            ["`│ cos α     0     sen α     0   │`", "`│   0       1       0       0   │`", "`│ −sen α    0     cos α     0   │`", "`│   0       0       0       1   │`"]],
           ["x′ = x cos α − y sen α\ny′ = x sen α + y cos α\nz′ = z".split("\n"),
            "x′ = x\ny′ = y cos α − z sen α\nz′ = y sen α + z cos α".split("\n"),
            "x′ = x cos α + z sen α\ny′ = y\nz′ = −x sen α + z cos α".split("\n")]],
          size=8.5, widths=[1, 1, 1]),
        "Rotação **em torno de um eixo** mantém **a coordenada desse eixo** inalterada (em Z, z′ = z).",
    ]),
    BOX("erro", "Pegadinhas de sinais", [
        "- Em **Rz** e **Rx** o seno negativo fica na **linha de cima** (x′ ou y′); em **Ry** o sinal está **trocado** (sen α na 1ª linha, −sen α na 3ª). É por causa da orientação dos eixos (regra da mão direita).",
        "- A matriz da rotação **inversa** é a **transposta** (ou use −α). A da translação inversa usa −Δ; a da escala inversa usa 1/E.",
        "- Escala com valor **negativo** produz **espelhamento**; escala 0 **achata** o objeto (matriz singular).",
    ]),
    BOX("exemplo", "Aplicando as matrizes", [
        "- **Translação:** P = (1, 2, 3) com T(4, −1, 2) ⇒ P′ = (5, 1, 5).",
        "- **Escala:** P = (1, 2, 4) com E(2, 3, 0,5) ⇒ P′ = (2, 6, 2).",
        "- **Rz(90°):** P = (1, 0, 0): x′ = 1·0 − 0·1 = 0; y′ = 1·1 + 0 = 1 ⇒ P′ = **(0, 1, 0)**.",
        "- **Ry(90°):** P = (1, 0, 0): x′ = 1·cos90° + 0 = 0; z′ = −1·sen90° + 0 = −1 ⇒ P′ = **(0, 0, −1)**.",
        "- **Rx(90°):** P = (0, 1, 0): y′ = 1·0 − 0 = 0; z′ = 1·1 + 0 = 1 ⇒ P′ = **(0, 0, 1)**.",
    ]),
    H2("Rotação genérica e rotação sobre um ponto (pivô)"),
    P("Qualquer rotação intermediária é uma **composição de rotações** nos eixos x, y e z. E toda rotação (ou escala) é feita **em torno da origem**. "
      "Para girar um objeto **em torno do seu próprio centro de massa (cm)** — ou de qualquer pivô — a receita é “**levar à origem → girar → trazer de volta**”:"),
    F("P′ = T(cm_x, cm_y, cm_z) · R_z(α) · T(−cm_x, −cm_y, −cm_z) · P"),
    P("Para uma rotação genérica, substitui-se R_z por G(γ) (composição das rotações). O mesmo vale para escala em torno de um ponto: T(c) · E · T(−c)."),
    BOX("exemplo", "Girar P = (3, 1, 0) em 90° (eixo Z) em torno do pivô c = (2, 1, 0)", [
        "- T(−c): P − c = (1, 0, 0).",
        "- Rz(90°): (1, 0, 0) → (0, 1, 0).",
        "- T(c): (0, 1, 0) + (2, 1, 0) = **(2, 2, 0)**.",
        "Sem o pivô (girando em torno da origem), o resultado seria (−1, 3, 0): o ponto “orbitaria” a origem em vez de girar em torno do pivô.",
    ]),
    H2("Composição: a ordem importa"),
    BOX("def", "Como ler o produto de matrizes", [
        "Com vetores **coluna**, P′ = M₃ · M₂ · M₁ · P: a transformação **mais próxima de P (à direita) é aplicada primeiro**. Leia o produto **da direita para a esquerda**.",
        "Convenção do modelo: **M_Model = T · R · S** ⇒ primeiro **escala**, depois **rotaciona**, por fim **translada**.",
    ]),
    BOX("exemplo", "Rotação e translação não comutam", [
        "P = (1, 0, 0); Rz(90°) e T(2, 0, 0).",
        "- **Rotaciona e depois translada** (T · R · P): R → (0, 1, 0); T → **(2, 1, 0)**.",
        "- **Translada e depois rotaciona** (R · T · P): T → (3, 0, 0); R → **(0, 3, 0)**.",
        "Resultados diferentes! Escala + translação também: S(2,2,2) depois T(1,0,0) em (1,1,0) dá (3,2,0); T depois S dá (4,2,0).",
    ]),
    BOX("erro", None, [
        "- Escrever a composição na ordem **de leitura** (esquerda → direita) em vez da ordem de **aplicação** (direita → esquerda).",
        "- Esquecer de **voltar** do pivô (T(+c)) depois de girar.",
        "- Achar que a ordem das rotações em eixos diferentes não importa: **Rx·Ry ≠ Ry·Rx** (rotações 3D não comutam).",
        "- Em OpenGL a **última** chamada de transformação escrita no código é a **primeira** aplicada ao vértice (as matrizes são pós-multiplicadas na pilha).",
    ]),
    H2("Pivô e composição de objetos"),
    BOX("def", "Pivô", [
        "O pivô de um objeto é o seu **sistema de coordenadas próprio**: tem **ponto de âncora**, serve de **referência de movimento** e de **apontamento vetorial**. Girar “em torno do pivô” é a receita T(c)·R·T(−c) acima.",
    ]),
    BOX("resumo", None, [
        "- Coordenadas homogêneas [x y z 1]ᵀ ⇒ T, E e R viram matrizes 4×4; sequências viram um produto.",
        "- Rotação/escala ocorrem em torno da **origem**; para um **pivô c**: T(c) · R · T(−c).",
        "- Produto lido da **direita para a esquerda**; modelo = T · R · S; transformações **não comutam**.",
    ]),
    EX([
        Q("Aplique T(2, 0, −1) seguida de E(2, 2, 2) ao ponto (1, 1, 1). Dê a matriz composta e o ponto final.",
          ["Primeiro T: (1+2, 1+0, 1−1) = (3, 1, 0). Depois E: **(6, 2, 0)**.",
           "Matriz composta (a última transformação aplicada fica à esquerda): M = E · T, com diagonal (2, 2, 2, 1) e última coluna (4, 0, −2, 1) — ou seja, M = [[2,0,0,4],[0,2,0,0],[0,0,2,−2],[0,0,0,1]]. Conferindo: M·(1,1,1,1)ᵀ = (2+4, 2+0, 2−2, 1) = (6, 2, 0, 1)."]),
        Q("Escreva a expressão para girar um objeto em 30° em torno do eixo X **passando pelo seu centro de massa** cm = (cm_x, cm_y, cm_z).",
          "P′ = T(cm_x, cm_y, cm_z) · R_x(30°) · T(−cm_x, −cm_y, −cm_z) · P  (lido da direita para a esquerda: leva o cm à origem, gira, devolve)."),
        Q("Gire P = (0, 2, 0) por 90° em torno do eixo X (origem). Em seguida, translade por (1, 0, 0). Qual o ponto final? E se a ordem fosse invertida?",
          ["Rx(90°): y′ = 2·0 − 0 = 0; z′ = 2·1 + 0 = 2 → (0, 0, 2). Translada → **(1, 0, 2)**.",
           "Invertendo: T → (1, 2, 0); Rx(90°): y′ = 2·0 − 0 = 0, z′ = 2·1 + 0 = 2 → **(1, 0, 2)**. Coincide aqui porque a translação é **ao longo do eixo de rotação** (X): é um caso especial; em geral não comuta."]),
        Q("V ou F: (a) a rotação em torno do eixo Z altera a coordenada z; (b) a inversa de Rz(α) é Rz(−α); (c) em P′ = T·R·S·P, a translação é aplicada primeiro; (d) a translação só pode ser matriz 4×4 graças às coordenadas homogêneas.",
          "(a) **F** — z′ = z. (b) **V**. (c) **F** — a escala é aplicada primeiro (mais próxima de P). (d) **V**."),
        Q("Por que a escala de um cubo que **não** está centrado na origem também o “desloca”?",
          "Porque a escala multiplica as **coordenadas de cada vértice** em relação à origem: o centro do cubo (cx, cy, cz) vira (Ex·cx, Ey·cy, Ez·cz). Para escalar “no lugar”, use T(c)·E·T(−c)."),
    ]),
]

# =====================================================================
# 2. OBJETOS 3D E MESH
# =====================================================================
C += [
    H1("Objetos tridimensionais: sólidos, poliedros e malhas (.obj)",
       "Slide 07 (parte 2) · Como representar a forma de um objeto no computador."),
    H2("O que é um “sólido válido”"),
    P("Nem toda coleção de polígonos é um objeto 3D utilizável. Os slides listam propriedades desejáveis da **representação** de sólidos:"),
    T(["Grupo", "Propriedade", "Significado"],
      [["**Validade** (o sólido)", "Rigidez", "Forma **invariante**"],
       ["", "Finitude", "Dimensões **finitas**"],
       ["", "Homogeneidade", "Mesmas propriedades em todos os pontos"],
       ["", "Determinismo dos limites", "Limites **internos e externos** bem definidos"],
       ["", "Fechamento de operações", "Operações geométricas resultam em um objeto **válido**"],
       ["**Propriedades da representação**", "Validade · Unicidade · Não ambiguidade · Completude", "Só sólidos válidos; um sólido ↔ **um único** modelo; um modelo ↔ **um** sólido; permite extrair as informações do sólido"],
       ["", "Concisão · Simplicidade · Eficiência · Fechamento", "Menor espaço possível; sem características especiais; resposta rápida; preservação do modelo nas operações"]],
      widths=[3.4, 5.4, 8.2], size=9),
    H2("Wireframe e ambiguidade"),
    P("**Wireframe** (estrutura de arames) representa o objeto só por **arestas**. É simples e rápido, mas **ambíguo**: o mesmo desenho de arames pode corresponder a **mais de um sólido** (ou a “dois pontos de vista” do mesmo cubo). "
      "Por isso se usam **faces**, que dão **superfície** e permitem iluminar/preencher."),
    BOX("insight", "Wireframe viola a “não ambiguidade”", [
        "O slide mostra um cubo de arames que pode ser lido como visto de cima ou de baixo. Com **faces opacas** (e normais), cada face tem frente/verso e a ambiguidade desaparece.",
    ]),
    H2("Faces, poliedros e convexidade"),
    B(["**Faces** do modelo devem ser **fechadas**, **orientáveis** (têm lado de dentro e de fora, dado pela **normal**) e formar o **limite regional (boundary)** do sólido.",
       "**Poliedro**: sólido limitado por **faces poligonais planas** (cubo, pirâmide, prismas, dodecaedro). **Não poliedros**: têm superfícies curvas (**esfera, cilindro, cone**).",
       "**Convexo**: qualquer segmento ligando dois pontos do objeto fica **dentro** dele. Um coração/objeto com reentrâncias é **côncavo**.",
       "**Faces não regulares**: malhas orgânicas (personagens) têm triângulos/polígonos de tamanhos diferentes."]),
    T(["Forma", "Faces", "Arestas", "Vértices"],
      [["Cubo / prisma retangular", "6", "12", "8"], ["Pirâmide (base quadrada)", "5", "8", "5"], ["Prisma triangular", "5", "9", "6"],
       ["Esfera / cilindro / cone", "não são poliedros (superfície curva)", "—", "—"]],
      widths=[6, 3.3, 3.3, 3.3], align=["l", "c", "c", "c"], size=9.5),
    BOX("extra", "Fórmula de Euler (poliedros convexos)", [
        "**V − A + F = 2** (vértices − arestas + faces). Cubo: 8 − 12 + 6 = 2 ✔; pirâmide: 5 − 8 + 5 = 2 ✔; prisma triangular: 6 − 9 + 5 = 2 ✔. "
        "Útil para **conferir** se uma malha fechada está consistente. Também: nº de arestas = (soma dos lados de todas as faces) / 2, pois cada aresta é compartilhada por 2 faces (cubo: 6·4/2 = 12).",
    ]),
    H2("Mesh (malha) e o formato .obj"),
    P("**Mesh** = conjunto de **polígonos/faces** que compõem o “esqueleto” da superfície de um objeto. Estrutura típica (a “Classe Mesh” recomendada para as atividades): "
      "**numVerts + vetor de pontos (vértices)**, **numNorms + vetor de normais** e **numFaces + vetor de faces**, onde cada face guarda a **lista de índices de vértices** e de normais."),
    BOX("def", "Formato Wavefront .obj (texto)", [
        "- **v x y z** → vértice   - **vt u v** → coordenada de textura   - **vn x y z** → normal   - **f v1 v2 v3 …** → face (**índices** dos vértices; começam em **1**, não em 0).",
        "- Variantes de face: **f v/vt/vn** (vértice/textura/normal) e **f v//vn** (sem textura).",
        "- Linhas com **#** são comentários.",
    ]),
    BOX("exemplo", "O cubo do slide (8 vértices, 6 faces)", [
        CODE("""# Objeto Cubo
v -1 -1  1     # vértice 1
v  1 -1  1     # 2
v  1  1  1     # 3
v -1  1  1     # 4
v -1 -1 -1     # 5
v  1 -1 -1     # 6
v  1  1 -1     # 7
v -1  1 -1     # 8
#frente  f 1 2 3 4        #trás    f 6 5 8 7
#cima    f 4 3 7 8        #baixo   f 2 1 5 6
#esquerda f 5 1 4 8       #direita f 2 6 7 3"""),
        "A face “frente” liga os vértices 1→2→3→4, todos com z = +1. A ordem dos vértices define a **orientação** (normal para fora, pela regra da mão direita).",
        "Para **desenhar o wireframe**, percorra cada face e ligue cada vértice ao seguinte (e o último ao primeiro) — é a Atividade 07/1 (+ rotações e projeção paralela).",
    ]),
    BOX("erro", None, [
        "- Indexar o .obj a partir de **0** (é a partir de **1**).",
        "- Confundir **vn** (normal) com **vt** (textura).",
        "- Esquecer que cada aresta interna é **compartilhada** por 2 faces (desenhá-la duas vezes é inofensivo, mas contá-la duas vezes não).",
        "- Aplicar a transformação **só aos vértices**, mas esquecer que as **normais** precisam de tratamento (rotação sim; translação não; escala não uniforme exige a inversa-transposta).",
    ]),
    BOX("resumo", None, [
        "- Sólido válido: rígido, finito, homogêneo, com limites e operações fechadas. Wireframe é ambíguo; faces orientáveis resolvem.",
        "- Poliedro = faces planas; esfera/cilindro/cone não são poliedros. Euler: V − A + F = 2.",
        "- .obj: v, vt, vn, f (índices a partir de 1). Mesh = vértices + normais + faces.",
    ]),
    EX([
        Q("Classifique como poliedro ou não poliedro: cubo, esfera, pirâmide, cilindro, prisma triangular, cone.",
          "**Poliedros:** cubo, pirâmide, prisma triangular (faces planas poligonais). **Não poliedros:** esfera, cilindro, cone (têm superfície curva)."),
        Q("Um poliedro convexo tem 7 vértices e 12 arestas. Quantas faces tem?",
          "Euler: V − A + F = 2 ⇒ 7 − 12 + F = 2 ⇒ **F = 7**."),
        Q("No arquivo .obj abaixo, quais são as coordenadas dos vértices da face f 1 3 2 e o que significa a ordem?\n\nv 0 0 0\nv 1 0 0\nv 0 1 0",
          ["Vértice 1 = (0,0,0); 3 = (0,1,0); 2 = (1,0,0) — os índices começam em 1.",
           "A ordem 1→3→2 define o sentido de percurso e, pela regra da mão direita, a **normal**: aqui o sentido é horário visto de +z, logo a normal aponta para **−z**."]),
        Q("Por que o wireframe é considerado ambíguo? Como o uso de faces resolve?",
          "Um desenho de arestas pode ser interpretado como **mais de um sólido/ponto de vista** (ex.: cubo visto por cima ou por baixo). Faces opacas e **orientáveis** (com normal) indicam qual lado é frente/verso e permitem remoção de superfícies ocultas e iluminação."),
        Q("V ou F: (a) o comando `vn` descreve uma coordenada de textura; (b) em .obj os índices de vértice começam em 1; (c) todo sólido de faces planas é convexo; (d) uma malha de uma esfera é composta de polígonos.",
          "(a) **F** — vn é normal; vt é textura. (b) **V**. (c) **F** — um poliedro pode ser côncavo. (d) **V** (aproxima a curvatura com muitos polígonos)."),
    ]),
]

# =====================================================================
# 3. PROJEÇÕES E CÂMERA
# =====================================================================
C += [
    H1("Projeções e câmera virtual",
       "Slide 08 · Como o mundo 3D é “fotografado” e achatado em uma imagem 2D."),
    H2("Por que projetar"),
    P("A tela é 2D; os objetos são 3D. A **projeção** mapeia pontos 3D em um **plano de imagem**. A **projeção em perspectiva** cria **realismo**: objetos distantes parecem menores e linhas paralelas convergem para um **ponto de fuga**. "
      "Também precisamos de um **controle de câmera**: facilita a navegação entre objetos e, mudando a câmera, **os objetos não são modificados**."),
    H2("Projeções geométricas planares"),
    T(["", "Paralela (ortográfica)", "Perspectiva"],
      [["Centro de projeção", "A **distância infinita**", "A **distância finita**"],
       ["Raios (projetores)", "**Paralelos** entre si", "**Convergem** no centro de projeção"],
       ["Efeito", "Preserva proporções/paralelismo; **sem encurtamento** com a distância", "Objetos distantes **menores**; realismo"],
       ["Uso", "Desenho técnico, CAD, a Atividade 07/1 (wireframe)", "Jogos, cenas realistas (Atividade 08/1)"]],
      widths=[3.6, 6.7, 6.7], size=9.5),
    BOX("def", "Perspectiva: a matemática (plano de projeção a distância d do centro)", [
        "Por semelhança de triângulos, com P = (x, y, z) projetado em P_p = (x_p, y_p, z_p = d):",
        "= x_p / z_p = x / z          y_p / z_p = y / z   ⇒   **x_p = x / (z/d)** ,  **y_p = y / (z/d)**",
        "Em matriz homogênea (o 4º elemento vira W = z/d, e depois se **divide tudo por W** — “divisão perspectiva”):",
        CODE("""[X]   [1 0 0  0 ] [x]               X/W = x / (z/d)
[Y] = [0 1 0  0 ] [y]    W = z/d    Y/W = y / (z/d)
[Z]   [0 0 1  0 ] [z]               Z/W = d
[W]   [0 0 1/d 0] [1]"""),
    ]),
    BOX("exemplo", "Projetando P = (4, 6, 8) com d = 2", [
        "W = z/d = 8/2 = 4  ⇒  x_p = 4/4 = **1**,  y_p = 6/4 = **1,5**,  z_p = d = **2**.  P_p = (1; 1,5; 2).",
        "Dobrando a distância (z = 16): x_p = 4/8 = 0,5 e y_p = 0,75 — metade do tamanho. É a **diminuição com a distância**.",
    ]),
    BOX("erro", None, [
        "- Esquecer a **divisão por W** (sem ela, o resultado da matriz ainda não é a projeção).",
        "- Confundir o **centro de projeção** (olho) com o **plano de projeção** (onde a imagem é formada, a distância d).",
        "- z = 0 (ponto no plano do olho) ⇒ divisão por zero: por isso há o plano **near** e o **clipping**.",
    ]),
    H2("Movimento e percepção: parallax"),
    P("**Parallax (paralaxe)**: a percepção de profundidade pela diferença de movimento aparente — com a mesma tela e a mesma cena, objetos **mais próximos** parecem **se mover mais** (ou ter outro tamanho) que os distantes. "
      "É usado em jogos (camadas de fundo que se movem em velocidades diferentes) para criar a sensação de profundidade."),
    H2("A câmera em perspectiva"),
    BOX("def", "Parâmetros da câmera", [
        "- **Olho (eye)**: posição da câmera na cena.",
        "- **Volume de visualização**: região entre os planos **near (perto)** e **far (longe)**, em forma de **pirâmide truncada (frustum)**.",
        "- **Ângulo de visão θ**: abertura **vertical** da pirâmide. Maior θ = “grande angular”.",
        "- **Razão de aspecto**: largura/altura do plano de imagem (resolução).",
        "- **Planos perto e longe**: o que estiver fora deles é descartado (**clipping**).",
    ]),
    H3("Os vetores da câmera: eye, look, up → u, v, n"),
    BOX("def", "Construção do sistema de coordenadas da câmera", [
        "= n = eye − look          u = up × n          v = n × u",
        "(depois de **normalizar** n e u). **n** aponta **para trás** da câmera (a câmera olha para −n); **u** aponta para a direita; **v** para cima.",
        "- **eye**: posição do olho · **look**: ponto para onde se olha · **up**: direção “para cima” (ex.: (0,1,0)).",
        "Câmera ≠ Mundo: os eixos da câmera (u, v, n) **não coincidem** com (x, y, z) do mundo; a matriz de visão faz a mudança de base.",
    ]),
    BOX("exemplo", "eye = (2, 0, 2), look = (0, 0, 0), up = (0, 1, 0)", [
        "- n = eye − look = (2, 0, 2) → normalizado **(0,707 ; 0 ; 0,707)**.",
        "- u = up × n = (0,1,0) × (0,707; 0; 0,707) = **(0,707 ; 0 ; −0,707)**.",
        "- v = n × u = **(0, 1, 0)** (já unitário, porque up ⟂ n).",
        "- A origem do mundo, vista pela câmera: coordenadas = (u·(P−eye), v·(P−eye), n·(P−eye)) = (0, 0, **−2,83**): está **no centro da imagem** e a 2,83 unidades **à frente** (−n).",
    ]),
    H3("Matriz de visão e “ModelView”"),
    BOX("def", "Matriz de visão (em memória, vetor m[16] por colunas)", [
        CODE("""m0=u.x  m4=u.y  m8 =u.z  m12 = −(eye·u)
m1=v.x  m5=v.y  m9 =v.z  m13 = −(eye·v)
m2=n.x  m6=n.y  m10=n.z  m14 = −(eye·n)
m3=0    m7=0    m11=0    m15 = 1"""),
        "As **linhas** da parte 3×3 são u, v, n (rotação para a base da câmera); a última coluna **translada** o olho para a origem. "
        "(Os slides escrevem m12 = o·u etc., com “o” = o vetor do olho; na prática a translação usa o **negativo** do produto escalar.)",
    ]),
    BOX("def", "A cadeia de matrizes (muito cobrada)", [
        "= M_ModelView = M_View · M_Model          M_Model = T · R · S",
        "= P_clip = M_Projection · M_View · M_Model · P",
        "- **Model** (coord. de **objeto** → **mundo**): *onde o objeto está*.   - **View** (mundo → **câmera**): *onde a câmera está*.",
        "- **ModelView** combina as duas: o objeto **em relação à câmera**.   - **Projection** (câmera → **recorte/clip**): como a câmera “enxerga”.",
        "Ordem dos espaços: **Objeto → Mundo → Câmera → Recorte → (divisão por W) → Normalizado → Tela (viewport)**.",
    ]),
    BOX("lembrete", "OpenGL clássico (código dos slides)", [
        "- **Projeção:** `glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(θ, aspecto, near, far);`",
        "- **Posição da câmera:** `glMatrixMode(GL_MODELVIEW); glLoadIdentity(); gluLookAt(eye, look, up);`",
        "- Pilha de matrizes: `glPushMatrix()` / `glPopMatrix()` (salva/restaura), `glMultMatrix(m[])` (multiplica), `glLoadMatrix(r)` (carrega).",
    ]),
    H3("Movimentos da câmera (classe Camera)"),
    T(["Movimento", "Eixo da câmera", "Efeito"],
      [["**slide** (deslizar)", "δu, δv, δn", "Move o **olho** ao longo de u, v e/ou n (ex.: 'Z' afasta, 'z' aproxima = deslizar em n)"],
       ["**roll** (rolar)", "em **n**", "Gira em torno do eixo de visão (inclina a cabeça)"],
       ["**pitch** (arfar)", "em **u**", "Olha para cima/baixo (acenar “sim”)"],
       ["**yaw** (guinar)", "em **v**", "Olha para esquerda/direita (acenar “não”)"]],
      widths=[3.8, 3.7, 9.5], size=9.5),
    BOX("insight", "Mnemônico dos três eixos", [
        "Avião: **roll** = rolar as asas (eixo do nariz = n); **pitch** = subir/descer o nariz (eixo das asas = u); **yaw** = virar o nariz para os lados (eixo vertical = v). "
        "Depois de cada movimento a classe **recalcula a matriz ModelView** e a carrega.",
    ]),
    BOX("resumo", None, [
        "- Paralela: centro no infinito; perspectiva: x_p = x/(z/d), y_p = y/(z/d) (dividir por W).",
        "- Câmera: eye, look, up → n = eye − look, u = up × n, v = n × u. Câmera olha para −n.",
        "- P_clip = M_proj · M_view · M_model · P; M_model = T · R · S.",
        "- slide/roll/pitch/yaw movem o olho ou giram em n/u/v.",
    ]),
    EX([
        Q("Projete em perspectiva (d = 3) o ponto P = (6, −3, 9).",
          "W = z/d = 3; x_p = 6/3 = **2**; y_p = −3/3 = **−1**; z_p = 3. P_p = (2, −1, 3)."),
        Q("Calcule n, u e v para eye = (0, 0, 5), look = (0, 0, 0), up = (0, 1, 0).",
          ["n = eye − look = (0, 0, 5) → **(0, 0, 1)**.",
           "u = up × n = (0,1,0) × (0,0,1) = (1·1 − 0·0, 0·0 − 0·1, 0·0 − 1·0) = **(1, 0, 0)**.",
           "v = n × u = (0,0,1) × (1,0,0) = **(0, 1, 0)**. Ou seja, a câmera coincide com os eixos do mundo, apenas deslocada para z = 5 e olhando para −z."]),
        Q("Associe: (a) pitch; (b) yaw; (c) roll — com (1) rotação em n; (2) rotação em u; (3) rotação em v.",
          "(a) pitch → **u** (2); (b) yaw → **v** (3); (c) roll → **n** (1)."),
        Q("Explique, com suas palavras, a diferença entre as matrizes Model, View e Projection.",
          "**Model** posiciona/orienta/escala o objeto no **mundo**. **View** posiciona a **câmera** (leva o mundo para o referencial da câmera). **Projection** define **como a câmera enxerga** (perspectiva ou paralela, ângulo, aspecto, near/far) levando para coordenadas de recorte. P_clip = Proj · View · Model · P."),
        Q("Em qual situação a projeção paralela é preferível à perspectiva? E por que a perspectiva dá mais realismo?",
          "Paralela: desenho técnico/CAD, quando é importante **preservar medidas e paralelismo**. Perspectiva: objetos mais distantes ficam **menores** e linhas paralelas **convergem**, como no olho humano/câmera."),
        Q("V ou F: (a) alterar a câmera modifica os vértices do objeto no mundo; (b) a câmera olha na direção de +n; (c) o ângulo de visão θ é a abertura vertical do frustum; (d) planos near e far delimitam o volume de visualização.",
          "(a) **F** — só muda a matriz de visão; o objeto não é alterado. (b) **F** — olha para **−n** (n = eye − look aponta para trás). (c) **V**. (d) **V**."),
    ]),
]

# =====================================================================
# 4. CENAS E PIPELINE
# =====================================================================
C += [
    H1("Composição de cenas e o pipeline gráfico",
       "Slide 09 · Cena = câmera + objetos + referências + iluminação; pipeline = a “linha de montagem” que gera os pixels."),
    H2("O que compõe uma cena"),
    B(["**Câmera**, **objetos**, **referências** (de câmera ou pontuais) e **iluminação**.",
       "**Composição de objetos**: formar e posicionar **objetos primitivos** de modo que representem um objeto maior (ex.: uma mesa = tampo + 4 pernas).",
       "**Transformações e deformações** aplicadas aos primitivos geram a composição de objetos que, por sua vez, forma a **cena**.",
       "Muitos pontos por figura; transformações de câmera ou iluminação; **não faz sentido** ter uma fonte de luz por objeto (usam-se poucas fontes para toda a cena)."]),
    H2("Técnicas de composição e modelagem"),
    T(["Técnica", "Ideia", "Exemplo"],
      [["**CSG** (Constructive Solid Geometry)", "Combina sólidos com **operações booleanas**: **união, interseção, diferença**", "Furo = cubo **menos** cilindro"],
       ["**Varredura** (sweep)", "O **“rastro”** da trajetória de um objeto/contorno ao se deformar/deslocar", "Extrusão de um perfil ao longo de uma reta"],
       ["**Varredura rotacional**", "O rastro de um contorno **girado em torno de um eixo**", "Vaso, taça, cone, esfera (revolução)"],
       ["**Corte** do sólido", "Corta com um plano; o **contorno** do corte vira **face**; depende da variação do plano", "Seção de um objeto"]],
      widths=[4.2, 8, 4.8], size=9.5),
    BOX("def", "Primitivas do GLUT", [
        "Wire/Solid: **Sphere, Cone, Cube, Torus, Dodecahedron, Octahedron, Tetrahedron, Teapot** (ex.: `glutSolidSphere`, `glutWireCube`). "
        "**Poliedros regulares** (platônicos) disponíveis: tetraedro, cubo, octaedro, dodecaedro (e icosaedro). “Wire” = só arestas; “Solid” = com faces.",
    ]),
    H2("O pipeline gráfico"),
    P("Sequência de etapas que transforma a descrição da cena (vértices, normais, materiais) em uma imagem de pixels. Os slides a descrevem **sem ray tracing** (pipeline de **rasterização**):"),
    T(["#", "Etapa", "O que faz"],
      [["1", "**Modelagem**", "Descreve a geometria: **vértices, arestas, faces, vetores normais, coordenadas de textura, materiais**"],
       ["2", "**Transformações**", "Transformações afins (model): **espaço do modelo → coordenadas do mundo → espaço de visualização**; define o volume de visualização. **Tesselação** (quando conveniente): cria novos triângulos"],
       ["3", "**Projeção de câmera**", "**Coordenadas homogêneas → coordenadas de perspectiva** (elementos distantes menores); razão de aspecto; **viewport**: coordenadas normalizadas → **coordenadas de tela**"],
       ["4", "**Clipping** (recorte)", "**Descarta** o que está **atrás da câmera**, **fora do campo de visão** ou além dos planos near/far; reduz o processamento das etapas seguintes"],
       ["5", "**Rasterização**", "**Primitivas geométricas → fragmentos** (candidatos a pixel). Decide **qual pixel pertence a qual triângulo** e **interpola** coordenadas de textura, normais e atributos de sombreamento"],
       ["6", "**Operações de fragmentos**", "Iluminação, **textura**, sombra, reflexão, transparência, normais, materiais. **Cor_final = Cor_textura × iluminação × Cor_material**"],
       ["7", "**Testes**", "**Profundidade (z-buffer)**: um objeto pode estar atrás de outro; **estêncil**: onde cada fragmento pode ser desenhado (máscaras, espelhos, contornos); **alpha**: transparência/mistura com o fragmento já no framebuffer"],
       ["8", "**Framebuffer**", "Armazena as **matrizes de imagem**; representação depende da GPU; depois vai ao **monitor**"]],
      widths=[0.8, 3.6, 12.6], align=["c", "l", "l"], size=9.5),
    BOX("insight", "Fragmento × pixel", [
        "Um **fragmento** é um “candidato a pixel”: o resultado da rasterização de um triângulo naquele ponto da tela, com cor, profundidade e atributos. "
        "Vários fragmentos (de triângulos diferentes) podem disputar **o mesmo pixel**; os **testes** (profundidade, estêncil, alpha) decidem quem aparece.",
    ]),
    BOX("erro", None, [
        "- **Clipping antes da rasterização**: descartar cedo é justamente o que **economiza** trabalho.",
        "- Confundir **rasterização** (geometria → fragmentos) com **iluminação** (cor dos fragmentos).",
        "- Achar que o **z-buffer** pertence à rasterização: está nos **testes** (depois das operações de fragmento).",
        "- O pipeline dos slides **não inclui ray tracing** (que é outra abordagem: lançar raios por pixel).",
    ]),
    BOX("resumo", None, [
        "- Cena = câmera + objetos + referências + luz. Composição por primitivas, **CSG** (∪ ∩ −), **varredura** (translacional/rotacional) e corte.",
        "- Pipeline: Modelagem → Transformações → Projeção/Viewport → **Clipping** → **Rasterização** → Operações de fragmentos → **Testes** → Framebuffer.",
    ]),
    EX([
        Q("Qual a diferença entre CSG e varredura rotacional? Dê um exemplo de cada.",
          "**CSG** combina sólidos com operações booleanas (união, interseção, diferença) — ex.: uma porca = cilindro menos cilindro menor. **Varredura rotacional** gera o sólido girando um contorno 2D em torno de um eixo — ex.: um vaso girando seu perfil."),
        Q("Ordene as etapas: rasterização, clipping, testes (profundidade), modelagem, operações de fragmentos, transformações, projeção.",
          "Modelagem → Transformações → Projeção de câmera → Clipping → Rasterização → Operações de fragmentos → Testes → Framebuffer."),
        Q("Um fragmento passa por todas as etapas, mas ao final **não** aparece na tela. Cite duas razões possíveis.",
          "(1) **Teste de profundidade**: há outro fragmento mais próximo no mesmo pixel; (2) **estêncil**: a máscara não permite desenhar ali; (3) **alpha**: totalmente transparente. (Fora do volume de visão ele nem chegaria aqui: seria descartado no clipping.)"),
        Q("Em qual etapa ocorre a interpolação de normais e de coordenadas de textura?",
          "Na **rasterização** (os atributos dos vértices são interpolados para cada fragmento do triângulo)."),
        Q("V ou F: (a) o clipping descarta primitivas fora do volume de visualização; (b) o framebuffer guarda a imagem final; (c) o pipeline estudado usa ray tracing; (d) “Solid” e “Wire” indicam, respectivamente, malha preenchida e só arestas.",
          "(a) **V**. (b) **V**. (c) **F** — é pipeline de rasterização. (d) **V**."),
    ]),
]

# =====================================================================
# 5. ILUMINAÇÃO
# =====================================================================
C += [
    H1("Iluminação, reflexão e shading",
       "Slide 10 · Como decidir a cor de cada ponto de uma superfície."),
    H2("Reflexão da luz"),
    B(["Quando a luz incide sobre uma superfície **opaca**, parte é **absorvida** e o restante é **refletido**; a parte refletida que chega ao olho é o que vemos.",
       "**Lei da reflexão:** o ângulo de saída é o ângulo de incidência **espelhado em relação à normal** (a perpendicular à superfície no ponto).",
       "A modelagem depende do material: **difusa** (espalha em todas as direções; superfície “fosca”) × **especular** (concentra em uma direção; superfície “polida/brilhante”). A turbidez/rugosidade da microestrutura define qual predomina."]),
    BOX("def", "Grandezas (radiometria)", [
        "- **Radiância da cena**: potência da luz emitida por cada ponto de uma superfície 3D.   - **Irradiância da imagem**: potência da luz chegando a cada ponto do plano de imagem.",
        "- **Reflectância**: relação (razão) entre o fluxo **incidente** e o **refletido**.",
    ]),
    H2("Os três vetores do modelo local"),
    P("Em um ponto **p** da superfície: **s** = vetor de p até a **fonte de luz**; **v** = vetor de p até o **olho**; **m** = vetor **normal** à superfície em p (normalize quando preciso)."),
    H2("Reflexão difusa: Lei de Lambert"),
    BOX("def", "Lambert", [
        "Modelo mais simples: a luz recebida é refletida **igualmente em todas as direções** ⇒ o brilho **não depende de onde o observador está**.",
        "= I_d = I_s · ρ_d · ( s·m ) / ( |s| |m| )  = I_s · ρ_d · cos θ",
        "- **I_d**: intensidade difusa refletida · **I_s**: intensidade da fonte · **ρ_d**: coeficiente de reflexão difusa do material · **θ**: ângulo entre s e m.",
    ]),
    BOX("insight", "Por que o cosseno?", [
        "A mesma quantidade de luz se espalha sobre uma **área maior** quando incide **inclinada**. Luz perpendicular (θ = 0°, cos = 1) = brilho máximo; luz rasante (θ → 90°, cos → 0) = escuro; luz por trás (cos < 0) → **0** (na prática, usa-se max(0, cos θ)).",
    ]),
    BOX("exemplo", "Intensidades difusas (I_s = 1, ρ_d = 0,8)", [
        T(["θ", "cos θ", "I_d"], [["0°", "1", "0,80"], ["30°", "0,866", "0,69"], ["60°", "0,5", "0,40"], ["90°", "0", "0"]], align=["c", "c", "c"], size=9.5),
        "Se s = (1,1,0) e m = (0,1,0): cos θ = (s·m)/(|s||m|) = 1/(√2·1) = 0,707 ⇒ I_d = 0,8 · 0,707 ≈ **0,57**.",
    ]),
    H2("Reflexão especular (brilho)"),
    BOX("def", "Vetor refletido r e intensidade especular", [
        "= r = −s + 2 · ( s·m / |m|² ) · m          I_sp = I_s · ρ_s · ( r·v / ( |r| |v| ) )^{f}",
        "- **r**: direção ideal de reflexão (s espelhado em torno de m).   - **ρ_s**: coeficiente especular do material.",
        "- **f** (expoente de brilho): controla o **tamanho do realce**. **f grande** = realce **pequeno e nítido** (superfície muito polida); **f pequeno** = realce **largo** e suave.",
        "- Depende do **observador** (ângulo entre r e v), ao contrário da difusa.",
    ]),
    BOX("exemplo", "Efeito do expoente f", [
        "s = (1, 1, 0), m = (0, 1, 0) ⇒ s·m = 1 ⇒ r = −(1,1,0) + 2·1·(0,1,0) = **(−1, 1, 0)**. Observador em v = (0, 1, 0): cos = r·v/(|r||v|) = 1/√2 ≈ 0,707.",
        T(["f", "cosᶠ", "Interpretação"],
          [["2", "0,5", "realce largo"], ["8", "0,0625", "mais concentrado"], ["32", "0,000015", "praticamente sem realce nessa posição (só brilha se v ≈ r)"]],
          align=["c", "c", "l"], size=9.5),
    ]),
    H2("Luz ambiente e o modelo completo"),
    P("Se existisse apenas luz direta, toda **penumbra seria sombra total**. A **luz ambiente** representa a luz “espalhada” pela cena toda: é a intensidade ambiente **I_a** vezes o coeficiente de reflexão ambiente do material **ρ_a**, **independente de posição e direção**."),
    BOX("def", "Combinação (modelo de iluminação local, no estilo Phong)", [
        "= I = I_a · ρ_a  +  I_s · ρ_d · max(0, cos θ)  +  I_s · ρ_s · max(0, cos φ)^{f}",
        "Soma das contribuições **ambiente + difusa + especular** (as três componentes das luzes e dos materiais do OpenGL). Os slides apresentam cada termo; a soma é a composição usual (Phong/Blinn).",
    ]),
    H3("Materiais (coeficientes ρ_a, ρ_d, ρ_s e expoente f)"),
    T(["Material", "Ambiente (RGB)", "Difusa (RGB)", "Especular (RGB)", "Expoente f"],
      [["Latão", "0,33 · 0,22 · 0,03", "0,78 · 0,57 · 0,11", "0,99 · 0,94 · 0,81", "27,9"],
       ["Bronze", "0,21 · 0,13 · 0,05", "0,71 · 0,43 · 0,18", "0,39 · 0,27 · 0,17", "25,6"],
       ["Cromado", "0,25 · 0,25 · 0,25", "0,40 · 0,40 · 0,40", "0,77 · 0,77 · 0,77", "76,8"],
       ["Prata polida", "0,23 · 0,23 · 0,23", "0,28 · 0,28 · 0,28", "0,77 · 0,77 · 0,77", "89,6"]],
      widths=[3, 3.5, 3.5, 3.5, 3.5], align=["l", "c", "c", "c", "c"], size=9),
    BOX("lembrete", "Como ler a tabela", [
        "Materiais **polidos/metálicos** (cromado, prata polida) têm **f alto** (realce pequeno e forte); o **asfalto** tem ambiente e difusa praticamente nulos (muito escuro). O **cobre/latão/bronze** têm o tom da cor na componente difusa e especular **colorida**; no cromado/prata o especular é **cinza** (branco).",
    ]),
    H2("Fontes de luz e shading no OpenGL"),
    T(["Fonte / componente", "Descrição"],
      [["**Ambiente**", "Luz uniforme em toda a cena; sem direção; ilumina tudo igualmente (um toro só com ambiente parece “chapado”)"],
       ["**Difusa**", "Luz com direção/posição; gera o sombreamento gradual (Lambert)"],
       ["**Especular**", "Gera o **realce** brilhante (depende do observador)"],
       ["**Direcional**", "Fonte no **infinito** (ex.: sol): raios **paralelos**, mesma direção para todos os pontos (no OpenGL: posição com w = 0)"],
       ["**Spot (holofote)**", "Fonte **pontual com cone**: tem **direção** (GL_SPOT_DIRECTION) e **ângulo de corte** (GL_SPOT_CUTOFF); ilumina só dentro do cone"]],
      widths=[4, 13], size=9.5),
    T(["Constante OpenGL", "Valor padrão (luz 0)", "Significado"],
      [["GL_AMBIENT", "(0, 0, 0, 1)", "Cor **ambiente** da luz"], ["GL_DIFFUSE", "(1, 1, 1, 1)", "Cor **difusa** da luz"],
       ["GL_SPECULAR", "(1, 1, 1, 1)", "Cor **especular** da luz"], ["GL_POSITION", "(0, 0, 1)", "**Posição** da luz"],
       ["GL_SPOT_DIRECTION", "(1, 1, −1)", "**Direção** da luz spot (valor do slide)"], ["GL_SPOT_CUTOFF", "180", "**Ângulo de corte** da luz spot (180 = sem cone)"]],
      widths=[5, 4, 8], align=["l", "c", "l"], size=9.5),
    P("Funções: **glLightfv** (parâmetros da luz) e **glMaterialfv** (propriedades do material). Para ligar a iluminação: `glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glEnable(GL_DEPTH_TEST); glEnable(GL_COLOR_MATERIAL);`."),
    BOX("def", "Normais e modelos de sombreamento", [
        "- É preciso **fornecer a normal de cada vértice** antes do vértice: `glNormal3f(nx, ny, nz); glVertex3f(x, y, z);` (a iluminação depende da normal!).",
        "- **GL_FLAT** (flat shading): **uma cor por face** (usa uma só normal/cor) ⇒ aparência facetada; barato.",
        "- **GL_SMOOTH** (**Gouraud**): calcula a cor **nos vértices** e **interpola** pela face ⇒ aparência suave. Na Atividade 10 é pedido o **smooth shading** com preenchimento e cor difusa.",
    ]),
    BOX("erro", None, [
        "- Esquecer de **normalizar** as normais (as fórmulas de Lambert/especular assumem |m| = 1 ou dividem por |s||m|).",
        "- Esquecer `glEnable(GL_LIGHTING)`/`GL_LIGHT0` ou a **normal** do vértice: a cena fica preta/sem sombreamento.",
        "- Achar que o brilho **difuso** depende do observador (não depende); o **especular** depende.",
        "- Confundir Gouraud (interpola **cores**) com Phong shading (interpola **normais** e calcula a luz por pixel); o OpenGL clássico do slide usa Gouraud (GL_SMOOTH).",
    ]),
    BOX("resumo", None, [
        "- Lambert: I_d = I_s ρ_d cos θ (independe do observador). Especular: I_sp = I_s ρ_s (cos φ)^f; r = −s + 2(s·m/|m|²)m.",
        "- Ambiente evita sombras totais. Modelo completo = ambiente + difusa + especular.",
        "- Fontes: ambiente, difusa, especular, direcional, spot. GL_FLAT (facetado) × GL_SMOOTH (Gouraud, suave).",
    ]),
    EX([
        Q("Uma luz com I_s = 2 incide sobre uma superfície de ρ_d = 0,5 com ângulo de 60° entre s e a normal. Qual a intensidade difusa? E com 90°?",
          "I_d = 2 · 0,5 · cos60° = 2 · 0,5 · 0,5 = **0,5**. Com 90°: cos90° = 0 ⇒ **I_d = 0** (luz rasante não ilumina)."),
        Q("Dados s = (0, 1, 1) e m = (0, 0, 1), calcule o vetor refletido r.",
          ["s·m = 1; |m|² = 1 ⇒ r = −s + 2(1)·m = (0,−1,−1) + (0,0,2) = **(0, −1, 1)**.",
           "Interpretação: r tem o mesmo componente ao longo da normal (z = +1) e o componente tangencial (y) com sinal trocado — s é espelhado em torno de m."]),
        Q("Duas esferas recebem a mesma luz. A esfera A tem expoente especular f = 5 e a B f = 80. Qual terá o realce menor e mais nítido? Qual parecerá mais “emborrachada/fosca”?",
          "**B** (f = 80) tem o realce **pequeno e nítido** (superfície polida, como metal cromado). **A** (f = 5) tem o realce **largo e difuso** (aparência mais fosca/plástico)."),
        Q("Marque a correta:",
          opts=["O brilho difuso (Lambert) depende da posição do observador.",
                "A luz ambiente é necessária para que áreas não iluminadas diretamente não fiquem totalmente escuras.",
                "GL_FLAT interpola as cores entre os vértices.",
                "Uma luz direcional tem posição finita e cone de iluminação."],
          a="**b).** a) falsa — o difuso é independente do observador; c) falsa — GL_FLAT usa uma cor por face (GL_SMOOTH interpola); d) falsa — direcional está no infinito (raios paralelos); o cone é do **spot**."),
        Q("Por que cada vértice precisa de uma normal para a iluminação, e o que muda entre normais por face e normais por vértice ao usar GL_SMOOTH?",
          "Lambert e especular usam **m** (normal) para calcular o ângulo da luz. Com **normais por face**, a face fica com uma só cor (aparência facetada). Com **normais por vértice** (média das faces vizinhas) e GL_SMOOTH, a cor é calculada nos vértices e **interpolada**, dando superfície suave."),
        Q("V ou F: (a) a luz spot possui direção e ângulo de corte; (b) o expoente especular só afeta a luz ambiente; (c) Phong shading interpola normais; (d) a luz ambiente depende da posição do observador.",
          "(a) **V**. (b) **F** — afeta a especular. (c) **V**. (d) **F** — a ambiente é uniforme."),
    ]),
]

# =====================================================================
# 6. COLA
# =====================================================================
C += [
    H1("Cola de última hora e erros comuns", "Releia na véspera."),
    H2("Fórmulas e matrizes essenciais"),
    T(["Tema", "Lembrar"],
      [["Homogêneas", "P = [x y z 1]ᵀ; P′ = M · P; composição lida da **direita p/ esquerda**"],
       ["Translação", "última coluna (Δx, Δy, Δz); x′ = x + Δx …"],
       ["Escala", "diagonal (Ex, Ey, Ez, 1); em torno da **origem**"],
       ["Rz / Rx / Ry", "Rz: x′ = x cos − y sen; y′ = x sen + y cos · Rx: y′ = y cos − z sen; z′ = y sen + z cos · Ry: x′ = x cos + z sen; z′ = −x sen + z cos"],
       ["Rotação com pivô", "T(c) · R · T(−c)"],
       ["Modelo", "M_Model = T · R · S;  M_ModelView = M_View · M_Model"],
       ["Perspectiva", "x_p = x/(z/d), y_p = y/(z/d); dividir por W"],
       ["Câmera", "n = eye − look;  u = up × n;  v = n × u  (olha para −n)"],
       ["Cadeia", "P_clip = M_Proj · M_View · M_Model · P"],
       ["Câmera: movimentos", "slide (δu,δv,δn) · roll (n) · pitch (u) · yaw (v)"],
       ["Euler", "V − A + F = 2 (poliedro convexo)"],
       [".obj", "v, vt, vn, f (índices a partir de 1)"],
       ["Pipeline", "Modelagem → Transformações → Projeção → Clipping → Rasterização → Fragmentos → Testes → Framebuffer"],
       ["Lambert", "I_d = I_s ρ_d (s·m)/(|s||m|)"],
       ["Especular", "r = −s + 2(s·m/|m|²)m;  I_sp = I_s ρ_s (r·v/|r||v|)^f"],
       ["Shading", "GL_FLAT (1 cor/face) × GL_SMOOTH (Gouraud, interpola); luzes: ambiente, difusa, especular, direcional, spot"]],
      widths=[3.6, 13.4], size=9.5),
    H2("Erros que mais custam pontos"),
    N(["Ordem das matrizes: **T·R·S aplica S primeiro**.",
       "Girar/escalar sem **levar o pivô à origem** (esquecer T(−c) e T(+c)).",
       "Sinais das matrizes **Ry** (invertidos em relação a Rx e Rz).",
       "Esquecer a **divisão por W** na perspectiva.",
       "Câmera olha para **−n**; n = **eye − look** (e não look − eye).",
       "Indexar o .obj a partir de 0 (começa em **1**).",
       "Colocar o clipping **depois** da rasterização.",
       "Dizer que o difuso depende do observador.",
       "Confundir **flat** (uma cor por face) com **smooth** (interpolado).",
       "Esquecer a **normal** nos vértices ao ligar a iluminação."]),
    H2("Mini-simulado final"),
    EX([
        Q("Escreva a matriz (4×4, em forma de produto) que escala um objeto por 2 em todos os eixos **em torno do ponto c = (1, 1, 1)**, e aplique-a ao vértice (2, 1, 1).",
          ["M = T(1,1,1) · E(2,2,2) · T(−1,−1,−1).",
           "(2,1,1) − c = (1,0,0) → escala → (2,0,0) → + c = **(3, 1, 1)**. (O ponto se afastou do pivô de distância 1 para 2.)"]),
        Q("Dada a face `f 1 2 3 4` do cubo de v ±1 apresentado (vértices 1 (−1,−1,1), 2 (1,−1,1), 3 (1,1,1), 4 (−1,1,1)), em qual plano ela está e qual a normal para fora?",
          "Todos têm z = +1: é a **face frontal** no plano z = 1. A ordem 1→2→3→4 é anti-horária vista de +z ⇒ normal **(0, 0, +1)**."),
        Q("Um ponto P = (2, 4, 6) é projetado em perspectiva com d = 1. Qual o ponto no plano de imagem e o que acontece com x_p se z dobrar?",
          "W = z/d = 6; x_p = 2/6 = **0,333**; y_p = 4/6 = **0,667**; z_p = 1. Se z dobrar (12): x_p = 2/12 = **0,167** — **metade**."),
        Q("Descreva em 4 linhas o que acontece, no pipeline, com um triângulo da cena até o pixel azul na tela.",
          "O triângulo (vértices, normais, material) é transformado (model → mundo → câmera) e projetado; o **clipping** descarta o que estiver fora do volume; a **rasterização** gera fragmentos e interpola atributos; "
          "nas **operações de fragmento** aplica-se iluminação/textura/material (cor final = textura × iluminação × material); os **testes** (profundidade, estêncil, alpha) decidem se o fragmento vence; o vencedor é gravado no **framebuffer** e vai ao monitor."),
    ], title="Exercícios — Mini-simulado"),
]
