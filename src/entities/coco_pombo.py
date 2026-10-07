from engine.textura import scanline_textura
from entities.entidade import Entidade
from config.cores import Cores


class CocoPombo(Entidade):

    def __init__(self, imagem_textura):

        # =================================================
        # RETÂNGULO VISUAL
        # =================================================
        pontos_visuais = [
            (-10, -10),
            (10, -10),
            (10, 10),
            (-10, 10)
        ]

        # =================================================
        # RETÂNGULO DE COLISÃO
        # =================================================
        pontos_colisao = [
            (-7, -7),
            (7, -7),
            (7, 7),
            (-7, 7)
        ]

        super().__init__(pontos_visuais, Cores.BRANCO, pontos_colisao)

        self.cor_minimapa = Cores.MINIMAPA_COCO

        # =================================================
        # TEXTURA
        # =================================================
        self.imagem_textura = imagem_textura


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        super().atualizar(dt)


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