import pygame

from config.caminhos import FONTE_PRINCIPAL
from estados.estado import Estado
from ui import Painel
from config.cores import Cores
from config.constantes import (
    LARGURA_PAINEL_FIM,
    ALTURA_PAINEL_FIM,
    MSG_VOLTAR_AO_MENU
)



class EstadoFim(Estado):

    def __init__(self, jogo, mensagem):

        super().__init__(jogo)

        self.mensagem = mensagem

        # =================================================
        # FONTES
        # =================================================
        self.fonte_titulo = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 48))
        self.fonte_mensagem = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 25))
        self.fonte_pequena = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 22))

        # =================================================
        # PAINEL
        # =================================================
        self.largura_painel = LARGURA_PAINEL_FIM
        self.altura_painel = ALTURA_PAINEL_FIM

        self.x_painel = (self.jogo.largura // 2 - self.largura_painel // 2)
        self.y_painel = (self.jogo.altura // 2 - self.altura_painel // 2)
        
        self.painel = Painel(self.x_painel, self.y_painel, self.largura_painel, self.altura_painel)


    # =====================================================
    # EVENTOS
    # =====================================================
    def processar_eventos(self, entrada):
        # ENTER
        if entrada.teclas[pygame.K_RETURN]:
            from estados.menu import EstadoMenu
            self.jogo.mudar_estado(EstadoMenu(self.jogo))
            return

    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        pass


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, tela):

        # -------------------------------------------------
        # CENÁRIO
        # -------------------------------------------------
        self.jogo.cenario_menu.desenhar(tela)

        # -------------------------------------------------
        # PAINEL
        # -------------------------------------------------
        self.painel.desenhar(tela)

        # -------------------------------------------------
        # TÍTULO
        # -------------------------------------------------
        txt_titulo = self.fonte_titulo.render("FIM DE JOGO", True, Cores.TEXTO)
        tela.blit(txt_titulo, (self.jogo.largura // 2 - txt_titulo.get_width() // 2, self.y_painel + 30))

        # -------------------------------------------------
        # MENSAGEM
        # -------------------------------------------------
        txt_res = self.fonte_mensagem.render(self.mensagem, True, Cores.TXT_MENSAGEM_FINAL)
        tela.blit(txt_res, (self.jogo.largura // 2 - txt_res.get_width() // 2, self.y_painel + 105))

        # -------------------------------------------------
        # CONTROLE
        # -------------------------------------------------
        txt_enter = self.fonte_pequena.render(MSG_VOLTAR_AO_MENU, True, Cores.TXT_VOLTAR_AO_MENU)
        tela.blit(txt_enter, (self.jogo.largura // 2 - txt_enter.get_width() // 2, self.y_painel + 230))