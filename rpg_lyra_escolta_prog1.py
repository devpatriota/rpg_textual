import os
import random

# LORE DO RPG: A história base foi retirada do Dungeongeek21.com e aprimorada usando Inteligência Artificial para criação de novos capítulos.
# Possui escalabilidade para novos capítulos, mas ainda não salva dados da história. Pretendo implementar futuramente pra salvar localmente.

# DADOS GLOBAIS
 
jogador = {}
lyra = {}
estado = {}

CLASSES = [
    {"nome": "Guerreiro", "hp": 42, "atk": 7, "defe": 4, "especial": "golpe",
     "mods": {"forca": 3, "astucia": 0, "carisma": 1},
     "desc": "Resistente e brutal. Habilidade: Golpe Poderoso (dano dobrado)."},
    {"nome": "Ladino", "hp": 32, "atk": 6, "defe": 2, "especial": "furtivo",
     "mods": {"forca": 1, "astucia": 4, "carisma": 2},
     "desc": "Rápido e esperto. Habilidade: Ataque Furtivo (ignora armadura)."},
    {"nome": "Clérigo", "hp": 36, "atk": 5, "defe": 3, "especial": "luz",
     "mods": {"forca": 1, "astucia": 1, "carisma": 3},
     "desc": "Fé e lábia. Habilidade: Luz Sagrada (cura você e Lyra)."},
    {"nome": "Mago", "hp": 27, "atk": 4, "defe": 1, "especial": "fogo",
     "mods": {"forca": 0, "astucia": 3, "carisma": 1},
     "desc": "Frágil, mas devastador. Habilidade: Bola de Fogo (dano mágico alto)."},
]

NOMES_ESPECIAIS = {
    "golpe": "Golpe Poderoso",
    "furtivo": "Ataque Furtivo",
    "luz": "Luz Sagrada",
    "fogo": "Bola de Fogo",
}


def iniciar_estado():
    jogador.clear()
    lyra.clear()
    estado.clear()
    lyra.update({"hp": 20, "hp_max": 20, "confianca": 5})
    estado.update({"prometeu_irmao": False, "mentiu": False})



# UTILIDADES

def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\n  [ENTER para continuar]")


def d(lados):
    return random.randint(1, lados)


def titulo(texto):
    limpar()
    print("=" * 60)
    print(texto.center(60))
    print("=" * 60)
    print()


def barra(atual, maximo, tam=12):
    atual = max(0, atual)
    cheio = int(round(tam * atual / maximo)) if maximo else 0
    return "[" + "█" * cheio + "░" * (tam - cheio) + "]"


def escolher(opcoes):
    for i, texto in enumerate(opcoes, 1):
        print(f"  {i}) {texto}")
    while True:
        r = input("\n  > ").strip()
        if r.isdigit() and 1 <= int(r) <= len(opcoes):
            return int(r)
        print("  Opção inválida.")


def teste(atributo, dc, descricao=""):
    """Teste de atributo: d20 + modificador contra uma dificuldade."""
    rolagem = d(20)
    mod = jogador["mods"][atributo]
    total = rolagem + mod
    sucesso = total >= dc
    print(f"\n  Teste de {atributo.upper()} {descricao}(DC {dc}): "
          f"d20={rolagem} + {mod} = {total} -> "
          f"{'SUCESSO!' if sucesso else 'FALHA.'}")
    return sucesso


def mudar_confianca(valor, motivo=""):
    antes = lyra["confianca"]
    lyra["confianca"] = max(0, min(10, antes + valor))
    sinal = "+" if valor >= 0 else ""
    if lyra["confianca"] != antes:
        print(f"\n  ♥ Confiança de Lyra: {sinal}{valor} {motivo}"
              f"(agora {lyra['confianca']}/10)")


def mostrar_status():
    print("-" * 60)
    print(f"  {jogador['nome']} ({jogador['classe']})  "
          f"HP {barra(jogador['hp'], jogador['hp_max'])} "
          f"{jogador['hp']}/{jogador['hp_max']}")
    print(f"  Lyra  HP {barra(lyra['hp'], lyra['hp_max'])} "
          f"{lyra['hp']}/{lyra['hp_max']}   Confiança: {lyra['confianca']}/10")
    print(f"  Ouro: {jogador['ouro']} | Poções: {jogador['pocoes']} | "
          f"Rações: {jogador['racoes']} | Cordas: {jogador['cordas']}")
    print("-" * 60)


