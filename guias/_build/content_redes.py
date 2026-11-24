# -*- coding: utf-8 -*-
from guide_builder import *

COLOR = "C62828"  # vermelho
TITLE = "Redes de Computadores"
PROF = "Prof. Mario Lemes Proença Jr. · Departamento de Computação · UEL"
EXAM = "30/11/2026"
SOURCES = "Apostilas: Redes de Computadores (200 p.) · Gerência de Redes (71 p.) · Segurança em TIC (47 p.)"
TOPICS = ["Camadas OSI e TCP/IP", "Nível Físico", "Enlace e Ethernet", "Rede e Roteamento", "TCP/IP: IP, TCP, UDP", "Gerência (SNMP/FCAPS)", "Segurança"]
NOTE = "Versão enxuta: só os tópicos centrais das apostilas (a prova é objetiva e de peso menor). Detalhes históricos, tabelas de mercado e fabricantes ficaram de fora de propósito."

C = []

# =====================================================================
# 0. COMO ESTUDAR
# =====================================================================
C += [
    H1("Como estudar Redes para esta prova", numbered=False,
       intro="Prova objetiva e de peso pequeno: foque em reconhecer conceitos, siglas e números-chave. Este guia é uma versão enxuta das três apostilas."),
    BOX("lembrete", "Prioridades (do mais para o menos provável)", [
        "- **Camadas** OSI e TCP/IP: o que cada camada faz, onde cada equipamento/protocolo se encaixa.",
        "- **Ethernet / enlace**: CSMA/CD, quadro 802.3, MAC, switch × hub × roteador, domínio de colisão e de broadcast, VLAN.",
        "- **IP**: classes, máscara, sub-redes, CIDR, endereços privados, NAT, ARP, ICMP.",
        "- **TCP × UDP**, portas dos serviços mais comuns, roteamento (vetor de distância × estado de enlace; RIP/OSPF/BGP).",
        "- **Gerência**: FCAPS, SLA/disponibilidade, SNMP/MIB, fluxos (NetFlow/IPFIX).",
        "- **Segurança**: pilares (CIA), ataques (DoS, MITM, phishing…), defesas (firewall, IDS).",
    ]),
    BOX("insight", "Um truque para tudo: pense em “quem fala com quem”", [
        "Cada camada conversa com a camada **de mesmo nível** na outra máquina (protocolo) e presta serviço à camada **de cima** (interface). "
        "Quase toda pergunta de Redes se resolve perguntando: *em que camada isso acontece?* (ex.: MAC → enlace; IP → rede; porta → transporte).",
    ]),
]

# =====================================================================
# 1. INTRODUÇÃO
# =====================================================================
C += [
    H1("Introdução, tipos de rede e padronização",
       "Apostila de Redes — Introdução · Os conceitos básicos que sustentam o resto."),
    H2("O que é uma rede e por que existe"),
    P("Rede de computadores = conjunto de computadores **autônomos** interligados por um meio de comunicação (cabos metálicos, fibra, rádio/wi-fi, satélite) que trocam informações para **cooperar**. "
      "Surgiu da junção de computadores com telecomunicações, substituindo os mainframes/centros de computação centralizados. "
      "Benefícios: compartilhar recursos de hardware e software, serviços distribuídos, melhor custo/benefício, comunicação (e-mail, web, videoconferência)."),
    BOX("def", "Elementos de uma rede", [
        "- **Hosts/estações**: computadores que executam as aplicações.",
        "- **Sistema de comunicação**: **nós de comutação** (roteadores, switches) + **meios/enlaces** de transmissão.",
        "- **Protocolo**: conjunto de regras (formatos, ordem, tratamento de erros) que governa a comunicação, pois o meio **não é confiável** (erros, perda, atraso, congestionamento).",
    ]),
    H2("Comutação de circuitos × comutação de pacotes"),
    T(["", "Comutação de **circuitos**", "Comutação de **pacotes**"],
      [["Ideia", "Canal **reservado** de ponta a ponta durante a comunicação", "Dados divididos em pacotes que **compartilham** os enlaces"],
       ["Fases", "Estabelece o circuito (call setup) → transfere → encerra", "Sem setup; cada pacote é encaminhado"],
       ["Eficiência", "Desperdício quando o canal fica ocioso", "Alta (multiplexação estatística)"],
       ["Problemas", "Congestionamento = bloqueio de novas chamadas", "Overhead de cabeçalho, atrasos variáveis, roteamento/sequenciação"],
       ["Exemplo", "Telefonia tradicional (PSTN)", "Internet (IP), X.25, Frame Relay"]],
      widths=[2.6, 7, 7.4], size=9.5),
    BOX("erro", "Pacote menor nem sempre é melhor", [
        "O cabeçalho é um custo fixo por pacote. No exemplo do slide (40 bytes de dados + 4 bytes de cabeçalho por pacote), dividir demais **aumenta o tempo total** (muitos cabeçalhos). Há um tamanho de pacote “ótimo”.",
    ]),
    H2("Classificação de redes"),
    T(["Critério", "Tipos"],
      [["Por **tecnologia de transmissão**", "**Broadcast/multiacesso** (um meio compartilhado: LANs Ethernet) × **ponto a ponto** (enlaces dedicados, WANs)"],
       ["Por **escala**", "**PAN** (pessoal: Bluetooth/Zigbee, IEEE 802.15) · **LAN** (campus, até ~2 km, 10 Mbit/s a 100+ Gbit/s, Ethernet 802.3 e Wi-Fi 802.11) · **MAN** (cidade, ~10 km) · **WAN** (país/continente; operadoras; enlaces dedicados, SDH, DWDM, Metro/Carrier Ethernet)"],
       ["Sem fio", "WPAN (802.15), WLAN (802.11, Wi-Fi), WMAN/WWAN (4G LTE, 5G)"]],
      widths=[4, 13], size=9.5),
    H2("Organizações de padronização"),
    T(["Sigla", "Quem é", "Exemplo"],
      [["**IETF**", "Internet Engineering Task Force", "TCP/IP, RFCs"],
       ["**IEEE**", "Institute of Electrical and Electronics Engineers", "802.3 (Ethernet), 802.11 (Wi-Fi), 802.1Q (VLAN)"],
       ["**ITU**", "International Telecommunication Union", "Telecomunicações e rádio; 5G = IMT-2020"],
       ["**ISO**", "International Organization for Standardization", "Modelo OSI"]],
      widths=[3, 7.5, 6.5], size=9.5),
    BOX("resumo", None, [
        "- Rede = computadores autônomos + meio + protocolos. Protocolos existem porque o meio não é confiável.",
        "- Circuitos = canal reservado (telefonia); pacotes = compartilhado (Internet), com overhead de cabeçalho.",
        "- PAN < LAN < MAN < WAN; Ethernet = IEEE 802.3, Wi-Fi = IEEE 802.11.",
    ]),
    EX([
        Q("Qual afirmação descreve corretamente a comutação de pacotes?",
          opts=["Aloca um canal exclusivo para cada comunicação durante todo o tempo.",
                "Permite o compartilhamento dos enlaces, evita o setup inicial, mas acrescenta overhead de cabeçalho e atrasos variáveis.",
                "É a tecnologia da telefonia analógica tradicional.",
                "Não precisa de endereçamento."],
          a="**b).** a) descreve comutação de **circuitos**; c) a telefonia tradicional usa circuitos; d) pacotes **precisam** de endereço no cabeçalho."),
        Q("Associe: (1) LAN; (2) WAN; (3) PAN; (4) MAN — a) cidade (~10 km); b) cobre país/continente, operadoras; c) campus, poucos km; d) curtas distâncias pessoais (Bluetooth).",
          "(1)-c, (2)-b, (3)-d, (4)-a."),
        Q("V ou F: (a) IEEE 802.11 é Ethernet cabeada; (b) o IETF padroniza TCP/IP via RFCs; (c) em uma rede de broadcast, toda mensagem é recebida por todos os nós do meio.",
          "(a) **F** — 802.11 é Wi-Fi (Ethernet é 802.3). (b) **V**. (c) **V** (cada nó ouve; só o destinatário a processa)."),
    ]),
]

