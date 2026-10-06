

NOME_JOGO = "Nome do jogo"
NOME_JANELA = "Nome da janela"


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
            "a apresentação decisiva da sua vida no prédio central "
            "da faculdade!\n\n"

            "Ele passou meses preparando relatórios, pastas e "
            "documentos impecáveis.\n\n"

            "Porém, ao chegar ansioso à entrada do prédio, o desastre "
            "acontece. Ele escorrega feio, sua pasta voa e todos os "
            "papéis da reunião começam a cair lentamente pelo ar.\n\n"

            "Para piorar a situação, acima dele está uma colônia de "
            "pombos que decidiu bombardear o local exatamente nesse "
            "momento!\n\n"

            "Agora, Ele precisa correr contra o tempo, movimentando-se "
            "de um lado para o outro para resgatar as pastas cruciais "
            "antes que caiam no chão sujo, enquanto se esquiva "
            "agilmente dos cocôs dos pombos.\n\n"

            "Se Ele se sujar demais, não poderá fazer a apresentação.\n\n\n"

            "MANUAL\n\n"

            "OBJETIVO\n\n"

            "Recupere a quantidade necessária de pastas sem perder "
            "todas as suas vidas.\n\n"

            "CONTROLES\n\n"

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
MINIMAPA_ZOOM_INICIAL = 1.5
MINIMAPA_VIEWPORT = (
    20,
    20,
    180,
    140
)