def game_over(motivo):
    print("\n" + "▓" * 60)
    print("  FIM DE JOGO")
    print("▓" * 60)
    print(f"\n  {motivo}")
    return False


# COMBATE

def criar_inimigo(nome, hp, atk, defe):
    return {"nome": nome, "hp": hp, "hp_max": hp, "atk": atk, "defe": defe}


def causar_dano(alvo, dano):
    alvo["hp"] -= dano
    print(f"  → {alvo['nome']} sofre {dano} de dano.")
    if alvo["hp"] <= 0:
        print(f"  ✖ {alvo['nome']} cai derrotado!")


def escolher_alvo(vivos):
    if len(vivos) == 1:
        return vivos[0]
    print("\n  Escolha o alvo:")
    nomes = [f"{i['nome']} ({i['hp']}/{i['hp_max']})" for i in vivos]
    return vivos[escolher(nomes) - 1]


def usar_especial(vivos):
    tipo = jogador["especial"]
    if tipo == "golpe":
        alvo = escolher_alvo(vivos)
        dano = max(1, jogador["atk"] * 2 + d(6) - alvo["defe"])
        print(f"\n  Você desfere um GOLPE PODEROSO em {alvo['nome']}!")
        causar_dano(alvo, dano)
    elif tipo == "furtivo":
        alvo = escolher_alvo(vivos)
        dano = jogador["atk"] + d(6) + 6
        print(f"\n  Você surge das sombras e acerta {alvo['nome']} num ponto vital!")
        causar_dano(alvo, dano)
    elif tipo == "fogo":
        alvo = escolher_alvo(vivos)
        dano = 10 + d(6)
        print(f"\n  Uma BOLA DE FOGO explode sobre {alvo['nome']}!")
        causar_dano(alvo, dano)
    elif tipo == "luz":
        jogador["hp"] = min(jogador["hp_max"], jogador["hp"] + 12)
        lyra["hp"] = min(lyra["hp_max"], lyra["hp"] + 6)
        print("\n  Uma LUZ SAGRADA envolve vocês: +12 HP para você, +6 HP para Lyra.")


