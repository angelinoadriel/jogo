from engine.transformacoes import translacao, escala, multiplica_matrizes

def matriz_mundo_para_viewport(window, viewport):

    xw_min, yw_min, xw_max, yw_max = window
    xv_min, yv_min, xv_max, yv_max = viewport

    sx = (xv_max - xv_min) / (xw_max - xw_min)
    sy = (yv_max - yv_min) / (yw_max - yw_min)

    # M = T(xv_min, yv_min) * S(sx, sy) * T(-xw_min, -yw_min)
    t1 = translacao(-xw_min, -yw_min)
    s  = escala(sx, sy)
    t2 = translacao(xv_min, yv_min)

    return multiplica_matrizes(t2, multiplica_matrizes(s, t1))
