import pygame

from config.constantes import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS_ALVO,
    NOME_JANELA
)
from core.recursos import GerenciadorRecursos
from core.entrada import Entrada
from cenario import CenarioMenu
from estados import EstadoMenu


class Jogo:
    
    # construtor
    def __init__(self, largura=LARGURA_TELA, altura=ALTURA_TELA):       # passa a largura e altura com valores fixos
        pygame.init()                                                   # inicializa o pygame
        self.largura = largura
        self.altura = altura

        self.tela = pygame.display.set_mode((self.largura, self.altura))    # cria a tela
        pygame.display.set_caption(NOME_JANELA)                      # título da janela
        
        self.clock = pygame.time.Clock()
        self.rodando = True

        # Recursos compartilhados
        self.recursos = GerenciadorRecursos()

        self.entrada = Entrada()

        # Cenário compartilhado do menu
        self.cenario_menu = CenarioMenu(self)
        
        # Variáveis globais de configuração
        self.dificuldade_atual = 2                          # 1: Fácil, 2: Normal, 3: Difícil
        self.estado_atual = EstadoMenu(self)                # Inicia no estado de Menu
        self.estado_atual.entrar()

    
    def mudar_estado(self, novo_estado):

        # Estado atual está sendo encerrado
        if self.estado_atual is not None:
            self.estado_atual.sair()

        # Troca o estado
        self.estado_atual = novo_estado

        # Novo estado está sendo iniciado
        if self.estado_atual is not None:
            self.estado_atual.entrar()


    def executar(self):
        while self.rodando:            
            dt = self.clock.tick(FPS_ALVO) / 1000.0
            
            self.entrada.atualizar()

            for evento in self.entrada.eventos:
                if evento.type == pygame.QUIT:
                    self.rodando = False

            self.estado_atual.processar_eventos(self.entrada)
            self.estado_atual.atualizar(dt)
            self.estado_atual.desenhar(self.tela)
            
            pygame.display.flip()

        pygame.quit()