def combate(inimigos, pode_fugir=True):
    """Retorna 'vitoria', 'fuga', 'derrota' ou 'lyra_morta'."""
    especial_usado = False
    rodada = 0
    print("\n  ⚔  COMBATE!  " + ", ".join(i["nome"] for i in inimigos))
    pausa()

    while True:
        rodada += 1
        vivos = [i for i in inimigos if i["hp"] > 0]
        if not vivos:
            return "vitoria"

        print("\n" + "=" * 60)
        print(f"  RODADA {rodada}")
        for i in vivos:
            print(f"  {i['nome']:<24} {barra(i['hp'], i['hp_max'])} "
                  f"{i['hp']}/{i['hp_max']}")
        mostrar_status()

        # Lyra ajuda se confiar o bastante em você
        if lyra["confianca"] >= 6:
            alvo = random.choice(vivos)
            print("\n  Lyra, confiando em você, arremessa uma pedra!")
            causar_dano(alvo, 3)
            vivos = [i for i in inimigos if i["hp"] > 0]
            if not vivos:
                return "vitoria"

        nome_esp = NOMES_ESPECIAIS[jogador["especial"]]
        opcoes = [
            "Atacar",
            f"Habilidade: {nome_esp}" + (" (já usada)" if especial_usado else ""),
            "Proteger Lyra (defesa +2, inimigos só miram em você)",
            f"Usar poção (+15 HP) [x{jogador['pocoes']}]",
            "Fugir" + ("" if pode_fugir else " (impossível!)"),
        ]
        escolha = escolher(opcoes)
        protegendo = False

        if escolha == 1:
            alvo = escolher_alvo(vivos)
            dano = max(1, jogador["atk"] + d(6) - alvo["defe"])
            print(f"\n  Você ataca {alvo['nome']}!")
            causar_dano(alvo, dano)
        elif escolha == 2:
            if especial_usado:
                print("\n  Você já usou sua habilidade neste combate.")
                continue
            especial_usado = True
            usar_especial(vivos)
        elif escolha == 3:
            protegendo = True
            print("\n  Você se coloca diante de Lyra, de guarda alta.")
        elif escolha == 4:
            if jogador["pocoes"] <= 0:
                print("\n  Você não tem poções!")
                continue
            jogador["pocoes"] -= 1
            jogador["hp"] = min(jogador["hp_max"], jogador["hp"] + 15)
            print("\n  Você bebe uma poção: +15 HP.")
        elif escolha == 5:
            if not pode_fugir:
                print("\n  Não há como fugir deste combate!")
                continue
            if d(20) + jogador["mods"]["astucia"] >= 12:
                print("\n  Você agarra Lyra e foge a toda velocidade!")
                mudar_confianca(-1, "(fuga) ")
                return "fuga"
            print("\n  A fuga falhou! Os inimigos bloqueiam o caminho.")

        if not [i for i in inimigos if i["hp"] > 0]:
            return "vitoria"

        # Turno dos inimigos
        print()
        for i in [x for x in inimigos if x["hp"] > 0]:
            if not protegendo and d(100) <= 30:
                dano = max(1, i["atk"] + d(4) - 1)
                lyra["hp"] -= dano
                print(f"  {i['nome']} ataca LYRA! (-{dano} HP)")
            else:
                bonus = 2 if protegendo else 0
                dano = max(1, i["atk"] + d(6) - jogador["defe"] - bonus)
                jogador["hp"] -= dano
                print(f"  {i['nome']} ataca você! (-{dano} HP)")

        if lyra["hp"] <= 0:
            return "lyra_morta"
        if jogador["hp"] <= 0:
            return "derrota"


def resolver_combate(resultado):
    """Converte o resultado do combate em True (segue) / False (fim)."""
    if resultado == "derrota":
        return game_over("Você tomba na estrada. Lyra é levada, e o Ducado vence.")
    if resultado == "lyra_morta":
        return game_over("Lyra não resiste aos ferimentos. A carga está perdida, "
                         "e com ela o seu pagamento.")
    if resultado == "vitoria":
        saque = d(10) + 5
        jogador["ouro"] += saque
        print(f"\n  Vitória! Você saqueia {saque} de ouro dos inimigos.")
    return True



# CAPÍTULOS

def intro():
    titulo("A ESCOLTA DE LYRA ASHGROVE")
    print("""  O Ducado de Valdoria apodrece sob o governo do Duque Aldric Voss.
  Nas Marchas Livres, ao norte, um Conselho de rebeldes tenta resistir.

  Lyra Ashgrove, arquivista pessoal do Duque, fugiu de Valdoria carregando
  o "Livro das Dívidas": a prova de que o Duque financia mercenários,
  assassinos e a própria guerra civil.

  Você foi contratado para levá-la, viva, até a Fortaleza Alvorada,
  nas Marchas Livres. Pagamento: 200 moedas de ouro na chegada.

  A jornada será longa. Muitos querem Lyra morta... ou de volta.
""")
    pausa()


def criar_personagem():
    titulo("CRIAÇÃO DE PERSONAGEM")
    nome = input("  Qual é o seu nome? ").strip() or "Viajante"
    print("\n  Escolha sua classe:\n")
    for i, c in enumerate(CLASSES, 1):
        print(f"  {i}) {c['nome']:<10} HP {c['hp']:<3} ATK {c['atk']} DEF {c['defe']}")
        print(f"     {c['desc']}")
    escolha = escolher([c["nome"] for c in CLASSES])
    c = CLASSES[escolha - 1]
    jogador.update({
        "nome": nome, "classe": c["nome"],
        "hp": c["hp"], "hp_max": c["hp"],
        "atk": c["atk"], "defe": c["defe"],
        "especial": c["especial"], "mods": dict(c["mods"]),
        "ouro": 60, "pocoes": 1, "racoes": 2, "cordas": 0,
    })
    print(f"\n  Bem-vindo, {nome} o {c['nome']}.")
    pausa()


