import pygame
from config.constantes import (
    MINIMAPA_ZOOM_INICIAL,
    MINIMAPA_VIEWPORT
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

        tela.blit(self.superficie_moldura, (xv_min, yv_min))
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
    def desenhar_entidade(self, tela, entidade, matriz_viewport):

        (xv_min, yv_min, xv_max, yv_max) = self.viewport

        pontos_viewport = (self.transformar_entidade(entidade, matriz_viewport))

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
            desenhar_linha(tela, int(rx0), int(ry0), int(rx1), int(ry1), entidade.cor)


    # =====================================================
    # DESENHO COMPLETO
    # =====================================================
    def desenhar(self, tela, jogador, objetos):

        self.desenhar_moldura(tela)

        # =================================================
        # WINDOW
        # =================================================
        window = self.obter_window(jogador)

        # =================================================
        # VIEWPORT
        # =================================================
        viewport = self.viewport
        matriz_viewport = (matriz_mundo_para_viewport(window, viewport))

        # =================================================
        # ENTIDADES
        # =================================================
        todas_entidades = ([jogador] + objetos)

        for entidade in todas_entidades:
            self.desenhar_entidade(tela, entidade, matriz_viewport)