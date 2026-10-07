import pygame
from config.constantes import (
    MINIMAPA_ZOOM_INICIAL,
    MINIMAPA_VIEWPORT,
    MINIMAPA_TAMANHO_MIN_CONTORNO
)
from config.caminhos import FONTE_PRINCIPAL
from config.cores import Cores
from engine.rasterizacao import (
    scanline_fill,
    desenhar_poligono,
    desenhar_linha
)
from engine.viewport import (
    matriz_mundo_para_viewport
)
from engine.transformacoes import (
    aplica_transformacao
)
from engine.recorte import (
    cohen_sutherland
)


class MiniMapa:

    def __init__(self, jogo):

        self.jogo = jogo

        # =================================================
        # CONFIGURAÇÃO
        # =================================================
        self.zoom = MINIMAPA_ZOOM_INICIAL
        self.viewport = MINIMAPA_VIEWPORT

        # =================================================
        # FONTE
        # =================================================
        self.fonte = (jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 24))

        # ---- Monta a moldura uma vez só ----
        (xv_min, yv_min, xv_max, yv_max) = self.viewport

        largura_caixa = int(xv_max - xv_min) + 1
        altura_caixa = int(yv_max - yv_min) + 1

        self.superficie_moldura = pygame.Surface((largura_caixa, altura_caixa))

        pontos_locais = [
            (0, 0),
            (largura_caixa - 1, 0),
            (largura_caixa - 1, altura_caixa - 1),
            (0, altura_caixa - 1)
        ]

        scanline_fill(self.superficie_moldura, pontos_locais, Cores.MINIMAPA_FUNDO)
        desenhar_poligono(self.superficie_moldura, pontos_locais, Cores.MINIMAPA_BORDA)

        # Superfície onde as entidades são desenhadas a cada frame.
        # Como ela tem o tamanho exato do minimapa, nada vaza para fora da caixa.
        self.superficie_mapa = pygame.Surface((largura_caixa, altura_caixa))
        self.pontos_borda = pontos_locais

        # Viewport em coordenadas locais da superfície (origem em 0,0)
        self.viewport_local = (0, 0, largura_caixa - 1, altura_caixa - 1)

        # ---- Monta o texto uma vez só ----
        mensagem_zoom = f"Zoom: {self.zoom:.1f}x"
        self.texto_zoom = self.fonte.render(mensagem_zoom, True, Cores.MINIMAPA_TEXTO)
        self.texto_zoom_sombra = self.fonte.render(mensagem_zoom, True, (0, 0, 0))


    # =====================================================
    # WINDOW
    # =====================================================
    def obter_window(self, jogador):

        largura_mundo = self.jogo.largura
        altura_mundo = self.jogo.altura

        largura_window = (largura_mundo / self.zoom)
        altura_window = (altura_mundo / self.zoom)

        centro_x = jogador.x
        centro_y = jogador.y

        x_min = (centro_x - largura_window / 2)
        x_max = (centro_x + largura_window / 2)

        y_min = (centro_y - altura_window / 2)
        y_max = (centro_y + altura_window / 2)

        # =================================================
        # LIMITA WINDOW AO MUNDO
        # =================================================
        if x_min < 0:
            x_min = 0
            x_max = largura_window

        if x_max > largura_mundo:
            x_max = largura_mundo
            x_min = (largura_mundo - largura_window)

        if y_min < 0:
            y_min = 0
            y_max = altura_window

        if y_max > altura_mundo:
            y_max = altura_mundo
            y_min = (altura_mundo - altura_window)

        return (x_min, y_min, x_max, y_max)


    # =====================================================
    # MOLDURA
    # =====================================================
    def desenhar_moldura(self, tela):

        (xv_min, yv_min, xv_max, yv_max) = self.viewport

        tela.blit(self.superficie_mapa, (xv_min, yv_min))
        tela.blit(self.texto_zoom_sombra, (xv_min + 7, yv_max + 7))
        tela.blit(self.texto_zoom, (xv_min + 5, yv_max + 5))


    # =====================================================
    # TRANSFORMAÇÃO DE UMA ENTIDADE
    # =====================================================
    def transformar_entidade(self, entidade, matriz_viewport):

        pontos_mundo = (entidade.obter_pontos_mundo())

        return aplica_transformacao(matriz_viewport, pontos_mundo)


    # =====================================================
    # DESENHAR UMA ENTIDADE
    # =====================================================
    def desenhar_entidade(self, superficie, entidade, matriz_viewport):

        (xv_min, yv_min, xv_max, yv_max) = self.viewport_local

        pontos_viewport = (self.transformar_entidade(entidade, matriz_viewport))

        # =================================================
        # PREENCHIMENTO (scanline)
        # Cada tipo de entidade tem a sua cor.
        # Os pixels fora da superfície são descartados no setPixel.
        # =================================================
        scanline_fill(superficie, pontos_viewport, entidade.cor_minimapa)

        # =================================================
        # CONTORNO
        # Só em objetos grandes o bastante para o contorno não
        # esconder a cor do preenchimento.
        # =================================================
        xs = [p[0] for p in pontos_viewport]
        ys = [p[1] for p in pontos_viewport]

        if max(max(xs) - min(xs), max(ys) - min(ys)) < MINIMAPA_TAMANHO_MIN_CONTORNO:
            return

        n = len(pontos_viewport)

        for i in range(n):

            x0, y0 = pontos_viewport[i]
            x1, y1 = pontos_viewport[(i + 1) % n]

            # =================================================
            # COHEN-SUTHERLAND
            # =================================================
            visivel, rx0, ry0, rx1, ry1 = (cohen_sutherland(x0, y0, x1, y1, xv_min, yv_min, xv_max, yv_max))

            if not visivel:
                continue

            # =================================================
            # BRESENHAM
            # =================================================
            desenhar_linha(superficie, int(rx0), int(ry0), int(rx1), int(ry1), Cores.MINIMAPA_CONTORNO)


    # =====================================================
    # DESENHO COMPLETO
    # =====================================================
    def desenhar(self, tela, jogador, objetos):

        # =================================================
        # FUNDO (começa cada frame limpo)
        # =================================================
        self.superficie_mapa.blit(self.superficie_moldura, (0, 0))

        # =================================================
        # WINDOW
        # =================================================
        window = self.obter_window(jogador)

        # =================================================
        # VIEWPORT
        # =================================================
        matriz_viewport = (matriz_mundo_para_viewport(window, self.viewport_local))

        # =================================================
        # ENTIDADES
        # Objetos caindo primeiro, jogador por cima.
        # =================================================
        for objeto in objetos:
            self.desenhar_entidade(self.superficie_mapa, objeto, matriz_viewport)

        self.desenhar_entidade(self.superficie_mapa, jogador, matriz_viewport)

        # =================================================
        # BORDA POR CIMA (as entidades não cobrem a moldura)
        # =================================================
        desenhar_poligono(self.superficie_mapa, self.pontos_borda, Cores.MINIMAPA_BORDA)

        # =================================================
        # COLA NA TELA
        # =================================================
        self.desenhar_moldura(tela)