# =====================================================================
# 2. MODELOS DE CAMADAS
# =====================================================================
C += [
    H1("Arquitetura em camadas: OSI e TCP/IP",
       "Apostila de Redes — Software de Rede, RM-OSI e TCP/IP · A divisão de trabalho que organiza toda a disciplina."),
    H2("Por que camadas?"),
    P("“Dividir para conquistar”: cada camada resolve um problema específico, **presta serviços à camada superior** usando os da inferior, e conversa com a **camada de mesmo nível** do outro lado por meio de um **protocolo**."),
    BOX("def", "Vocabulário", [
        "- **Protocolo**: regras de conversa entre camadas **pares** (horizontal).",
        "- **Interface / serviço**: o que a camada oferece à camada **de cima** (vertical). O ponto de acesso é o **SAP** (Service Access Point).",
        "- **Entidade**: elemento ativo de uma camada (software ou chip). **Pilha de protocolos** (protocol stack): conjunto de protocolos de um sistema.",
        "- **Primitivas** de serviço: Request, Indication, Response, Confirm. **Serviço orientado a conexão** (negocia antes) × **não orientado** (envia direto).",
    ]),
    BOX("insight", "Vantagens do modelo em camadas", [
        "**Divisão** da complexidade e **independência** entre camadas ⇒ facilidade de **manutenção** (troca uma camada sem mexer nas outras, se o serviço for o mesmo) e de **evolução** (novas aplicações aproveitam as camadas inferiores).",
    ]),
    H2("As 7 camadas do RM-OSI (ISO)"),
    P("O OSI é um **modelo de referência** (não define protocolos específicos). Os protocolos reais vêm de outras arquiteturas — a mais importante: **TCP/IP**."),
    T(["#", "Camada", "Função principal", "Unidade / exemplos"],
      [["7", "**Aplicação**", "Protocolos que as aplicações precisam", "Mensagem · HTTP, SMTP, FTP, DNS, SNMP"],
       ["6", "**Apresentação**", "**Sintaxe e semântica** dos dados (codificação, compressão, criptografia)", "—"],
       ["5", "**Sessão**", "Estabelecer e gerir **sessões** entre máquinas (login remoto, sincronização)", "—"],
       ["4", "**Transporte**", "Comunicação **fim a fim**; quebra dados, garante entrega correta e ordem (se for o caso)", "Segmento / datagrama · TCP, UDP"],
       ["3", "**Rede**", "Roteamento de pacotes da origem ao destino por várias sub-redes; endereçamento lógico; 1ª camada fim a fim", "Pacote/datagrama · IP, ICMP, OSPF"],
       ["2", "**Enlace**", "Acesso ao meio (MAC), **quadros** (frames), detecção/correção de erros (CRC), controle de fluxo entre nós vizinhos", "Quadro · Ethernet 802.3, PPP, HDLC"],
       ["1", "**Física**", "Transmissão de **bits** pelo meio (sinais, cabos, conectores, modulação)", "Bit · UTP, fibra, rádio"]],
      widths=[1, 3, 8.5, 4.5], align=["c", "l", "l", "l"], size=9.5),
    BOX("lembrete", "Mnemônico (de cima para baixo)", [
        "**A**plicação · **A**presentação · **S**essão · **T**ransporte · **R**ede · **E**nlace · **F**ísica — ou: *“A**P**lique **S**empre **T**oda **R**eta **E**m **F**ábrica”* (use o que ficar mais fácil).",
    ]),
    H2("O modelo TCP/IP e o encapsulamento"),
    T(["Camada TCP/IP", "Equivale no OSI", "Protocolos"],
      [["**Aplicação**", "Aplicação + Apresentação + Sessão", "HTTP, HTTPS, FTP, SMTP, DNS, SNMP, Telnet, SSH"],
       ["**Transporte**", "Transporte", "TCP, UDP"],
       ["**Internet / Rede**", "Rede", "IP, ICMP, ARP, OSPF, BGP"],
       ["**Enlace / Acesso à rede**", "Enlace + Física", "Ethernet, Wi-Fi, PPP"]],
      widths=[4.5, 6, 6.5], size=9.5),
    P("**Encapsulamento:** cada camada acrescenta seu **cabeçalho** (header) aos dados recebidos de cima. "
      "Na LAN 802.3: dados da aplicação → **+ cabeçalho TCP** (segmento) → **+ cabeçalho IP** (datagrama) → **+ cabeçalho/trailer Ethernet** (quadro). O receptor desencapsula em ordem inversa."),
    CODE("""[ Eth hdr | IP hdr | TCP hdr | Dados da aplicação | Eth FCS ]
   enlace     rede     transporte      aplicação      enlace""", "Encapsulamento TCP/IP sobre Ethernet"),
    BOX("erro", None, [
        "- Dizer que o OSI “é” a arquitetura da Internet: a Internet usa **TCP/IP**; o OSI é referência didática.",
        "- Confundir camadas: **MAC = enlace**, **IP = rede**, **porta = transporte**, **roteador = rede**, **switch = enlace**, **hub/repetidor = física**.",
    ]),
    BOX("resumo", None, [
        "- 7 camadas OSI: Física, Enlace, Rede, Transporte, Sessão, Apresentação, Aplicação. TCP/IP: 4 camadas (Aplicação, Transporte, Internet, Acesso à rede).",
        "- Cada camada: serviço para cima, protocolo com a camada par, encapsulamento com cabeçalho.",
    ]),
    EX([
        Q("Em qual camada do OSI atuam, respectivamente: roteador, switch e hub?",
          opts=["Rede, enlace, física", "Enlace, rede, física", "Transporte, rede, enlace", "Rede, física, enlace"],
          a="**a).** Roteador = rede (IP); switch = enlace (MAC); hub = física (repete bits)."),
        Q("Quais camadas do OSI correspondem à camada de **Aplicação** do TCP/IP?",
          "Aplicação, Apresentação e Sessão."),
        Q("V ou F: (a) o protocolo conversa verticalmente entre camadas adjacentes; (b) o encapsulamento adiciona cabeçalhos ao descer pela pilha; (c) o OSI define os protocolos usados na Internet.",
          "(a) **F** — protocolo é a conversa **horizontal** entre camadas pares; a vertical é a **interface/serviço**. (b) **V**. (c) **F** — o OSI é só modelo de referência."),
        Q("Qual a unidade de dados de cada camada: enlace, rede e transporte?",
          "Enlace: **quadro (frame)**; rede: **pacote/datagrama**; transporte: **segmento** (TCP) ou datagrama UDP."),
    ]),
]

