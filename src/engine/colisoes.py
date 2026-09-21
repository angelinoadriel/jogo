def obter_aabb(poligono):
    """
    Calcula a caixa delimitadora alinhada aos eixos (AABB) de um polígono transformado.
    Retorna (min_x, min_y, max_x, max_y).
    """
    xs = [p[0] for p in poligono]
    ys = [p[1] for p in poligono]
    return min(xs), min(ys), max(xs), max(ys)


def colisao_aabb(box1, box2):
    """
    Verifica se duas AABBs (min_x, min_y, max_x, max_y) estão se sobrepondo.
    """
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # Se estiver fora em qualquer um dos eixos, não há colisão
    if x1_max < x2_min or x1_min > x2_max:
        return False
    if y1_max < y2_min or y1_min > y2_max:
        return False

    return True


def colisao_poligonos_aabb(poligono1, poligono2):
    """
    Verifica a colisão entre dois polígonos quaisquer usando suas AABBs.
    """
    box1 = obter_aabb(poligono1)
    box2 = obter_aabb(poligono2)
    return colisao_aabb(box1, box2)