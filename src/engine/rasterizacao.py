

def setPixel(superficie, x, y, color):
    # desenha um pixel com verificação de limites
    x = int(x)
    y = int(y)
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), color)

#==============================================
# Reta
#==============================================
def bresenham(superficie, x0, y0, x1, y1, cor):
    # BRESENHAM -> algoritmo de reta
    
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

    inclinada = abs(y1 -y0) > abs(x1 - x0)  # calcula se a reta é íngreme ou mais horizontal

    if inclinada:         # troca as coordenadas para poder trabalhar com a reta mais vertical
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:         # troca os x, para percorrer também no sentido da direita para esquerda
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # variações em x e y
    dx = x1 - x0
    dy = abs(y1 - y0)

    y_passo = 1 if y0 < y1 else -1  # decidir para qual direção y deve caminhar

    d = 2 * dy - dx         # erro/acumulador de decisão
    y = y0          # começa no ponto inicial

    for x in range(x0, x1 + 1):     # percorre cada posição horizontal

        if inclinada:
            setPixel(superficie, y, x, cor)    # destroca as coordenadas que foram trocadas anteriormente
        else:
            setPixel(superficie, x, y, cor)

        if d > 0:           # o erro acumulado indica que deve mudar o y
            y += y_passo
            d -= 2 * dx

        d += 2 * dy 

def desenhar_linha(superficie, x0, y0, x1, y1, cor):
    bresenham(superficie, x0, y0, x1, y1, cor)

#==============================================
# Círculo
#==============================================
def desenhar_circulo(superficie, xc, yc, r, cor):
    xc = int(xc)
    yc = int(yc)
    r = int(r)

    # começa no ponto (0,r), ou seja, no topo do círculo relativo ao centro
    x = 0
    y = r
    d = 1 - r

    def desenhar_octantes(cx, cy, px, py, c):
        setPixel(superficie, cx + px, cy + py, c)
        setPixel(superficie, cx - px, cy + py, c)
        setPixel(superficie, cx + px, cy - py, c)
        setPixel(superficie, cx - px, cy - py, c)
        setPixel(superficie, cx + py, cy + px, c)
        setPixel(superficie, cx - py, cy + px, c)
        setPixel(superficie, cx + py, cy - px, c)
        setPixel(superficie, cx - py, cy - px, c)

    desenhar_octantes(xc, yc, x, y, cor)    # no primeiro ponto (0,r)

    # enquanto estamos na região do círculo, # avançamos horizontalmente
    while x < y:
        x += 1          
        if d < 0:           # o valor de decisão indica se devemos manter ou mudar o y
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1

        desenhar_octantes(xc, yc, x, y, cor)

#==============================================
# Elipse
#==============================================
def desenhar_elipse(superficie, xc, yc, rx, ry, cor):
    xc = int(xc)
    yc = int(yc)
    rx = int(rx)
    ry = int(ry)

    # começa no topo da elipse, relativamente ao centro
    x = 0
    y = ry

    def desenhar_quadrantes(cx, cy, px, py, c):
        setPixel(superficie, cx + px, cy + py, c)
        setPixel(superficie, cx - px, cy + py, c)
        setPixel(superficie, cx + px, cy - py, c)
        setPixel(superficie, cx - px, cy - py, c)

    # a elipse tem regiões onde a curva muda de comportamento

    # região 1
    # parâmetro de decisão da primeira região
    d1 = (ry ** 2) - (rx ** 2 * ry) + (0.25 * rx ** 2)
    # controlam a mudança da inclinação
    dx = 2 * (ry ** 2) * x
    dy = 2 * (rx ** 2) * y

    while dx < dy:      # enquanto continuamos na primeira região
        desenhar_quadrantes(xc, yc, x, y, cor)    # desenha os quatros pixels
        x += 1          # avança horizontalmente
        dx += 2 * (ry ** 2) # atualiza o dx

        # decidi se mantém o y ou muda
        if d1 < 0:
            d1 += dx + (ry ** 2)
        else:
            y -= 1
            dy -= 2 * (rx ** 2)
            d1 += dx - dy + (ry ** 2)

    # região 2
     # parâmetro de decisão da segunda região
    d2 = ((ry ** 2) * ((x + 0.5) ** 2)) + ((rx ** 2) * ((y - 1) ** 2)) - ((rx ** 2) * (ry ** 2))

    while y >= 0:           # continuamos, enquanto y não fica negativo
        desenhar_quadrantes(xc, yc, x, y, cor)    # desenhamos
        y -= 1      # avançamos verticalmente
        dy -= 2 * (rx ** 2) # atualiza dy

        # decidi se mantém ou muda o x
        if d2 > 0:
            d2 += (rx ** 2) - dy
        else:
            x += 1
            dx += 2 * (ry ** 2)
            d2 += dx - dy + (rx ** 2)

