# Códigos de região de Cohen-Sutherland
DENTRO = 0  # 0000
ESQUERDA = 1 # 0001
DIREITA = 2  # 0010
INFERIOR = 4 # 0100
SUPERIOR = 8 # 1000

def _calcular_codigo_regiao(x, y, x_min, y_min, x_max, y_max):

    codigo = DENTRO
    if x < x_min:
        codigo |= ESQUERDA
    elif x > x_max:
        codigo |= DIREITA

    if y < y_min:
        codigo |= INFERIOR
    elif y > y_max:
        codigo |= SUPERIOR

    return codigo

def cohen_sutherland(x0, y0, x1, y1, x_min, y_min, x_max, y_max):

    # calculo o outcode dos dois pontos
    codigo0 = _calcular_codigo_regiao(x0, y0, x_min, y_min, x_max, y_max)
    codigo1 = _calcular_codigo_regiao(x1, y1, x_min, y_min, x_max, y_max)
    aceito = False  # indica se a reta deve ser aceita

    while True:     # continua até chegar a uma conclusão, aceita ou rejeita

        # caso 1: Ambos os pontos dentro da janela
        if (codigo0 | codigo1) == 0:
            aceito = True
            break
        # caso 2: ambos os pontos compartilham uma região externa (totalmente fora)
        elif (codigo0 & codigo1) != 0:
            break
        # caso 3: interseção necessária
        else: 
            x, y = 0.0, 0.0
            codigo_fora = codigo0 if codigo0 != DENTRO else codigo1    # escolhe o ponto que está fora

            # descobre qual borda da janela será atravessada e faz o devido cálculo para saber o x e y
            if codigo_fora & SUPERIOR:
                x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                y = y_max
            elif codigo_fora & INFERIOR:
                x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                y = y_min
            elif codigo_fora & DIREITA:
                y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                x = x_max
            elif codigo_fora & ESQUERDA:
                y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                x = x_min

            # descobre qual ponto tem que ser substituido e substitui
            if codigo_fora == codigo0:
                x0, y0 = x, y
                codigo0 = _calcular_codigo_regiao(x0, y0, x_min, y_min, x_max, y_max)
            else:
                x1, y1 = x, y
                codigo1 = _calcular_codigo_regiao(x1, y1, x_min, y_min, x_max, y_max)

    if aceito:
        return True, x0, y0, x1, y1     # retorna os pontos recortados
    else:
        return False, None, None, None, None         # ou none, se foi totalmente descartada