# =====================================================================
# 3. NÍVEL FÍSICO
# =====================================================================
C += [
    H1("Nível Físico: sinais, meios e acesso",
       "Apostila de Redes — Teoria da Comunicação, Meios de Transmissão, xDSL, Wireless · Como bits viram sinais e por quais meios viajam."),
    H2("Sinais e problemas da transmissão"),
    B(["**Sinal digital**: níveis discretos de tensão (0/1). **Analógico**: varia continuamente em amplitude e tempo.",
       "Uma onda senoidal tem **amplitude** (valor de pico), **frequência** (ciclos/s, em Hz) e **fase** (posição relativa no tempo).",
       "**Atenuação**: perda de energia (em dB/km; piora com a frequência e a distância). **Distorção**: deformação sistemática do canal (pode ser equalizada). **Ruído**: eco, impulsivo, **cross-talk** (interferência entre pares)."]),
    H2("Bits × bauds, Nyquist e Shannon"),
    BOX("def", "Conceitos e leis", [
        "- **Baud** = símbolos/s (taxa de sinalização); **bit/s** = taxa de informação. Com L níveis por símbolo: **1 baud = log₂L bit/s** por símbolo.",
        "- **Nyquist (canal sem ruído, largura de banda W Hz):** máx. **2W bauds** → = C = 2 · W · log₂ L  (bit/s)",
        "- **Shannon (canal com ruído):** limite de capacidade dado pela relação sinal-ruído → = C = W · log₂(1 + S/N)  (S/N em escala linear, não em dB)",
    ]),
    BOX("exemplo", "Contas dos slides (canal telefônico W = 3400 Hz)", [
        "- Nyquist, 2 bits por símbolo (L = 4): C = 2 · 3400 · 2 = **13.600 bit/s**. Com 8 bits por símbolo (L = 256 níveis): C = 2 · 3400 · 8 = **54.400 bit/s**.",
        "- Shannon, S/N = 30 dB ⇒ S/N = 10^{30/10} = 1000: C = 3400 · log₂(1 + 1000) ≈ 3400 · 9,97 ≈ **33,9 kbit/s**.",
    ]),
    BOX("erro", "Cuidados", [
        "- A apostila escreve “C = 2W log₂(1+S/N)” no texto, mas na **conta** usa C = 3400·log₂(1+1000). A forma padrão de Shannon é **C = W·log₂(1+S/N)** (sem o fator 2). Na dúvida, siga a conta do exemplo.",
        "- **dB → razão**: S/N(dB) = 10·log₁₀(S/N). 30 dB = 1000×; 20 dB = 100×; 10 dB = 10×.",
        "- Baud ≠ bit/s: só são iguais se cada símbolo carrega **1 bit** (sinal binário).",
    ]),
    H2("Meios de transmissão"),
    T(["Meio", "Características", "Uso típico"],
      [["**Par trançado** (UTP/STP)", "Barato; limite de **100 m** em LAN; categorias: Cat5 (100 MHz, 100BASE-TX), **Cat5e** (1000BASE-T), **Cat6** (250 MHz, 10GBASE-T até 55 m), **Cat6A** (500 MHz, 10GBASE-T a 100 m), Cat8 (2000 MHz, 25/40GBASE-T)", "Cabeamento estruturado de LANs; linha de assinante (xDSL)"],
       ["**Cabo coaxial**", "Maior blindagem que o par trançado; barramento 10BASE5/10BASE2 (legado)", "TV a cabo (HFC), Ethernet antiga"],
       ["**Fibra óptica**", "Sinal de **luz**; imune a interferência eletromagnética; maior distância e banda. **Multimodo** (degrau/índice gradual, curtas distâncias) × **monomodo** (longas distâncias)", "Backbones, FTTH, enlaces submarinos, DWDM"],
       ["**Sem fio**", "Rádio; compartilhado, sujeito a interferência. Wi-Fi 802.11 (2,4/5/6 GHz), Bluetooth/Zigbee (PAN), 4G/5G", "WLAN, celular, IoT"]],
      widths=[3.4, 9, 4.6], size=9),
    BOX("def", "Notação IEEE: “ABC”", [
        "**A** = taxa em Mbit/s · **B** = modo (BASE = banda base) · **C** = alcance em centenas de metros (número) **ou** tipo de meio (T = par trançado, F = fibra). Ex.: **10BASE-T** = 10 Mbit/s, banda base, par trançado; **10BASE5** = 10 Mbit/s, 500 m (coaxial).",
    ]),
    H3("Multiplexação e hierarquias digitais"),
    B(["**FDM**: divide o canal em **faixas de frequência** (ex.: TV a cabo). **TDM**: divide o **tempo** em slots. **DWDM**: múltiplos comprimentos de onda (cores) na mesma fibra (ex.: 160 canais × 10 Gbit/s).",
       "**PDH** (E1 = 2,048 Mbit/s, E3 = 34 Mbit/s; canal B = 64 kbit/s) e **SDH/SONET** (OC-1, OC-3…) são as hierarquias digitais das operadoras."]),
    H2("Acesso à Internet: xDSL, HFC, FTTH, wireless"),
    T(["Tecnologia", "Meio", "Ideia-chave"],
      [["**xDSL** (ADSL etc.)", "Par telefônico de cobre", "Aproveita a linha de assinante. **ADSL é assimétrico** (download > upload); SDSL/HDSL simétricos; VDSL mais rápido, distância menor"],
       ["**HFC / cabo**", "Fibra + coaxial (TV a cabo)", "Cable modem; meio compartilhado"],
       ["**FTTH / GPON**", "Fibra até a casa", "Banda muito alta; padrão atual (ADSL em retirada)"],
       ["**LTE / 5G**", "Rádio", "Móvel e “última milha” sem fio"]],
      widths=[3.4, 4.6, 9], size=9.5),
    H3("Wireless em uma linha"),
    B(["**Wi-Fi (IEEE 802.11)**: gerações 5 (ac), **6 (ax)**, **7 (be)**; modos: com **infraestrutura** (Access Point) ou **ad hoc** (sem infra).",
       "**Bluetooth** (WPAN, IEEE 802.15): classes de alcance 100 m / 10 m / 1 m; substitui cabos em curta distância. **Zigbee**: baixa taxa/baixo consumo (IoT)."]),
    BOX("lembrete", None, [
        "Conversões úteis: **1 byte = 8 bits**. 100 Mbit/s = 12,5 MB/s; **1 Gbit/s = 125 MB/s**; 10 Gbit/s = 1,25 GB/s.",
        "Padrões Ethernet: 802.3 (10 Mbit/s) → **802.3u** (Fast, 100) → **802.3z** (Gigabit) → **802.3ae** (10 Gbit/s) → 802.3ba (40/100 Gbit/s).",
    ]),
    BOX("resumo", None, [
        "- Nyquist: C = 2W·log₂L (sem ruído). Shannon: C = W·log₂(1+S/N) (com ruído).",
        "- Par trançado ≤ 100 m em LAN; fibra para longa distância e alta banda; ADSL é assimétrico.",
        "- “10BASE-T” = 10 Mbit/s · banda base · par trançado.",
    ]),
    EX([
        Q("Um canal de 3400 Hz sem ruído usa 4 níveis de sinal (2 bits/símbolo). Qual a capacidade máxima segundo Nyquist?",
          "C = 2·W·log₂L = 2 · 3400 · 2 = **13.600 bit/s**."),
        Q("Qual a relação sinal-ruído em escala linear de um canal com 20 dB? E a capacidade de Shannon com W = 1000 Hz?",
          ["S/N = 10^{20/10} = **100**.",
           "C = W·log₂(1+100) = 1000 · log₂(101) ≈ 1000 · 6,66 ≈ **6,66 kbit/s**."]),
        Q("Qual o significado de “1000BASE-T”?",
          "1000 Mbit/s (1 Gbit/s), transmissão em banda base, sobre **par trançado** (Cat5e ou superior), até 100 m."),
        Q("V ou F: (a) o ADSL é simétrico; (b) a fibra monomodo é indicada para longas distâncias; (c) cross-talk é interferência entre pares de fios próximos; (d) 1 baud sempre equivale a 1 bit/s.",
          "(a) **F** — é assimétrico (download maior). (b) **V**. (c) **V**. (d) **F** — só com sinal binário."),
    ]),
]

