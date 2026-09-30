import pygame
import random
import os
from abc import ABC, abstractmethod

from engine.rasterizacao import (
    scanline_fill, 
    desenhar_poligono, 
    desenhar_circulo, 
    desenhar_elipse, 
    desenhar_linha, 
    flood_fill,
    scanline_textura
)
from engine.colisoes import colisao_poligonos_aabb
from engine.viewport import matriz_mundo_para_viewport
from engine.transformacoes import aplica_transformacao
from engine.recorte import cohen_sutherland
from game.entidades import Jogador, Pasta, CocoPombo



# classe base abstrata
class Estado(ABC):
    
    # construtor
    def __init__(self, jogo):
        self.jogo = jogo

    # funções que devem ser implementadas pelas classes filhas
    @abstractmethod
    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        pass

    @abstractmethod
    def atualizar(self, dt):
        pass

    @abstractmethod
    def desenhar(self, tela):
        pass



class EstadoMenu(Estado):
    
    def __init__(self, jogo):
        super().__init__(jogo)
        
        self.fonte_botoes = pygame.font.SysFont("Courier New", 26, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Courier New", 45, bold=True)
        self.opcoes = ["INICIAR", "DIFICULDADE", "HISTÓRIA / MANUAL"]

    
    
    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):        # essa função será chamada enquanto o jogo estiver no menu
        if not clicou:
            return
        
        centro_de_x = self.jogo.largura // 2
        
        for i in range(len(self.opcoes)):
            cy = 260 + (i * 90)
            
            # Checagem simples de clique em área retangular
            if centro_de_x - 180 <= mouse_pos[0] <= centro_de_x + 180 and cy - 32 <= mouse_pos[1] <= cy + 32:   # verifica se o mouse está dentro de algum retângulo das opções

                # muda o estado
                if i == 0:
                    self.jogo.mudar_estado(EstadoJogando(self.jogo))
                elif i == 1:
                    self.jogo.mudar_estado(EstadoDificuldade(self.jogo))
                elif i == 2:
                    self.jogo.mudar_estado(EstadoHistoria_Manual(self.jogo))


    # o menu não possui animação, então não precisa implementar
    def atualizar(self, dt):
        pass



    def _desenhar_emblema_nc2a(self, tela, cx, cy):
        """
        Gera o emblema utilizando exatamente as primitivas exigidas:
        - Elipse
        - Circunferência
        - Retas (Bresenham)
        - Preenchimento Flood Fill
        """
        cor_linha = (255, 215, 0)      # Dourado
        cor_preenchimento = (180, 50, 50) # Vinho/Vermelho

        # 1. Elipse Externa
        desenhar_elipse(tela, cx, cy, rx=70, ry=45, cor=cor_linha)

        # 2. Círculo Interno
        desenhar_circulo(tela, cx, cy, r=25, cor=cor_linha)

        # 3. Retas (Bresenham) formando um losango central
        desenhar_linha(tela, cx, cy - 20, cx + 20, cy, cor_linha)
        desenhar_linha(tela, cx + 20, cy, cx, cy + 20, cor_linha)
        desenhar_linha(tela, cx, cy + 20, cx - 20, cy, cor_linha)
        desenhar_linha(tela, cx - 20, cy, cx, cy - 20, cor_linha)

        # 4. Preenchimento Flood Fill no centro do losango
        # Nota: Executamos o Flood Fill em uma região pequena para manter 60 FPS
        flood_fill(tela, cx, cy, cor_preenchimento)

    def desenhar(self, tela):
        largura_tela = self.jogo.largura
        altura_tela = self.jogo.altura

        # 1. Fundo da tela preenchido com a SUA Engine (substitui o tela.fill)
        fundo_pontos = [
            (0, 0),
            (largura_tela, 0),
            (largura_tela, altura_tela),
            (0, altura_tela)
        ]

        scanline_fill(tela, fundo_pontos, (30, 40, 50))         # pinta toda a tela

        self._desenhar_emblema_nc2a(tela, largura_tela // 2, 90)
        
        titulo = self.fonte_titulo.render("DESASTRE NO NC2A", True, (255, 255, 255))    # "desenha" o título na tela
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 150))       # posiciona o título na tela

        mouse_x, mouse_y = pygame.mouse.get_pos()       # pega a posição onde o mouse está na tela
        cx = largura_tela // 2
        
        for i, texto in enumerate(self.opcoes):
            cy = 270 + (i * 85)
            
            # Dimensões do botão (360x64) centrais
            x_ini, y_ini = cx - 180, cy - 30
            w_bot, h_bot = 360, 60
            
            hover = x_ini <= mouse_x <= x_ini + w_bot and y_ini <= mouse_y <= y_ini + h_bot
            cor_fundo = (90, 190, 245) if hover else (60, 160, 225)
            
            # Converte o retângulo do botão em vértices de um polígono
            pontos_botao = [
                (x_ini, y_ini),
                (x_ini + w_bot, y_ini),
                (x_ini + w_bot, y_ini + h_bot),
                (x_ini, y_ini + h_bot)
            ]
            
            # Preenche e desenha a borda com a sua Engine
            scanline_fill(tela, pontos_botao, cor_fundo)
            desenhar_poligono(tela, pontos_botao, (255, 255, 255)) # Borda branca
            
            # Renderiza apenas o texto (Pygame renderiza fontes nativamente)
            txt_surf = self.fonte_botoes.render(texto, True, (10, 25, 45))
            tela.blit(txt_surf, txt_surf.get_rect(center=(cx, cy)))



