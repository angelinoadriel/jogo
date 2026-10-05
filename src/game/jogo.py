import pygame
from game.estados import EstadoMenu

class Jogo:
    
    # construtor
    def __init__(self, largura=800, altura=600):                        # passa a largura e altura com valores fixos
        pygame.init()                                                   # inicializa o pygame
        self.largura = largura
        self.altura = altura
        
        self.tela = pygame.display.set_mode((self.largura, self.altura))    # cria a tela
        pygame.display.set_caption("Desastre no NC2A")                      # título da janela
        
        self.clock = pygame.time.Clock()
        self.rodando = True
        
        # Variáveis globais de configuração
        self.dificuldade_atual = 2                          # 1: Fácil, 2: Normal, 3: Difícil
        self.estado_atual = EstadoMenu(self)                # Inicia no estado de Menu
    
    def mudar_estado(self, novo_estado):
        self.estado_atual = novo_estado

    def executar(self):
        while self.rodando:            
            dt = self.clock.tick(60)/1000.0
            mouse_pos = pygame.mouse.get_pos()
            clicou = False
            eventos = pygame.event.get()

            for evento in eventos:
                
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    clicou = True

            teclas = pygame.key.get_pressed()

            # Processamento delegado ao estado ativo
            self.estado_atual.processar_eventos(eventos, teclas, mouse_pos, clicou)
            self.estado_atual.atualizar(dt)
            self.estado_atual.desenhar(self.tela)
            pygame.display.flip()

        pygame.quit()
