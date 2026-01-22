import pygame, sys
from configs import *
from tabuleiro import criar_tabuleiro, desenhar_tabuleiro
from regras import gerar_movimentos, aplicar
from ia import minimax, IA_LOG

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Dama contra o Minimax =)")
    clock = pygame.time.Clock()

    tab = criar_tabuleiro()
    selecionado = None
    turno = HUMANO
    vencedor = None
    destaques = []

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if turno == HUMANO and e.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                l,c = y//TAM_QUAD, x//TAM_QUAD

                if selecionado:
                    for mov in gerar_movimentos(tab, HUMANO):
                        if mov[0][0] == selecionado and mov[0][-1] == (l,c):
                            aplicar(tab, mov)
                            turno = IA
                            break
                    selecionado = None
                    destaques = []
                elif tab[l][c] in (HUMANO, DAMA_H):
                    selecionado = (l,c)
                    destaques = [mov[0][-1] for mov in gerar_movimentos(tab, HUMANO) if mov[0][0] == selecionado]

        if turno == IA:
            _, m = minimax(tab, 2, True)
            if m:
                aplicar(tab, m)
            turno = HUMANO

        h = sum(p in (HUMANO, DAMA_H) for linha in tab for p in linha)
        i = sum(p in (IA, DAMA_IA) for linha in tab for p in linha)
        if h == 0: vencedor = "IA"
        if i == 0: vencedor = "Humano"
        if vencedor: break

        desenhar_tabuleiro(tela, tab, destaques)
        pygame.display.flip()

    tela.fill(PRETO)
    fonte = pygame.font.SysFont(None, 28)
    tela.blit(fonte.render(f"Vencedor: {vencedor}", True, BRANCO), (200,40))

    y = 100
    for linha in IA_LOG[-15:]:
        tela.blit(fonte.render(linha, True, BRANCO), (30,y))
        y += 26

    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()
