from configs import *
from utils import dentro

def direcoes(p):
    if p == HUMANO:
        return [(-1, -1), (-1, 1)]
    if p == IA:
        return [(1, -1), (1, 1)]
    return [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def inimigo(p):
    return (IA, DAMA_IA) if p in (HUMANO, DAMA_H) else (HUMANO, DAMA_H)


def gerar_movimentos(tab, jogador):
    movs, caps = [], []
    for l in range(8):
        for c in range(8):
            p = tab[l][c]
            if jogador == HUMANO and p not in (HUMANO, DAMA_H):
                continue
            if jogador == IA and p not in (IA, DAMA_IA):
                continue

            for dl, dc in direcoes(p):
                nl, nc = l + dl, c + dc
                cl, cc = l + 2*dl, c + 2*dc

                if (dentro(cl, cc) and dentro(nl, nc)
                        and tab[nl][nc] in inimigo(p)
                        and tab[cl][cc] == VAZIO):
                    caps.append((l, c, cl, cc))

                elif dentro(nl, nc) and tab[nl][nc] == VAZIO:
                    movs.append((l, c, nl, nc))

    return caps if caps else movs


def aplicar(tab, m):
    l1, c1, l2, c2 = m
    p = tab[l1][c1]
    tab[l1][c1] = VAZIO
    tab[l2][c2] = p

    if abs(l2 - l1) == 2:
        tab[(l1 + l2)//2][(c1 + c2)//2] = VAZIO

    if l2 == 0 and p == HUMANO:
        tab[l2][c2] = DAMA_H
    if l2 == 7 and p == IA:
        tab[l2][c2] = DAMA_IA
