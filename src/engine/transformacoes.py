import math

def identidade():

    return [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
    ]

def translacao(tx, ty):  
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def escala(sx, sy):    
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotacao(angulo_rad):
    cos = math.cos(angulo_rad)
    sen = math.sin(angulo_rad)
    return [
        [cos, -sen, 0.0],
        [sen,  cos, 0.0],
        [0.0, 0.0, 1.0]
    ]

def multiplica_matrizes(A, B):
    C = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]   # cria uma matriz C inicialmente com zeros

    # calcula a multiplicação de matrizes, primeira linha com a primeira coluna
    for i in range(3):
        for j in range(3):
           for k in range(3):
                C[i][j] += A[i][k] * B[k][j]

    return C

def aplica_transformacao(M, pontos):

    novos_pontos = []
    for x, y in pontos:

        v = [x, y, 1]

        x_novo = (
            M[0][0] * v[0] +
            M[0][1] * v[1] + 
            M[0][2]
        )

        y_novo = (
            M[1][0] * v[0] +
            M[1][1] * v[1] +
            M[1][2]
        )

        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def rotacionar(C, alfa):
    # aplica rotação alfa à matriz de transformação C (rotaciona em torno da posição atual).
    
    R = rotacao(alfa)

    # posição atual (tx, ty)
    tx = C[0][2]
    ty = C[1][2]

    T = translacao(-tx, -ty)
    T_inv = translacao(tx, ty)

    return multiplica_matrizes(
        T_inv,
        multiplica_matrizes(
            R,
            multiplica_matrizes(T, C)
        )
    )
