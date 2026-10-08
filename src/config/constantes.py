

NOME_JOGO = "Guerra dos Pombos: O Resgate das Pastas"
NOME_JANELA = "Guerra dos Pombos: O Resgate das Pastas"


# =========================================================
# CONFIGURAÇÕES DA JANELA
# =========================================================
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS_ALVO = 60


# =========================================================
# CONFIGURAÇÕES DO JOGO
# =========================================================
MAX_PASTAS_FASE = 30
INTERVALO_SPAWN_PASTA = 0.8
POSICAO_INICIAL_JOGADOR_Y = ALTURA_TELA - 80
MARGEM_HORIZONTAL_OBJETOS = 30


# =========================================================
# CONFIGURAÇÕES DAS ENTIDADES
# =========================================================
JOGADOR_VELOCIDADE = 400.0
JOGADOR_INTERVALO_ANIMACAO = 0.08

PASTA_VELOCIDADE_ROTACAO = 3.6

# ========================================================
# CONFIGURAÇÕES DE INTERFACE
# ========================================================
MSG_PERDER_VIDAS = "DERROTA! Você sujou todas as camisas!"

MSG_VOLTAR_AO_MENU = "Aperte ENTER para voltar ao menu"

TXT_DE_HISTORIA_MANUAL = (
            "HISTÓRIA\n\n"

            "Hoje é o dia mais importante da sua carreira: "
            "a reunião para decidir seu futuro na universidade "
            "está para começar no prédio central "
            "da faculdade!\n\n"

            "Matheus passou meses preparando relatórios, pastas e "
            "documentos impecáveis.\n\n"

            "Porém, atrasado para à reunião, logo quando chegou "
            "na entrada do prédio, ele escorregou e suas pastas "
            "voaram para todos os lados.\n\n"

            "Para piorar a situação, acima de Matheus estão muitos "
            "pombos que com raiva decidiram bombardear o local "
            "exatamente nesse momento!\n\n"

            "Agora, Matheus precisa pegar o máximo de pastas que estão caíndo "
            "e não se sujar muito para conseguir participar da reunião.\n\n\n"

            "MANUAL\n\n"

            "CONTROLES:\n"
            "A / SETA ESQUERDA - mover para a esquerda\n"
            "D / SETA DIREITA - mover para a direita\n"
            "F3 - mostrar caixas de colisões\n"
            "ENTER - voltar ao menu\n"
            "MOUSE - selecionar opções dos menus"
        )


# =========================================================
# CONFIGURAÇÕES DE PAINEL E BOTÃO
# =========================================================
LARGURA_PAINEL_FIM = 600
ALTURA_PAINEL_FIM = 280

LARGURA_PAINEL_HISTORIA = 600
ALTURA_PAINEL_HISTORIA = 340

LARGURA_BOTAO_MENU = 360
ALTURA_BOTAO_MENU = 60
Y_INICIAL_BOTOES_MENU = 270
ESPACAMENTO_BOTOES_MENU = 85

Y_INICIAL_BOTOES_DIFICULDADE = 220
ESPACAMENTO_BOTOES_DIFICULDADE = 85

LARGURA_BOTAO_VOLTAR = 180
ALTURA_BOTAO_VOLTAR = 50
Y_BOTAO_HISTORIA = 550


# =========================================================
# HUD
# =========================================================
HUD_VIDAS_X = 590
HUD_VIDAS_Y = 20

HUD_VIDAS_LARGURA = 210
HUD_VIDAS_ALTURA = 52

HUD_PASTAS_X = 590
HUD_PASTAS_Y = 82

HUD_PASTAS_LARGURA = 210
HUD_PASTAS_ALTURA = 82

HUD_CAMISA_LARGURA = 32
HUD_CAMISA_ALTURA = 32
HUD_CAMISA_ESPACAMENTO = 6

HUD_BARRA_MARGEM = 15
HUD_BARRA_ALTURA = 10

HUD_FPS_MARGEM_X = 5
HUD_FPS_MARGEM_Y = 5


# =========================================================
# CONFIGURAÇÕES DO MINIMAPA
# =========================================================
# Zoom 1.0 mostra o mundo inteiro (professor + tudo que está caindo).
# Valores maiores aproximam a câmera e ela passa a seguir o professor.
MINIMAPA_ZOOM_INICIAL = 1.0
MINIMAPA_VIEWPORT = (
    20,
    20,
    220,
    170
)

# Objetos menores que isso (em pixels no minimapa) não recebem contorno,
# senão a borda "come" a cor do preenchimento.
MINIMAPA_TAMANHO_MIN_CONTORNO = 8