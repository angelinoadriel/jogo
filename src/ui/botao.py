from engine.rasterizacao import (
    scanline_fill,
    desenhar_poligono
)
from config.cores import Cores


class Botao:

    def __init__(self, centro_x, centro_y, largura, altura, texto, fonte):

        # =================================================
        # GEOMETRIA
        # =================================================
        self.centro_x = centro_x
        self.centro_y = centro_y

        self.largura = largura
        self.altura = altura

        # =================================================
        # TEXTO
        # =================================================
        self.texto = texto
        self.fonte = fonte


    # =====================================================
    # POSIÇÃO
    # =====================================================
    def obter_limites(self):
        x_ini = (self.centro_x - self.largura // 2)
        y_ini = (self.centro_y - self.altura // 2)
        x_fim = (x_ini + self.largura)
        y_fim = (y_ini + self.altura)

        return (x_ini, y_ini, x_fim, y_fim)


    # =====================================================
    # COLISÃO COM O MOUSE
    # =====================================================
    def contem_ponto(self, posicao):
        mouse_x, mouse_y = posicao
        
        (x_ini, y_ini, x_fim, y_fim) = self.obter_limites()
        
        return (
            x_ini <= mouse_x <= x_fim
            and
            y_ini <= mouse_y <= y_fim
        )


    # =====================================================
    # DESENHO
    # =====================================================
    def desenhar(self, tela, mouse_pos):
        (x_ini, y_ini, x_fim, y_fim) = self.obter_limites()

        # -------------------------------------------------
        # HOVER
        # -------------------------------------------------
        hover = self.contem_ponto(mouse_pos)

        if hover:
            cor_fundo = Cores.BOTAO_HOVER
        else:
            cor_fundo = Cores.BOTAO

        # -------------------------------------------------
        # POLÍGONO DO BOTÃO
        # -------------------------------------------------
        pontos = [(x_ini, y_ini), (x_fim, y_ini), (x_fim, y_fim), (x_ini, y_fim)]

        # -------------------------------------------------
        # PREENCHIMENTO
        # -------------------------------------------------
        scanline_fill(tela, pontos, cor_fundo)

        # -------------------------------------------------
        # BORDA
        # -------------------------------------------------
        desenhar_poligono(tela, pontos, Cores.BRANCO)

        # -------------------------------------------------
        # TEXTO
        # -------------------------------------------------
        texto_renderizado = self.fonte.render(self.texto, True, Cores.TEXTO)
        tela.blit(texto_renderizado, texto_renderizado.get_rect(center=(self.centro_x, self.centro_y)))