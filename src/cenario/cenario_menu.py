import pygame

from config.caminhos import (
    POMBO_FRENTE,
    POMBO_COSTAS,
    POMBO_VOANDO_FRENTE,
    POMBO_VOANDO,
    POMBO_PLANANDO,
    POMBO_PARANDO
)
from engine.rasterizacao import (
    scanline_fill_gradiente,
    desenhar_poligono,
    retangulo_para_poligono,
    desenhar_circulo,
    desenhar_elipse,
    boundary_fill,
)
from engine.textura import scanline_textura
from config.cores import Cores


class CenarioMenu:

    def __init__(self, jogo):
        self.jogo = jogo
        self.largura = jogo.largura
        self.altura = jogo.altura

        # =================================================
        # SURFACE DO CENÁRIO
        # =================================================
        self.superficie = pygame.Surface((self.largura, self.altura))

        # =================================================
        # RECURSOS
        # =================================================
        recursos = self.jogo.recursos
        self.img_pombo_frente = (recursos.carregar_imagem(POMBO_FRENTE))
        self.img_pombo_costas = (recursos.carregar_imagem(POMBO_COSTAS))
        self.img_pombo_voando_frente = (recursos.carregar_imagem(POMBO_VOANDO_FRENTE))
        self.img_pombo_voando = (recursos.carregar_imagem(POMBO_VOANDO))
        self.img_pombo_planando = (recursos.carregar_imagem(POMBO_PLANANDO))
        self.img_pombo_parando = (recursos.carregar_imagem(POMBO_PARANDO))

        # =================================================
        # CONFIGURAÇÃO DOS POMBOS
        # =================================================
        self.largura_pombo = 40
        self.altura_pombo = 40

        # =================================================
        # RENDERIZA O CENÁRIO UMA VEZ
        # =================================================
        self._renderizar()


    # =====================================================
    # TEXTURA EM QUADRADO
    # =====================================================
    def _desenhar_textura_quadrado(self, tela, x, y, largura, altura, imagem, u_invertido=False):

        if u_invertido:
            vertices = [
                ((x, y), (1.0, 0.0)),
                ((x + largura, y), (0.0, 0.0)),
                ((x + largura, y + altura), (0.0, 1.0)),
                ((x, y + altura), (1.0, 1.0))
            ]

        else:
            vertices = [
                ((x, y), (0.0, 0.0)),
                ((x + largura, y), (1.0, 0.0)),
                ((x + largura, y + altura), (1.0, 1.0)),
                ((x, y + altura), (0.0, 1.0))
            ]

        scanline_textura(tela, vertices, imagem, usar_alpha=True)


    # =====================================================
    # RENDERIZAÇÃO DO CENÁRIO
    # =====================================================
    def _renderizar(self):

        tela = self.superficie

        # =================================================
        # FUNDO COM GRADIENTE
        # =================================================
        fundo = retangulo_para_poligono(0, 0, self.largura, self.altura)
        scanline_fill_gradiente(tela, fundo, Cores.FUNDO_CEU)

        # =================================================
        # POSTE
        # =================================================
        borda = Cores.PRETO
        poste = [
            (50, 600),
            (50, 50),
            (60, 50),
            (60, 35),
            (70, 35),
            (70, 50),
            (80, 50),
            (80, 600)
        ]
        desenhar_poligono(tela, poste, borda)
        boundary_fill(tela, 65, 400, Cores.POSTE, borda)

        # =================================================
        # BRAÇO DO POSTE
        # =================================================
        braco_poste = [
            (60, 35),
            (140, 20),
            (140, 30),
            (70, 55)
        ]
        desenhar_poligono(tela, braco_poste, borda)
        boundary_fill(tela, 100, 35, Cores.POSTE, borda)

        # =================================================
        # LUMINÁRIA
        # =================================================
        xc_luz = 140
        yc_luz = 35
        desenhar_elipse(tela, xc_luz, yc_luz, 20, 8, borda)
        boundary_fill(tela, xc_luz, yc_luz, Cores.LUMINÁRIA, borda)

        # =================================================
        # LÂMPADA
        # =================================================
        desenhar_circulo(tela, xc_luz, yc_luz + 10, 12, borda)
        boundary_fill(tela, xc_luz, yc_luz + 10, Cores.LÂMPADA, borda)

        # =================================================
        # FIOS
        # =================================================
        fio1 = [
            (80, 100),
            (80, 101),
            (800, 101),
            (800, 100)
        ]
        fio2 = [
            (80, 110),
            (80, 111),
            (800, 111),
            (800, 110)
        ]
        fio3 = [
            (80, 120),
            (80, 121),
            (800, 121),
            (800, 120)
        ]
        desenhar_poligono(tela, fio1, borda)
        desenhar_poligono(tela, fio2, borda)
        desenhar_poligono(tela, fio3, borda)

        # =================================================
        # POMBOS
        # =================================================
        self._desenhar_textura_quadrado(tela, 200, 63, self.largura_pombo, self.altura_pombo, self.img_pombo_frente)
        self._desenhar_textura_quadrado(tela, 400, 70, self.largura_pombo, self.altura_pombo, self.img_pombo_costas)
        self._desenhar_textura_quadrado(tela, 700, 20, self.largura_pombo, self.altura_pombo, self.img_pombo_voando_frente)
        self._desenhar_textura_quadrado(tela, 130, 330, self.largura_pombo, self.altura_pombo, self.img_pombo_voando)
        self._desenhar_textura_quadrado(tela, 630, 250, self.largura_pombo, self.altura_pombo, self.img_pombo_planando)
        self._desenhar_textura_quadrado(tela, 230, 150, self.largura_pombo, self.altura_pombo, self.img_pombo_parando)
        self._desenhar_textura_quadrado(tela, 630, 430, self.largura_pombo, self.altura_pombo, self.img_pombo_voando, u_invertido=True)


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, tela):
        tela.blit(self.superficie, (0, 0))