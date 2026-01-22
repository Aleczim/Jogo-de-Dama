import math
from configs import *
from regras import gerar_movimentos, aplicar
from utils import copiar

IA_LOG = []

def avaliar(tab):
    score = 0
    for linha in tab:
        for p in linha:
            if p == IA: score += 1
            if p == DAMA_IA: score += 3
            if p == HUMANO: score -= 1
            if p == DAMA_H: score -= 3
    return score


def minimax(tab, depth, max_player, nivel=0):
    if depth == 0:
        return avaliar(tab), None

    jogador = IA if max_player else HUMANO
    melhor = -math.inf if max_player else math.inf
    melhor_mov = None

    for m in gerar_movimentos(tab, jogador):
        copia_tab = copiar(tab)
        aplicar(copia_tab, m)
        val, _ = minimax(copia_tab, depth-1, not max_player, nivel+1)

        if max_player and val > melhor:
            melhor, melhor_mov = val, m
        if not max_player and val < melhor:
            melhor, melhor_mov = val, m

    if nivel == 0 and melhor_mov:
        IA_LOG.append(f"IA escolheu {melhor_mov} com score {melhor}")

    return melhor, melhor_mov
