from engine.rasterizacao import (
    scanline_fill,
    desenhar_poligono
)
from config.cores import Cores


class Painel:

    def __init__(self, x, y, largura, altura, cor_fundo=Cores.PAINEL, cor_borda=Cores.BRANCO):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda


    # =====================================================
    # GEOMETRIA
    # =====================================================
    def obter_pontos(self):
        return [
            (self.x, self.y),
            (self.x + self.largura, self.y),
            (self.x + self.largura, self.y + self.altura),
            (self.x, self.y + self.altura)
        ]


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, tela):

        pontos = self.obter_pontos()
        # Preenchimento
        scanline_fill(tela, pontos, self.cor_fundo)
        # Borda
        if self.cor_borda is not None:
            desenhar_poligono(tela, pontos, self.cor_borda)