# =====================================================================
# 4. ENLACE / ETHERNET
# =====================================================================
C += [
    H1("Nível de Enlace e Ethernet (IEEE 802.3)",
       "Apostila de Redes — Nível de Enlace, MAC, 802.3, Switch, VLAN · A camada mais cobrada em LANs."),
    H2("Funções do enlace"),
    B(["**Enquadramento** (framing): delimita os quadros — *character stuffing* e **bit stuffing** (HDLC usa a flag **01111110**).",
       "**Detecção de erros**: paridade, **CRC/FCS**. **Confirmação**: ACK/NACK, timeout, retransmissão.",
       "**Controle de fluxo**: *stop-and-wait* e **janela deslizante** (*sliding window*): o transmissor pode ter até L quadros sem ACK.",
       "**Acesso ao meio** (subcamada **MAC**) em canais compartilhados.",
       "**Protocolos**: **HDLC** (orientado a bit, “pai” dos protocolos de enlace), **PPP** (ponto a ponto na Internet; deriva do HDLC; autenticação e negociação de IP) e a família **IEEE 802**."]),
    BOX("def", "Subcamadas do enlace nas LANs 802", [
        "- **LLC (IEEE 802.2)**: comum a todos os padrões 802; multiplexação, controle de erro e fluxo.",
        "- **MAC**: depende da tecnologia (802.3 Ethernet/CSMA-CD, 802.11 Wi-Fi…); resolve **quem usa o canal e quando**.",
    ]),
    H2("O problema do acesso ao meio e o CSMA/CD"),
    P("Em canais **broadcast** compartilhados, se duas estações transmitem ao mesmo tempo, os quadros **colidem** e são perdidos. O Ethernet (802.3) usa **CSMA/CD** (Carrier Sense Multiple Access with Collision Detection) 1-persistente:"),
    N(["**Escuta o meio** (carrier sense). Se **livre**, transmite; se ocupado, espera até liberar (1-persistente: transmite assim que liberar).",
       "Enquanto transmite, **detecta colisão** (compara o sinal enviado/recebido).",
       "Se colidiu: envia sinal de reforço **JAM**, interrompe e aguarda um tempo aleatório (**backoff binário exponencial**).",
       "Retransmite. Após **16 tentativas** sem sucesso, desiste e reporta erro."]),
    BOX("def", "Backoff binário exponencial truncado", [
        "Após a *i*-ésima colisão, a estação sorteia um número de **slots** entre **0 e 2^{i} − 1** e espera esse tempo. Slot = **51,2 µs** (a 10 Mbit/s) = tempo de 512 bits.",
        "- 1ª colisão: {0, 1} · 2ª: {0…3} · 3ª: {0…7} · 4ª: {0…15} … (trunca em 2^{10} − 1; máximo de **16 tentativas**).",
    ]),
    BOX("insight", "Por que existe um tamanho mínimo de quadro?", [
        "Para detectar uma colisão, a estação precisa **ainda estar transmitindo** quando o sinal de colisão voltar do ponto mais distante: o quadro tem que durar pelo menos o **round-trip** da rede. "
        "A apostila calcula M_{min} = 2 · C · T_{p} = 2 · (10 Mbit/s) · (25,6 µs) = **512 bits = 64 bytes**, equivalente a **51,2 µs** a 10 Mbit/s.",
    ]),
    H2("Quadro Ethernet (802.3)"),
    T(["Campo", "Tamanho", "Função"],
      [["Preâmbulo + SFD", "7 + 1 bytes", "10101010… e 10101011: sincronizam o relógio do receptor"],
       ["Endereço de destino", "6 bytes", "MAC de destino. **FF:FF:FF:FF:FF:FF = broadcast**"],
       ["Endereço de origem", "6 bytes", "MAC de origem (48 bits; os 24 primeiros identificam o fabricante)"],
       ["Tipo/Tamanho", "2 bytes", "< 1500: **tamanho**; ≥ 1536 (0x0600): **protocolo** (ex.: 0x0800 = IPv4)"],
       ["Dados (+ PAD)", "**46 a 1500** bytes", "PAD completa até o mínimo"],
       ["FCS (CRC-32)", "4 bytes", "Detecção de erros"]],
      widths=[3.6, 3.2, 10.2], size=9.5),
    BOX("lembrete", "Números do quadro (decore)", [
        "- Quadro válido: **64 a 1518 bytes** (6+6+2+até 1500+4), sem contar preâmbulo/SFD. MTU Ethernet = **1500 bytes**.",
        "- **Endereço MAC**: 6 bytes (48 bits), em hexadecimal (ex.: 00-0C-F1-F4-48-E4); identifica a **placa** na LAN, é **horizontal** (sem hierarquia), ao contrário do endereço IP (hierárquico).",
    ]),
    BOX("def", "Erros comuns observados em Ethernet", [
        "**Colisão** · **Fragments/Runt**: quadro < 64 B (geralmente colisão) · **Jabber**: > 1518 B com CRC errado · **Oversize**: > 1518 com CRC correto · **CRC error**: FCS inválido.",
    ]),
    H2("Equipamentos: hub, switch e roteador"),
    T(["Equipamento", "Camada", "O que faz", "Domínios"],
      [["**Hub / repetidor**", "1 (Física)", "Repete bits para todas as portas", "1 domínio de colisão e 1 de broadcast para tudo"],
       ["**Switch**", "2 (Enlace)", "Comuta quadros pelo **MAC**, em hardware; aprende em quais portas estão os MACs", "**Cada porta = 1 domínio de colisão**; broadcast continua único"],
       ["**Roteador**", "3 (Rede)", "Encaminha pacotes pelo **IP**, em software; segmenta broadcast, conecta redes/WAN", "Cada interface = **1 domínio de broadcast** (e de colisão)"]],
      widths=[3, 2.2, 6.6, 5.2], size=9.5),
    BOX("insight", "O fim prático do CSMA/CD", [
        "Com **switches full-duplex**, cada porta é um canal dedicado e **não há colisões**: o CSMA/CD deixou de ser usado nas LANs atuais, restando o formato lógico do quadro. "
        "Switch **segmenta domínios de colisão**; roteador (ou VLAN) **segmenta domínios de broadcast**.",
    ]),
    H2("VLAN (IEEE 802.1Q) e Spanning Tree"),
    B(["**VLAN** = LAN virtual: define um **domínio de broadcast lógico** independente da localização física. Reduz broadcast e melhora a **segurança**. Comunicação entre VLANs exige **roteamento** (nível 3).",
       "**802.1Q** insere uma **tag** no quadro com o **VID (1 a 4094)**. Portas **access** (*untagged*, uma VLAN) × portas **trunk** (*tagged*, várias VLANs, entre switches).",
       "Tipos de VLAN: por **porta**, por **MAC**, por **endereço de rede (camada 3)**, por multicast IP.",
       "**STP (802.1D)** evita **laços** (loops) em topologias com caminhos redundantes entre switches; **RSTP (802.1w)** converge mais rápido; MSTP (802.1s)."]),
    H2("Desempenho e congestionamento"),
    B(["Dois parâmetros: **vazão (throughput)** e **atraso**; interligados. Confiabilidade (taxa de erros) também conta.",
       "Sintomas de congestionamento para o usuário: resposta lenta, demora de login, perda de conexões. Sinais para o administrador (referências da apostila): **picos > 50 %**, **utilização média > 15 %** (em Ethernet compartilhada), **colisões > 5 %**.",
       "Ferramentas: SNMP, sFlow/NetFlow/IPFIX, sniffers."]),
    BOX("resumo", None, [
        "- CSMA/CD: escutar → transmitir → detectar colisão → JAM → backoff (0…2^i−1 slots) → ≤16 tentativas.",
        "- Quadro 802.3: 64–1518 B; dados 46–1500; MAC 6 B; FCS CRC-32.",
        "- Hub 1 domínio de colisão; switch 1 por porta; roteador/VLAN dividem broadcast. 802.1Q: VID 1–4094.",
    ]),
    EX([
        Q("Um switch de 8 portas conecta 8 computadores diretamente (1 por porta). Quantos domínios de colisão e quantos domínios de broadcast existem?",
          "**8 domínios de colisão** (um por porta) e **1 domínio de broadcast** (um switch simples não separa broadcast)."),
        Q("Qual o tamanho mínimo e máximo de um quadro Ethernet 802.3 (do endereço de destino ao FCS) e por que existe o mínimo?",
          "Mínimo **64 bytes** e máximo **1518 bytes**. O mínimo garante que a estação ainda esteja transmitindo quando a notícia da colisão chegar (detecção de colisão); quadros menores recebem **PAD**."),
        Q("Após a 3ª colisão consecutiva, entre quantos slots a estação sorteia o tempo de espera? Quantas tentativas no máximo?",
          "Entre **0 e 7** slots (2³ − 1). Máximo de **16** tentativas; depois disso, erro."),
        Q("Marque V ou F: (a) o MAC pertence à camada de rede; (b) o endereço FF:FF:FF:FF:FF:FF é de broadcast; (c) VLANs diferentes se comunicam sem roteamento; (d) o STP evita laços entre switches.",
          "(a) **F** — MAC é enlace. (b) **V**. (c) **F** — precisa de camada 3. (d) **V**."),
        Q("Quem separa domínios de broadcast?",
          opts=["Hub", "Switch comum", "Roteador (ou VLAN)", "Cabo Cat6"],
          a="**c).** Hub não separa nada; switch comum separa colisão (não broadcast)."),
    ]),
]

