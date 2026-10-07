from engine.textura import scanline_textura
from config.constantes import (
    JOGADOR_VELOCIDADE,
    JOGADOR_INTERVALO_ANIMACAO
)
from entities.entidade import Entidade
from config.cores import Cores



class Jogador(Entidade):

    def __init__(self, textura_parado, texturas_corrida):

        # =================================================
        # RETÂNGULO VISUAL
        # =================================================
        pontos_visuais = [
            (-30, -70),
            (30, -70),
            (30, 70),
            (-30, 70)
        ]

        # =================================================
        # RETÂNGULO DE COLISÃO
        # =================================================
        pontos_colisao = [
            (-25, -70),
            (25, -70),
            (25, 70),
            (-25, 70)
        ]

        super().__init__(pontos_visuais, Cores.BRANCO, pontos_colisao)

        # O jogador usa textura, portanto não desenha borda.
        self.cor_borda = None

        self.cor_minimapa = Cores.MINIMAPA_JOGADOR

        # =================================================
        # MOVIMENTO
        # =================================================
        self.vel_movimento = JOGADOR_VELOCIDADE

        # =================================================
        # TEXTURAS
        # =================================================
        self.textura_parado = textura_parado
        self.texturas_corrida = texturas_corrida

        # =================================================
        # ANIMAÇÃO
        # =================================================
        self.indice_frame = 0
        self.tempo_animacao = 0.0
        self.intervalo_frame = JOGADOR_INTERVALO_ANIMACAO

        self.direcao = 1
        self.movendo = False


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        super().atualizar(dt)

        # Verifica se o jogador está se movimentando
        self.movendo = abs(self.vel_x) > 0

        if self.movendo:

            # Descobre a direção
            if self.vel_x > 0:
                self.direcao = 1

            elif self.vel_x < 0:
                self.direcao = -1

            # Atualiza o tempo da animação
            self.tempo_animacao += dt

            if self.tempo_animacao >= self.intervalo_frame:
                self.tempo_animacao -= self.intervalo_frame
                self.indice_frame += 1
                # Volta para o primeiro frame
                if self.indice_frame >= len(self.texturas_corrida):
                    self.indice_frame = 0

        else:
            # Jogador parado
            self.indice_frame = 0
            self.tempo_animacao = 0.0


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, superficie):

        # Escolhe a imagem
        if self.movendo:
            imagem = self.texturas_corrida[self.indice_frame]
        else:
            imagem = self.textura_parado

        pontos_mundo = self.obter_pontos_mundo()

        # -------------------------------------------------
        # TEXTURA NORMAL
        # -------------------------------------------------
        if self.direcao == 1:

            vertices_texturizados = [
                (pontos_mundo[0], (0.0, 0.0)),
                (pontos_mundo[1], (1.0, 0.0)),
                (pontos_mundo[2], (1.0, 1.0)),
                (pontos_mundo[3], (0.0, 1.0))
            ]

        # -------------------------------------------------
        # TEXTURA INVERTIDA
        # -------------------------------------------------
        else:

            vertices_texturizados = [
                (pontos_mundo[0], (1.0, 0.0)),
                (pontos_mundo[1], (0.0, 0.0)),
                (pontos_mundo[2], (0.0, 1.0)),
                (pontos_mundo[3], (1.0, 1.0))
            ]

        scanline_textura(superficie, vertices_texturizados, imagem, usar_alpha=True)