import pygame
from configs import *

def criar_tabuleiro():
    tab = [[VAZIO for _ in range(COLUNAS)] for _ in range(LINHAS)]
    for l in range(3):
        for c in range(COLUNAS):
            if (l + c) % 2:
                tab[l][c] = IA
    for l in range(5, 8):
        for c in range(COLUNAS):
            if (l + c) % 2:
                tab[l][c] = HUMANO
    return tab


def desenhar_tabuleiro(tela, tab):
    for l in range(LINHAS):
        for c in range(COLUNAS):
            cor = BEGE if (l + c) % 2 == 0 else MARROM
            pygame.draw.rect(
                tela, cor,
                (c*TAM_QUAD, l*TAM_QUAD, TAM_QUAD, TAM_QUAD)
            )

            p = tab[l][c]
            if p:
                cor_p = BRANCO if p in (HUMANO, DAMA_H) else PRETO
                pygame.draw.circle(
                    tela, cor_p,
                    (c*TAM_QUAD + TAM_QUAD//2, l*TAM_QUAD + TAM_QUAD//2),
                    TAM_QUAD//2 - 10
                )
                if p in (DAMA_H, DAMA_IA):
                    pygame.draw.circle(
                        tela, VERMELHO,
                        (c*TAM_QUAD + TAM_QUAD//2, l*TAM_QUAD + TAM_QUAD//2),
                        10
                    )