# =====================================================================
# 5. REDE E ROTEAMENTO
# =====================================================================
C += [
    H1("Nível de Rede, Internetworking e Roteamento",
       "Apostila de Redes — Camada de Rede · Como pacotes cruzam várias redes até o destino."),
    H2("Funções da camada de rede"),
    B(["Levar pacotes da **origem ao destino** passando por vários **roteadores** (cada passagem = **1 hop**). É a **1ª camada fim a fim** do OSI.",
       "**Endereçamento** lógico, **roteamento** (decidir a saída por onde o pacote segue), controle de congestionamento, fragmentação.",
       "**Internetworking**: interligar redes heterogêneas; o protocolo dominante é o **IP**. Elementos: sub-redes, **End Systems** (hosts) e **Intermediate Systems** (roteadores)."]),
    H2("Circuito virtual × datagrama"),
    T(["", "Circuito virtual (orientado a conexão; ex.: ATM, X.25)", "Datagrama (não orientado; ex.: IP)"],
      [["Setup", "Necessário (cria o VC)", "Não é necessário"],
       ["Endereço no pacote", "Só um **número de VC**", "**Endereço completo** de origem e destino"],
       ["Roteamento", "Decidido no setup; pacotes seguem o mesmo caminho", "**Cada pacote** é roteado independentemente"],
       ["Falha de roteador", "Todos os VCs que passam por ele **caem**", "Só os pacotes no roteador se perdem; os demais seguem outra rota"],
       ["Controle de congestionamento", "Fácil (reserva buffers no setup)", "Difícil"],
       ["Filosofia", "Telecomunicações: rede confiável, **complexidade na rede**", "Internet: rede “burra”, **complexidade nas pontas** (transporte)"]],
      widths=[3.3, 7, 6.7], size=9.5),
    BOX("def", "Endereçamento: hierárquico × horizontal", [
        "- **Hierárquico** (IP): rede + sub-rede + estação; muda se a máquina muda de rede.",
        "- **Horizontal/plano** (MAC 802.x): sem relação com a localização.",
    ]),
    H2("Algoritmos de roteamento"),
    T(["Tipo", "Como funciona"],
      [["**Não adaptativos (estáticos)**", "Rotas fixas, definidas com a rede “fora do ar”; não reagem a mudanças"],
       ["**Adaptativos (dinâmicos)**", "Reagem a mudanças de topologia/tráfego; roteadores **trocam informações**"]],
      widths=[5, 12]),
    BOX("def", "Os principais algoritmos", [
        "- **Menor caminho (Shortest Path / Dijkstra)** e **Flooding** (inunda todas as saídas; usado para medir atrasos).",
        "- **Vetor de distância (distance vector)** — usado no **RIP**: cada roteador mantém uma tabela com a melhor distância conhecida a cada destino e **troca-a com os vizinhos**; “roteamento por rumor”. Simples, mas converge devagar.",
        "- **Estado de enlace (link state)** — usado no **OSPF**: cada roteador **divulga o estado de seus enlaces a todos**, monta o mapa da rede e calcula os caminhos mínimos (Dijkstra). Converge rápido, escala melhor.",
        "- **Roteamento hierárquico**: divide a rede em **Sistemas Autônomos (AS)**.",
    ]),
    BOX("def", "Roteamento na Internet: interno × externo", [
        "- **IGP** (dentro de um AS): **RIP**, **OSPF**.   - **EGP** (entre ASs): **BGP**.",
        "- **AS (Autonomous System)**: conjunto de redes sob uma mesma administração técnica. PTTs/IXPs interligam ASs.",
    ]),
    BOX("exemplo", "Slide: rota de menor atraso de A para E", [
        "Atrasos (s): AB=4, AC=6, AD=3, BE=8, CE=2, CF=5, DC=2, DF=1.",
        T(["Rota", "Soma", "Atraso"],
          [["A→B→E", "4 + 8", "12"], ["A→C→E", "6 + 2", "8"], ["A→D→F→C→E", "3 + 1 + 5 + 2", "11"], ["A→D→C→E", "3 + 2 + 2", "**7**"]],
          align=["l", "c", "c"], size=9.5),
        "Pela conta, o menor atraso é **ADCE = 7 s**. A apostila afirma “ACE (8 s)”: parece ser uma **inconsistência do slide** — se cair na prova, some você mesmo e use o menor valor.",
    ]),
    BOX("resumo", None, [
        "- Rede = roteamento fim a fim. Datagrama (IP) × circuito virtual (ATM).",
        "- RIP = vetor de distância; OSPF = estado de enlace; BGP = entre ASs.",
        "- Adaptativo reage a mudanças; estático não.",
    ]),
    EX([
        Q("Qual protocolo de roteamento é de estado de enlace e é usado dentro de um AS?",
          opts=["RIP", "OSPF", "BGP", "ARP"],
          a="**b).** RIP é vetor de distância; BGP é entre ASs; ARP não é roteamento."),
        Q("Em uma rede de datagramas, o que acontece quando um roteador falha?",
          "Só os pacotes que estavam nele se perdem; os demais pacotes podem ser **roteados por outro caminho** (cada pacote é independente). No circuito virtual, **todos os VCs** que passam pelo roteador se perdem."),
        Q("V ou F: (a) o endereço IP é hierárquico; (b) o BGP é usado dentro de um mesmo AS; (c) algoritmos adaptativos reagem a mudanças de topologia; (d) cada hop corresponde à passagem por um roteador.",
          "(a) **V**. (b) **F** — BGP é entre ASs. (c) **V**. (d) **V**."),
    ]),
]

