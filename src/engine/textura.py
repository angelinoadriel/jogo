import pygame

def scanline_textura(superficie, vertices_texturizados, imagem_textura, usar_alpha=False):

    if len(vertices_texturizados) < 3:
        return

    largura_tex = imagem_textura.get_width()
    altura_tex = imagem_textura.get_height()

    w_sup = superficie.get_width()
    h_sup = superficie.get_height()

    ys = [p[0][1] for p in vertices_texturizados]
    y_min = max(0, int(min(ys)))
    y_max = min(h_sup - 1, int(max(ys)))

    n = len(vertices_texturizados)

    # =====================================================
    # ACESSO DIRETO AOS PIXELS
    # =====================================================
    px_dst = pygame.PixelArray(superficie)
    px_src = pygame.PixelArray(imagem_textura)

    # =====================================================
    # SCANLINES
    # =====================================================
    for y in range(y_min, y_max + 1):

        intersecoes = []

        for i in range(n):

            (x0, y0), (u0, v0) = (vertices_texturizados[i])
            (x1, y1), (u1, v1) = (vertices_texturizados[(i + 1) % n])

            # ---------------------------------------------
            # Aresta horizontal
            # ---------------------------------------------
            if y0 == y1:
                continue

            # ---------------------------------------------
            # Organiza a aresta
            # ---------------------------------------------
            if y0 > y1:
                x0, y0, x1, y1 = (x1, y1, x0, y0)
                u0, v0, u1, v1 = (u1, v1, u0, v0)

            # ---------------------------------------------
            # Verifica se a scanline cruza a aresta
            # ---------------------------------------------
            if y < y0 or y >= y1:
                continue

            # ---------------------------------------------
            # Interpolação vertical
            # ---------------------------------------------
            t = ((y - y0) / (y1 - y0))
            x = (x0 + t * (x1 - x0))
            u = (u0 + t * (u1 - u0))
            v = (v0 + t * (v1 - v0))

            intersecoes.append((x, u, v))

        # =================================================
        # ORDENA INTERSEÇÕES
        # =================================================
        intersecoes.sort(key=lambda item: item[0])

        # =================================================
        # PREENCHIMENTO DOS SEGMENTOS
        # =================================================
        for i in range(0, len(intersecoes), 2):

            if i + 1 >= len(intersecoes):
                continue

            (x_inicio, u_inicio, v_inicio) = intersecoes[i]
            (x_fim, u_fim, v_fim) = intersecoes[i + 1]
            xi = max(0, int(x_inicio))
            xf = min(w_sup - 1, int(x_fim))

            largura_segmento = (x_fim - x_inicio)

            if largura_segmento <= 0:
                continue

            inv_largura = (1.0 / largura_segmento)

            passo_u = (u_fim - u_inicio) * inv_largura
            passo_v = (v_fim - v_inicio) * inv_largura

            deslocamento_inicial = (xi - x_inicio)
            u_atual = (u_inicio + deslocamento_inicial * passo_u)
            v_atual = (v_inicio + deslocamento_inicial * passo_v)

            for x in range(xi, xf + 1):

                # -----------------------------------------
                # Coordenada atual da textura
                # -----------------------------------------
                tx = int(u_atual * (largura_tex - 1))
                ty = int(v_atual * (altura_tex - 1))

                # -----------------------------------------
                # Limita coordenadas
                # -----------------------------------------
                if tx < 0:
                    tx = 0

                elif tx >= largura_tex:
                    tx = largura_tex - 1

                if ty < 0:
                    ty = 0

                elif ty >= altura_tex:
                    ty = altura_tex - 1

                # -----------------------------------------
                # Lê pixel da textura
                # -----------------------------------------
                cor_inteira = px_src[tx, ty]

                # -----------------------------------------
                # Alpha
                # -----------------------------------------
                if usar_alpha:

                    _, _, _, a = imagem_textura.unmap_rgb(cor_inteira)

                    if a == 0:
                        u_atual += passo_u
                        v_atual += passo_v
                        continue

                # -----------------------------------------
                # Escreve pixel
                # -----------------------------------------
                px_dst[x, y] = cor_inteira

                # -----------------------------------------
                # Avança na textura
                # -----------------------------------------
                u_atual += passo_u
                v_atual += passo_v

    # =====================================================
    # LIBERA OS PixelArrays
    # =====================================================
    del px_dst
    del px_src