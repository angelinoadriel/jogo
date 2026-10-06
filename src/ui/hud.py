from engine.rasterizacao import (
    scanline_fill,
    desenhar_poligono,
    desenhar_linha,
)
from engine.textura import scanline_textura
from config.cores import Cores
from config.caminhos import FONTE_PRINCIPAL
from config.constantes import (
    HUD_VIDAS_X,
    HUD_VIDAS_Y,
    HUD_VIDAS_LARGURA,
    HUD_VIDAS_ALTURA,
    HUD_PASTAS_X,
    HUD_PASTAS_Y,
    HUD_PASTAS_LARGURA,
    HUD_PASTAS_ALTURA,
    HUD_CAMISA_LARGURA,
    HUD_CAMISA_ALTURA,
    HUD_CAMISA_ESPACAMENTO,
    HUD_BARRA_MARGEM,
    HUD_BARRA_ALTURA,
    HUD_FPS_MARGEM_X,
    HUD_FPS_MARGEM_Y
)


class HUD:

    def __init__(self, jogo, imagem_camisa):

        self.jogo = jogo
        self.imagem_camisa = imagem_camisa

        # =================================================
        # FONTES
        # =================================================
        self.fonte = (jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 24))
        self.fonte_pastas_titulo = (jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 16))
        self.fonte_pastas_numero = (jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 13))
        self.fonte_pastas_percentual = (jogo.recursos.carregar_fonte(FONTE_PRINCIPAL, 14))


    # =====================================================
    # CAMISA DE VIDA
    # =====================================================
    def desenhar_camisa_vida(self, tela, x, y, perdida=False):

        vertices = [
            ((x, y), (0.0, 0.0)),
            ((x + HUD_CAMISA_LARGURA, y), (1.0, 0.0)),
            ((x + HUD_CAMISA_LARGURA, y + HUD_CAMISA_ALTURA), (1.0, 1.0)),
            ((x, y + HUD_CAMISA_ALTURA), (0.0, 1.0))
        ]
        scanline_textura(tela, vertices, self.imagem_camisa, usar_alpha=True)

        if perdida:
            margem = 8

            x1 = x + margem
            y1 = y + margem
            x2 = (x + HUD_CAMISA_LARGURA - margem)
            y2 = (y + HUD_CAMISA_ALTURA - margem)
            
            desenhar_linha(tela, x1, y1, x2, y2, Cores.VIDA_PERDIDA)
            desenhar_linha(tela, x2, y1, x1, y2, Cores.VIDA_PERDIDA)


    # =====================================================
    # PAINEL DE VIDAS
    # =====================================================
    def desenhar_vidas(self, tela, vidas, vidas_maximas):

        painel = [
            (HUD_VIDAS_X, HUD_VIDAS_Y),
            (HUD_VIDAS_X + HUD_VIDAS_LARGURA, HUD_VIDAS_Y),
            (HUD_VIDAS_X + HUD_VIDAS_LARGURA, HUD_VIDAS_Y + HUD_VIDAS_ALTURA),
            (HUD_VIDAS_X, HUD_VIDAS_Y + HUD_VIDAS_ALTURA)
        ]
        scanline_fill(tela, painel, Cores.HUD_FUNDO)
        desenhar_poligono(tela,painel, Cores.HUD_BORDA)
        
        largura_total = (vidas_maximas * HUD_CAMISA_LARGURA + (vidas_maximas - 1) * HUD_CAMISA_ESPACAMENTO)
        x_inicial = (HUD_VIDAS_X + (HUD_VIDAS_LARGURA - largura_total) // 2)
        y_inicial = (HUD_VIDAS_Y + (HUD_VIDAS_ALTURA - HUD_CAMISA_ALTURA) // 2)

        for i in range(vidas_maximas):

            x = (x_inicial + i * (HUD_CAMISA_LARGURA + HUD_CAMISA_ESPACAMENTO))
            vida_perdida = i >= vidas
            self.desenhar_camisa_vida(tela, x, y_inicial, vida_perdida)


    # =====================================================
    # PAINEL DE PASTAS
    # =====================================================
    def desenhar_progresso(self, tela, pastas_coletadas, max_pastas):

        painel = [
            (HUD_PASTAS_X, HUD_PASTAS_Y),
            (HUD_PASTAS_X + HUD_PASTAS_LARGURA, HUD_PASTAS_Y),
            (HUD_PASTAS_X + HUD_PASTAS_LARGURA, HUD_PASTAS_Y + HUD_PASTAS_ALTURA),
            (HUD_PASTAS_X, HUD_PASTAS_Y + HUD_PASTAS_ALTURA)
        ]
        scanline_fill(tela, painel, Cores.HUD_FUNDO)
        desenhar_poligono(tela, painel, Cores.HUD_BORDA)

        # =================================================
        # TÍTULO
        # =================================================
        txt_titulo = (self.fonte_pastas_titulo.render("PASTAS RESGATADAS", True, Cores.HUD_TEXTO))
        tela.blit(txt_titulo, txt_titulo.get_rect(center=(HUD_PASTAS_X + HUD_PASTAS_LARGURA // 2, HUD_PASTAS_Y + 15)))

        # =================================================
        # CONTADOR
        # =================================================
        txt_contador = (self.fonte_pastas_numero.render(f"{pastas_coletadas} / {max_pastas}", True, Cores.HUD_TEXTO))
        tela.blit(txt_contador, txt_contador.get_rect(center=(HUD_PASTAS_X + HUD_PASTAS_LARGURA // 2, HUD_PASTAS_Y + 38)))

        # =================================================
        # BARRA
        # =================================================
        barra_x = (HUD_PASTAS_X + HUD_BARRA_MARGEM)
        barra_y = (HUD_PASTAS_Y + 53)
        barra_largura = (HUD_PASTAS_LARGURA - HUD_BARRA_MARGEM * 2)

        pontos_barra = [
            (barra_x, barra_y),
            (barra_x + barra_largura, barra_y),
            (barra_x + barra_largura, barra_y + HUD_BARRA_ALTURA),
            (barra_x, barra_y + HUD_BARRA_ALTURA)
        ]
        scanline_fill(tela, pontos_barra, Cores.HUD_BARRA_FUNDO)
        desenhar_poligono(tela, pontos_barra, Cores.HUD_BORDA)

        # =================================================
        # PROGRESSO
        # =================================================
        progresso = (pastas_coletadas / max_pastas if max_pastas > 0 else 0)

        largura_preenchida = int(barra_largura * progresso)

        if largura_preenchida > 0:
            pontos_progresso = [
                (barra_x, barra_y),
                (barra_x + largura_preenchida, barra_y),
                (barra_x + largura_preenchida, barra_y + HUD_BARRA_ALTURA),
                (barra_x, barra_y + HUD_BARRA_ALTURA)
            ]
            scanline_fill(tela, pontos_progresso, Cores.HUD_PROGRESSO)

        # =================================================
        # PORCENTAGEM
        # =================================================
        percentual = int(progresso * 100)

        txt_percentual = (self.fonte_pastas_percentual.render(f"{percentual}%", True, Cores.HUD_TEXTO))
        tela.blit(txt_percentual, txt_percentual.get_rect(center= (HUD_PASTAS_X + HUD_PASTAS_LARGURA // 2, HUD_PASTAS_Y + 72)))


    # =====================================================
    # FPS
    # =====================================================
    def desenhar_fps(self, tela):

        fps = int(self.jogo.clock.get_fps())

        if fps >= 50:
            cor_fps = Cores.FPS_BOM
        else:
            cor_fps = Cores.FPS_ATENCAO

        txt_fps = self.fonte.render(f"FPS: {fps}", True, cor_fps)
        tela.blit(txt_fps, (HUD_PASTAS_X + HUD_FPS_MARGEM_X, HUD_PASTAS_Y + HUD_PASTAS_ALTURA + HUD_FPS_MARGEM_Y))


    # =====================================================
    # DESENHO COMPLETO
    # =====================================================
    def desenhar(self, tela, vidas, vidas_maximas, pastas_coletadas, max_pastas):

        self.desenhar_vidas(tela, vidas, vidas_maximas)
        self.desenhar_progresso(tela, pastas_coletadas, max_pastas)
        self.desenhar_fps(tela)