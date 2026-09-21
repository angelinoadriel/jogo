from engine.transformacoes import translacao, aplica_transformacao
from engine.rasterizacao import retangulo_para_poligono

class Entidade:
    def __init__(self, pontos, cor):
        self.pontos_locais = pontos
        self.cor = cor
        self.x = 0.0
        self.y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.ativa = True

    def atualizar(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def obter_pontos_mundo(self):
        # Cria a matriz de translação para a posição atual da entidade
        T = translacao(self.x, self.y)
        return aplica_transformacao(T, self.pontos_locais)

class Jogador(Entidade):
    def __init__(self):
        # Forma do jogador (um retângulo que representa o personagem de camisa)
        pontos = retangulo_para_poligono(-15, -30, 30, 60)
        super().__init__(pontos, (50, 150, 200)) # Azul claro (Camisa limpa)
        self.vel_movimento = 400.0

class Pasta(Entidade):
    def __init__(self):
        # Forma da pasta (retângulo deitado)
        pontos = retangulo_para_poligono(-12, -8, 24, 16)
        super().__init__(pontos, (240, 230, 180)) # Bege/Amarelo claro

class CocoPombo(Entidade):
    def __init__(self):
        # Forma do cocô (um triângulo)
        pontos = [(0, -8), (-8, 8), (8, 8)]
        super().__init__(pontos, (255, 255, 255)) # Branco