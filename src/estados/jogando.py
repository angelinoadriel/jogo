import pygame
import random

from config.constantes import (
    MAX_PASTAS_FASE,
    INTERVALO_SPAWN_PASTA,
    POSICAO_INICIAL_JOGADOR_Y,
    MARGEM_HORIZONTAL_OBJETOS,
    MSG_PERDER_VIDAS
)
from config.caminhos import (
    CENARIO,
    COCO_POMBO,
    PAPEL_1,
    PAPEL_2,
    PROFESSOR_PARADO,
    professor_correndo,
    CAMISA_VIDA
)
from config.dificuldades import DIFICULDADES
from engine.rasterizacao import (
    desenhar_poligono
)
from engine.textura import scanline_textura
from engine.colisoes import colisao_poligonos_aabb
from entities import (
    Jogador,
    Pasta,
    CocoPombo
)
from estados.estado import Estado
from estados.fim import EstadoFim
from ui import HUD
from ui import MiniMapa
from config.cores import Cores



class EstadoJogando(Estado):

    def __init__(self, jogo):
        
        super().__init__(jogo)


        # Recursos
        self.imagem_camisa = self.jogo.recursos.carregar_imagem(CAMISA_VIDA)

        self.imagem_cenario = self.jogo.recursos.carregar_imagem(CENARIO)


        # Cenário
        w, h = self.jogo.largura, self.jogo.altura
        self.buffer_fundo = pygame.Surface((w, h))
        # 3. Define os vértices do polígono do fundo
        vertices_cenario = [
            ((0, 0), (0.0, 0.0)),
            ((w, 0), (1.0, 0.0)),
            ((w, h), (1.0, 1.0)),
            ((0, h), (0.0, 1.0))
        ]
        # 4. EXECUTA O SCANLINE DE TEXTURA APENAS UMA VEZ AQUI
        scanline_textura(self.buffer_fundo, vertices_cenario, self.imagem_cenario)


        # Texturas
        self.texturas_pasta = [
            self.jogo.recursos.carregar_imagem(PAPEL_1, recortar_transparencia=True),
            self.jogo.recursos.carregar_imagem(PAPEL_2, recortar_transparencia=True)
        ]
        
        self.textura_coco = self.jogo.recursos.carregar_imagem(COCO_POMBO, recortar_transparencia=True)

        self.textura_jogador_parado = (self.jogo.recursos.carregar_imagem(PROFESSOR_PARADO, recortar_transparencia=True))
        self.texturas_jogador_corrida = []
        for i in range(1, 9):
            textura = (self.jogo.recursos.carregar_imagem(professor_correndo(i), recortar_transparencia=True))
            self.texturas_jogador_corrida.append(textura)        


        # Jogador        
        self.jogador = Jogador(self.textura_jogador_parado,self.texturas_jogador_corrida)      # cria uma instância da classe Jogador

        # =====================================================
        # ESTADO DA PARTIDA
        # =====================================================

        self.objetos_caindo = []

        self.max_pastas_fase = MAX_PASTAS_FASE

        self.total_pastas_lancadas = 0
        self.pastas_coletadas = 0
        self.pastas_em_jogo = 0

        self.temporizador_pasta = 0.0
        self.temporizador_coco = 0.0

        self.vidas = 0
        self.vidas_maximas = 0

        self.meta = 0.0
        self.vel_queda = 0.0
        self.freq_coco = 0.0

        self.mostrar_colisoes = False

        # Componentes
        self.hud = HUD(self.jogo, self.imagem_camisa)
        self.minimapa = MiniMapa(self.jogo)
    

    def entrar(self):
        self.iniciar_partida()

    def iniciar_partida(self):

        # =================================================
        # LIMPA OBJETOS DA PARTIDA ANTERIOR
        # =================================================
        self.objetos_caindo.clear()

        # =================================================
        # CONTADORES
        # =================================================
        self.total_pastas_lancadas = 0
        self.pastas_coletadas = 0
        self.pastas_em_jogo = 0

        # =================================================
        # TEMPORIZADORES
        # =================================================
        self.temporizador_pasta = 0.0
        self.temporizador_coco = 0.0

        # =================================================
        # DIFICULDADE
        # =================================================
        self._aplicar_dificuldade()
        self.vidas_maximas = self.vidas

        # =================================================
        # JOGADOR
        # =================================================
        self.jogador.x = (self.jogo.largura / 2)
        self.jogador.y = (POSICAO_INICIAL_JOGADOR_Y)
        self.jogador.vel_x = 0.0
        self.jogador.vel_y = 0.0
        self.jogador.cor = Cores.JOGADOR

        # =================================================
        # ANIMAÇÃO
        # =================================================
        self.jogador.indice_frame = 0
        self.jogador.tempo_animacao = 0.0
        self.jogador.movendo = False

        # =================================================
        # DEBUG
        # =================================================
        self.mostrar_colisoes = False


    def sair(self):
        self.jogador.vel_x = 0
        self.jogador.vel_y = 0

        
    # verifica qual a dificuldade escolhida, se não começa com 'normal'
    def _aplicar_dificuldade(self):
        config = DIFICULDADES[
            self.jogo.dificuldade_atual
        ]

        self.vidas = config.vidas
        self.meta = config.meta
        self.vel_queda = config.velocidade_pasta
        self.freq_coco = config.frequencia_coco



    def processar_eventos(self, entrada):
        self.jogador.vel_x = 0

        if entrada.teclas[pygame.K_LEFT] or entrada.teclas[pygame.K_a]:
            self.jogador.vel_x = -self.jogador.vel_movimento

        if entrada.teclas[pygame.K_RIGHT] or entrada.teclas[pygame.K_d]:
            self.jogador.vel_x = self.jogador.vel_movimento

        # Ativa/desativa visualização das caixas de colisão
        for evento in entrada.eventos:

            if (evento.type == pygame.KEYDOWN and evento.key == pygame.K_F3):
                self.mostrar_colisoes = (not self.mostrar_colisoes)

    def atualizar(self, dt):
        self.jogador.atualizar(dt)                      # jogador atualiza a posição
        self.jogador.x = max(30, min(self.jogo.largura - 30, self.jogador.x))   # limita para que o jogador não saia da tela

        # Lógica de Spawn
        if self.total_pastas_lancadas < self.max_pastas_fase:           # enquanto não tiver lançados 30 pastas
            self.temporizador_pasta += dt                               # acumula o temporizador da pasta
            if self.temporizador_pasta >= INTERVALO_SPAWN_PASTA:        # a cada 0.8s
                pasta = Pasta(random.choice(self.texturas_pasta))       # cria uma pasta
                pasta.x = random.randint(MARGEM_HORIZONTAL_OBJETOS, self.jogo.largura - MARGEM_HORIZONTAL_OBJETOS)    # posição da pasta
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
            coco.x = random.randint(MARGEM_HORIZONTAL_OBJETOS, self.jogo.largura - MARGEM_HORIZONTAL_OBJETOS)
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

            elif obj.y > self.jogo.altura + 50:             # caso passe do chão, inativa o objeto
                obj.ativa = False
                if isinstance(obj, Pasta):
                    self.pastas_em_jogo -= 1

        self.objetos_caindo = [obj for obj in self.objetos_caindo if obj.ativa]         # cria uma nova lista somente com os obejtos ativos


        # Condição de Fim
        
        progresso = self.pastas_coletadas / self.max_pastas_fase
        if self.vidas <= 0:
            self.jogo.mudar_estado(EstadoFim(self.jogo, MSG_PERDER_VIDAS))
        
        elif self.total_pastas_lancadas >= self.max_pastas_fase and self.pastas_em_jogo == 0:
            if progresso >= self.meta:
                self.jogo.mudar_estado(EstadoFim(self.jogo, f"PARABÉNS! Você recuperou {int(progresso*100)}% das pastas!"))
            else:
                self.jogo.mudar_estado(EstadoFim(self.jogo, f"DERROTA! Salvou apenas {int(progresso*100)}% das pastas."))

    

    def desenhar_colisoes(self, tela):
        if not self.mostrar_colisoes:
            return

        # -------------------------
        # Jogador
        # -------------------------
        pontos = (self.jogador.obter_pontos_colisao_mundo())
        desenhar_poligono(tela, pontos, Cores.COLISAO)

        # -------------------------
        # Objetos
        # -------------------------

        for obj in self.objetos_caindo:

            pontos = (obj.obter_pontos_colisao_mundo())
            desenhar_poligono(tela, pontos, Cores.COLISAO)



    def desenhar(self, tela):
        # Fundo
        tela.blit(self.buffer_fundo, (0, 0))

        # Jogador
        self.jogador.desenhar(tela)

        # Objetos
        for obj in self.objetos_caindo:
            obj.desenhar(tela)

        # HUD
        self.hud.desenhar(tela, self.vidas, self.vidas_maximas, self.pastas_coletadas, self.max_pastas_fase)

        # Minimapa
        self.minimapa.desenhar(tela, self.jogador, self.objetos_caindo)

        # Colisões
        self.desenhar_colisoes(tela)