class EstadoJogando(Estado):
    
    def __init__(self, jogo):
        super().__init__(jogo)
        self.fonte = pygame.font.SysFont("Arial", 24, bold=True)        # fonte usada no HUD


        w, h = self.jogo.largura, self.jogo.altura
        # 1. Cria um buffer de fundo com o tamanho da tela
        self.buffer_fundo = pygame.Surface((w, h))
        # 2. Carrega a imagem do cenário
        caminho_cenario = os.path.join("assets", "cenario_alternativo.png")
        self.imagem_cenario = pygame.image.load(caminho_cenario).convert()
        # 3. Define os vértices do polígono do fundo
        vertices_cenario = [
            ((0, 0), (0.0, 0.0)),
            ((w, 0), (1.0, 0.0)),
            ((w, h), (1.0, 1.0)),
            ((0, h), (0.0, 1.0))
        ]
        # 4. EXECUTA O SCANLINE DE TEXTURA APENAS UMA VEZ AQUI
        scanline_textura(self.buffer_fundo, vertices_cenario, self.imagem_cenario)

        
        self.jogador = Jogador()                                        # cria uma instância da classe Jogador
        self.jogador.x = jogo.largura / 2                               # posiciona o jogador na tela
        self.jogador.y = jogo.altura - 50                               # bota em (400,550), perto do chão e no centro da tela

        self.objetos_caindo = []                                        # cria uma lista para guardar os objeto
        self.max_pastas_fase = 30                                       # contadores
        self.total_pastas_lancadas = 0
        self.pastas_coletadas = 0
        self.pastas_em_jogo = 0

        self.temporizador_pasta = 0.0                                   # temporizadores
        self.temporizador_coco = 0.0

        self._aplicar_dificuldade()                                     # método interno da classe

    
    # verifica qual a dificuldade escolhida, se não começa com 'normal'
    def _aplicar_dificuldade(self):
        dif = self.jogo.dificuldade_atual
        if dif == 1:
            self.vidas = 5; self.meta = 0.3; self.vel_queda = 150.0; self.freq_coco = 2.0
        elif dif == 3:
            self.vidas = 1; self.meta = 0.7; self.vel_queda = 350.0; self.freq_coco = 0.5
        else: # Normal
            self.vidas = 3; self.meta = 0.5; self.vel_queda = 250.0; self.freq_coco = 1.0


    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        self.jogador.vel_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.jogador.vel_x = -self.jogador.vel_movimento
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.jogador.vel_x = self.jogador.vel_movimento


    def atualizar(self, dt):
        self.jogador.atualizar(dt)                      # jogador atualiza a posição
        self.jogador.x = max(20, min(self.jogo.largura - 20, self.jogador.x))   # limita para que o jogador não saia da tela

        # Lógica de Spawn
        if self.total_pastas_lancadas < self.max_pastas_fase:           # enquanto não tiver lançados 30 pastas
            self.temporizador_pasta += dt                               # acumula o temporizador da pasta
            if self.temporizador_pasta >= 0.8:                          # a cada 0.8s
                pasta = Pasta()                                         # cria uma pasta
                pasta.x = random.randint(30, self.jogo.largura - 30)    # posição da pasta
                pasta.y = -20                                           # começa em cima da tela
                pasta.vel_y = self.vel_queda                            # velocidade de queda da pasta, depende da dificuldade
                self.objetos_caindo.append(pasta)                       # adiciona na lista
                self.total_pastas_lancadas += 1                         # atualiza contadores
                self.pastas_em_jogo += 1
                self.temporizador_pasta = 0.0                           # começa a contar de novo
        
        # lógica parecida com a das pastas 
        self.temporizador_coco += dt
        if self.temporizador_coco >= self.freq_coco:
            coco = CocoPombo()
            coco.x = random.randint(30, self.jogo.largura - 30)
            coco.y = -20
            coco.vel_y = self.vel_queda
            self.objetos_caindo.append(coco)
            self.temporizador_coco = 0.0


        # Lógica de Colisão e Limpeza
        pontos_jogador = self.jogador.obter_pontos_mundo()          # obtém os pontos do jogador
        for obj in self.objetos_caindo:                             # percorre os objetos da lista
            if not obj.ativa: continue                              # ignora objetos inativos

            obj.atualizar(dt)
            pontos_obj = obj.obter_pontos_mundo()

            if colisao_poligonos_aabb(pontos_jogador, pontos_obj):          # verifica a colisão
                obj.ativa = False
                # verifica qual foi o objeto que colidiu
                if isinstance(obj, Pasta):
                    self.pastas_coletadas += 1
                    self.pastas_em_jogo -= 1
                elif isinstance(obj, CocoPombo):
                    self.vidas -= 1
                    self.jogador.cor = (139, 69, 19)            # pinta de marrom, para simular uma animação

            elif obj.y > self.jogo.altura + 50:             # caso passe do chão, inativa o objeto
                obj.ativa = False
                if isinstance(obj, Pasta):
                    self.pastas_em_jogo -= 1

        self.objetos_caindo = [obj for obj in self.objetos_caindo if obj.ativa]         # cria uma nova lista somente com os obejtos ativos

        if self.jogador.cor != (50, 150, 200):                  # atualiza a cor do jogador caso atingido pelo coco, dura muito pouco tempo (aprox um frame)
            self.jogador.cor = (50, 150, 200)

        # Condição de Fim
        progresso = self.pastas_coletadas / self.max_pastas_fase
        if self.vidas <= 0:
            self.jogo.mudar_estado(EstadoFim(self.jogo, "DERROTA! Você sujou todas as camisas!"))
        elif self.total_pastas_lancadas >= self.max_pastas_fase and self.pastas_em_jogo == 0:
            if progresso >= self.meta:
                self.jogo.mudar_estado(EstadoFim(self.jogo, f"VITÓRIA! Resgatou {int(progresso*100)}%!"))
            else:
                self.jogo.mudar_estado(EstadoFim(self.jogo, f"DERROTA! Salvou apenas {int(progresso*100)}%."))



    def desenhar_minimapa(self, tela):
        # 1. Definições da Window (Mundo) e Viewport (Tela)
        window = (0, 0, self.jogo.largura, self.jogo.altura)
        viewport = (620, 20, 780, 140)  # (xv_min, yv_min, xv_max, yv_max)
        xv_min, yv_min, xv_max, yv_max = viewport
    
        # 2. Fundo e Moldura do Mini-mapa (Engine)
        pts_moldura = [
            (xv_min, yv_min),
            (xv_max, yv_min),
            (xv_max, yv_max),
            (xv_min, yv_max)
        ]
        scanline_fill(tela, pts_moldura, (20, 20, 30))       # Fundo escuro
        desenhar_poligono(tela, pts_moldura, (255, 255, 0))  # Borda amarela

        # 3. Calcula a matriz de transformação Mundo -> Viewport uma única vez por frame
        M_vp = matriz_mundo_para_viewport(window, viewport)
    
        # 4. Desenha todas as entidades dentro do Mini-mapa
        todas_entidades = [self.jogador] + self.objetos_caindo
    
        for ent in todas_entidades:
            pts_mundo = ent.obter_pontos_mundo()

            # Converte todos os pontos do mundo para a Viewport usando a sua matriz
            pts_vp = aplica_transformacao(M_vp, pts_mundo)
            n = len(pts_vp)
    
            for i in range(n):
                x0, y0 = pts_vp[i]
                x1, y1 = pts_vp[(i + 1) % n]

                # Chama a SUA função de Cohen-Sutherland com os 8 parâmetros individuais
                visivel, rx0, ry0, rx1, ry1 = cohen_sutherland(
                    x0, y0, x1, y1, xv_min, yv_min, xv_max, yv_max
                )
    
                # Se a aresta for visível/recortada, desenha com o Bresenham
                if visivel:
                    desenhar_linha(tela, int(rx0), int(ry0), int(rx1), int(ry1), ent.cor)


    
    def desenhar(self, tela):
        # 1. Copia o fundo pré-renderizado instantaneamente (sem lag)
        tela.blit(self.buffer_fundo, (0, 0))

        # 2. Desenha o jogador e os objetos em tempo real
        self.jogador.desenhar(tela)
        for obj in self.objetos_caindo:
            obj.desenhar(tela)

       # 3. HUD (Camisas, Pastas e FPS)
        fps = int(self.jogo.clock.get_fps())
        cor_fps = (0, 255, 128) if fps >= 50 else (255, 215, 0) # Verde se fluido, Amarelo se cair

        txt_vidas = self.fonte.render(f"Camisas: {self.vidas}", True, (0,0,0))
        txt_pastas = self.fonte.render(f"Pastas: {self.pastas_coletadas}/{self.max_pastas_fase}", True, (0,0,0))
        txt_fps = self.fonte.render(f"FPS: {fps}", True, cor_fps)

        # Exibe as informações na tela
        tela.blit(txt_vidas, (20, 20))
        tela.blit(txt_pastas, (20, 50))
        tela.blit(txt_fps, (20, 80)) # Exibe no canto superior direito

        self.desenhar_minimapa(tela)




