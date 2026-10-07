import math

from engine.transformacoes import (
    escala,
    rotacao,
    translacao,
    multiplica_matrizes
)
from engine.textura import scanline_textura
from entities.entidade import Entidade
from config.constantes import (
    PASTA_VELOCIDADE_ROTACAO
)
from config.cores import Cores


class Pasta(Entidade):

    def __init__(self, imagem_textura):

        # =================================================
        # RETÂNGULO VISUAL
        # =================================================
        pontos_visuais = [
            (-15, -15),
            (15, -15),
            (15, 15),
            (-15, 15)
        ]

        # =================================================
        # RETÂNGULO DE COLISÃO
        # =================================================
        pontos_colisao = [
            (-10, -13),
            (10, -13),
            (10, 13),
            (-10, 13)
        ]

        super().__init__(pontos_visuais, Cores.BORDA_PASTA, pontos_colisao)

        self.cor_minimapa = Cores.MINIMAPA_COCO

        # =================================================
        # TEXTURA
        # =================================================
        self.imagem_textura = imagem_textura

        # =================================================
        # TRANSFORMAÇÕES
        # =================================================
        self.angulo = 0.0
        self.fator_escala = 1.0

        # Velocidade angular em radianos por segundo
        self.velocidade_rotacao = PASTA_VELOCIDADE_ROTACAO


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        super().atualizar(dt)

        self.angulo = (self.angulo + self.velocidade_rotacao * dt) % (2 * math.pi)


    # =====================================================
    # MATRIZ DE TRANSFORMAÇÃO
    # =====================================================
    def obter_matriz_mundo(self):
        S = escala(self.fator_escala, self.fator_escala)
        R = rotacao(self.angulo)
        T = translacao(self.x, self.y)

        return multiplica_matrizes(T, multiplica_matrizes(R, S))


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, superficie):

        pontos_mundo = self.obter_pontos_mundo()

        vertices_texturizados = [
            (pontos_mundo[0], (0.0, 0.0)),
            (pontos_mundo[1], (1.0, 0.0)),
            (pontos_mundo[2], (1.0, 1.0)),
            (pontos_mundo[3], (0.0, 1.0))
        ]

        scanline_textura(superficie, vertices_texturizados, self.imagem_textura, usar_alpha=True)