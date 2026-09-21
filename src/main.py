import pygame
import sys
import random

from game.entidades import Jogador, Pasta, CocoPombo
from engine.rasterizacao import scanline_fill, desenhar_poligono
from engine.colisoes import colisao_poligonos_aabb

# Estados do Jogo
MENU = 0
JOGANDO = 1
FIM = 2

def main():
    pygame.init()
    LARG, ALT = 800, 600
    tela = pygame.display.set_mode((LARG, ALT))
    pygame.display.set_caption("Desastre no NC2A")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("Arial", 24, bold=True)
    fonte_grande = pygame.font.SysFont("Arial", 48, bold=True)

    estado = MENU
    dificuldade_nome = ""
    
    # Variáveis de Sessão
    jogador = None
    objetos_caindo = []
    
    vidas = 0
    meta_percentual = 0
    vel_queda = 0
    frequencia_pombos = 0
    
    total_pastas_lancadas = 0
    pastas_coletadas = 0
    max_pastas_fase = 30
    
    temporizador_pasta = 0.0
    temporizador_coco = 0.0

    mensagem_final = ""

    def iniciar_jogo(dificuldade):
        nonlocal estado, jogador, objetos_caindo, vidas, meta_percentual, vel_queda, frequencia_pombos
        nonlocal total_pastas_lancadas, pastas_coletadas, temporizador_pasta, temporizador_coco, dificuldade_nome
        
        estado = JOGANDO
        jogador = Jogador()
        jogador.x = LARG / 2
        jogador.y = ALT - 50 # Posição perto do chão
        objetos_caindo = []
        
        total_pastas_lancadas = 0
        pastas_coletadas = 0
        temporizador_pasta = 0.0
        temporizador_coco = 0.0

        if dificuldade == 1:
            dificuldade_nome = "FÁCIL"
            vidas = 5
            meta_percentual = 0.3
            vel_queda = 150.0
            frequencia_pombos = 2.0  # Um cocô a cada 2 segundos
        elif dificuldade == 2:
            dificuldade_nome = "NORMAL"
            vidas = 3
            meta_percentual = 0.5
            vel_queda = 250.0
            frequencia_pombos = 1.0
        elif dificuldade == 3:
            dificuldade_nome = "DIFÍCIL"
            vidas = 1
            meta_percentual = 0.7
            vel_queda = 400.0
            frequencia_pombos = 0.4 # Chovendo cocô

    rodando = True
    while rodando:
        dt = relogio.tick(60) / 1000.0 
        tela.fill((30, 40, 50)) # Fundo cinza azulado escuro (Prédio NC2A à noite)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()

        if estado == MENU:
            # Renderização do Menu
            titulo = fonte_grande.render("DESASTRE NO NC2A", True, (255, 255, 0))
            instrucoes1 = fonte.render("Pressione 1 - Fácil (5 Vidas, 30% Pastas)", True, (100, 255, 100))
            instrucoes2 = fonte.render("Pressione 2 - Normal (3 Vidas, 50% Pastas)", True, (255, 255, 100))
            instrucoes3 = fonte.render("Pressione 3 - Difícil (1 Vida, 70% Pastas)", True, (255, 100, 100))
            
            tela.blit(titulo, (LARG//2 - titulo.get_width()//2, 100))
            tela.blit(instrucoes1, (LARG//2 - instrucoes1.get_width()//2, 250))
            tela.blit(instrucoes2, (LARG//2 - instrucoes2.get_width()//2, 300))
            tela.blit(instrucoes3, (LARG//2 - instrucoes3.get_width()//2, 350))

            if teclas[pygame.K_1]: iniciar_jogo(1)
            if teclas[pygame.K_2]: iniciar_jogo(2)
            if teclas[pygame.K_3]: iniciar_jogo(3)

        elif estado == JOGANDO:
            # --- ATUALIZAÇÃO ---
            
            # Movimentação do Jogador
            jogador.vel_x = 0
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                jogador.vel_x = -jogador.vel_movimento
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                jogador.vel_x = jogador.vel_movimento
                
            jogador.atualizar(dt)
            # Trava o jogador na tela
            jogador.x = max(20, min(LARG - 20, jogador.x))

            # Lógica de Spawn (Geração) de Itens
            if total_pastas_lancadas < max_pastas_fase:
                temporizador_pasta += dt
                if temporizador_pasta >= 0.8: # A cada 0.8s cai uma pasta
                    nova_pasta = Pasta()
                    nova_pasta.x = random.randint(30, LARG - 30)
                    nova_pasta.y = -20
                    nova_pasta.vel_y = vel_queda
                    objetos_caindo.append(nova_pasta)
                    total_pastas_lancadas += 1
                    temporizador_pasta = 0.0

            temporizador_coco += dt
            if temporizador_coco >= frequencia_pombos:
                novo_coco = CocoPombo()
                novo_coco.x = random.randint(30, LARG - 30)
                novo_coco.y = -20
                novo_coco.vel_y = vel_queda * 1.2 # Cocô cai um pouco mais rápido
                objetos_caindo.append(novo_coco)
                temporizador_coco = 0.0

            # Atualização e Colisão
            pontos_jogador = jogador.obter_pontos_mundo()
            
            for obj in objetos_caindo:
                if not obj.ativa: continue
                
                obj.atualizar(dt)
                pontos_obj = obj.obter_pontos_mundo()
                
                # Checa colisão usando a sua Engine!
                if colisao_poligonos_aabb(pontos_jogador, pontos_obj):
                    obj.ativa = False
                    
                    if isinstance(obj, Pasta):
                        pastas_coletadas += 1
                    elif isinstance(obj, CocoPombo):
                        vidas -= 1
                        # Jogador "sujo" (Fica marrom por um instante)
                        jogador.cor = (139, 69, 19) 
                
                # Destrói objeto se passar do chão
                if obj.y > ALT + 50:
                    obj.ativa = False

            # Limpa lista de inativos
            objetos_caindo = [obj for obj in objetos_caindo if obj.ativa]
            
            # Restaura cor original do jogador gradativamente se ele se sujou
            if jogador.cor != (50, 150, 200):
                 jogador.cor = (50, 150, 200)

            # CONDIÇÕES DE VITÓRIA / DERROTA
            progresso_atual = pastas_coletadas / max_pastas_fase
            
            if vidas <= 0:
                mensagem_final = "DERROTA! Você sujou todas as camisas e não pôde entrar na reunião!"
                estado = FIM
            elif total_pastas_lancadas >= max_pastas_fase and len(objetos_caindo) == 0:
                if progresso_atual >= meta_percentual:
                    mensagem_final = f"VITÓRIA! Você resgatou {int(progresso_atual*100)}% das pastas!"
                else:
                    mensagem_final = f"DERROTA! Você salvou apenas {int(progresso_atual*100)}%. Faltaram dados na reunião!"
                estado = FIM

            # --- RENDERIZAÇÃO DA ENGINE ---
            
            # Desenha jogador
            scanline_fill(tela, jogador.obter_pontos_mundo(), jogador.cor)
            desenhar_poligono(tela, jogador.obter_pontos_mundo(), (255, 255, 255))
            
            # Desenha itens
            for obj in objetos_caindo:
                scanline_fill(tela, obj.obter_pontos_mundo(), obj.cor)
                desenhar_poligono(tela, obj.obter_pontos_mundo(), (0, 0, 0)) # Borda preta

            # --- HUD (Textos) ---
            txt_vidas = fonte.render(f"Camisas (Vidas): {vidas}", True, (255, 255, 255))
            txt_pastas = fonte.render(f"Pastas: {pastas_coletadas}/{max_pastas_fase}", True, (255, 255, 255))
            txt_meta = fonte.render(f"Meta: {int(meta_percentual*100)}%", True, (200, 200, 200))
            
            tela.blit(txt_vidas, (20, 20))
            tela.blit(txt_pastas, (20, 50))
            tela.blit(txt_meta, (LARG - 150, 20))
            
        elif estado == FIM:
            # Tela de Fim de Jogo
            txt_resultado = fonte_grande.render(mensagem_final, True, (255, 255, 255))
            # Escala do texto para caber se for muito grande
            txt_resultado = pygame.transform.scale(txt_resultado, (min(760, txt_resultado.get_width()), txt_resultado.get_height()))
            
            instrucoes_voltar = fonte.render("Pressione ENTER para voltar ao Menu", True, (200, 200, 200))
            
            tela.blit(txt_resultado, (LARG//2 - txt_resultado.get_width()//2, ALT//2 - 50))
            tela.blit(instrucoes_voltar, (LARG//2 - instrucoes_voltar.get_width()//2, ALT//2 + 50))

            if teclas[pygame.K_RETURN]:
                estado = MENU

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()