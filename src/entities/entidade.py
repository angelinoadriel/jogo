from engine.transformacoes import (
    translacao,
    aplica_transformacao
)
from engine.rasterizacao import (
    scanline_fill,
    desenhar_poligono
)
from config.cores import Cores



class Entidade:

    def __init__(self, pontos_locais, cor, pontos_colisao_locais=None):

        # =================================================
        # GEOMETRIA VISUAL
        # =================================================
        self.pontos_locais = pontos_locais

        # =================================================
        # GEOMETRIA DE COLISÃO
        # =================================================
        if pontos_colisao_locais is None:
            self.pontos_colisao_locais = pontos_locais
        else:
            self.pontos_colisao_locais = pontos_colisao_locais

        # =================================================
        # APARÊNCIA
        # =================================================
        self.cor = cor

        self.cor_borda = Cores.PRETO

        # Cor usada para representar a entidade no minimapa
        self.cor_minimapa = Cores.BRANCO

        # =================================================
        # TRANSFORMAÇÃO
        # =================================================
        self.x = 0.0
        self.y = 0.0

        # =================================================
        # MOVIMENTO
        # =================================================
        self.vel_x = 0.0
        self.vel_y = 0.0

        # =================================================
        # ESTADO
        # =================================================
        self.ativa = True


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt


    # =====================================================
    # TRANSFORMAÇÃO
    # =====================================================
    def obter_matriz_mundo(self):
        return translacao(self.x, self.y)

    def obter_pontos_mundo(self):
        matriz = self.obter_matriz_mundo()
        return aplica_transformacao(matriz, self.pontos_locais)

    def obter_pontos_colisao_mundo(self):
        matriz = self.obter_matriz_mundo()
        return aplica_transformacao(matriz, self.pontos_colisao_locais)


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, superficie):
        pontos_mundo = self.obter_pontos_mundo()
        scanline_fill(superficie, pontos_mundo, self.cor)

        if self.cor_borda:
            desenhar_poligono(superficie, pontos_mundo, self.cor_borda)