class EstadoDificuldade(Estado):
    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        if clicou:
            self.jogo.dificuldade_atual = 3 # Exemplo: Forçando Difícil ao clicar
            self.jogo.mudar_estado(EstadoMenu(self.jogo))
    
    def atualizar(self, dt): 
        pass

    def desenhar(self, tela):
        tela.fill((100, 50, 50)) # Placeholder visual


class EstadoHistoria_Manual(Estado):
    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        if clicou: self.jogo.mudar_estado(EstadoMenu(self.jogo))
    
    def atualizar(self, dt):
        pass
    
    def desenhar(self, tela):
        tela.fill((50, 100, 50)) # Placeholder visual


class EstadoFim(Estado):
    def __init__(self, jogo, mensagem):
        super().__init__(jogo)
        self.mensagem = mensagem
        self.fonte = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 24)

    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        if teclas[pygame.K_RETURN]:
            self.jogo.mudar_estado(EstadoMenu(self.jogo))

    def atualizar(self, dt): pass

    def desenhar(self, tela):
        tela.fill((20, 20, 20))
        txt_res = self.fonte.render(self.mensagem, True, (255, 255, 255))
        txt_voltar = self.fonte_pequena.render("Pressione ENTER para voltar", True, (200, 200, 200))
        
        tela.blit(txt_res, (self.jogo.largura//2 - txt_res.get_width()//2, self.jogo.altura//2 - 50))
        tela.blit(txt_voltar, (self.jogo.largura//2 - txt_voltar.get_width()//2, self.jogo.altura//2 + 50))