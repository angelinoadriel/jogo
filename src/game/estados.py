import pygame
import random
import os
from abc import ABC, abstractmethod

from engine.rasterizacao import (
    scanline_fill, 
    desenhar_poligono,
    retangulo_para_poligono, 
    desenhar_circulo, 
    desenhar_elipse, 
    desenhar_linha, 
    boundary_fill,
    scanline_textura,
    scanline_fill_gradiente
)
from engine.colisoes import colisao_poligonos_aabb
from engine.viewport import matriz_mundo_para_viewport
from engine.transformacoes import aplica_transformacao
from engine.recorte import cohen_sutherland
from game.entidades import Jogador, Pasta, CocoPombo


def desenhar_textura_quadrado(tela,x,y,largura,altura,imagem,u_invertido=False):
    if u_invertido:
        vertices = [
            ((x, y), (1.0, 0.0)),
            ((x + largura, y), (0.0, 0.0)),
            ((x + largura, y + altura), (0.0, 1.0)),
            ((x, y + altura), (1.0, 1.0))
        ]
    else:
        vertices = [
            ((x, y), (0.0, 0.0)),
            ((x + largura, y), (1.0, 0.0)),
            ((x + largura, y + altura), (1.0, 1.0)),
            ((x, y + altura), (0.0, 1.0))
        ]

    scanline_textura(tela,vertices,imagem,usar_alpha=True)

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
        
        self.fonte_botoes = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 26)
        self.fonte_titulo = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 45)
        self.opcoes = ["INICIAR", "DIFICULDADE", "HISTÓRIA / MANUAL"]

        # Constantes dos botões para garantir consistência entre clique e desenho
        self.largura_botao = 360
        self.altura_botao = 60
        self.y_inicial_botoes = 270
        self.espacamento_botoes = 85

        self.img_pombo_frente = pygame.image.load("assets/pombos/pombo_facing_forward.png").convert_alpha()
        self.img_pombo_costas = pygame.image.load("assets/pombos/pombo_facing_back.png").convert_alpha()
        self.img_pombo_voando_frente = pygame.image.load("assets/pombos/pombo_flying_front_on.png").convert_alpha()
        self.img_pombo_voando = pygame.image.load("assets/pombos/pombo_fly_right_upbeat.png").convert_alpha()
        self.img_pombo_planando = pygame.image.load("assets/pombos/pombo_descending_gliding.png").convert_alpha()
        self.img_pombo_parando = pygame.image.load("assets/pombos/pombo_ascending_flight.png").convert_alpha()
        # Define o tamanho que o pombo terá na tela
        self.largura_pombo = 40
        self.altura_pombo = 40

    def desenhar_cenario(self, tela):        
        largura_tela = self.jogo.largura
        altura_tela = self.jogo.altura

        # --- FUNDO E CENÁRIO ---
        fundo = retangulo_para_poligono(0, 0,largura_tela,altura_tela)
        cores_fundo = [
            (48, 129, 255),
            (48, 129, 255),
            (166, 201, 255),
            (166, 201, 255)
        ]
        scanline_fill_gradiente(tela, fundo, cores_fundo)
        
        borda = (0, 0, 0)
        cor_poste = (98, 99, 99)
        # Poste
        poste = [
            (50, 600),
            (50, 50),
            (60, 50),
            (60, 35),
            (70, 35),
            (70, 50),
            (80, 50),
            (80, 600)
        ]
        desenhar_poligono(tela, poste, borda)
        boundary_fill(tela, 65, 400, cor_poste, borda)

        # Braço do poste
        braco_poste = [
            (60, 35),
            (140, 20),
            (140, 30),
            (70, 55)
        ]
        desenhar_poligono(tela, braco_poste, borda)
        boundary_fill(tela, 100, 35, cor_poste, borda)

        # Luminária
        cor_luminaria = (50, 50, 50)
        xc_luz = 140
        yc_luz = 35
        desenhar_elipse(tela, xc_luz, yc_luz, 20, 8, borda)
        boundary_fill(tela, xc_luz, yc_luz, cor_luminaria, borda)

        # Lâmpada
        cor_lampada = (255, 255, 200)
        desenhar_circulo(tela, xc_luz, yc_luz + 10, 12, borda)
        boundary_fill(tela, xc_luz, yc_luz + 10, cor_lampada, borda)

        # Fios
        fio1 = [
            (80, 100),
            (80, 101),
            (800, 101),
            (800, 100)
        ]
        fio2 = [
            (80, 110),
            (80, 111),
            (800, 111),
            (800, 110)
        ]
        fio3 = [
            (80, 120),
            (80, 121),
            (800, 121),
            (800, 120)
        ]
        desenhar_poligono(tela, fio1, borda)
        desenhar_poligono(tela, fio2, borda)
        desenhar_poligono(tela, fio3, borda)

        # -------------------------
        # Pombos com textura
        # -------------------------
        desenhar_textura_quadrado(tela, 200, 63, self.largura_pombo, self.altura_pombo, self.img_pombo_frente)
        desenhar_textura_quadrado(tela, 400, 70, self.largura_pombo, self.altura_pombo, self.img_pombo_costas)
        desenhar_textura_quadrado(tela, 700, 20, self.largura_pombo, self.altura_pombo, self.img_pombo_voando_frente)
        desenhar_textura_quadrado(tela, 130, 330, self.largura_pombo, self.altura_pombo, self.img_pombo_voando)
        desenhar_textura_quadrado(tela, 630, 250, self.largura_pombo, self.altura_pombo, self.img_pombo_planando)
        desenhar_textura_quadrado(tela, 230, 150, self.largura_pombo, self.altura_pombo, self.img_pombo_parando)
        desenhar_textura_quadrado(tela, 630, 430, self.largura_pombo, self.altura_pombo, self.img_pombo_voando, u_invertido=True)

    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        if not clicou:
            return
        
        cx = self.jogo.largura // 2
        w_bot, h_bot = self.largura_botao, self.altura_botao
        
        for i in range(len(self.opcoes)):
            cy = self.y_inicial_botoes + (i * self.espacamento_botoes)
            x_ini = cx - (w_bot // 2)
            y_ini = cy - (h_bot // 2)
            
            # Checagem de clique idêntica à área visual/hover
            if x_ini <= mouse_pos[0] <= x_ini + w_bot and y_ini <= mouse_pos[1] <= y_ini + h_bot:
                if i == 0:
                    self.jogo.mudar_estado(EstadoJogando(self.jogo))
                elif i == 1:
                    self.jogo.mudar_estado(EstadoDificuldade(self.jogo))
                elif i == 2:
                    self.jogo.mudar_estado(EstadoHistoria_Manual(self.jogo))

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        self.desenhar_cenario(tela)

        # --- TÍTULO ---
        titulo = self.fonte_titulo.render("Nome do jogo",True,(255, 255, 255))
        tela.blit(titulo,(self.jogo.largura // 2 - titulo.get_width() // 2,150))

         # --- BOTÕES ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cx = self.jogo.largura // 2

        for i, texto in enumerate(self.opcoes):

            cy = (self.y_inicial_botoes + i * self.espacamento_botoes)

            x_ini = cx - self.largura_botao // 2
            y_ini = cy - self.altura_botao // 2

            hover = (x_ini <= mouse_x <= x_ini + self.largura_botao and y_ini <= mouse_y <= y_ini + self.altura_botao)

            cor_fundo = ((90, 190, 245) if hover else (60, 160, 225))
            pontos_botao = [
                (x_ini, y_ini),
                (x_ini + self.largura_botao, y_ini),
                (x_ini + self.largura_botao, y_ini + self.altura_botao),
                (x_ini, y_ini + self.altura_botao)
            ]
            scanline_fill(tela, pontos_botao, cor_fundo)
            desenhar_poligono(tela, pontos_botao, (255, 255, 255))

            txt_surf = self.fonte_botoes.render(texto, True, (10, 25, 45))
            tela.blit(txt_surf, txt_surf.get_rect(center=(cx, cy)))

class EstadoJogando(Estado):

    def carregar_textura_pasta(self, caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        area_visivel = imagem.get_bounding_rect(min_alpha=1)
        if area_visivel.width > 0 and area_visivel.height > 0:
            imagem = imagem.subsurface(area_visivel).copy()
        return imagem

    def carregar_textura_coco(self, caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        area_visivel = imagem.get_bounding_rect(min_alpha=1)
        if area_visivel.width > 0 and area_visivel.height > 0:
            imagem = imagem.subsurface(area_visivel).copy()
        return imagem   

    def carregar_textura_personagem(self, caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        # Remove o espaço totalmente transparente
        area_visivel = imagem.get_bounding_rect(min_alpha=1)

        if (area_visivel.width > 0 and area_visivel.height > 0):
            imagem = imagem.subsurface(area_visivel).copy()

        return imagem

    def __init__(self, jogo):
        super().__init__(jogo)
        
        self.fonte = pygame.font.SysFont("Arial", 24, bold=True)        # fonte usada no HUD
        self.fonte_pastas_titulo = pygame.font.SysFont("Arial",16,bold=True)
        self.fonte_pastas_numero = pygame.font.SysFont("Arial",13,bold=True)
        self.fonte_pastas_percentual = pygame.font.SysFont("Arial",14,bold=True)

        w, h = self.jogo.largura, self.jogo.altura
        # 1. Cria um buffer de fundo com o tamanho da tela
        self.buffer_fundo = pygame.Surface((w, h))
        # 2. Carrega a imagem do cenário
        caminho_cenario = os.path.join("assets/cenario", "cenario.png")
        self.imagem_cenario = pygame.image.load(caminho_cenario).convert_alpha()
        # 3. Define os vértices do polígono do fundo
        vertices_cenario = [
            ((0, 0), (0.0, 0.0)),
            ((w, 0), (1.0, 0.0)),
            ((w, h), (1.0, 1.0)),
            ((0, h), (0.0, 1.0))
        ]
        # 4. EXECUTA O SCANLINE DE TEXTURA APENAS UMA VEZ AQUI
        scanline_textura(self.buffer_fundo, vertices_cenario, self.imagem_cenario)


        # Imagem usada para representar cada vida
        caminho_camisa = os.path.join("assets/vidas_camisa","camisa_vida.png")
        self.imagem_camisa = pygame.image.load(caminho_camisa).convert_alpha()
        
        self.largura_camisa = 32
        self.altura_camisa = 32
        self.espacamento_camisa = 6


        self.texturas_pasta = [
            self.carregar_textura_pasta(os.path.join("assets/pastas", "papel1.png")),
            self.carregar_textura_pasta(os.path.join("assets/pastas", "papel2.png"))
        ]

        self.textura_coco = self.carregar_textura_coco(os.path.join("assets/coco", "coco_pombo.png"))

        self.textura_jogador_parado = self.carregar_textura_personagem(os.path.join("assets/personagem_professor","professor_frente.png"))
        self.texturas_jogador_corrida = []
        for i in range(1, 9):

            textura = self.carregar_textura_personagem(os.path.join("assets/personagem_professor",f"prof_corre_{i}.png"))
            self.texturas_jogador_corrida.append(textura)

        self.jogador = Jogador(self.textura_jogador_parado,self.texturas_jogador_corrida)      # cria uma instância da classe Jogador
        self.jogador.x = jogo.largura / 2                               # posiciona o jogador na tela
        self.jogador.y = jogo.altura - 80                               # bota em (400,520), perto do chão e no centro da tela

        self.objetos_caindo = []                                        # cria uma lista para guardar os objeto
        self.max_pastas_fase = 30                                       # contadores
        self.total_pastas_lancadas = 0
        self.pastas_coletadas = 0
        self.pastas_em_jogo = 0

        self.temporizador_pasta = 0.0                                   # temporizadores
        self.temporizador_coco = 0.0

        self._aplicar_dificuldade()                                     # método interno da classe
        
        self.vidas_maximas = self.vidas

        self.mostrar_colisoes = False
        
        self.minimapa_zoom = 1.5
    
    # verifica qual a dificuldade escolhida, se não começa com 'normal'
    def _aplicar_dificuldade(self):
        dif = self.jogo.dificuldade_atual
        if dif == 1:
            self.vidas = 5; self.meta = 0.3; self.vel_queda = 150.0; self.freq_coco = 2.0
        elif dif == 3:
            self.vidas = 1; self.meta = 0.7; self.vel_queda = 350.0; self.freq_coco = 0.5
        else: # Normal
            self.vidas = 3; self.meta = 0.5; self.vel_queda = 250.0; self.freq_coco = 1.0

    def desenhar_camisa_vida(self, tela, x, y, perdida=False):

        vertices = [
            ((x, y), (0.0, 0.0)),
            ((x + self.largura_camisa, y), (1.0, 0.0)),
            ((x + self.largura_camisa, y + self.altura_camisa), (1.0, 1.0)),
            ((x, y + self.altura_camisa), (0.0, 1.0))
        ]

        # Desenha a camisa usando sua própria textura
        scanline_textura(tela,vertices,self.imagem_camisa,usar_alpha=True)

        # Se a vida foi perdida, desenha um X vermelho
        if perdida:
            margem = 8

            x1 = x + margem
            y1 = y + margem
            x2 = x + self.largura_camisa - margem
            y2 = y + self.altura_camisa - margem

            desenhar_linha(tela, x1, y1, x2, y2, (255, 0, 0))
            desenhar_linha(tela, x2, y1, x1, y2, (255, 0, 0))

    def processar_eventos(self,eventos,teclas,mouse_pos,clicou):
        self.jogador.vel_x = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.jogador.vel_x = -self.jogador.vel_movimento

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.jogador.vel_x = self.jogador.vel_movimento

        # Ativa/desativa visualização das caixas de colisão
        for evento in eventos:

            if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_F3):
                self.mostrar_colisoes = (not self.mostrar_colisoes)

    def atualizar(self, dt):
        self.jogador.atualizar(dt)                      # jogador atualiza a posição
        self.jogador.x = max(20, min(self.jogo.largura - 20, self.jogador.x))   # limita para que o jogador não saia da tela

        # Lógica de Spawn
        if self.total_pastas_lancadas < self.max_pastas_fase:           # enquanto não tiver lançados 30 pastas
            self.temporizador_pasta += dt                               # acumula o temporizador da pasta
            if self.temporizador_pasta >= 0.8:                          # a cada 0.8s
                pasta = Pasta(random.choice(self.texturas_pasta))       # cria uma pasta
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
            coco = CocoPombo(self.textura_coco)
            coco.x = random.randint(30, self.jogo.largura - 30)
            coco.y = -20
            coco.vel_y = self.vel_queda
            self.objetos_caindo.append(coco)
            self.temporizador_coco = 0.0

        # Lógica de Colisão e Limpeza
        pontos_jogador = (self.jogador.obter_pontos_colisao_mundo())          # obtém os pontos do jogador
        for obj in self.objetos_caindo:                             # percorre os objetos da lista
            if not obj.ativa: continue                              # ignora objetos inativos

            obj.atualizar(dt)
            pontos_obj = (obj.obter_pontos_colisao_mundo())
            
            if colisao_poligonos_aabb(pontos_jogador,pontos_obj):          # verifica a colisão
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
                self.jogo.mudar_estado(EstadoFim(self.jogo, f"PARABÉNS! Você recuperou {int(progresso*100)}% das pastas!"))
            else:
                self.jogo.mudar_estado(EstadoFim(self.jogo, f"DERROTA! Salvou apenas {int(progresso*100)}% das pastas."))

    def desenhar_hud(self, tela):
        # =====================================================
        # PAINEL DAS CAMISAS
        # =====================================================
        x_camisas = 590
        y_camisas = 20

        largura_camisas = 210
        altura_camisas = 52

        pontos_camisas = [
            (x_camisas, y_camisas),
            (x_camisas + largura_camisas, y_camisas),
            (x_camisas + largura_camisas, y_camisas + altura_camisas),
            (x_camisas, y_camisas + altura_camisas)
        ]

        # Fundo
        scanline_fill(tela, pontos_camisas, (235, 240, 245))
        # Borda
        desenhar_poligono(tela, pontos_camisas, (20, 30, 40))

        # -----------------------------------------------------
        # Camisas
        # -----------------------------------------------------
        largura_total = (self.vidas_maximas * self.largura_camisa + (self.vidas_maximas - 1) * self.espacamento_camisa)

        x_inicial = (x_camisas + (largura_camisas - largura_total) // 2)
        y_inicial = (y_camisas + (altura_camisas - self.altura_camisa) // 2)

        for i in range(self.vidas_maximas):
            x = (x_inicial + i * (self.largura_camisa + self.espacamento_camisa))

            vida_perdida = i >= self.vidas
            self.desenhar_camisa_vida(tela, x, y_inicial, vida_perdida)

        # =====================================================
        # PAINEL DE PROGRESSO DAS PASTAS
        # =====================================================
        x_pastas = 590
        y_pastas = 82

        largura_pastas = 210
        altura_pastas = 82

        pontos_pastas = [
            (x_pastas, y_pastas),
            (x_pastas + largura_pastas, y_pastas),
            (x_pastas + largura_pastas, y_pastas + altura_pastas),
            (x_pastas, y_pastas + altura_pastas)
        ]

        # Fundo
        scanline_fill(tela, pontos_pastas, (235, 240, 245))
        # Borda
        desenhar_poligono(tela, pontos_pastas, (20, 30, 40))

        # =====================================================
        # TÍTULO
        # =====================================================
        txt_titulo_pastas = self.fonte_pastas_titulo.render("PASTAS RESGATADAS", True, (10, 25, 45))
        tela.blit(
            txt_titulo_pastas,
            txt_titulo_pastas.get_rect(center= (x_pastas + largura_pastas // 2, y_pastas + 15)))

        # =====================================================
        # CONTADOR
        # =====================================================
        txt_contador = self.fonte_pastas_numero.render(f"{self.pastas_coletadas} / {self.max_pastas_fase}", True, (10, 25, 45))
        tela.blit(txt_contador, txt_contador.get_rect(center= (x_pastas + largura_pastas // 2, y_pastas + 38)))

        # =====================================================
        # BARRA DE PROGRESSO
        # =====================================================
        margem_barra = 15

        barra_x = x_pastas + margem_barra
        barra_y = y_pastas + 53

        barra_largura = largura_pastas - margem_barra * 2
        barra_altura = 10

        # Fundo da barra
        pontos_barra = [
            (barra_x, barra_y),
            (barra_x + barra_largura, barra_y),
            (barra_x + barra_largura, barra_y + barra_altura),
            (barra_x, barra_y + barra_altura)
        ]
        scanline_fill(tela, pontos_barra, (190, 200, 210))
        desenhar_poligono(tela, pontos_barra, (40, 50, 60))

        # Calcula o progresso
        progresso = (self.pastas_coletadas / self.max_pastas_fase)

        largura_preenchida = int(barra_largura * progresso)

        if largura_preenchida > 0:

            pontos_progresso = [
                (barra_x, barra_y),
                (barra_x + largura_preenchida, barra_y),
                (barra_x + largura_preenchida, barra_y + barra_altura),
                (barra_x, barra_y + barra_altura)
            ]
            scanline_fill(tela, pontos_progresso, (50, 180, 90))

        # =====================================================
        # PORCENTAGEM
        # =====================================================
        percentual = int(progresso * 100)

        txt_percentual = self.fonte_pastas_percentual.render(f"{percentual}%", True, (10, 25, 45))

        tela.blit(txt_percentual, txt_percentual.get_rect(center= (x_pastas + largura_pastas // 2, y_pastas + 72)))
        
        # =====================================================
        # FPS
        # =====================================================
        fps = int(self.jogo.clock.get_fps())

        if fps >= 50:
            cor_fps = (0, 170, 70)
        else:
            cor_fps = (220, 150, 0)

        txt_fps = self.fonte.render(f"FPS: {fps}", True, cor_fps)
        tela.blit(txt_fps, (x_pastas + 5, y_pastas + altura_pastas + 5))

    def desenhar_colisoes(self, tela):
        if not self.mostrar_colisoes:
            return

        cor_colisao = (255, 0, 0)

        # -------------------------
        # Jogador
        # -------------------------
        pontos = (self.jogador.obter_pontos_colisao_mundo())
        desenhar_poligono(tela, pontos, cor_colisao)

        # -------------------------
        # Objetos
        # -------------------------

        for obj in self.objetos_caindo:

            pontos = (obj.obter_pontos_colisao_mundo())
            desenhar_poligono(tela, pontos, cor_colisao)

    def obter_window_minimapa(self):

        largura_mundo = self.jogo.largura
        altura_mundo = self.jogo.altura

        largura_window = largura_mundo / self.minimapa_zoom
        altura_window = altura_mundo / self.minimapa_zoom

        centro_x = self.jogador.x
        centro_y = self.jogador.y

        x_min = centro_x - largura_window / 2
        x_max = centro_x + largura_window / 2

        y_min = centro_y - altura_window / 2
        y_max = centro_y + altura_window / 2

        # Impede que a Window saia dos limites do mundo
        if x_min < 0:
            x_min = 0
            x_max = largura_window

        if x_max > largura_mundo:
            x_max = largura_mundo
            x_min = largura_mundo - largura_window

        if y_min < 0:
            y_min = 0
            y_max = altura_window

        if y_max > altura_mundo:
            y_max = altura_mundo
            y_min = altura_mundo - altura_window

        return (x_min, y_min, x_max, y_max)

    def desenhar_minimapa(self, tela):
        # 1. Definições da Window (Mundo) e Viewport (Tela)
        window = self.obter_window_minimapa()
        viewport = (20, 20, 180, 140)  # (xv_min, yv_min, xv_max, yv_max)
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

        txt_zoom = self.fonte.render(f"Zoom: {self.minimapa_zoom:.1f}x",True,(255, 255, 255))
        tela.blit(txt_zoom,(25, 145))

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
                visivel, rx0, ry0, rx1, ry1 = cohen_sutherland(x0, y0, x1, y1, xv_min, yv_min, xv_max, yv_max)
    
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
        self.desenhar_hud(tela)

        self.desenhar_minimapa(tela)

        self.desenhar_colisoes(tela)

class EstadoDificuldade(Estado):

    def __init__(self, jogo):
        super().__init__(jogo)

        self.menu_visual = EstadoMenu(self.jogo)

        self.fonte_botoes = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 26)
        self.fonte_titulo = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 45)

        self.opcoes = ["FÁCIL", "NORMAL", "DIFÍCIL", "VOLTAR"]

        self.largura_botao = 360
        self.altura_botao = 60
        self.y_inicial_botoes = 220
        self.espacamento_botoes = 85

    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):
        if not clicou:
            return

        cx = self.jogo.largura // 2
        for i, texto in enumerate(self.opcoes):

            cy = (self.y_inicial_botoes + i * self.espacamento_botoes)

            x_ini = (cx - self.largura_botao // 2)
            y_ini = (cy - self.altura_botao // 2)

            clicou_no_botao = (x_ini <= mouse_pos[0] <= x_ini + self.largura_botao and y_ini <= mouse_pos[1] <= y_ini + self.altura_botao)

            if not clicou_no_botao:
                continue

            # FÁCIL
            if i == 0:
                self.jogo.dificuldade_atual = 1
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

            # NORMAL
            elif i == 1:
                self.jogo.dificuldade_atual = 2
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

            # DIFÍCIL
            elif i == 2:
                self.jogo.dificuldade_atual = 3
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

            # VOLTAR
            elif i == 3:
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        # Mesmo cenário visual do menu
        self.menu_visual.desenhar_cenario(tela)

        # --- TÍTULO ---
        titulo = self.fonte_titulo.render("DIFICULDADE", True, (255, 255, 255))
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 120))

        # --- BOTÕES ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cx = self.jogo.largura // 2

        for i, texto in enumerate(self.opcoes):
            cy = (self.y_inicial_botoes + i * self.espacamento_botoes)

            x_ini = (cx - self.largura_botao // 2)
            y_ini = (cy - self.altura_botao // 2)

            hover = (x_ini <= mouse_x <= x_ini + self.largura_botao and y_ini <= mouse_y <= y_ini + self.altura_botao)

            # Destaca a dificuldade atualmente escolhida
            selecionado = (
                (i == 0 and self.jogo.dificuldade_atual == 1)
                or
                (i == 1 and self.jogo.dificuldade_atual == 2)
                or
                (i == 2 and self.jogo.dificuldade_atual == 3)
            )

            if hover:
                cor_fundo = (90, 190, 245)
            else:
                cor_fundo = (60, 160, 225)

            pontos_botao = [
                (x_ini, y_ini),
                (x_ini + self.largura_botao, y_ini),
                (x_ini + self.largura_botao, y_ini + self.altura_botao),
                (x_ini, y_ini + self.altura_botao)
            ]

            scanline_fill(tela, pontos_botao, cor_fundo)
            desenhar_poligono(tela, pontos_botao, (255, 255, 255))

            # Indicador da dificuldade selecionada
            if selecionado:
                raio = 8

                x_bolinha = x_ini + self.largura_botao - 25
                y_bolinha = cy

                desenhar_circulo(tela, x_bolinha, y_bolinha, raio, (0, 220, 80))
                boundary_fill(tela, x_bolinha, y_bolinha, (0, 220, 80), (0, 220, 80))

            txt_surf = self.fonte_botoes.render(texto, True, (10, 25, 45))
            tela.blit(txt_surf, txt_surf.get_rect(center=(cx, cy)))

class EstadoHistoria_Manual(Estado):

    def __init__(self, jogo):
        super().__init__(jogo)

        self.menu_visual = EstadoMenu(self.jogo)

        # =====================================================
        # TEXTO 
        # Para mudar a história, basta alterar esta variável.
        # =====================================================
        self.texto_conteudo = (
            "HISTÓRIA\n\n"
            
            "Hoje é o dia mais importante da sua carreira: "
            "a apresentação decisiva da sua vida no prédio central "
            "da faculdade!\n\n"

            "Ele passou meses preparando relatórios, pastas e "
            "documentos impecáveis.\n\n"

            "Porém, ao chegar ansioso à entrada do prédio, o desastre "
            "acontece. Ele escorrega feio, sua pasta voa e todos os "
            "papéis da reunião começam a cair lentamente pelo ar.\n\n"

            "Para piorar a situação, acima dele está uma colônia de "
            "pombos que decidiu bombardear o local exatamente nesse "
            "momento!\n\n"

            "Agora, Ele precisa correr contra o tempo, movimentando-se "
            "de um lado para o outro para resgatar as pastas cruciais "
            "antes que caiam no chão sujo, enquanto se esquiva "
            "agilmente dos cocôs dos pombos.\n\n"

            "Se Ele se sujar demais, não poderá fazer a apresentação.\n\n\n"

            "MANUAL\n\n"

            "OBJETIVO\n\n"

            "Recupere a quantidade necessária de pastas sem perder "
            "todas as suas vidas.\n\n"

            "CONTROLES\n\n"

            "A / SETA ESQUERDA - mover para a esquerda\n"
            "D / SETA DIREITA - mover para a direita\n"
            "f3 - mostrar caixar de colisões\n"
            "ENTER - voltar ao menu\n"
            "MOUSE - selecionar opções dos menus"
        )

        # =====================================================
        # FONTES
        # =====================================================
        self.fonte_titulo = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 45)
        self.fonte_secao = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 30)
        self.fonte_texto = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 20)
        self.fonte_botao = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 24)

        # =====================================================
        # DIMENSÕES DO PAINEL
        # =====================================================
        self.largura_painel = 600
        self.altura_painel = 340

        self.x_painel = (self.jogo.largura // 2 - self.largura_painel // 2)
        self.y_painel = 155

        # Rolagem
        self.scroll = 0
        self.largura_barra = 12
        self.arrastando_barra = False
        self.posicao_mouse_barra = 0

        # Botão voltar
        self.largura_botao = 180
        self.altura_botao = 50
        self.y_botao = 550

    # =========================================================
    # EVENTOS
    # =========================================================
    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):

        for evento in eventos:
            if evento.type == pygame.MOUSEWHEEL:
                self.scroll -= evento.y * 30
                altura_linha = 24

                linhas = self.quebrar_texto(self.texto_conteudo, self.fonte_texto, 520)
                altura_total = len(linhas) * altura_linha
                altura_visivel = (self.altura_painel - 40)

                max_scroll = max(0, altura_total - altura_visivel)
                self.scroll = max(0, min(self.scroll, max_scroll))

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    mouse_x, mouse_y = evento.pos

                    x_barra = (self.x_painel + self.largura_painel - self.largura_barra - 8)
                    y_barra = (self.y_painel + 20)

                    largura_conteudo = (self.largura_painel - 20 * 2 - self.largura_barra - 8)
                    altura_conteudo = (self.altura_painel - 40)

                    if (x_barra <= mouse_x <= x_barra + self.largura_barra and y_barra <= mouse_y <= y_barra + altura_conteudo):
                        self.arrastando_barra = True

            if evento.type == pygame.MOUSEMOTION:
                if self.arrastando_barra:

                    mouse_y = evento.pos[1]

                    # Aqui convertemos a posição da barra
                    # para a posição do texto.

                    altura_conteudo = (self.altura_painel - 40)
                    linhas = self.quebrar_texto(self.texto_conteudo, self.fonte_texto, 550)
                    altura_total = len(linhas) * 24

                    max_scroll = max(0, altura_total - altura_conteudo)
                    deslocamento = (mouse_y - self.y_painel - 20)

                    if altura_conteudo > 0:
                        porcentagem = (deslocamento / altura_conteudo)
                        porcentagem = max(0, min(1, porcentagem))
                        self.scroll = int(porcentagem * max_scroll)

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.arrastando_barra = False

        # ENTER também permite voltar
        if teclas[pygame.K_RETURN]:
            self.jogo.mudar_estado(EstadoMenu(self.jogo))
            return

        # Clique no botão VOLTAR
        if clicou:
            cx = self.jogo.largura // 2

            x_ini = (cx - self.largura_botao // 2)
            y_ini = (self.y_botao - self.altura_botao // 2)

            clicou_no_botao = (x_ini <= mouse_pos[0] <= x_ini + self.largura_botao and y_ini <= mouse_pos[1] <= y_ini + self.altura_botao)

            if clicou_no_botao:
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

    # =========================================================
    # ATUALIZAÇÃO
    # =========================================================
    def atualizar(self, dt):
        pass

    # =========================================================
    # QUEBRA DE TEXTO
    # =========================================================
    def quebrar_texto(self, texto, fonte, largura_maxima):
        linhas_finais = []
        paragrafos = texto.split("\n")
        for paragrafo in paragrafos:

            # Linha vazia continua sendo uma linha vazia
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

    # =========================================================
    # DESENHAR TEXTO DENTRO DE UM PAINEL
    # =========================================================
    def desenhar_conteudo_rolavel(self, tela):

        margem = 20

        x_conteudo = self.x_painel + margem
        y_conteudo = self.y_painel + margem

        largura_conteudo = (self.largura_painel - margem * 2 - self.largura_barra - 8)
        altura_conteudo = (self.altura_painel - margem * 2)

        linhas = self.quebrar_texto(self.texto_conteudo, self.fonte_texto, largura_conteudo)

        espacamento = 24
        altura_total = len(linhas) * espacamento

        # -------------------------------------------------
        # Limita o desenho à área interna do painel
        # -------------------------------------------------
        tela.set_clip((x_conteudo, y_conteudo, largura_conteudo, altura_conteudo))

        y_texto = y_conteudo - self.scroll

        for linha in linhas:
            if linha == "":
                y_texto += espacamento
                continue

            texto = self.fonte_texto.render(linha, True, (10, 25, 45))
            tela.blit(texto, (x_conteudo, y_texto))

            y_texto += espacamento

        # Remove o clipping
        tela.set_clip(None)

        # -------------------------------------------------
        # Barra de rolagem
        # -------------------------------------------------
        if altura_total > altura_conteudo:
            x_barra = (self.x_painel + self.largura_painel - self.largura_barra - 8)
            y_barra = y_conteudo
            altura_area = altura_conteudo

            # Fundo da barra
            pontos_fundo = [
                (x_barra, y_barra),
                (x_barra + self.largura_barra, y_barra),
                (x_barra + self.largura_barra, y_barra + altura_area),
                (x_barra, y_barra + altura_area)
            ]
            scanline_fill(tela, pontos_fundo, (190, 200, 210))

            # Proporção visível
            proporcao = (altura_conteudo / altura_total)

            altura_barrinha = max(40, int(altura_area * proporcao))
            max_scroll = (altura_total - altura_conteudo)

            if max_scroll > 0:
                porcentagem = (self.scroll / max_scroll)
            else:
                porcentagem = 0

            y_barrinha = (y_barra + (altura_area - altura_barrinha) * porcentagem)

            pontos_barrinha = [
                (x_barra, y_barrinha),
                (x_barra + self.largura_barra, y_barrinha),
                (x_barra + self.largura_barra, y_barrinha + altura_barrinha),
                (x_barra, y_barrinha + altura_barrinha)
            ]
            scanline_fill(tela, pontos_barrinha, (70, 160, 220))
            desenhar_poligono(tela, pontos_barrinha, (255, 255, 255))

    # =========================================================
    # DESENHAR
    # =========================================================
    def desenhar(self, tela):
        # =====================================================
        # CENÁRIO
        # =====================================================
        self.menu_visual.desenhar_cenario(tela)

        # =====================================================
        # TÍTULO
        # =====================================================
        titulo = self.fonte_titulo.render("HISTÓRIA / MANUAL", True, (255, 255, 255))
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 110))

        # =====================================================
        # PAINEL ÚNICO
        # =====================================================
        pontos_painel = [
            (self.x_painel, self.y_painel),
            (self.x_painel + self.largura_painel, self.y_painel),
            (self.x_painel + self.largura_painel, self.y_painel + self.altura_painel),
            (self.x_painel, self.y_painel + self.altura_painel)
        ]
        scanline_fill(tela, pontos_painel, (230, 240, 250))
        desenhar_poligono(tela, pontos_painel, (255, 255, 255))

        # =====================================================
        # CONTEÚDO
        # =====================================================
        self.desenhar_conteudo_rolavel(tela)
        # =====================================================
        # BOTÃO VOLTAR
        # =====================================================
        cx = self.jogo.largura // 2
        x_ini = (cx - self.largura_botao // 2)

        y_ini = (self.y_botao - self.altura_botao // 2)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        hover = (x_ini <= mouse_x <= x_ini + self.largura_botao and y_ini <= mouse_y <= y_ini + self.altura_botao)

        if hover:
            cor_botao = (90, 190, 245)
        else:
            cor_botao = (60, 160, 225)

        pontos_botao = [
            (x_ini, y_ini),
            (x_ini + self.largura_botao, y_ini),
            (x_ini + self.largura_botao, y_ini + self.altura_botao),
            (x_ini, y_ini + self.altura_botao)
        ]
        scanline_fill(tela, pontos_botao, cor_botao)
        desenhar_poligono(tela, pontos_botao, (255, 255, 255))

        txt_voltar = self.fonte_botao.render("VOLTAR", True, (10, 25, 45))

        tela.blit(txt_voltar, txt_voltar.get_rect(center= (cx, self.y_botao)))

class EstadoFim(Estado):

    def __init__(self, jogo, mensagem):
        super().__init__(jogo)

        self.mensagem = mensagem
        self.menu_visual = EstadoMenu(self.jogo)
        self.fonte_titulo = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 48)
        self.fonte_mensagem = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 36)
        self.fonte_pequena = pygame.font.Font("assets/fonte/DiaryOfAWimpyKidFontRegular.ttf", 22)

        # =====================================================
        # PAINEL
        # =====================================================
        self.largura_painel = 600
        self.altura_painel = 280

        self.x_painel = (self.jogo.largura // 2 - self.largura_painel // 2)

        self.y_painel = (self.jogo.altura // 2 - self.altura_painel // 2)

        # Botão
        self.largura_botao = 230
        self.altura_botao = 55
        self.y_botao = (self.y_painel + self.altura_painel - 55)

    def processar_eventos(self, eventos, teclas, mouse_pos, clicou):

        if teclas[pygame.K_RETURN]:
            self.jogo.mudar_estado(EstadoMenu(self.jogo))

        # Clique no botão
        if clicou:
            cx = self.jogo.largura // 2
            x_ini = (cx - self.largura_botao // 2)
            y_ini = (self.y_botao - self.altura_botao // 2)

            clicou_no_botao = (x_ini <= mouse_pos[0] <= x_ini + self.largura_botao and y_ini <= mouse_pos[1] <= y_ini + self.altura_botao)

            if clicou_no_botao:
                self.jogo.mudar_estado(EstadoMenu(self.jogo))

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):

        # =====================================================
        # CENÁRIO
        # =====================================================
        self.menu_visual.desenhar_cenario(tela)
        # =====================================================
        # PAINEL
        # =====================================================
        pontos_painel = [
            (self.x_painel, self.y_painel),
            (self.x_painel + self.largura_painel, self.y_painel),
            (self.x_painel + self.largura_painel, self.y_painel + self.altura_painel),
            (self.x_painel, self.y_painel + self.altura_painel)
        ]
        scanline_fill(tela, pontos_painel, (230, 240, 250))
        desenhar_poligono(tela, pontos_painel, (255, 255, 255))

        # =====================================================
        # TÍTULO
        # =====================================================
        txt_titulo = self.fonte_titulo.render("FIM DE JOGO", True, (10, 25, 45))
        tela.blit(txt_titulo, (self.jogo.largura // 2 - txt_titulo.get_width() // 2, self.y_painel + 30))

        # =====================================================
        # MENSAGEM
        # =====================================================
        txt_res = self.fonte_mensagem.render(self.mensagem, True, (20, 70, 100))
        tela.blit(txt_res, (self.jogo.largura // 2 - txt_res.get_width() // 2, self.y_painel + 105))

        # =====================================================
        # TEXTO DE CONTROLE
        # =====================================================
        txt_enter = self.fonte_pequena.render("Aperte ENTER para voltar ao menu", True, (40, 50, 60))
        tela.blit(txt_enter, (self.jogo.largura // 2 - txt_enter.get_width() // 2, self.y_painel + self.altura_painel + 15))
        