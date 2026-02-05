from configs import *
from utils import copiar


def direcoes(p):
    if p in (DAMA_H, DAMA_IA):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if p == HUMANO:
        return [(-1, -1), (-1, 1)]
    if p == IA:
        return [(1, -1), (1, 1)]
    return []


def pode_capturar(p, peca_inimiga):
    """Verifica se uma peça pode capturar outra peça"""
    if p in (HUMANO, DAMA_H):
        return peca_inimiga in (IA, DAMA_IA)  # Humano só captura IA
    elif p in (IA, DAMA_IA):
        return peca_inimiga in (HUMANO, DAMA_H)  # IA só captura Humano
    return False


def gerar_capturas(tab, x, y, p, caminho=None, capturadas=None):
    if caminho is None:
        caminho = [(x, y)]
    if capturadas is None:
        capturadas = []

    resultados = []

    if p in (DAMA_H, DAMA_IA):
        # Capturas para damas
        for dx, dy in direcoes(p):
            nx, ny = x + dx, y + dy

            # Procura uma peça inimiga na direção
            while 0 <= nx < 8 and 0 <= ny < 8 and tab[nx][ny] == VAZIO:
                nx += dx
                ny += dy

            # Se encontrou uma peça, verifica se é inimiga
            if 0 <= nx < 8 and 0 <= ny < 8 and pode_capturar(p, tab[nx][ny]):
                # Posição após a peça capturada
                lx, ly = nx + dx, ny + dy

                # Verifica se pode pousar em alguma casa vazia após a captura
                while 0 <= lx < 8 and 0 <= ly < 8 and tab[lx][ly] == VAZIO:
                    # Cria tabuleiro temporário para a captura
                    novo = copiar(tab)
                    novo[lx][ly] = novo[x][y]
                    novo[x][y] = VAZIO
                    novo[nx][ny] = VAZIO  # Remove a peça capturada

                    # Recursão para capturas múltiplas
                    sub = gerar_capturas(
                        novo, lx, ly, p,
                        caminho + [(lx, ly)],
                        capturadas + [(nx, ny)]
                    )

                    if sub:
                        resultados.extend(sub)
                    else:
                        resultados.append((caminho + [(lx, ly)], capturadas + [(nx, ny)]))

                    lx += dx
                    ly += dy
    else:
        # Capturas para peças comuns
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            mx, my = x + dx, y + dy
            nx, ny = x + 2 * dx, y + 2 * dy

            if 0 <= nx < 8 and 0 <= ny < 8:
                # Verifica se há uma peça inimiga adjacente e casa vazia após
                if (tab[mx][my] != VAZIO and
                        pode_capturar(p, tab[mx][my]) and
                        tab[nx][ny] == VAZIO):

                    # Cria tabuleiro temporário para a captura
                    novo = copiar(tab)
                    novo[nx][ny] = novo[x][y]
                    novo[x][y] = VAZIO
                    novo[mx][my] = VAZIO

                    # Recursão para capturas múltiplas
                    sub = gerar_capturas(
                        novo, nx, ny, p,
                        caminho + [(nx, ny)],
                        capturadas + [(mx, my)]
                    )

                    if sub:
                        resultados.extend(sub)
                    else:
                        resultados.append((caminho + [(nx, ny)], capturadas + [(mx, my)]))

    return resultados


def gerar_movimentos(tab, jogador):
    capturas = []
    movimentos = []

    for i in range(8):
        for j in range(8):
            p = tab[i][j]
            if jogador == HUMANO and p not in (HUMANO, DAMA_H):
                continue
            if jogador == IA and p not in (IA, DAMA_IA):
                continue

            caps = gerar_capturas(tab, i, j, p)
            if caps:
                capturas.extend(caps)
            else:
                if p in (DAMA_H, DAMA_IA):
                    for dx, dy in direcoes(p):
                        ni, nj = i + dx, j + dy
                        while 0 <= ni < 8 and 0 <= nj < 8 and tab[ni][nj] == VAZIO:
                            movimentos.append(([(i, j), (ni, nj)], []))
                            ni += dx
                            nj += dy
                else:
                    for dx, dy in direcoes(p):
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < 8 and 0 <= nj < 8 and tab[ni][nj] == VAZIO:
                            movimentos.append(([(i, j), (ni, nj)], []))

    return capturas if capturas else movimentos


def aplicar(tab, movimento):
    caminho, capturadas = movimento
    (x0, y0) = caminho[0]
    (xf, yf) = caminho[-1]
    p = tab[x0][y0]

    tab[x0][y0] = VAZIO
    tab[xf][yf] = p

    for cx, cy in capturadas:
        tab[cx][cy] = VAZIO

    # Coroação de peças
    if p == HUMANO and xf == 0:
        tab[xf][yf] = DAMA_H
    elif p == IA and xf == 7:
        tab[xf][yf] = DAMA_IA
    # Damas que capturam e voltam à linha inicial mantêm-se damas
    elif p == DAMA_H and xf == 0:
        tab[xf][yf] = DAMA_H
    elif p == DAMA_IA and xf == 7:
        tab[xf][yf] = DAMA_IA
