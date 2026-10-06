import pygame


class Entrada:

    def __init__(self):

        self.eventos = []
        self.teclas = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)
        self.clicou = False


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self):

        self.eventos = pygame.event.get()
        self.clicou = False

        for evento in self.eventos:
            if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                self.clicou = True

        self.teclas = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()