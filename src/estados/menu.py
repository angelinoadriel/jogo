import pygame

from config.constantes import (
    LARGURA_BOTAO_MENU,
    ALTURA_BOTAO_MENU,
    Y_INICIAL_BOTOES_MENU,
    ESPACAMENTO_BOTOES_MENU,
    NOME_JOGO
)
from config.caminhos import FONTE_PRINCIPAL
from config.cores import Cores
from ui import Botao
from estados.estado import Estado



# =========================================================
# ESTADO MENU
# =========================================================
class EstadoMenu(Estado):

    def __init__(self, jogo):

        super().__init__(jogo)

        # -------------------------------------------------
        # FONTES
        # -------------------------------------------------
        self.fonte_botoes = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 26))
        self.fonte_titulo = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 45))
        
        # -------------------------------------------------
        # OPÇÕES
        # -------------------------------------------------
        self.opcoes = ["INICIAR", "DIFICULDADE", "HISTÓRIA / MANUAL"]

        # -------------------------------------------------
        # BOTÕES
        # -------------------------------------------------
        self.botoes = self._criar_botoes()



    def _criar_botoes(self):
        botoes = []
        centro_x = self.jogo.largura // 2
    
        for i, texto in enumerate(self.opcoes):
    
            centro_y = (Y_INICIAL_BOTOES_MENU + i * ESPACAMENTO_BOTOES_MENU)
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

            # ---------------------------------------------
            # INICIAR
            # ---------------------------------------------
            if i == 0:
                from estados.jogando import EstadoJogando
                self.jogo.mudar_estado(EstadoJogando(self.jogo))

            # ---------------------------------------------
            # DIFICULDADE
            # ---------------------------------------------
            elif i == 1:
                from estados.dificuldade import EstadoDificuldade
                self.jogo.mudar_estado(EstadoDificuldade(self.jogo))

            # ---------------------------------------------
            # HISTÓRIA / MANUAL
            # ---------------------------------------------
            elif i == 2:
                from estados.historia import EstadoHistoria_Manual
                self.jogo.mudar_estado(EstadoHistoria_Manual(self.jogo))


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
        titulo = self.fonte_titulo.render(NOME_JOGO, True, Cores.BRANCO)
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 150))

        # =================================================
        # BOTÕES
        # =================================================
        mouse_pos = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.desenhar(tela, mouse_pos)