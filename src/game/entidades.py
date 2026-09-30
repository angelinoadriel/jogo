from engine.transformacoes import translacao, aplica_transformacao, escala, rotacao, multiplica_matrizes
from engine.rasterizacao import scanline_fill, desenhar_poligono




class Entidade:

    # construtor
    def __init__(self, pontos_locais, cor):
        self.pontos_locais = pontos_locais              # definem a forma do objeto ao redor do centro (0,0)
        self.cor = cor                                  # Cor de preenchimento
        self.cor_borda = (0, 0, 0)                      # Cor do contorno (padrão: preto)
        self.x = 0.0                                    # Posição X atual no mundo
        self.y = 0.0                                    # Posição Y atual no mundo
        self.vel_x = 0.0                                # Velocidade de movimento no eixo X
        self.vel_y = 0.0                                # Velocidade de movimento no eixo Y
        self.ativa = True                               # Flag para saber se o objeto ainda existe/está ativo



    # atualiza a posição (x, y) somando o deslocamento baseado na velocidade.
    def atualizar(self, dt):
        self.x += self.vel_x * dt                       # dt = tempo decorrido desde o último frame.
        self.y += self.vel_y * dt                       # garante que o objeto se mova na mesma velocidade, independente da taxa de quadros por segundo (FPS) em diferentes computadores.



    # desenhar o objeto na posição correta da tela (self.x, self.y), transformando os pontos locais em coordenadas do mundo.
    def obter_pontos_mundo(self):
        T = translacao(self.x, self.y)
        return aplica_transformacao(T, self.pontos_locais)



    def desenhar(self, superficie):
        pontos_mundo = self.obter_pontos_mundo()            # calcula onde os pontos estão no mundo.
        scanline_fill(superficie, pontos_mundo, self.cor)   # pinta o interior do polígono
        if self.cor_borda:                                  # se houver uma cor de borda definida, desenha o contorno por cima.
            desenhar_poligono(superficie, pontos_mundo, self.cor_borda)



#=================================================
# CLASSES FILHAS
#=================================================

class Jogador(Entidade):
    def __init__(self):
        pontos = [(-15, -30), (15, -30), (15, 30), (-15, 30)]   # forma de um retângulo 30x60
        
        super().__init__(pontos, (50, 150, 200))            # inicializa a entidade com esses pontos e a cor
        self.cor_borda = (255, 255, 255)                    # muda a cor da borda
        self.vel_movimento = 400.0          # atributo exclusivo de jogador


class Pasta(Entidade):
    def __init__(self):
        pontos = [(-12, -8), (6, -8), (6, 16), (-12, 16)]   # forma de um retângulo 18x24
        super().__init__(pontos, (240, 230, 180))
        self.angulo = 0.0
        self.fator_escala = 1.0
        self.tempo_uma_volta = 100.0
        self.velocidade_rotacao = 360.0 / self.tempo_uma_volta

    def atualizar(self, dt):
        super().atualizar(dt)
        # Atualiza a rotação contínua enquanto cai
        self.angulo = (self.angulo + self.velocidade_rotacao * dt) % 360

    def obter_pontos_mundo(self):
        # Matrizes de transformação
        S = escala(self.fator_escala, self.fator_escala)
        R = rotacao(self.angulo)
        T = translacao(self.x, self.y)

        # Combinação: T * R * S (Aplica Escala, depois Rotação, depois Translação)
        M = multiplica_matrizes(T, multiplica_matrizes(R, S))
        return aplica_transformacao(M, self.pontos_locais)

class CocoPombo(Entidade):
    def __init__(self):
        pontos = [(0, -8), (-8, 8), (8, 8)]             # forma de um triângulo
        super().__init__(pontos, (255, 255, 255))