def loja():
    while True:
        titulo("PREPARATIVOS - TAVERNA DO CORVO CANSADO")
        mostrar_status()
        print("  O taverneiro estende a mão: \"O que vai ser?\"\n")
        op = escolher([
            "Poção de cura (15 ouro)",
            "Ração de viagem (5 ouro)",
            "Corda resistente (10 ouro)",
            "Partir",
        ])
        precos = {1: 15, 2: 5, 3: 10}
        if op == 4:
            return
        if jogador["ouro"] < precos[op]:
            print("\n  Ouro insuficiente.")
            pausa()
            continue
        jogador["ouro"] -= precos[op]
        if op == 1:
            jogador["pocoes"] += 1
        elif op == 2:
            jogador["racoes"] += 1
        else:
            jogador["cordas"] += 1
        print("\n  Comprado!")


def cap_taverna():
    titulo("CAPÍTULO 1 - O CONTRATO")
    print("""  Numa mesa escura do Corvo Cansado, Mestre Orlan, agente do Conselho
  Livre, desliza um mapa até você.

  "Lyra está no quarto dos fundos. Ela acha que somos todos rebeldes
  idealistas. Não sabe que o Duque pôs um assassino, chamado A Sombra,
  no seu encalço. Mantenha-a calma. Proteja-a sem que ela saiba."

  Orlan hesita, e a voz falha:
  "O Duque também mantém minha filha, Mira, como refém. Se o Conselho
  tiver algum oficial do Duque preso... talvez haja uma troca. Lembre-se
  disso quando for negociar."

  Você sobe as escadas. Lyra o encara, desconfiada, abraçada a uma bolsa
  de couro. Como você a cumprimenta?
""")
    op = escolher([
        "Cordialmente: \"Vou levá-la em segurança, senhorita.\"",
        "Profissional: \"Fique perto e faça o que eu mandar.\"",
        "Seco: \"Sou pago para entregar a carga. Não faça perguntas.\"",
    ])
    if op == 1:
        mudar_confianca(1, "(gentileza) ")
    elif op == 3:
        mudar_confianca(-1, "(frieza) ")
    pausa()
    loja()
    return True


def cap_emboscada():
    titulo("CAPÍTULO 2 - A PRIMEIRA EMBOSCADA")
    print("""  Ao amanhecer, vocês deixam a cidade pela estrada do norte. Mal passam
  do último moinho quando dois homens com o brasão de Valdoria bloqueiam
  o caminho, de espadas desembainhadas.

  "Entreguem a escriba e ninguém se machuca."
""")
    inimigos = [criar_inimigo("Capanga do Duque", 14, 5, 1),
                criar_inimigo("Capanga do Duque", 14, 5, 1)]
    return resolver_combate(combate(inimigos))


def rota_real():
    print("""\n  A Estrada Real é larga e rápida, mas patrulhada. Na curva do rio,
  um posto de controle dos Corvos Negros, soldados leais ao Duque,
  bloqueia a ponte.
""")
    guardas = [criar_inimigo("Corvo Negro", 18, 6, 3),
               criar_inimigo("Corvo Negro", 18, 6, 3)]
    while True:
        op = escolher([
            "Blefar: dizer que são mercadores (Carisma)",
            "Subornar o sargento (30 ouro)",
            "Atacar de surpresa (Astúcia)",
            "Contornar pelo mato (Astúcia)",
        ])
        if op == 1:
            if teste("carisma", 13, "(blefe) "):
                print("\n  O sargento acena, entediado. Vocês passam.")
                return True
            print("\n  O sargento estreita os olhos: \"Mercadores não têm mãos de lâmina.\"")
            break
        if op == 2:
            if jogador["ouro"] < 30:
                print("\n  Você não tem 30 ouro.")
                continue
            jogador["ouro"] -= 30
            print("\n  O sargento embolsa as moedas e vira o rosto. Vocês passam.")
            return True
        if op == 3:
            if teste("astucia", 12, "(emboscada) "):
                print("\n  Você acerta o primeiro golpe antes que reajam!")
                guardas[0]["hp"] -= 8
            else:
                print("\n  Um galho estala. Eles já esperavam o ataque.")
            break
        if op == 4:
            if teste("astucia", 12, "(contornar) "):
                print("\n  Vocês atravessam o rio a vau, sem serem vistos.")
                return True
            print("\n  Vocês são vistos na margem! Soldados correm em sua direção.")
            break
    return resolver_combate(combate(guardas))


