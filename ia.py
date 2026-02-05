import math
import time
import random
from configs import *
from regras import gerar_movimentos, aplicar
from utils import copiar

IA_LOG = []
TEMPO_IA = 0.0


def avaliar(tab):
    score = 0
    peso_posicional = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 2, 0, 2, 0, 2, 0],
        [0, 3, 0, 3, 0, 3, 0, 3],
        [3, 0, 4, 0, 4, 0, 4, 0],
        [0, 5, 0, 5, 0, 5, 0, 5],
        [5, 0, 6, 0, 6, 0, 6, 0],
        [0, 7, 0, 7, 0, 7, 0, 7]
    ]

    for i in range(8):
        for j in range(8):
            p = tab[i][j]
            pos_score = peso_posicional[i][j]

            if p == IA:
                score += 10 + pos_score
            if p == DAMA_IA:
                score += 30 + (7 - pos_score) * 2
            if p == HUMANO:
                score -= 10 + (7 - pos_score)
            if p == DAMA_H:
                score -= 30 + pos_score * 2

    # Bônus por mobilidade
    mobilidade_ia = len(gerar_movimentos(tab, IA))
    mobilidade_humano = len(gerar_movimentos(tab, HUMANO))
    score += (mobilidade_ia - mobilidade_humano) * 0.5

    return score


def avaliar_movimento_simples(tab, movimento):
    """Avaliação muito simples para o modo fácil"""
    score = 0
    caminho, capturas = movimento

    # Capturas são boas
    score += len(capturas) * 5

    # Avançar é bom
    (xf, yf) = caminho[-1]
    if xf > 3:  # Mais perto de virar dama
        score += 2

    # Não ficar muito na borda
    if yf == 0 or yf == 7:
        score -= 1

    return score


def minimax(tab, depth, max_player, nivel=0, alpha=-math.inf, beta=math.inf):
    if depth == 0:
        return avaliar(tab), None

    jogador = IA if max_player else HUMANO
    melhor = -math.inf if max_player else math.inf
    melhor_mov = None

    movimentos = gerar_movimentos(tab, jogador)

    if not movimentos:
        return avaliar(tab), None

    # Ordenar movimentos para melhorar poda alfa-beta
    if max_player:
        movimentos.sort(key=lambda m: (-len(m[1]), -avaliar_movimento_medio(tab, m)))
    else:
        movimentos.sort(key=lambda m: (len(m[1]), avaliar_movimento_medio(tab, m)))

    for m in movimentos:
        copia_tab = copiar(tab)
        aplicar(copia_tab, m)
        val, _ = minimax(copia_tab, depth - 1, not max_player, nivel + 1, alpha, beta)

        if max_player:
            if val > melhor:
                melhor, melhor_mov = val, m
            alpha = max(alpha, val)
        else:
            if val < melhor:
                melhor, melhor_mov = val, m
            beta = min(beta, val)

        if beta <= alpha:
            break

    return melhor, melhor_mov


def avaliar_movimento_medio(tab, movimento):
    """Avaliação para o modo médio"""
    score = 0
    caminho, capturas = movimento

    # Capturas são muito boas
    score += len(capturas) * 15

    # Promover a dama é excelente
    (xf, yf) = caminho[-1]
    p = tab[caminho[0][0]][caminho[0][1]]
    if p == IA and xf == 7:
        score += 25

    # Centralizar as peças
    if 2 <= yf <= 5:
        score += 2

    # Não ficar exposto
    for dx, dy in [(1, 1), (1, -1)]:
        nx, ny = xf + dx, yf + dy
        if 0 <= nx < 8 and 0 <= ny < 8:
            if tab[nx][ny] in (HUMANO, DAMA_H):
                score -= 3

    return score


def jogada_ia_facil(tab):
    """IA BURRÍSSIMA - Modo fácil"""
    movimentos = gerar_movimentos(tab, IA)

    if not movimentos:
        return None

    # Prioridade 1: Se tiver captura, faz (mas nem sempre)
    capturas = [m for m in movimentos if m[1]]
    if capturas and random.random() > 0.3:  # 70% das vezes faz captura
        # Escolhe uma captura aleatória, não necessariamente a melhor
        return random.choice(capturas)

    # Prioridade 2: Movimentos aleatórios
    movimento_aleatorio = random.choice(movimentos)

    # As vezes faz movimento estúpido de propósito
    if random.random() < 0.2:  # 20% das vezes faz movimento ruim
        # Tenta encontrar movimento que deixa peça vulnerável
        movimentos_ruins = []
        for m in movimentos:
            caminho = m[0]
            xf, yf = caminho[-1]
            # Movimentos que deixam peça na borda são mais vulneráveis
            if yf == 0 or yf == 7:
                movimentos_ruins.append(m)
            # Movimentos que não avançam
            if xf <= caminho[0][0]:
                movimentos_ruins.append(m)

        if movimentos_ruins:
            return random.choice(movimentos_ruins)

    return movimento_aleatorio


def jogada_ia_medio(tab):
    """IA MODERADA - Modo médio"""
    global TEMPO_IA
    start_time = time.time()

    # Usa minimax com profundidade baixa
    profundidade = 2

    _, melhor_mov = minimax(tab, profundidade, True)

    TEMPO_IA = time.time() - start_time
    IA_LOG.append(f"Modo Médio - Tempo: {TEMPO_IA:.2f}s")

    return melhor_mov


def jogada_ia_dificil(tab):
    """IA MUITO INTELIGENTE - Modo difícil"""
    global TEMPO_IA
    start_time = time.time()

    # Usa minimax com profundidade alta
    profundidade = 6

    # Tenta pensar mais em posições complexas
    movimentos_disponiveis = len(gerar_movimentos(tab, IA))
    if movimentos_disponiveis < 5:  # Final de jogo
        profundidade = 8  # Pensar mais profundamente

    _, melhor_mov = minimax(tab, profundidade, True)

    TEMPO_IA = time.time() - start_time
    IA_LOG.append(f"Modo Difícil - Tempo: {TEMPO_IA:.2f}s - Profundidade: {profundidade}")

    return melhor_mov


def jogada_ia(tab, dificuldade):
    """Função principal que escolhe a estratégia baseada na dificuldade"""
    if dificuldade == FACIL:
        return jogada_ia_facil(tab)
    elif dificuldade == MEDIO:
        return jogada_ia_medio(tab)
    elif dificuldade == DIFICIL:
        return jogada_ia_dificil(tab)
    else:
        return jogada_ia_facil(tab)  # Padrão para fácil