# =====================================================================
# 6. TCP/IP
# =====================================================================
C += [
    H1("TCP/IP: IP, sub-redes, ARP, ICMP, TCP e UDP",
       "Apostila de Redes — TCP/IP · O coração da prova: endereçamento IP e os protocolos de rede/transporte."),
    H2("Características do TCP/IP"),
    B(["Independe de fabricante; permite que dois hosts quaisquer da Internet se comuniquem; define padrões para aplicações (FTP, e-mail, login remoto).",
       "Cada equipamento precisa de dois “endereços”: o **IP** (identifica o host globalmente) e a **porta** (identifica o serviço/processo no host).",
       "História: ARPANET (anos 70), TCP/IP adotado em 1983, incluído no Unix de Berkeley (**sockets** = API para aplicações), WWW em 1990."]),
    H2("Endereçamento IPv4"),
    P("Endereço de **32 bits**, escrito em 4 números decimais (0–255) separados por ponto (ex.: 200.250.5.10). Parte de **rede** + parte de **host**."),
    T(["Classe", "1º octeto", "Faixa", "Bits de rede/host", "Observação"],
      [["**A**", "1–126", "1.0.0.0 – 126.255.255.255", "8 / 24", "Até 16.777.214 hosts por rede"],
       ["**B**", "128–191", "128.0.0.0 – 191.255.255.255", "16 / 16", "Até 65.534 hosts"],
       ["**C**", "192–223", "192.0.0.0 – 223.255.255.255", "24 / 8", "Até 254 hosts"],
       ["**D**", "224–239", "224.0.0.0 – 239.255.255.255", "—", "**Multicast**"],
       ["**E**", "240–255", "240.0.0.0 em diante (a apostila lista 240–247)", "—", "Reservado"]],
      widths=[1.8, 2.2, 5.5, 3, 4.5], align=["c", "c", "l", "c", "l"], size=9.5),
    BOX("lembrete", "Endereços especiais", [
        "- **127.x.x.x** = **loopback** (a própria máquina; não sai na rede).",
        "- **Host todo em 0** = endereço da **rede**; **host todo em 1** = **broadcast** da rede; **255.255.255.255** = broadcast limitado.",
        "- Por isso, em cada rede/sub-rede perdem-se **2 endereços**: hosts úteis = 2^{n} − 2 (n = bits de host).",
        "- **Privados (RFC 1918)**: **10.0.0.0/8** · **172.16.0.0/12** (172.16–172.31) · **192.168.0.0/16**. Não roteáveis na Internet.",
    ]),
    H2("Máscara de sub-rede e CIDR"),
    BOX("def", "Máscara", [
        "A máscara marca com **1** os bits de rede e com **0** os de host. **Rede = IP AND máscara.** Sub-redes tomam **bits emprestados** da parte de host (reduz o domínio de broadcast e economiza endereços).",
        "Valores do último octeto: 128 = /25 · 192 = /26 · 224 = /27 · 240 = /28 · 248 = /29 · 252 = /30.",
        "**CIDR / supernetting** (RFC 1519/4632): ignora classes; notação **barra**: 192.168.10.0**/26** = máscara 255.255.255.192. Permite blocos de tamanho 2^{n} e **agregar** várias redes (reduz tabelas de roteamento).",
    ]),
    BOX("exemplo", "Como calcular rapidamente (192.168.10.0/26)", [
        "- /26 ⇒ 26 bits de rede, **6 bits de host** ⇒ 2⁶ = **64 endereços** por sub-rede ⇒ **62 hosts úteis**.",
        "- Máscara: 255.255.255.**192** (256 − 64). Sub-redes de 64 em 64: **.0 · .64 · .128 · .192**.",
        "- Sub-rede 192.168.10.0: **rede** = .0, hosts .1 a .62, **broadcast** = **.63**.",
        "- Sub-rede 192.168.10.64: rede = .64, hosts .65–.126, broadcast = .127.",
        "- O host 192.168.10.100 pertence à sub-rede **.64** (64 ≤ 100 < 128).",
    ]),
    BOX("erro", None, [
        "- Esquecer de **subtrair 2** (rede e broadcast) ao contar hosts.",
        "- Dizer que /24 tem 256 hosts: tem 256 **endereços** e **254 hosts**.",
        "- Confundir endereços privados: **172.16.0.0/12** vai até **172.31.255.255** (não até 172.255).",
    ]),
    H2("NAT e quem distribui endereços"),
    B(["**NAT (Network Address Translation)**: o roteador/firewall traduz **endereços privados** da rede interna em endereços públicos para acessar a Internet (*IP masquerading*). Vantagens: economiza IPs públicos, mais segurança/controle. Problemas: pode atrapalhar UDP/IPsec e traz custo de desempenho.",
       "**IANA** distribui blocos aos **RIRs** (5 no mundo; **LACNIC** = América Latina; **ARIN** = EUA/Canadá; **RIPE** = Europa; **APNIC** = Ásia-Pacífico; **AFRINIC** = África). No Brasil: **Registro.br / NIC.br** (Comitê Gestor da Internet)."]),
    H2("Datagrama IP"),
    B(["IP é **não orientado a conexão** (“o carteiro”), de **melhor esforço** (não confiável), **sem controle de fluxo** e com **checksum só do cabeçalho**. Cada datagrama é independente.",
       "Oferece **fragmentação e remontagem** (quando o MTU da rede é menor que o datagrama).",
       "Campos principais do cabeçalho: **Versão**, **IHL** (tamanho do cabeçalho), **Tipo de serviço**, **Comprimento total**, **Identificação / flags / Fragment offset** (fragmentação), **TTL** (tempo de vida; diminui a cada hop e **descarta** o datagrama ao chegar a 0 — evita loops), **Protocolo** (6 = TCP, 17 = UDP, 1 = ICMP), **Checksum do cabeçalho**, **Endereço de origem**, **Endereço de destino**, Opções."]),
    H2("ARP, RARP e ICMP"),
    T(["Protocolo", "Para que serve", "Como funciona"],
      [["**ARP** (RFC 826)", "Descobrir o **MAC** a partir do **IP**", "Host envia **broadcast** “quem tem o IP X?”; só o dono responde (unicast) com seu MAC. Para outra rede, usa-se o MAC do **gateway**"],
       ["**RARP** (RFC 903)", "Descobrir o **IP** a partir do MAC", "Pedido a um servidor (hoje substituído por BOOTP/DHCP)"],
       ["**ICMP**", "Controle e **mensagens de erro/diagnóstico** da camada IP", "Exemplos: **ping** (echo request/reply); tracert/traceroute usam o TTL"]],
      widths=[3.2, 5.3, 8.5], size=9.5),
    H2("Transporte: TCP × UDP e portas"),
    T(["", "**TCP**", "**UDP**"],
      [["Conexão", "**Orientado a conexão** (handshake SYN/ACK)", "**Sem conexão**"],
       ["Confiabilidade", "**Confiável**: ACK, retransmissão, **sequenciação**, controle de erro", "Não confiável: sem correção de erro e **sem garantir ordem**"],
       ["Controle de fluxo", "**Janela deslizante** (campo janela de 16 bits)", "Não há"],
       ["Cabeçalho", "**20 bytes** no mínimo (5 palavras de 32 bits); com opções vai até 60 bytes no padrão (a apostila cita o máximo de 10 palavras = 40 bytes)", "**8 bytes**: porta origem, porta destino, tamanho, checksum"],
       ["Usos", "Web, e-mail, transferência de arquivos", "DNS, SNMP, voz/vídeo em tempo real"]],
      widths=[3.2, 7, 6.8], size=9.5),
    P("**Cabeçalho TCP:** porta de origem e destino (16 bits cada), **número de sequência**, **número de reconhecimento** (próximo byte esperado), tamanho do cabeçalho, **flags** (**URG, ACK, PSH, RST, SYN, FIN**), **janela**, checksum, ponteiro de urgência, opções. "
      "A conexão é aberta com **SYN → SYN+ACK → ACK** e encerrada com FIN."),
    T(["Serviço", "Porta", "Transporte"],
      [["FTP (dados/controle)", "20 / **21**", "TCP"], ["SSH", "22", "TCP"], ["Telnet", "**23**", "TCP"], ["**SMTP** (envio de e-mail)", "**25**", "TCP"],
       ["**DNS**", "**53**", "UDP (e TCP)"], ["**HTTP**", "**80**", "TCP"], ["POP3 / IMAP", "110 / 143", "TCP"], ["**HTTPS**", "**443**", "TCP"], ["**SNMP**", "**161 / 162** (traps)", "UDP"]],
      widths=[8, 4.5, 4.5], align=["l", "c", "c"], size=9.5),
    BOX("extra", "Fora das apostilas, mas cai", [
        "Portas 20/22/25/53/80/110/143/161/443 são padrão IANA (o slide só lista algumas explicitamente: FTP 21, Telnet 23, SMTP 25, SNMP 161/162). "
        "DNS traduz **nomes em endereços IP**; DHCP entrega IP/máscara/gateway automaticamente.",
    ]),
    BOX("resumo", None, [
        "- IP: 32 bits, classes A/B/C/D/E, 127 = loopback, privados 10/8, 172.16/12, 192.168/16; hosts úteis = 2^{n} − 2.",
        "- ARP: IP → MAC (broadcast); ICMP: erros/ping; TTL evita loops.",
        "- TCP: confiável, conexão, janela; UDP: leve, sem garantias. Porta identifica o serviço.",
    ]),
    EX([
        Q("Quantos hosts úteis tem a sub-rede 192.168.1.0/27? Qual a máscara e o endereço de broadcast?",
          ["/27 ⇒ 5 bits de host ⇒ 2⁵ = 32 endereços ⇒ **30 hosts** úteis.",
           "Máscara **255.255.255.224**; broadcast = 192.168.1.**31**."]),
        Q("Dado o IP 172.16.50.10 com máscara 255.255.255.0, qual é o endereço da rede? Esse IP é público ou privado?",
          "Rede = 172.16.50.0 (IP AND máscara). **Privado** (faixa 172.16.0.0–172.31.255.255)."),
        Q("Qual afirmação é verdadeira?",
          opts=["O UDP garante ordem e retransmissão.", "O TCP é orientado a conexão e usa janela deslizante para controle de fluxo.",
                "O IP é confiável e orientado a conexão.", "O ARP descobre o IP a partir do nome do host."],
          a="**b).** a) falsa — UDP não garante; c) IP é não confiável e sem conexão; d) ARP descobre **MAC a partir do IP** (DNS é que resolve nomes)."),
        Q("Para que serve o campo TTL do cabeçalho IP?",
          "Limita a vida do datagrama: é decrementado em cada roteador e o pacote é **descartado quando chega a 0**, evitando que circule indefinidamente (loops de roteamento)."),
        Q("Associe: (1) HTTP; (2) DNS; (3) SMTP; (4) SNMP — a) 25; b) 161; c) 80; d) 53.",
          "(1)-c, (2)-d, (3)-a, (4)-b."),
    ]),
]