#==============================================
# Flood fill
#==============================================
def flood_fill(superficie, x_inicio, y_inicio, cor_preenchimento):
    x_inicio = int(x_inicio)
    y_inicio = int(y_inicio)

    # pega o tamanho da tela
    largura = superficie.get_width()
    altura = superficie.get_height()

    if not (0 <= x_inicio < largura and 0 <= y_inicio < altura):    # se o ponto estiver fora, ignora
        return

    cor_alvo = superficie.get_at((x_inicio, y_inicio))[:3]
    cor_preenchimento_rgb = cor_preenchimento[:3]   # pega as "coordenadas" do rgb

    if cor_alvo == cor_preenchimento_rgb:
        return

    pilha = [(x_inicio, y_inicio)]

    while pilha:        # enquanto existirem pontos para analisar, continua o flood fill
        x, y = pilha.pop()    # remove o último elemento da pilha (LIFO = last in, first out)

        if 0 <= x < largura and 0 <= y < altura:
            if superficie.get_at((x, y))[:3] == cor_alvo:
                setPixel(superficie, x, y, cor_preenchimento)
                # adiciona os 4 vizinhos
                pilha.append((x + 1, y))
                pilha.append((x - 1, y))
                pilha.append((x, y + 1))
                pilha.append((x, y - 1))

#==============================================
# Scanline
#==============================================
def scanline_fill(superficie, pontos, cor):
    # preenchimento scanline para polígonos com uma única cor
    
    if len(pontos) < 3:     # um polígono tem no mínimo três pontos
        return

    ys = [p[1] for p in pontos]    #pega todos os y dos pontos
    y_min = max(0, int(min(ys)))        # pega o menor y, converte para inteiro e garante que não seja menor que 0
    y_max = min(superficie.get_height() - 1, int(max(ys)))        # pega o maior y e garante que não passe da altura da tela

    n = len(pontos)

    for y in range(y_min, y_max + 1):   # percorre o y mínimo até o máximo

        intersecoes = []      # vai guardar os valores de x, onde o scanline cruza as bordas

        for i in range(n):      # percorre as arestas

            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]    # precisa do operador resto, para fecharmos o polígono

            if y0 == y1:    # ignora aresta horizontal
                continue
            
            if y0 > y1:     # organiza a ordem da aresta para facilitar cálculo
                x0, y0, x1, y1 = x1, y1, x0, y0

            if y < y0 or y >= y1:   # se a scanline cruza a aresta
                continue

            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)   # encontrar o x onde a scanline y cruza a aresta
            intersecoes.append(x)     # adiciona a interseção

        intersecoes.sort()    # organiza as interseções, porque vamos trabalhar em pares

        for i in range(0, len(intersecoes), 2):   # percorre de dois em dois

            if i + 1 < len(intersecoes):  # garante que existe um segundo elemento

                # converte as interseções para inteiros
                x_inicio = int(intersecoes[i])
                x_fim = int(intersecoes[i + 1])

                # encontrou esquerda, encontrou direita, então preenche todos os pontos entre elas
                for x in range(x_inicio, x_fim + 1):
                    setPixel(superficie, x, y, cor)