def rota_floresta():
    print("""\n  A Floresta Sombria engole a luz. Raízes retorcidas, silêncio demais...
  Então, os olhos amarelos: lobos famintos cercam o grupo.
""")
    lobos = [criar_inimigo("Lobo Faminto", 12, 6, 0),
             criar_inimigo("Lobo Faminto", 12, 6, 0)]
    if not resolver_combate(combate(lobos, pode_fugir=False)):
        return False
    print("""\n  Entre as árvores, vocês encontram uma capela abandonada.
  O telhado resiste, e há lenha seca lá dentro.
""")
    op = escolher(["Descansar na capela (+10 HP você, +5 HP Lyra)", "Seguir viagem"])
    if op == 1:
        jogador["hp"] = min(jogador["hp_max"], jogador["hp"] + 10)
        lyra["hp"] = min(lyra["hp_max"], lyra["hp"] + 5)
        print("\n  Vocês dormem em paz por algumas horas.")
        mudar_confianca(1, "(descanso) ")
    return True


def rota_montanha():
    print("""\n  O Passo da Montanha é gelado e íngreme. A ponte de cordas que
  cruza o abismo está rompida pela metade.
""")
    while True:
        op = escolher([
            "Cruzar carregando Lyra nas costas (Força)",
            "Usar uma corda para atravessar (consome 1 corda)",
            "Procurar outro caminho (Astúcia)",
        ])
        if op == 1:
            if teste("forca", 12, "(travessia) "):
                print("\n  Com esforço, você atravessa. Lyra o encara, impressionada.")
                mudar_confianca(1, "(bravura) ")
            else:
                print("\n  Uma tábua cede! Vocês se agarram na borda, feridos.")
                jogador["hp"] = max(1, jogador["hp"] - 6)
                lyra["hp"] = max(1, lyra["hp"] - 3)
            return True
        if op == 2:
            if jogador["cordas"] <= 0:
                print("\n  Você não tem corda.")
                continue
            jogador["cordas"] -= 1
            print("\n  Você ancora a corda e guia Lyra com segurança.")
            return True
        if op == 3:
            if teste("astucia", 11, "(rastreio) "):
                print("\n  Você acha uma trilha de cabras e um baú esquecido: +20 ouro.")
                jogador["ouro"] += 20
            else:
                print("\n  Uma avalanche de pedras cai sobre vocês!")
                jogador["hp"] = max(1, jogador["hp"] - 8)
                lyra["hp"] = max(1, lyra["hp"] - 4)
            return True


def cap_rota():
    titulo("CAPÍTULO 3 - A ENCRUZILHADA")
    print("""  Três caminhos levam às Marchas Livres:

  • Estrada Real     - rápida, mas cheia de patrulhas do Duque.
  • Floresta Sombria - escondida, mas cheia de feras.
  • Passo da Montanha- deserto, mas traiçoeiro.
""")
    mostrar_status()
    op = escolher(["Estrada Real", "Floresta Sombria", "Passo da Montanha"])
    if op == 1:
        return rota_real()
    if op == 2:
        return rota_floresta()
    return rota_montanha()


def perseguicao():
    print("""\n  Você acorda sobressaltado: o lugar de Lyra está vazio!
  Pegadas levam para a escuridão do bosque. Você corre atrás dela.
""")
    jogador["hp"] = max(1, jogador["hp"] - 6)
    print("  Tropeçando em raízes e espinhos, você perde 6 HP.")
    print("""
  Você a encontra à beira de um riacho, de joelhos, chorando.

  "Meu irmão Teo ainda está em Valdoria! Se o Duque descobrir que fui
   eu, vai matá-lo! Eu só queria voltar e implorar perdão..."
""")
    op = escolher([
        "\"Vou fazer o possível para tirá-lo de lá. Eu prometo.\"",
        "\"Seu irmão já está perdido. Volte para o acampamento.\"",
        "Agarrá-la em silêncio e levá-la de volta.",
    ])
    if op == 1:
        estado["prometeu_irmao"] = True
        mudar_confianca(2, "(promessa) ")
    elif op == 2:
        mudar_confianca(-2, "(crueldade) ")
    else:
        mudar_confianca(-1, "(força) ")


