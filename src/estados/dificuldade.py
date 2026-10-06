import pygame

from config.caminhos import FONTE_PRINCIPAL
from engine.rasterizacao import (
    desenhar_circulo,
    boundary_fill
)
from config.constantes import (
    LARGURA_BOTAO_MENU,
    ALTURA_BOTAO_MENU,
    Y_INICIAL_BOTOES_DIFICULDADE,
    ESPACAMENTO_BOTOES_DIFICULDADE
)
from estados.estado import Estado
from ui import Botao
from config.cores import Cores


class EstadoDificuldade(Estado):

    def __init__(self, jogo):

        super().__init__(jogo)

        # =================================================
        # FONTES
        # =================================================
        self.fonte_botoes = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 26))
        self.fonte_titulo = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 45))

        # =================================================
        # OPÇÕES
        # =================================================
        self.opcoes = ["FÁCIL", "NORMAL", "DIFÍCIL", "VOLTAR"]

        # =================================================
        # BOTÕES
        # =================================================
        self.botoes = self._criar_botoes()


    def _criar_botoes(self):
        botoes = []
        centro_x = self.jogo.largura // 2
    
        for i, texto in enumerate(self.opcoes):
            centro_y = (Y_INICIAL_BOTOES_DIFICULDADE + i * ESPACAMENTO_BOTOES_DIFICULDADE)
            botao = Botao(centro_x, centro_y, LARGURA_BOTAO_MENU, ALTURA_BOTAO_MENU, texto, self.fonte_botoes)
            botoes.append(botao)
    
        return botoes

    
    # =====================================================
    # EVENTOS
    # =====================================================
    def processar_eventos(self, entrada):

        if not entrada.clicou:
            return

        for i, botao in enumerate(self.botoes):

            if not botao.contem_ponto(entrada.mouse_pos):
                continue

            from estados.menu import EstadoMenu
            # ---------------------------------------------
            # FÁCIL
            # ---------------------------------------------
            if i == 0:
                self.jogo.dificuldade_atual = 1
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

            # ---------------------------------------------
            # NORMAL
            # ---------------------------------------------
            elif i == 1:
                self.jogo.dificuldade_atual = 2
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

            # ---------------------------------------------
            # DIFÍCIL
            # ---------------------------------------------
            elif i == 2:
                self.jogo.dificuldade_atual = 3
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

            # ---------------------------------------------
            # VOLTAR
            # ---------------------------------------------
            elif i == 3:
                self.jogo.mudar_estado(EstadoMenu(self.jogo))


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        pass


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, tela):

        self.jogo.cenario_menu.desenhar(tela)

        # =================================================
        # TÍTULO
        # =================================================
        titulo = self.fonte_titulo.render("DIFICULDADE", True, Cores.BRANCO)
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 120))

        # =================================================
        # BOTÕES
        # =================================================
        mouse_pos = pygame.mouse.get_pos()

        for i, botao in enumerate(self.botoes):
            botao.desenhar(tela, mouse_pos)

            # ---------------------------------------------
            # INDICADOR DA DIFICULDADE
            # ---------------------------------------------
            selecionado = (
                (i == 0 and self.jogo.dificuldade_atual == 1)
                or
                (i == 1 and self.jogo.dificuldade_atual == 2)
                or
                (i == 2 and self.jogo.dificuldade_atual == 3)
            )

            if selecionado:
                x_ini, _, x_fim, _ = (botao.obter_limites())

                x_bolinha = (x_fim - 25)
                y_bolinha = (botao.centro_y)
                desenhar_circulo(tela, x_bolinha, y_bolinha, 8, Cores.VIDA_ATIVA)
                boundary_fill(tela, x_bolinha, y_bolinha, Cores.VIDA_ATIVA, Cores.VIDA_ATIVA)