# =====================================================================
# 7. GERÊNCIA
# =====================================================================
C += [
    H1("Gerência de Redes: FCAPS, SLA, SNMP e fluxos",
       "Apostila de Gerência de Redes · Por que e como administrar uma rede para ela funcionar 24 horas por dia."),
    H2("Por que gerenciar"),
    P("Gerenciamento de rede = **disponibilizar, integrar e coordenar elementos de hardware, software e humanos** para monitorar, testar, configurar, analisar e controlar a rede, atendendo requisitos de **qualidade, tempo real e custo**. Motivos: "
      "**(1)** controlar o uso dos recursos, **(2)** melhorar o uso (otimizar), **(3)** reduzir custos e **(4)** manter disponível um serviço essencial. Deve ser **proativa**, não só reativa."),
    H2("FCAPS: as cinco áreas funcionais"),
    T(["Letra", "Área", "O que faz", "Exemplos"],
      [["**F**", "**Falhas** (Fault)", "**Localizar, isolar e corrigir** problemas", "Logs, alarmes, checklist, plano de contingência"],
       ["**C**", "**Configuração**", "Inicializar, alterar e **armazenar a configuração** dos equipamentos; inventário", "Documentação, padronização, backup de configs"],
       ["**A**", "**Contabilização** (Accounting)", "Medir o **uso** por usuário/serviço; cotas e cobrança", "Logs de proxy/e-mail/servidor de contas (LDAP)"],
       ["**P**", "**Performance** (Desempenho)", "Monitorar e ajustar; evitar congestionamento; planejar crescimento; **baseline**", "Medições de vazão, atraso, gargalos"],
       ["**S**", "**Segurança**", "Proteger equipamentos e dados; controle de acesso", "Firewall, análise de logs, **backup**"]],
      widths=[1.3, 3.7, 6.5, 5.5], align=["c", "l", "l", "l"], size=9.5),
    BOX("def", "Baseline", [
        "Perfil do comportamento **normal** da rede (limiares mínimos/máximos de uso). Serve de referência para detectar **anomalias** e dimensionar a rede.",
    ]),
    BOX("insight", "Documentação reduz o tempo de reparo", [
        "A falta de documentação faz perder tempo em incidentes e a **visão do todo** à medida que a rede cresce. Prática moderna: **infraestrutura como código** (config versionada, detecção de drift; ferramentas como Ansible/NetBox). Reduz o **MTTR** (tempo médio de reparo).",
    ]),
    H2("SLA e disponibilidade"),
    P("**SLA (Service Level Agreement)**: acordo de nível de serviço que define os parâmetros mínimos de qualidade (ex.: % do tempo disponível). Um ano tem **525.600 minutos**."),
    T(["Disponibilidade", "Tempo fora do ar / ano", "Em minutos"],
      [["90 %", "≈ 36,5 dias", "52.560"], ["95 %", "≈ 18,25 dias", "26.280"], ["99 %", "≈ 3,65 dias", "5.256"],
       ["**99,9 %** (três noves)", "≈ 8,76 h", "525,6"], ["**99,99 %**", "≈ 52,6 min", "52,56"], ["**99,999 %** (cinco noves)", "≈ 5,26 min", "5,26"]],
      widths=[5, 6, 4], align=["l", "c", "c"], size=9.5),
    BOX("lembrete", "Como calcular", [
        "Tempo fora = (1 − disponibilidade) × 525.600 min. Ex.: 99,9 % ⇒ 0,001 × 525.600 = **525,6 min** ≈ 8,76 h.",
    ]),
    H2("SNMP — Simple Network Management Protocol"),
    BOX("def", "Modelo gerente–agente", [
        "- **Gerente (NMS)**: estação com software de gerenciamento; **consulta** (polling) os agentes.",
        "- **Agente**: software no equipamento (switch, roteador, servidor…) que mantém a **MIB** e atende às consultas. Deve ser **simples**.",
        "- **MIB (Management Information Base)**: base de objetos gerenciados, organizada em **árvore** (OIDs). **SMI** define como descrever os objetos. **MIB-II** = grupos como *system*, *interfaces*, *ip*, *tcp*, *udp*…",
        "- **Protocolo SNMP**: usa **UDP**, portas **161** (agente) e **162** (traps). Operações: **get-request**, **get-next-request**, **set-request**, get-response e **trap** (alerta espontâneo do agente).",
        "- Padronizado em 1988 pelo IAB/IETF (RFC 1157; SMI = 1155; MIB-I = 1156; MIB-II = 1213).",
    ]),
    BOX("insight", "Por que o SNMP deu certo e qual o custo", [
        "É **simples** e está disponível em quase todo equipamento. Custo: o **polling** do gerente gera **tráfego** na rede — é preciso avaliar o impacto. "
        "Exemplos de objetos do grupo *interfaces*: ifSpeed, ifOperStatus, ifInOctets, ifInErrors, ifOutDiscards.",
    ]),
    H2("Gerência por fluxos: NetFlow e IPFIX"),
    B(["**Fluxo** = conjunto de pacotes IP que passam por um ponto de observação em um intervalo de tempo e compartilham propriedades comuns (**chaves do fluxo**, classicamente: IP origem, IP destino, porta origem, porta destino e protocolo).",
       "**Exportador** (probe: switch/roteador que gera e exporta fluxos) → **coletor** (collector, armazena/analisa). O fluxo é **enviado** ao coletor (push); no SNMP o gerente faz **pull** (polling).",
       "**NetFlow** (Cisco) deu origem ao padrão **IPFIX** (IETF, baseado no NetFlow v9). Também: sFlow, J-Flow.",
       "Responde “**quem** está usando a rede, **com qual aplicação** e **quanto**” (*top talkers*), identifica baseline e anomalias — **complementa** o SNMP (que só tem contadores)."]),
    H2("NOC"),
    P("**Network Operations Center**: centro de operações responsável por **gerenciar e controlar a rede**; produz baseline, monitora as cinco áreas FCAPS, detecta intrusão e resolve problemas de forma proativa."),
    BOX("resumo", None, [
        "- FCAPS = Falhas, Configuração, Contabilização, Performance, Segurança.",
        "- SLA: tempo fora = (1 − disp.) × 525.600 min. 99,999 % ≈ 5 min/ano.",
        "- SNMP: gerente–agente–MIB, UDP 161/162, get/set/trap. IPFIX/NetFlow: fluxos exportados a um coletor.",
    ]),
    EX([
        Q("Associe a área FCAPS: (1) medir o uso por usuário para cobrança; (2) localizar e isolar uma falha; (3) manter o inventário e as configurações dos equipamentos; (4) construir o baseline e prevenir congestionamentos.",
          "(1) Contabilização; (2) Falhas; (3) Configuração; (4) Performance."),
        Q("Um serviço contratado exige disponibilidade de 99,99 %. Quanto tempo por ano pode ficar fora do ar?",
          "0,0001 × 525.600 = **52,56 min** por ano."),
        Q("Qual a diferença essencial entre coletar dados via SNMP e via IPFIX/NetFlow?",
          "No SNMP o gerente faz **polling (pull)** de contadores da MIB; no IPFIX o equipamento **exporta fluxos** (push) a um coletor, com detalhe de IPs, portas e protocolo (quem usa o quê)."),
        Q("V ou F: (a) o SNMP usa TCP; (b) um trap é enviado pelo agente sem ser solicitado; (c) a MIB é organizada em árvore de objetos; (d) o NOC é o centro de operações da rede.",
          "(a) **F** — UDP (161/162). (b) **V**. (c) **V**. (d) **V**."),
    ]),
]