def cap_acampamento():
    titulo("CAPÍTULO 4 - A NOITE")
    print("  Cai a noite. Vocês montam acampamento.\n")
    if jogador["racoes"] > 0:
        jogador["racoes"] -= 1
        print("  Vocês dividem uma ração de viagem.")
    else:
        print("  Sem comida! Vocês dormem de estômago vazio.")
        jogador["hp"] = max(1, jogador["hp"] - 5)
        mudar_confianca(-1, "(fome) ")

    print("""
  Lyra está inquieta, olha para o escuro. Você sente que ela vai tentar
  fugir esta noite. O que faz?
""")
    while True:
        op = escolher([
            "Ficar de vigia a noite toda (Astúcia)",
            "Amarrá-la (consome 1 corda)",
            "Conversar abertamente antes de dormir (Carisma)",
        ])
        if op == 1:
            if teste("astucia", 12, "(vigília) "):
                print("\n  Perto do amanhecer, você a flagra tentando escapar.")
                print("  Ela desiste, em lágrimas, e conta sobre o irmão preso em Valdoria.")
                resp = escolher([
                    "\"Vou tentar libertá-lo. Prometo.\"",
                    "\"Não posso prometer nada.\"",
                ])
                if resp == 1:
                    estado["prometeu_irmao"] = True
                    mudar_confianca(2, "(promessa) ")
                else:
                    mudar_confianca(-1, "(frieza) ")
            else:
                print("\n  O cansaço vence você por um instante... e ela sumiu.")
                perseguicao()
            break
        if op == 2:
            if jogador["cordas"] <= 0:
                print("\n  Você não tem corda.")
                continue
            jogador["cordas"] -= 1
            print("\n  Você a amarra pelos pulsos. Ela não protesta, apenas o fuzila com o olhar.")
            mudar_confianca(-2, "(prisioneira) ")
            break
        if op == 3:
            if teste("carisma", 11, "(conversa) "):
                print("\n  Lyra desabafa: o irmão Teo ainda está em Valdoria, "
                      "e ela teme por ele.")
                print("  Você a escuta com atenção. Ela se acalma e fica.")
                mudar_confianca(2, "(confiança) ")
                resp = escolher([
                    "\"Faremos o que for possível por ele.\"",
                    "Apenas ouvir, sem prometer.",
                ])
                if resp == 1:
                    estado["prometeu_irmao"] = True
                    mudar_confianca(1, "(promessa) ")
            else:
                print("\n  Suas palavras soam vazias. Lyra se cala, desconfiada.")
                mudar_confianca(-1, "")
                perseguicao()
            break

    jogador["hp"] = min(jogador["hp_max"], jogador["hp"] + 8)
    lyra["hp"] = min(lyra["hp_max"], lyra["hp"] + 4)
    print("\n  Vocês descansam o que podem. (+8 HP você, +4 HP Lyra)")
    pausa()
    return True


def evento_azar():
    titulo("NA ESTRADA")
    e = d(4)
    if e == 1:
        print("  Uma chuva torrencial cai por horas. Todos chegam encharcados e gelados.")
        jogador["hp"] = max(1, jogador["hp"] - 3)
        print("  (-3 HP)")
    elif e == 2:
        print("  Ratos roeram suas provisões durante a noite.")
        if jogador["racoes"] > 0:
            jogador["racoes"] -= 1
            print("  (-1 ração)")
        else:
            print("  Por sorte, não havia nada para roer.")
    elif e == 3:
        print("  Um mercador ambulante oferece uma poção por 12 ouro.")
        op = escolher(["Comprar", "Recusar"])
        if op == 1:
            if jogador["ouro"] >= 12:
                jogador["ouro"] -= 12
                jogador["pocoes"] += 1
                print("  Poção comprada.")
            else:
                print("  Você não tem ouro suficiente.")
    else:
        print("  Um dia tranquilo. Lyra conta, entre risos tímidos, histórias dos "
              "arquivos do Duque.")
        mudar_confianca(1, "(boa companhia) ")
    pausa()
    return True


