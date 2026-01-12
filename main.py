import pygame
import sys
from configs import *
from tabuleiro import criar_tabuleiro, desenhar_tabuleiro
from regras import gerar_movimentos, aplicar
from ia import minimax

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Damas - Humano vs IA (Minimax)")
    clock = pygame.time.Clock()

    tab = criar_tabuleiro()
    selecionado = None
    turno = HUMANO

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if turno == HUMANO and e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                l, c = y // TAM_QUAD, x // TAM_QUAD

                if selecionado:
                    m = (*selecionado, l, c)
                    if m in gerar_movimentos(tab, HUMANO):
                        aplicar(tab, m)
                        turno = IA
                    selecionado = None
                elif tab[l][c] in (HUMANO, DAMA_H):
                    selecionado = (l, c)

        if turno == IA:
            _, m = minimax(tab, 3, True)
            if m:
                aplicar(tab, m)
            turno = HUMANO

        desenhar_tabuleiro(tela, tab)
        pygame.display.flip()


if __name__ == "__main__":
    main()
