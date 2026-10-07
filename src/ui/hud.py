import pygame
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

        # =================================================
        # CACHE DOS PAINÉIS
        # =================================================
        # Camada 1 (buffer_estatico): fundo e borda dos painéis e da barra.
        #   É desenhada UMA vez só (é a parte mais cara, milhares de pixels).
        # Camada 2 (buffer_hud): camada 1 + conteúdo que muda (camisas, textos,
        #   preenchimento da barra). Cada painel é refeito separadamente e só
        #   quando o seu valor muda.
        # Nos demais frames, apenas um blit copia o buffer para a tela.
        self.rect_vidas = pygame.Rect(HUD_VIDAS_X, HUD_VIDAS_Y, HUD_VIDAS_LARGURA + 1, HUD_VIDAS_ALTURA + 1)
        self.rect_pastas = pygame.Rect(HUD_PASTAS_X, HUD_PASTAS_Y, HUD_PASTAS_LARGURA + 1, HUD_PASTAS_ALTURA + 1)

        self.buffer_estatico = pygame.Surface((jogo.largura, jogo.altura)).convert()
        self.desenhar_fundo_vidas(self.buffer_estatico)
        self.desenhar_fundo_pastas(self.buffer_estatico)

        self.buffer_hud = self.buffer_estatico.copy()
        self.chave_vidas = None
        self.chave_pastas = None


    # =====================================================
    # FUNDOS ESTÁTICOS (desenhados uma única vez)
    # =====================================================
    def _pontos_painel_vidas(self):
        return [
            (HUD_VIDAS_X, HUD_VIDAS_Y),
            (HUD_VIDAS_X + HUD_VIDAS_LARGURA, HUD_VIDAS_Y),
            (HUD_VIDAS_X + HUD_VIDAS_LARGURA, HUD_VIDAS_Y + HUD_VIDAS_ALTURA),
            (HUD_VIDAS_X, HUD_VIDAS_Y + HUD_VIDAS_ALTURA)
        ]

    def _pontos_painel_pastas(self):
        return [
            (HUD_PASTAS_X, HUD_PASTAS_Y),
            (HUD_PASTAS_X + HUD_PASTAS_LARGURA, HUD_PASTAS_Y),
            (HUD_PASTAS_X + HUD_PASTAS_LARGURA, HUD_PASTAS_Y + HUD_PASTAS_ALTURA),
            (HUD_PASTAS_X, HUD_PASTAS_Y + HUD_PASTAS_ALTURA)
        ]

    def _pontos_barra(self):
        barra_x = (HUD_PASTAS_X + HUD_BARRA_MARGEM)
        barra_y = (HUD_PASTAS_Y + 53)
        barra_largura = (HUD_PASTAS_LARGURA - HUD_BARRA_MARGEM * 2)
        return [
            (barra_x, barra_y),
            (barra_x + barra_largura, barra_y),
            (barra_x + barra_largura, barra_y + HUD_BARRA_ALTURA),
            (barra_x, barra_y + HUD_BARRA_ALTURA)
        ]

    def desenhar_fundo_vidas(self, tela):
        painel = self._pontos_painel_vidas()
        scanline_fill(tela, painel, Cores.HUD_FUNDO)
        desenhar_poligono(tela, painel, Cores.HUD_BORDA)

    def desenhar_fundo_pastas(self, tela):
        painel = self._pontos_painel_pastas()
        scanline_fill(tela, painel, Cores.HUD_FUNDO)
        desenhar_poligono(tela, painel, Cores.HUD_BORDA)

        pontos_barra = self._pontos_barra()
        scanline_fill(tela, pontos_barra, Cores.HUD_BARRA_FUNDO)
        desenhar_poligono(tela, pontos_barra, Cores.HUD_BORDA)


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
    def desenhar_vidas(self, tela, vidas, vidas_maximas, fundo=True):

        painel = [
            (HUD_VIDAS_X, HUD_VIDAS_Y),
            (HUD_VIDAS_X + HUD_VIDAS_LARGURA, HUD_VIDAS_Y),
            (HUD_VIDAS_X + HUD_VIDAS_LARGURA, HUD_VIDAS_Y + HUD_VIDAS_ALTURA),
            (HUD_VIDAS_X, HUD_VIDAS_Y + HUD_VIDAS_ALTURA)
        ]
        if fundo:
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
    def desenhar_progresso(self, tela, pastas_coletadas, max_pastas, fundo=True):

        painel = [
            (HUD_PASTAS_X, HUD_PASTAS_Y),
            (HUD_PASTAS_X + HUD_PASTAS_LARGURA, HUD_PASTAS_Y),
            (HUD_PASTAS_X + HUD_PASTAS_LARGURA, HUD_PASTAS_Y + HUD_PASTAS_ALTURA),
            (HUD_PASTAS_X, HUD_PASTAS_Y + HUD_PASTAS_ALTURA)
        ]
        if fundo:
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
        if fundo:
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

        # Painel de vidas: só refaz quando as vidas mudam
        chave_vidas = (vidas, vidas_maximas)
        if chave_vidas != self.chave_vidas:
            self.chave_vidas = chave_vidas
            self.buffer_hud.blit(self.buffer_estatico, self.rect_vidas, self.rect_vidas)
            self.desenhar_vidas(self.buffer_hud, vidas, vidas_maximas, fundo=False)

        # Painel de pastas: só refaz quando as pastas mudam
        chave_pastas = (pastas_coletadas, max_pastas)
        if chave_pastas != self.chave_pastas:
            self.chave_pastas = chave_pastas
            self.buffer_hud.blit(self.buffer_estatico, self.rect_pastas, self.rect_pastas)
            self.desenhar_progresso(self.buffer_hud, pastas_coletadas, max_pastas, fundo=False)

        tela.blit(self.buffer_hud, self.rect_vidas, self.rect_vidas)
        tela.blit(self.buffer_hud, self.rect_pastas, self.rect_pastas)

        # O FPS muda a todo momento, então continua sendo desenhado por frame
        self.desenhar_fps(tela)