# =====================================================================
# 8. SEGURANÇA
# =====================================================================
C += [
    H1("Segurança em TIC: princípios, ataques e defesas",
       "Apostila de Segurança · O que proteger, de quem e como."),
    H2("Princípios fundamentais"),
    T(["Princípio", "Objetivo"],
      [["**Confidencialidade**", "Só pessoas/entidades **autorizadas** acessam a informação"],
       ["**Integridade**", "A informação mantém suas **características originais** (não é alterada indevidamente)"],
       ["**Disponibilidade**", "A informação está **sempre disponível** aos autorizados"],
       ["**Autenticação**", "**Identificar** quem usa o recurso"],
       ["**Controle de acesso**", "Cada um acessa **só o que seu perfil permite**"],
       ["**Não repúdio**", "Quem realizou uma ação/transação **não pode negá-la**"]],
      widths=[4.5, 12.5], size=10),
    BOX("lembrete", "CIA (a tríade)", ["**C**onfidencialidade · **I**ntegridade · **D**isponibilidade (*Availability*). As outras três (autenticação, controle de acesso, não repúdio) complementam."]),
    BOX("def", "Ameaça × vulnerabilidade × risco", [
        "- **Vulnerabilidade**: falha de projeto, instalação, configuração, hardware ou software.",
        "- **Ameaça**: algo (malware, atacante, desastre) que **explora** uma vulnerabilidade.",
        "- Ambas podem ser identificadas, prevenidas e mitigadas ⇒ **gerenciamento de risco**. Ativos a proteger: dados/informação, pessoas, processos, tecnologia (hardware e software).",
        "- Ferramentas organizacionais: **política** de segurança (princípios), **normas** (controles, regras e procedimentos), **plano de contingência** (backup, spare/clone, contratos), treinamento e **auditoria**.",
    ]),
    H2("Tipos de ataque"),
    T(["Ataque", "Em uma frase"],
      [["**Passivo**", "Escuta/monitoramento do tráfego (ameaça a **confidencialidade**)"],
       ["**Ativo**", "Disfarce (**masquerade**), captura e reenvio, **alteração** de mensagens, **negação de serviço**"],
       ["**Força bruta**", "Testar todas as combinações possíveis (de chave/senha). Senhas fracas (datas, nomes) caem por tentativas “previsíveis”"],
       ["**Criptoanálise**", "Tentar decifrar usando conhecimento do algoritmo, reduzindo o trabalho da força bruta"],
       ["**Man-in-the-middle (MITM)**", "Atacante se infiltra **entre** duas partes, captura/retransmite sem que percebam"],
       ["**Replay**", "Captura de dados legítimos para **retransmissão posterior**. Contramedidas: session token, timestamp, **nonce**, MAC"],
       ["**DoS / DDoS**", "Sobrecarrega um serviço com solicitações válidas para impedir o atendimento normal; **DDoS** usa muitos computadores (**zumbis/botnet**). Atinge a **disponibilidade**"],
       ["**Scanning**", "Varredura de endereços/portas para achar serviços vulneráveis"],
       ["**DNS spoofing**", "Falsifica respostas DNS e direciona a vítima a sites falsos"],
       ["**Phishing**", "Obtém dados pessoais por **engenharia social** (e-mails/páginas falsas se passando por entidade confiável)"],
       ["**Engenharia social**", "Explora a **pessoa** (telefonema, boatos); **firewall não protege** contra isso — treinamento é a defesa"]],
      widths=[4, 13], size=9.5),
    H3("Malware (software malicioso)"),
    T(["Tipo", "Característica"],
      [["**Vírus**", "Precisa de **programa hospedeiro**; infecta e tenta copiar-se (execução de arquivo infectado)"],
       ["**Worm**", "**Independente**; **propaga-se sozinho pela rede** enviando cópias de si mesmo"],
       ["**Trojan (cavalo de Troia)**", "Parece útil/normal mas executa função maliciosa; permite dominar o sistema"],
       ["**Spyware**", "Coleta informações do usuário sem autorização e as envia a terceiros"],
       ["**Backdoor**", "Porta/ponto de entrada deixado propositalmente no software"],
       ["**Bomba lógica**", "Código embutido que dispara em determinada condição (sabotagem)"],
       ["**Bot / Botnet**", "Bot dá controle remoto da máquina (“zumbi”); botnets = centenas a milhares de zumbis, usadas em DDoS, spam, keylogging"],
       ["**Ransomware**", "Sequestra/criptografa dados e exige resgate. Defesa principal: **backup testado**"],
       ["**Spam**", "Mensagens não solicitadas (boatos, golpes, phishing)"]],
      widths=[4.2, 12.8], size=9.5),
    BOX("erro", None, [
        "- Vírus × worm: **vírus precisa de hospedeiro**; **worm é autônomo** e se espalha pela rede.",
        "- DoS não “invade” nem rouba dados: **derruba a disponibilidade**.",
        "- Ataque passivo **não altera** nada (só observa) e é difícil de detectar; ativo altera ou interrompe.",
    ]),
    H2("Defesas"),
    T(["Defesa", "O que é / faz"],
      [["**Firewall**", "“Porta” por onde **todo o tráfego** passa; aplica regras **inbound/outbound**: controle de serviços, de direção, de usuário e de comportamento. Ex.: **iptables** (Linux). **Não** protege contra ataques que o contornam (ex.: engenharia social) nem totalmente contra ameaças internas"],
       ["**IDS** (Intrusion Detection System)", "“2ª linha de defesa”: **o intruso já está dentro**. Por **assinaturas** (*knowledge-based*: precisa de atualização constante) ou por **comportamento/anomalia** (*behavior-based*: exige **baseline**). Problemas: **falsos positivos** e **falsos negativos**"],
       ["**IPS / UTM**", "IPS tenta **bloquear** a intrusão; **UTM** integra firewall + IDS/IPS + antivírus + antispam + filtro de URL em uma só solução"],
       ["**Honeypot**", "Computador **isca**, propositalmente vulnerável, para registrar ataques e **aprender** com eles"],
       ["**Antivírus / antispam**", "Detectam e removem malware e spam"],
       ["**Criptografia e protocolos seguros**", "Protegem confidencialidade e integridade (ex.: **HTTPS**, VPN/IPsec)"]],
      widths=[4.5, 12.5], size=9.5),
    BOX("lembrete", "Boas práticas do usuário (as da apostila)", [
        "Ser **cético**; fazer **backup** regular (**em local separado** e **mais de uma cópia**); usar **software legal** e **atualizado**; não responder e-mails suspeitos; usar antivírus, antispyware e firewall; **trocar senhas** (fortes, únicas, sem dados pessoais); usar só computadores confiáveis. "
        "As **pessoas** continuam sendo o elo mais fraco.",
    ]),
    BOX("resumo", None, [
        "- CIA + autenticação, controle de acesso, não repúdio. Ameaça explora vulnerabilidade.",
        "- Ataques: passivo × ativo; DoS/DDoS (disponibilidade), MITM, replay, phishing, spoofing, scanning.",
        "- Defesas: firewall (perímetro), IDS (já dentro), UTM, honeypot, backup, treinamento.",
    ]),
    EX([
        Q("Um ataque que inunda um servidor web com solicitações válidas até torná-lo indisponível viola principalmente:",
          opts=["Confidencialidade", "Integridade", "Disponibilidade", "Não repúdio"],
          a="**c).** É um ataque de negação de serviço (DoS/DDoS) — afeta a disponibilidade."),
        Q("Qual a diferença entre vírus e worm?",
          "O **vírus** precisa de um programa hospedeiro e é ativado ao executar o arquivo infectado; o **worm** é independente e **se propaga automaticamente pela rede**."),
        Q("V ou F: (a) um firewall protege contra engenharia social; (b) IDS baseado em assinatura precisa de atualização constante; (c) um honeypot é um computador-isca; (d) o ataque passivo altera as mensagens.",
          "(a) **F** — pessoas são a defesa (treinamento). (b) **V**. (c) **V**. (d) **F** — passivo só observa."),
        Q("Que contramedidas combatem o ataque de replay?",
          "Tokens de sessão, **timestamps**, **nonce** (número usado uma vez) e códigos de autenticação de mensagem (MAC)."),
    ]),
]

# =====================================================================
# 9. COLA
# =====================================================================
C += [
    H1("Cola de última hora", "Uma página para reler antes da prova."),
    T(["Tema", "Lembrar"],
      [["Camadas OSI", "Física · Enlace · Rede · Transporte · Sessão · Apresentação · Aplicação"],
       ["Equipamentos", "Hub = física · Switch = enlace (MAC) · Roteador = rede (IP)"],
       ["Domínios", "Hub: 1 colisão · Switch: 1 colisão **por porta** · Roteador/VLAN: separa **broadcast**"],
       ["Nyquist / Shannon", "C = 2W·log₂L  /  C = W·log₂(1+S/N)"],
       ["Ethernet", "CSMA/CD · slot 51,2 µs · backoff 0…2^i−1 · 16 tentativas · quadro 64–1518 B · dados 46–1500 · MAC 6 B · CRC-32"],
       ["VLAN", "IEEE 802.1Q · VID 1–4094 · access × trunk · STP evita laços"],
       ["IP", "32 bits · A 1–126 · B 128–191 · C 192–223 · D multicast · 127 loopback · hosts = 2^n − 2"],
       ["Privados", "10/8 · 172.16/12 · 192.168/16"],
       ["Máscaras", "/24 255.255.255.0 · /25 .128 · /26 .192 · /27 .224 · /28 .240 · /29 .248 · /30 .252"],
       ["ARP / ICMP", "ARP: IP→MAC (broadcast) · ICMP: erros/ping · TTL evita loop"],
       ["TCP × UDP", "TCP conexão/confiável/janela (cabeçalho ≥ 20 B) · UDP sem conexão (8 B)"],
       ["Portas", "FTP 21 · SSH 22 · Telnet 23 · SMTP 25 · DNS 53 · HTTP 80 · HTTPS 443 · SNMP 161/162"],
       ["Roteamento", "RIP vetor de distância · OSPF estado de enlace · BGP entre ASs"],
       ["FCAPS", "Falhas · Configuração · Contabilização · Performance · Segurança"],
       ["SLA", "Tempo fora = (1−disp.) × 525.600 min  (99,999 % ≈ 5 min/ano)"],
       ["SNMP", "Gerente–agente–MIB · UDP 161/162 · get/set/trap · IPFIX = fluxos (push)"],
       ["Segurança", "CIA · DoS = disponibilidade · vírus (hospedeiro) × worm (rede) · firewall × IDS × honeypot"]],
      widths=[3.6, 13.4], size=9.5),
    H2("Mini-simulado final"),
    EX([
        Q("Uma empresa recebeu o bloco 200.10.20.0/24 e precisa de 4 sub-redes iguais. Qual máscara usar e quantos hosts úteis por sub-rede?",
          ["4 sub-redes ⇒ 2 bits emprestados ⇒ **/26** (255.255.255.192).",
           "64 endereços por sub-rede ⇒ **62 hosts** úteis. Sub-redes: .0, .64, .128, .192."]),
        Q("Descreva o caminho de um pacote HTTP de um PC até um servidor em outra rede, citando uma função de cada camada.",
          "Aplicação (HTTP gera a requisição) → Transporte (TCP, porta 80, segmenta e garante entrega) → Rede (IP escolhe a rota; o roteador consulta a tabela) → Enlace (Ethernet: ARP descobre o MAC do gateway; quadro com CRC) → Física (bits no meio). No destino, desencapsula em ordem inversa."),
        Q("Marque V ou F: (a) 192.168.5.7 é um IP público; (b) o switch separa domínios de broadcast; (c) o SNMP usa a porta UDP 161; (d) um IDS baseado em comportamento precisa de baseline.",
          "(a) **F** — é privado (192.168/16). (b) **F** — separa colisão, não broadcast. (c) **V**. (d) **V**."),
        Q("O que muda quando passamos de hub para switch em uma LAN Ethernet?",
          "Cada porta passa a ser um **domínio de colisão** próprio e, com full-duplex, as colisões desaparecem (o CSMA/CD deixa de ser necessário); a banda deixa de ser compartilhada e o switch encaminha quadros pelo MAC aprendido."),
    ], title="Exercícios — Mini-simulado"),
]