def scanline_textura(superficie, vertices_texturizados, imagem_textura):

    if len(vertices_texturizados) < 3:  # um polígono precisa ter no mínimo três vértices
        return

    # pega o tamanho da textura
    largura_tex = imagem_textura.get_width()
    altura_tex = imagem_textura.get_height()


    ys = [p[0][1] for p in vertices_texturizados]  # pega todos os y dos pontos
    y_min = max(0, int(min(ys)))
    y_max = min(superficie.get_height() - 1, int(max(ys)))

    n = len(vertices_texturizados)

    for y in range(y_min, y_max + 1):       # percorre o y mínimo até o máximo

        intersecoes = []   # guardar os valores de x, onde o scanline cruza as bordas e também o (u,v) naquele ponto

        for i in range(n):      # percorre as arestas

            (x0, y0), (u0, v0) = vertices_texturizados[i]
            (x1, y1), (u1, v1) = vertices_texturizados[(i + 1) % n]    # precisa do operador resto, para fecharmos o polígono

            if y0 == y1:    # ignora aresta horizontal
                continue

            if y0 > y1:     # # organiza a ordem da aresta para facilitar cálculo
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:   # # se a scanline cruza a aresta
                continue

            # o parâmetro t -> quanto avançamos do ponto inicial até o ponto final da aresta.
            t = (y - y0) / (y1 - y0)
            # encontra o x da interseção
            x = x0 + t * (x1 - x0)
            # Interpolação de UV na aresta
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)
            
            intersecoes.append((x, u, v))     # guardamos a interseção

        intersecoes.sort(key=lambda item: item[0])      # ordena pela coordenada x

        for i in range(0, len(intersecoes), 2):     # percorre as interseções em pares
            if i + 1 < len(intersecoes):    # garante que existe um segundo elemento

                # pega o início e o fim 
                x_inicio, u_inicio, v_inicio = intersecoes[i]
                x_fim, u_fim, v_fim = intersecoes[i + 1]
                xi = int(x_inicio)
                xf = int(x_fim)

                largura_segmento = x_fim - x_inicio    # distância horizontal entre as duas interseções

                for x in range(xi, xf + 1):
                    t_x = 0.0 if largura_segmento == 0 else (x - x_inicio) / largura_segmento
                    u_pixel = u_inicio + t_x * (u_fim - u_inicio)
                    v_pixel = v_inicio + t_x* (v_fim - v_inicio)

                    # Mapeia (u, v) normalizados para os pixels reais da textura
                    tx = max(0, min(largura_tex - 1, int(u_pixel * (largura_tex - 1))))
                    ty = max(0, min(altura_tex - 1, int(v_pixel * (altura_tex - 1))))

                    rgba = imagem_textura.get_at((tx, ty))

                    # Se o pixel for transparente (Alpha < 128), pula sem desenhar no framebuffer
                    if len(rgba) > 3 and rgba[3] < 128:
                        continue

                    cor_pixel = rgba[:3]
                    setPixel(superficie, x, y, cor_pixel)

# Função auxiliar de interpolação
def interpolaCor(cor1, cor2, t):
    # Interpolação linear entre duas cores RGB
    r = int(cor1[0] + (cor2[0] - cor1[0]) * t)
    g = int(cor1[1] + (cor2[1] - cor1[1]) * t)
    b = int(cor1[2] + (cor2[2] - cor1[2]) * t)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

def scanline_fill_gradiente(superficie, pontos_com_cor):

    if len(pontos_com_cor) < 3:     
        return

    ys = [p[0][1] for p in pontos_com_cor]
    y_min = max(0, int(min(ys)))
    y_max = min(superficie.get_height() - 1, int(max(ys)))
    n = len(pontos_com_cor)

    for y in range(y_min, y_max + 1):
        intersecoes = []

        for i in range(n):
            (x0, y0), cor0 = pontos_com_cor[i]
            (x1, y1), cor1 = pontos_com_cor[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                cor0, cor1 = cor1, cor0

            if y < y0 or y >= y1:
                continue
            # até aqui usou o mesmo processo do scanline normal, implementado anteriormente
            
            t = (y - y0) / (y1 - y0)    # parâmetro que indica a posição relativa entre os dois vértices (varia entre o início(0) e fim(1) da aresta)
            x = x0 + t * (x1 - x0)      # encontra o x correspondente ao y
            
            # Interpolação RGB na aresta
            cor_interpolada = interpolaCor(cor0, cor1, t)
            
            intersecoes.append((x, cor_interpolada)) # adiciona à interseção

        intersecoes.sort(key=lambda item: item[0])  # ordena pela primeira coordenada da interseção

        # mesma lógica usada no scanline normal, com algumas mudanças que estão anotadas
        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):

                # pega as duas extremidades
                x_inicio, cor_inicio = intersecoes[i]
                x_fim, cor_fim = intersecoes[i + 1]

                xi = int(round(x_inicio))
                xf = int(round(x_fim))

                largura_segmento = x_fim - x_inicio    # distância horizontal entre as duas interseções

                for x in range(xi, xf + 1):
                    t_x = 0.0 if largura_segmento == 0 else (x - x_inicio) / largura_segmento
                    cor_pixel = interpolaCor(cor_inicio, cor_fim, t_x)
                    setPixel(superficie, x, y, cor_pixel)



#==============================================
# Desenhar polígono
#==============================================
def desenhar_poligono(superficie, pontos, cor):
    n = len(pontos)

    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]
        bresenham(superficie,x0, y0,x1, y1,cor)

def retangulo_para_poligono(x, y, largura, altura):
    # passa um retângulo para vértices de um polígono
    return [
        (x, y),
        (x + largura, y),
        (x + largura, y + altura),
        (x, y + altura)
    ]