def cap_sombra():
    titulo("CAPÍTULO 5 - A SOMBRA")
    print("""  No fim da tarde, Lyra pára de caminhar, pálida.

  "Alguém nos segue desde ontem. Eu sinto. Estamos sendo seguidos?"

  Você sabe que ela tem razão: A Sombra está perto.
""")
    op = escolher([
        "Contar a verdade (ela entrará em pânico, mas vocês se prepararão)",
        "Mentir: \"É só o vento, senhorita.\" (manter a calma, como Orlan pediu)",
    ])
    sombra = criar_inimigo("A Sombra (assassino)", 30, 8, 3)
    if op == 1:
        mudar_confianca(-1, "(pânico) ")
        print("\n  Juntos, vocês armam uma armadilha de arame na trilha.")
        sombra["hp"] -= 6
    else:
        estado["mentiu"] = True
        print("\n  Lyra relaxa... por enquanto.")
    pausa()
    print("""
  Ao entardecer, uma lâmina cintila na penumbra. A Sombra ataca!
""")
    return resolver_combate(combate([sombra], pode_fugir=False))


def cap_fortaleza():
    titulo("CAPÍTULO 6 - A FORTALEZA ALVORADA")
    print("""  Depois de dias de viagem, as torres da Fortaleza Alvorada surgem no
  horizonte. Mas algo está errado: fumaça sobe do pátio e o estandarte
  do Conselho jaz rasgado no chão.

  O portão está aberto. Dentro, o enviado do Conselho foi assassinado.
  O Capitão Varro, comandante da guarnição, vendeu a fortaleza ao Duque.

  Não há ninguém para receber Lyra. Agora é VOCÊ quem terá de fazer o
  trabalho do destino: acender o Farol de Alvorada para chamar o exército
  rebelde e segurar o portão até que ele chegue.
""")
    mostrar_status()
    op = escolher(["Entrar pelo portão principal", "Escalar o muro dos fundos (Astúcia)"])
    varro = criar_inimigo("Capitão Varro", 36, 7, 4)
    traidores = [criar_inimigo("Guarda Traidor", 14, 5, 2),
                 criar_inimigo("Guarda Traidor", 14, 5, 2)]
    if op == 2:
        if teste("astucia", 12, "(escalada) "):
            print("\n  Vocês surpreendem o Capitão Varro pelas costas!")
            varro["hp"] -= 8
        else:
            print("\n  Uma sentinela os vê! Varro ri: \"Sabia que viriam.\"")
    else:
        print("\n  Varro os aguarda no pátio, de espada em punho.")
        print("  \"Você chegou tarde, mercenário. O Duque paga melhor.\"")
    pausa()
    if not resolver_combate(combate([varro] + traidores, pode_fugir=False)):
        return False
    print("""
  Com a guarnição traidora caída, você sobe a torre. Lyra o segue,
  e juntos acendem o Farol de Alvorada.
""")
    if lyra["confianca"] >= 5:
        print("  Lyra entrega o Livro das Dívidas às suas mãos: \"Eu confio em você.\"")
    pausa()
    return True


