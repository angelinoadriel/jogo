import pygame

from config.caminhos import FONTE_PRINCIPAL
from engine.rasterizacao import (
    scanline_fill,
    desenhar_poligono
)
from config.constantes import (
    TXT_DE_HISTORIA_MANUAL,
    LARGURA_PAINEL_HISTORIA,
    ALTURA_PAINEL_HISTORIA,
    MSG_VOLTAR_AO_MENU
)
from estados.estado import Estado
from estados.menu import EstadoMenu
from ui import Painel
from engine.recorte import cohen_sutherland
from config.cores import Cores


class EstadoHistoria_Manual(Estado):

    def __init__(self, jogo):

        super().__init__(jogo)

        # =================================================
        # TEXTO
        # =================================================
        self.texto_conteudo = TXT_DE_HISTORIA_MANUAL

        # =================================================
        # FONTES
        # =================================================
        self.fonte_titulo = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 45))
        self.fonte_texto = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 20))
        self.fonte_msg_voltar_menu = (self.jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 24))


        # =================================================
        # DIMENSÕES DO PAINEL
        # =================================================
        self.largura_painel = LARGURA_PAINEL_HISTORIA
        self.altura_painel = ALTURA_PAINEL_HISTORIA

        self.x_painel = (self.jogo.largura // 2 - self.largura_painel // 2)
        self.y_painel = 155
        self.painel = Painel(self.x_painel, self.y_painel, self.largura_painel, self.altura_painel)

        # =================================================
        # ÁREA DO CONTEÚDO
        # =================================================
        self.margem_conteudo = 20
        self.espacamento_linha = 24
        self.largura_barra = 12

        self.x_conteudo = (self.x_painel + self.margem_conteudo)
        self.y_conteudo = (self.y_painel + self.margem_conteudo)

        self.largura_conteudo = (self.largura_painel - self.margem_conteudo * 2 - self.largura_barra - 8)
        self.altura_conteudo = (self.altura_painel - self.margem_conteudo * 2)

        self.linhas = self.quebrar_texto(self.texto_conteudo, self.fonte_texto, self.largura_conteudo)

        self.textos_renderizados = []
        for linha in self.linhas:
            if linha == "":
                self.textos_renderizados.append(None)
                continue
            texto_renderizado = self.fonte_texto.render(linha, True, Cores.TEXTO)
            self.textos_renderizados.append(texto_renderizado)

        self.altura_total = (len(self.linhas) * self.espacamento_linha)

        self.max_scroll = max(0, self.altura_total - self.altura_conteudo)

        # =================================================
        # ROLAGEM
        # =================================================
        self.scroll = 0
        self.arrastando_barra = False


    def limitar_scroll(self):
        self.scroll = max(0, min(self.scroll, self.max_scroll))


    # =====================================================
    # EVENTOS
    # =====================================================
    def processar_eventos(self, entrada):

        for evento in entrada.eventos:

            # -------------------------------------------------
            # ROLAGEM DO MOUSE
            # -------------------------------------------------

            if evento.type == pygame.MOUSEWHEEL:
                self.scroll -= evento.y * 30
                self.limitar_scroll()

            # -------------------------------------------------
            # CLIQUE DO MOUSE
            # -------------------------------------------------
            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:
                    mouse_x, mouse_y = evento.pos

                    x_barra = (self.x_painel + self.largura_painel - self.largura_barra - 8)
                    y_barra = (self.y_painel + 20)

                    largura_conteudo = (self.largura_painel - 20 * 2 - self.largura_barra - 8)
                    altura_conteudo = (self.altura_painel - 40)

                    if (
                        x_barra <= mouse_x
                        <= x_barra + self.largura_barra
                        and
                        y_barra <= mouse_y
                        <= y_barra + altura_conteudo
                    ):

                        self.arrastando_barra = True

            # -------------------------------------------------
            # ARRASTAR BARRA
            # -------------------------------------------------
            if evento.type == pygame.MOUSEMOTION:
                if self.arrastando_barra:
                    mouse_y = evento.pos[1]
                    deslocamento = (mouse_y - self.y_conteudo)

                    if self.altura_conteudo > 0:
                        porcentagem = (deslocamento / self.altura_conteudo)
                        porcentagem = max(0.0, min(1.0, porcentagem))
                        
                        self.scroll = int(porcentagem * self.max_scroll)

                    self.limitar_scroll()

            # -------------------------------------------------
            # SOLTAR BARRA
            # -------------------------------------------------
            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.arrastando_barra = False

        # =====================================================
        # ENTER
        # =====================================================
        if entrada.teclas[pygame.K_RETURN]:
            self.jogo.mudar_estado(EstadoMenu(self.jogo))
            return   


    # =====================================================
    # ATUALIZAÇÃO
    # =====================================================
    def atualizar(self, dt):
        pass


    # =====================================================
    # QUEBRA DE TEXTO
    # =====================================================
    def quebrar_texto(self, texto, fonte, largura_maxima):

        linhas_finais = []

        paragrafos = texto.split("\n")

        for paragrafo in paragrafos:

            # Linha vazia continua sendo linha vazia
            if paragrafo.strip() == "":
                linhas_finais.append("")
                continue

            palavras = paragrafo.split(" ")

            linha_atual = ""

            for palavra in palavras:

                teste = (linha_atual + " " + palavra if linha_atual else palavra)

                largura = fonte.size(teste)[0]

                if largura <= largura_maxima:
                    linha_atual = teste

                else:

                    if linha_atual:
                        linhas_finais.append(linha_atual)

                    linha_atual = palavra

            if linha_atual:

                linhas_finais.append(linha_atual)

        return linhas_finais


    
    def linha_dentro_da_area(self, y, altura_linha):
        y_superior = y
        y_inferior = y + altura_linha

        aceito_superior, _, _, _, _ = cohen_sutherland(
            self.x_conteudo,
            y_superior,
            self.x_conteudo + self.largura_conteudo,
            y_superior,
            self.x_conteudo,
            self.y_conteudo,
            self.x_conteudo + self.largura_conteudo,
            self.y_conteudo + self.altura_conteudo
        )

        aceito_inferior, _, _, _, _ = cohen_sutherland(
            self.x_conteudo,
            y_inferior,
            self.x_conteudo + self.largura_conteudo,
            y_inferior,
            self.x_conteudo,
            self.y_conteudo,
            self.x_conteudo + self.largura_conteudo,
            self.y_conteudo + self.altura_conteudo
        )

        return aceito_superior and aceito_inferior



    # =====================================================
    # CONTEÚDO ROLÁVEL
    # =====================================================
    def desenhar_conteudo_rolavel(self, tela):
        y_texto = self.y_conteudo - self.scroll

        for indice, texto_renderizado in enumerate(self.textos_renderizados):
            if texto_renderizado is None:
                y_texto += self.espacamento_linha
                continue

            if self.linha_dentro_da_area(y_texto, self.espacamento_linha):
                tela.blit(texto_renderizado, (self.x_conteudo, y_texto))

            y_texto += self.espacamento_linha

        # =================================================
        # BARRA DE ROLAGEM
        # =================================================
        if self.max_scroll > 0:

            x_barra = (self.x_painel + self.largura_painel - self.largura_barra - 8)

            y_barra = self.y_conteudo
            altura_area = self.altura_conteudo

            pontos_fundo = [
                (x_barra, y_barra),
                (x_barra + self.largura_barra, y_barra),
                (x_barra + self.largura_barra, y_barra + altura_area),
                (x_barra, y_barra + altura_area)
            ]

            scanline_fill(tela, pontos_fundo, Cores.BARRA)
            porcentagem = (self.scroll / self.max_scroll)

            altura_barrinha = max(40, int(altura_area * self.altura_conteudo / self.altura_total))
            y_barrinha = (y_barra + (altura_area - altura_barrinha) * porcentagem)

            pontos_barrinha = [
                (x_barra, y_barrinha),
                (x_barra + self.largura_barra, y_barrinha),
                (x_barra + self.largura_barra, y_barrinha + altura_barrinha),
                (x_barra, y_barrinha + altura_barrinha)
            ]

            scanline_fill(tela, pontos_barrinha, Cores.BARRINHA)
            desenhar_poligono(tela, pontos_barrinha, Cores.BRANCO)


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, tela):

        self.jogo.cenario_menu.desenhar(tela)

        # =================================================
        # TÍTULO
        # =================================================
        titulo = self.fonte_titulo.render("HISTÓRIA / MANUAL", True, Cores.BRANCO)
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 110))

        # =================================================
        # PAINEL
        # =================================================
        self.painel.desenhar(tela)

        # =================================================
        # CONTEÚDO
        # =================================================
        self.desenhar_conteudo_rolavel(tela)

        mensagem_enter = self.fonte_msg_voltar_menu.render(MSG_VOLTAR_AO_MENU, True, Cores.BRANCO)
        tela.blit(mensagem_enter, (self.jogo.largura // 2 - mensagem_enter.get_width() // 2, self.jogo.altura - 25))