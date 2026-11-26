# A Escolta de Lyra Ashgrove

RPG textual para rodar no terminal, escrito em Python.
Você é um mercenário contratado para escoltar uma desertora política através de uma jornada perigosa, até um destino que pode não ser o que parece.

## Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa (usa apenas `os` e `random`)
- Terminal com suporte a UTF-8

## Como jogar

```bash
python3 rpg_lyra_escolta_prog1.py
```

No Windows, use `python rpg_lyra_escolta_prog1.py`. O jogo é controlado digitando o número da opção desejada e apertando ENTER.

## História

O Ducado de Valdoria apodrece sob o governo do Duque Aldric Voss. Lyra Ashgrove, arquivista pessoal do Duque, fugiu levando o "Livro das Dívidas", a prova de que ele financia mercenários, assassinos e a própria guerra civil. Você deve levá-la viva até a Fortaleza Alvorada, nas Marchas Livres, por 200 moedas de ouro.

O jogo é baseado na lore **Serviço de Escolta**, e usa vários de seus temas:

| Tema da lore | Como aparece no jogo |
|---|---|
| A carga é problemática e tenta fugir | Lyra tenta escapar durante a noite para voltar a Valdoria atrás do irmão |
| Proteger o alvo sem que ele saiba | O contratante pede que você esconda dela a existência de um assassino, A Sombra |
| O destino foi destruído ou subornado | A Fortaleza Alvorada foi vendida ao Duque; você precisa fazer o trabalho que ela faria |
| Deserção política | Lyra é uma desertora carregando segredos de Estado |
| Chegar não encerra a história | Há uma barganha final, com troca de dinheiro por um refém |

## Personagens

| Classe | HP | Ataque | Defesa | Habilidade (1x por combate) |
|---|---|---|---|---|
| Guerreiro | 42 | 7 | 4 | Golpe Poderoso: dano dobrado |
| Ladino | 32 | 6 | 2 | Ataque Furtivo: ignora armadura |
| Clérigo | 36 | 5 | 3 | Luz Sagrada: cura você e Lyra |
| Mago | 27 | 4 | 1 | Bola de Fogo: dano mágico alto |

Cada classe também tem modificadores de **Força**, **Astúcia** e **Carisma**, somados a uma rolagem de d20 nos testes de habilidade.

## Mecânicas

### Testes de habilidade
`d20 + modificador` contra uma dificuldade (DC). Usados para blefar, escalar, vigiar, negociar e outras situações.

### Combate por turnos
A cada rodada você escolhe uma ação:

- **Atacar:** dano = `ataque + d6 − defesa do inimigo`
- **Habilidade especial:** uma vez por combate
- **Proteger Lyra:** defesa +2, e os inimigos só miram em você
- **Usar poção:** cura 15 de HP
- **Fugir:** `d20 + Astúcia` contra DC 12 (impossível em algumas lutas)

Sem a postura de proteção, cada ataque inimigo tem 30% de chance de atingir Lyra. Se ela morrer, a missão fracassa.

### Confiança de Lyra
Um valor de 0 a 10 que muda conforme suas escolhas (gentileza, promessas, mentiras, crueldade). Com confiança 6 ou mais, ela ajuda nos combates arremessando pedras. Com confiança 7 ou mais, ela fala a seu favor na negociação final.

### Recursos
Ouro, poções, rações de viagem e cordas. Rações são consumidas a cada noite; sem comida, você perde vida e Lyra perde confiança.

## Estrutura da jornada

1. **O Contrato:** briefing com Mestre Orlan, escolha de como cumprimentar Lyra e loja inicial
2. **A Primeira Emboscada:** combate contra capangas do Duque
3. **A Encruzilhada:** escolha entre três rotas
   - Estrada Real: posto de controle (blefar, subornar, atacar ou contornar)
   - Floresta Sombria: lobos famintos e uma capela abandonada
   - Passo da Montanha: ponte quebrada e avalanche
4. **A Noite:** Lyra tenta fugir; você vigia, a amarra ou conversa com ela
5. **Evento de azar:** chuva, provisões roídas, um mercador ou um dia tranquilo
6. **A Sombra:** você decide se conta ou esconde a ameaça, e enfrenta o assassino
7. **A Fortaleza Alvorada:** luta contra o Capitão Varro e os guardas traidores, e o acendimento do farol
8. **A Barganha:** negociação final com a Dama Cássia, do Conselho Livre

## Finais

A barganha final tem quatro caminhos:

- Aceitar as 120 moedas oferecidas
- Barganhar pelas 200 moedas prometidas
- Trocar o ouro por um oficial inimigo preso, para libertar a filha de Orlan (e o irmão de Lyra, se você prometeu ajudá-lo)
- Vender Lyra ao arauto do Duque por 500 moedas

O resultado depende do ouro, da confiança de Lyra e das promessas feitas, e vai do final heroico ao sombrio.

## Organização do código

O código é dividido em seções dentro de um único arquivo:

| Seção | Conteúdo |
|---|---|
| Dados globais | Dicionários `jogador`, `lyra` e `estado`, e a lista `CLASSES` |
| Utilidades | `limpar`, `pausa`, `d`, `titulo`, `barra`, `escolher`, `teste`, `mudar_confianca`, `mostrar_status`, `game_over` |
| Combate | `criar_inimigo`, `causar_dano`, `escolher_alvo`, `usar_especial`, `combate`, `resolver_combate` |
| Capítulos | Uma função por capítulo ou rota (`cap_taverna`, `rota_real`, `cap_barganha` etc.) |
| Loop principal | `jogar` e `main` |

Cada capítulo devolve `True` (a história continua) ou `False` (fim de jogo), e `jogar()` percorre a lista de capítulos até um deles falhar.

## Personalização

- **Balanceamento:** altere os valores em `CLASSES` (HP, ataque, defesa, `mods`) ou nas chamadas de `criar_inimigo(nome, hp, atk, defe)`
- **Nova classe:** adicione um dicionário em `CLASSES` e, se tiver habilidade nova, trate-a em `usar_especial()` e em `NOMES_ESPECIAIS`
- **Novo capítulo:** crie uma função que devolva `True` ou `False` e inclua-a na lista `etapas` em `jogar()`
- **Novo item:** adicione a chave em `jogador` (em `criar_personagem`), em `mostrar_status` e na `loja`

## Ideias para o futuro

- Sistema de salvar e carregar partida
- Mais rotas e eventos aleatórios
- Subida de nível e equipamentos
- Mais companheiros além de Lyra