def cap_barganha():
    titulo("CAPÍTULO 7 - A BARGANHA")
    print("""  Ao amanhecer, os batalhões rebeldes chegam, liderados pela Dama
  Cássia, do Conselho Livre. Ela lê o Livro das Dívidas em silêncio.

  "Isto muda a guerra. Mas o tesouro do Conselho foi saqueado... Posso
   pagar apenas 120 moedas, em vez das 200 prometidas."

  Cássia mantém preso o Coronel Ferro, oficial do Duque capturado na
  última semana. E, lá fora, um arauto do Duque chegou com bandeira
  branca: oferece 500 moedas por Lyra, "sem perguntas".

  A palavra final é sua.
""")
    mostrar_status()
    op = escolher([
        "Aceitar as 120 moedas e partir.",
        "Barganhar pelas 200 moedas prometidas (Carisma).",
        "Abrir mão do ouro e pedir o Coronel Ferro, para trocá-lo por Mira, "
        "a filha de Orlan (Carisma).",
        "Vender Lyra ao arauto do Duque por 500 moedas.",
    ])
    bonus = 3 if lyra["confianca"] >= 7 else 0
    if bonus:
        print("\n  Lyra se adianta e fala a seu favor diante de Cássia (+3).")

    if op == 1:
        jogador["ouro"] += 120
        return final("seguro")
    if op == 2:
        rolagem = d(20) + jogador["mods"]["carisma"] + bonus
        print(f"\n  Barganha: d20 + mods = {rolagem} (DC 15)")
        if rolagem >= 15:
            jogador["ouro"] += 200
            print("  Cássia suspira e ordena que paguem tudo.")
        else:
            jogador["ouro"] += 80
            print("  Cássia se ofende: \"Ganância. Fica com 80.\"")
        return final("ouro")
    if op == 3:
        rolagem = d(20) + jogador["mods"]["carisma"] + bonus
        print(f"\n  Pedido de troca: d20 + mods = {rolagem} (DC 13)")
        if rolagem >= 13:
            return final("refem")
        jogador["ouro"] += 60
        print("  Cássia nega: \"Ferro é valioso demais.\" Paga apenas 60 moedas.")
        return final("negado")
    jogador["ouro"] += 500
    estado["traiu"] = True
    return final("traicao")


def final(tipo):
    titulo("EPÍLOGO")
    if tipo == "seguro":
        print("  Você parte com 120 moedas. O dever está cumprido.\n"
              "  Lyra acena à distância. Orlan nunca mais viu a filha.")
    elif tipo == "ouro":
        print("  Você vai embora de bolsos cheios e consciência tranquila.\n"
              "  Mira continua refém de Valdoria; Orlan lamenta, mas agradece.")
    elif tipo == "refem":
        print("  Cássia cede: o Coronel Ferro será trocado por Mira na fronteira.")
        if estado["prometeu_irmao"]:
            print("  Lembrando da promessa que você fez, ela inclui Teo, irmão de "
                  "Lyra, na troca.")
            print("\n  Dias depois, Mira e Teo cruzam a fronteira vivos.")
            print("  Lyra o abraça chorando. Orlan jura dívida eterna.")
            print("\n  ★ FINAL HEROICO: você cumpriu o contrato e salvou três vidas.")
        else:
            print("  Dias depois, Mira cruza a fronteira viva e abraça o pai.")
            print("  Lyra, sem promessa feita, não ousa pedir pelo irmão.")
            print("\n  ★ FINAL BOM: você escolheu a vida em vez do ouro.")
    elif tipo == "negado":
        print("  Sem troca e com pouco ouro, você deixa a fortaleza amargurado.")
    elif tipo == "traicao":
        print("  Você entrega Lyra ao arauto. Ela o encara, sem uma palavra.")
        if lyra["confianca"] >= 6:
            print("  \"Eu acreditei em você\", sussurra, antes de desaparecer.")
        print("  Você volta rico, mas o Farol de Alvorada ainda queima atrás de você.")
        print("\n  ☠ FINAL SOMBRIO: o ouro pesa mais do que parecia.")

    if estado["mentiu"] and tipo not in ("traicao",):
        print("\n  (Lyra descobriu que você mentiu sobre A Sombra, e nunca esqueceu.)")

    print()
    mostrar_status()
    print("\n  Obrigado por jogar A ESCOLTA DE LYRA ASHGROVE!")
    return True


# LOOP PRINCIPAL

def jogar():
    iniciar_estado()
    intro()
    criar_personagem()
    etapas = [cap_taverna, cap_emboscada, cap_rota, cap_acampamento,
              evento_azar, cap_sombra, cap_fortaleza, cap_barganha]
    for etapa in etapas:
        if etapa() is False:
            return


def main():
    while True:
        jogar()
        print()
        r = input("  Jogar novamente? (s/n) ").strip().lower()
        if r != "s":
            print("\n  Até a próxima jornada!\n")
            break


if __name__ == "__main__":
    main()