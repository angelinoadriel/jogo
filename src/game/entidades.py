from engine.transformacoes import translacao, aplica_transformacao, escala, rotacao, multiplica_matrizes
from engine.rasterizacao import scanline_fill, desenhar_poligono, scanline_textura



class Entidade:

    # construtor
    def __init__(self, pontos_locais, cor, pontos_colisao_locais=None):

        # Retângulo/polígono usado visualmente
        self.pontos_locais = pontos_locais

        # Se não foi informado outro retângulo,
        # usa o visual como colisão.
        if pontos_colisao_locais is None:
            self.pontos_colisao_locais = pontos_locais
        else:
            self.pontos_colisao_locais = pontos_colisao_locais

        self.cor = cor
        self.cor_borda = (0, 0, 0)

        self.x = 0.0
        self.y = 0.0

        self.vel_x = 0.0
        self.vel_y = 0.0

        self.ativa = True

    # atualiza a posição (x, y) somando o deslocamento baseado na velocidade.
    def atualizar(self, dt):
        self.x += self.vel_x * dt                       # dt = tempo decorrido desde o último frame.
        self.y += self.vel_y * dt                       # garante que o objeto se mova na mesma velocidade, independente da taxa de quadros por segundo (FPS) em diferentes computadores.

    def obter_matriz_mundo(self):
        T = translacao(self.x,self.y)
        return T

    # desenhar o objeto na posição correta da tela (self.x, self.y), transformando os pontos locais em coordenadas do mundo.
    def obter_pontos_mundo(self):    
        M = self.obter_matriz_mundo()
        return aplica_transformacao(M,self.pontos_locais)

    def obter_pontos_colisao_mundo(self):
        M = self.obter_matriz_mundo()
        return aplica_transformacao(M,self.pontos_colisao_locais)   

    def desenhar(self, superficie):
        pontos_mundo = self.obter_pontos_mundo()            # calcula onde os pontos estão no mundo.
        scanline_fill(superficie, pontos_mundo, self.cor)   # pinta o interior do polígono
        if self.cor_borda:                                  # se houver uma cor de borda definida, desenha o contorno por cima.
            desenhar_poligono(superficie, pontos_mundo, self.cor_borda)



#=================================================
# CLASSES FILHAS
#=================================================

class Jogador(Entidade):

    def __init__(self, textura_parado, texturas_corrida):

        # -------------------------
        # Retângulo visual
        # -------------------------
        pontos_visuais = [
            (-30, -70),
            (30, -70),
            (30, 70),
            (-30, 70)
        ]

        # -------------------------
        # Retângulo de colisão
        # -------------------------
        pontos_colisao = [
            (-25, -70),
            (25, -70),
            (25, 70),
            (-25, 70)
        ]

        super().__init__(pontos_visuais, (255, 255, 255), pontos_colisao)

        self.cor_borda = None

        self.vel_movimento = 400.0

        self.textura_parado = textura_parado
        self.texturas_corrida = texturas_corrida

        self.indice_frame = 0
        self.tempo_animacao = 0.0
        self.intervalo_frame = 0.08

        self.direcao = 1
        self.movendo = False

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

            # Avança o tempo da animação
            self.tempo_animacao += dt

            if self.tempo_animacao >= self.intervalo_frame:

                self.tempo_animacao -= self.intervalo_frame

                self.indice_frame += 1

                # Volta para o primeiro frame
                if self.indice_frame >= len(self.texturas_corrida):
                    self.indice_frame = 0

        else:

            # Parado volta para o primeiro frame
            self.indice_frame = 0
            self.tempo_animacao = 0.0

    def desenhar(self, superficie):

        # Escolhe a imagem que será usada
        if self.movendo:
            imagem = self.texturas_corrida[self.indice_frame]
        else:
            imagem = self.textura_parado

        pontos_mundo = self.obter_pontos_mundo()

        # Mapeamento normal da textura
        if self.direcao == 1:

            vertices_texturizados = [
                (pontos_mundo[0], (0.0, 0.0)),
                (pontos_mundo[1], (1.0, 0.0)),
                (pontos_mundo[2], (1.0, 1.0)),
                (pontos_mundo[3], (0.0, 1.0))
            ]

        # Mapeamento invertido horizontalmente
        else:

            vertices_texturizados = [
                (pontos_mundo[0], (1.0, 0.0)),
                (pontos_mundo[1], (0.0, 0.0)),
                (pontos_mundo[2], (0.0, 1.0)),
                (pontos_mundo[3], (1.0, 1.0))
            ]

        scanline_textura(superficie, vertices_texturizados, imagem, usar_alpha=True)

class Pasta(Entidade):
    def __init__(self, imagem_textura):

        # -------------------------
        # Retângulo visual
        # -------------------------
        pontos_visuais = [
            (-15, -15),
            (15, -15),
            (15, 15),
            (-15, 15)
        ]

        # -------------------------
        # Retângulo de colisão
        # -------------------------
        pontos_colisao = [
            (-10, -13),
            (10, -13),
            (10, 13),
            (-10, 13)
        ]

        super().__init__(pontos_visuais, (240, 230, 180), pontos_colisao)

        self.imagem_textura = imagem_textura

        self.angulo = 0.0
        self.fator_escala = 1.0

        self.tempo_uma_volta = 100.0
        self.velocidade_rotacao = (360.0 / self.tempo_uma_volta)

    def atualizar(self, dt):
        super().atualizar(dt)
        # Atualiza a rotação contínua enquanto cai
        self.angulo = (self.angulo + self.velocidade_rotacao * dt) % 360

    def obter_matriz_mundo(self):
        S = escala(self.fator_escala, self.fator_escala)
        R = rotacao(self.angulo)
        T = translacao(self.x, self.y)

        return multiplica_matrizes(T, multiplica_matrizes(R, S))

    def desenhar(self, superficie):

        pontos_mundo = self.obter_pontos_mundo()

        vertices_texturizados = [
            (pontos_mundo[0], (0.0, 0.0)),
            (pontos_mundo[1], (1.0, 0.0)),
            (pontos_mundo[2], (1.0, 1.0)),
            (pontos_mundo[3], (0.0, 1.0))
        ]

        scanline_textura(superficie, vertices_texturizados, self.imagem_textura, usar_alpha=True)

class CocoPombo(Entidade):

    def __init__(self, imagem_textura):

        # -------------------------
        # Retângulo visual
        # -------------------------
        pontos_visuais = [
            (-10, -10),
            (10, -10),
            (10, 10),
            (-10, 10)
        ]

        # -------------------------
        # Retângulo de colisão
        # -------------------------
        pontos_colisao = [
            (-7, -7),
            (7, -7),
            (7, 7),
            (-7, 7)
        ]

        super().__init__(pontos_visuais, (255, 255, 255), pontos_colisao)

        self.imagem_textura = imagem_textura
        self.tempo = 0.0

    def desenhar(self, superficie):

        pontos_mundo = self.obter_pontos_mundo()

        vertices_texturizados = [
            (pontos_mundo[0], (0.0, 0.0)),
            (pontos_mundo[1], (1.0, 0.0)),
            (pontos_mundo[2], (1.0, 1.0)),
            (pontos_mundo[3], (0.0, 1.0))
        ]

        scanline_textura(superficie, vertices_texturizados, self.imagem_textura, usar_alpha=True)

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt