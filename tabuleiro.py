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


def desenhar_tabuleiro(tela, tab, destaques=None):
    if destaques is None:
        destaques = []

    for l in range(LINHAS):
        for c in range(COLUNAS):
            # Quadrado do tabuleiro
            cor = CLARO if (l + c) % 2 == 0 else ESCURO
            rect = pygame.Rect(c * TAM_QUAD, l * TAM_QUAD, TAM_QUAD, TAM_QUAD)
            pygame.draw.rect(tela, cor, rect)

            # Efeito de profundidade nos quadrados escuros
            if cor == ESCURO:
                pygame.draw.rect(tela, (80, 50, 30), rect, 1)

            # Destaques para movimentos possíveis
            if (l, c) in destaques:
                highlight_surface = pygame.Surface((TAM_QUAD, TAM_QUAD), pygame.SRCALPHA)
                pygame.draw.circle(highlight_surface, DESTAQUE_MOV,
                                   (TAM_QUAD // 2, TAM_QUAD // 2),
                                   TAM_QUAD // 2 - 5)
                tela.blit(highlight_surface, (c * TAM_QUAD, l * TAM_QUAD))

                # Contorno do destaque
                pygame.draw.circle(tela, SUCESSO,
                                   (c * TAM_QUAD + TAM_QUAD // 2,
                                    l * TAM_QUAD + TAM_QUAD // 2),
                                   TAM_QUAD // 2 - 5, 2)

            # Peças
            p = tab[l][c]
            if p:
                # Sombra da peça
                pygame.draw.circle(tela, (20, 20, 20, 100),
                                   (c * TAM_QUAD + TAM_QUAD // 2 + 2,
                                    l * TAM_QUAD + TAM_QUAD // 2 + 2),
                                   TAM_QUAD // 2 - 8)

                # Cor da peça
                cor_p = BRANCO if p in (HUMANO, DAMA_H) else PRETO
                pygame.draw.circle(tela, cor_p,
                                   (c * TAM_QUAD + TAM_QUAD // 2,
                                    l * TAM_QUAD + TAM_QUAD // 2),
                                   TAM_QUAD // 2 - 10)

                # Contorno da peça
                contorno_cor = INFO if p in (HUMANO, DAMA_H) else TERCIARIO
                pygame.draw.circle(tela, contorno_cor,
                                   (c * TAM_QUAD + TAM_QUAD // 2,
                                    l * TAM_QUAD + TAM_QUAD // 2),
                                   TAM_QUAD // 2 - 10, 2)

                # Efeito de brilho
                pygame.draw.circle(tela, (255, 255, 255, 30),
                                   (c * TAM_QUAD + TAM_QUAD // 2 - 5,
                                    l * TAM_QUAD + TAM_QUAD // 2 - 5),
                                   8)

                # Dama
                if p in (DAMA_H, DAMA_IA):
                    coroa_cor = COROA_CLARA if p == DAMA_H else COROA_ESCURA

                    # Coroa principal
                    pygame.draw.circle(tela, coroa_cor,
                                       (c * TAM_QUAD + TAM_QUAD // 2,
                                        l * TAM_QUAD + TAM_QUAD // 2),
                                       12)

                    # Detalhe da coroa
                    coroa_detalhe = DESTAQUE if p == DAMA_H else INFO
                    pygame.draw.circle(tela, coroa_detalhe,
                                       (c * TAM_QUAD + TAM_QUAD // 2,
                                        l * TAM_QUAD + TAM_QUAD // 2),
                                       8)

                    # Centro da coroa
                    pygame.draw.circle(tela, AVISO,
                                       (c * TAM_QUAD + TAM_QUAD // 2,
                                        l * TAM_QUAD + TAM_QUAD // 2),
                                       4)

                    # Pontos da coroa
                    for i in range(4):
                        angulo = i * 90 * 3.14159 / 180
                        x = c * TAM_QUAD + TAM_QUAD // 2 + 15 * pygame.math.Vector2(1, 0).rotate(i * 90).x
                        y = l * TAM_QUAD + TAM_QUAD // 2 + 15 * pygame.math.Vector2(1, 0).rotate(i * 90).y
                        pygame.draw.circle(tela, coroa_cor, (int(x), int(y)), 3)
