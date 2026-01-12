import math
from configs import *
from regras import gerar_movimentos, aplicar

def avaliar(tab):
    score = 0
    for linha in tab:
        for p in linha:
            if p == IA:
                score += 1
            elif p == DAMA_IA:
                score += 3
            elif p == HUMANO:
                score -= 1
            elif p == DAMA_H:
                score -= 3
    return score


def minimax(tab, depth, max_player):
    if depth == 0:
        return avaliar(tab), None

    jogador = IA if max_player else HUMANO
    melhor = -math.inf if max_player else math.inf
    melhor_mov = None

    for m in gerar_movimentos(tab, jogador):
        copia = [r[:] for r in tab]
        aplicar(copia, m)
        val, _ = minimax(copia, depth-1, not max_player)

        if max_player and val > melhor:
            melhor, melhor_mov = val, m
        elif not max_player and val < melhor:
            melhor, melhor_mov = val, m

    return melhor, melhor_mov
