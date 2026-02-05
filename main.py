import pygame, sys
import time
import math
from configs import *
from tabuleiro import criar_tabuleiro, desenhar_tabuleiro
from regras import gerar_movimentos, aplicar
from ia import jogada_ia, IA_LOG, TEMPO_IA


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_normal, cor_hover, fonte, texto_cor=ACENTO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.fonte = fonte
        self.texto_cor = texto_cor
        self.hover = False
        self.border_radius = 15

    def desenhar(self, tela):
        cor = self.cor_hover if self.hover else self.cor_normal
        pygame.draw.rect(tela, cor, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(tela, ACENTO, self.rect, 3, border_radius=self.border_radius)

        texto_surf = self.fonte.render(self.texto, True, self.texto_cor)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def verificar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

    def verificar_clique(self, pos):
        return self.rect.collidepoint(pos)


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo de Damas - Desafie a IA")
        self.clock = pygame.time.Clock()

        # Fontes
        self.fonte_pequena = pygame.font.SysFont("Arial", 20)
        self.fonte_media = pygame.font.SysFont("Arial", 26)
        self.fonte_grande = pygame.font.SysFont("Arial", 48, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Arial", 56, bold=True)

        self.estado = MENU
        self.dificuldade = MEDIO
        self.resetar_jogo()
        self.inicializar_botoes()

    def inicializar_botoes(self):
        # Botões de dificuldade - CENTRALIZADOS E ALINHADOS
        largura_botao = 220
        altura_botao = 60
        espacamento = 20

        # Centralizado horizontalmente
        x_inicial = LARGURA // 2 - ((3 * largura_botao) + (2 * espacamento)) // 2

        self.botoes_dificuldade = [
            Botao(x_inicial, 350, largura_botao, altura_botao, "FÁCIL",
                  SUCESSO if self.dificuldade == FACIL else SECUNDARIO,
                  TERCIARIO, self.fonte_media),
            Botao(x_inicial + largura_botao + espacamento, 350, largura_botao, altura_botao, "MÉDIO",
                  SUCESSO if self.dificuldade == MEDIO else SECUNDARIO,
                  TERCIARIO, self.fonte_media),
            Botao(x_inicial + 2 * (largura_botao + espacamento), 350, largura_botao, altura_botao, "DIFÍCIL",
                  SUCESSO if self.dificuldade == DIFICIL else SECUNDARIO,
                  TERCIARIO, self.fonte_media)
        ]

        # Botão iniciar centralizado
        self.botao_iniciar = Botao(LARGURA // 2 - 150, 450, 300, 70, "INICIAR JOGO",
                                   TERCIARIO, INFO, self.fonte_media)

        # Botões do jogo - MELHOR POSICIONADOS
        self.botao_menu = Botao(TABULEIRO_LADO + 40, 650, 220, 50, "VOLTAR AO MENU",
                                SECUNDARIO, TERCIARIO, self.fonte_pequena)
        self.botao_reiniciar = Botao(TABULEIRO_LADO + 40, 710, 220, 50, "REINICIAR PARTIDA",
                                     SUCESSO, TERCIARIO, self.fonte_pequena)

        # Botões do resultado - CENTRALIZADOS E ALINHADOS
        self.botao_menu_resultado = Botao(LARGURA // 2 - 185, 650, 170, 60, "MENU",
                                          SECUNDARIO, TERCIARIO, self.fonte_media)
        self.botao_jogar_novamente = Botao(LARGURA // 2 + 15, 650, 170, 60, "JOGAR NOVAMENTE",
                                           TERCIARIO, INFO, self.fonte_media)

    def resetar_jogo(self):
        self.tab = criar_tabuleiro()
        self.selecionado = None
        self.turno = HUMANO
        self.vencedor = None
        self.destaques = []
        self.inicio_tempo = time.time()
        self.tempo_total = 0
        self.movimentos_humano = 0
        self.movimentos_ia = 0
        self.capturas_humano = 0
        self.capturas_ia = 0
        IA_LOG.clear()

    def desenhar_fundo_degradê(self):
        # Fundo com degradê sutil
        for y in range(ALTURA):
            cor = (
                int(PRIMARIO[0] + (SECUNDARIO[0] - PRIMARIO[0]) * y / ALTURA),
                int(PRIMARIO[1] + (SECUNDARIO[1] - PRIMARIO[1]) * y / ALTURA),
                int(PRIMARIO[2] + (SECUNDARIO[2] - PRIMARIO[2]) * y / ALTURA)
            )
            pygame.draw.line(self.tela, cor, (0, y), (LARGURA, y))

    def desenhar_menu(self):
        self.desenhar_fundo_degradê()

        # TÍTULO CENTRALIZADO
        titulo_y = 150

        # Efeito de sombra
        sombra = self.fonte_titulo.render("DAMAS IA", True, (20, 20, 20))
        self.tela.blit(sombra, (LARGURA // 2 - sombra.get_width() // 2 + 3, titulo_y + 3))

        titulo = self.fonte_titulo.render("DAMAS IA", True, TERCIARIO)
        self.tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, titulo_y))

        # SUBTÍTULO
        subtitulo = self.fonte_media.render("Desafie a Inteligência Artificial", True, ACENTO)
        self.tela.blit(subtitulo, (LARGURA // 2 - subtitulo.get_width() // 2, titulo_y + 70))

        # LINHA DECORATIVA
        linha_y = titulo_y + 120
        pygame.draw.line(self.tela, TERCIARIO, (LARGURA // 2 - 200, linha_y),
                         (LARGURA // 2 + 200, linha_y), 3)

        # SEÇÃO DIFICULDADE
        dificuldade_y = linha_y + 50
        dificuldade_texto = self.fonte_media.render("ESCOLHA A DIFICULDADE:", True, ACENTO)
        self.tela.blit(dificuldade_texto, (LARGURA // 2 - dificuldade_texto.get_width() // 2, dificuldade_y))

        # BOTÕES DE DIFICULDADE (já centralizados)
        for botao in self.botoes_dificuldade:
            botao.desenhar(self.tela)

        # BOTÃO INICIAR
        self.botao_iniciar.desenhar(self.tela)

        # INFORMAÇÕES SOBRE AS DIFICULDADES
        info_y = 530
        info_textos = [
            "FÁCIL: Movimentos básicos, decisões rápidas",
            "MÉDIO: Estratégia moderada, pensa alguns passos à frente",
            "DIFÍCIL: Estratégia avançada, pensa profundamente"
        ]

        for i, texto in enumerate(info_textos):
            texto_surf = self.fonte_pequena.render(texto, True, (180, 180, 180))
            self.tela.blit(texto_surf, (LARGURA // 2 - texto_surf.get_width() // 2, info_y + i * 25))

    def desenhar_painel_lateral(self):
        painel_x = TABULEIRO_LADO + 20
        painel_largura = LARGURA - TABULEIRO_LADO - 40

        # Fundo do painel
        pygame.draw.rect(self.tela, PRIMARIO, (painel_x, 20, painel_largura, ALTURA - 40), border_radius=15)
        pygame.draw.rect(self.tela, TERCIARIO, (painel_x, 20, painel_largura, ALTURA - 40), 3, border_radius=15)

        # Cabeçalho
        cabecalho_texto = self.fonte_media.render("INFORMAÇÕES", True, TERCIARIO)
        self.tela.blit(cabecalho_texto, (painel_x + painel_largura // 2 - cabecalho_texto.get_width() // 2, 50))

        # Temporizador
        self.tempo_total = time.time() - self.inicio_tempo
        minutos = int(self.tempo_total // 60)
        segundos = int(self.tempo_total % 60)

        tempo_texto = self.fonte_media.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, ACENTO)
        self.tela.blit(tempo_texto, (painel_x + painel_largura // 2 - tempo_texto.get_width() // 2, 100))

        # Estatísticas - ORGANIZADAS EM COLUNAS
        stats_y = 200
        stats_esquerda = [
            f"Seus Movimentos:",
            f"Suas Capturas:",
            f"Movimentos IA:",
            f"Capturas IA:"
        ]

        stats_direita = [
            f"{self.movimentos_humano}",
            f"{self.capturas_humano}",
            f"{self.movimentos_ia}",
            f"{self.capturas_ia}"
        ]

        for i, (texto_esq, texto_dir) in enumerate(zip(stats_esquerda, stats_direita)):
            # Texto à esquerda
            surf_esq = self.fonte_pequena.render(texto_esq, True, ACENTO)
            self.tela.blit(surf_esq, (painel_x + 30, stats_y + i * 35))

            # Texto à direita
            surf_dir = self.fonte_pequena.render(texto_dir, True, TERCIARIO)
            self.tela.blit(surf_dir, (painel_x + painel_largura - 60 - surf_dir.get_width(), stats_y + i * 35))
        pecas_humano = sum(1 for linha in self.tab for p in linha if p in (HUMANO, DAMA_H))
        pecas_ia = sum(1 for linha in self.tab for p in linha if p in (IA, DAMA_IA))

        pecas_y = stats_y + 4 * 35 + 20
        pecas_titulo = self.fonte_pequena.render("PEÇAS RESTANTES", True, TERCIARIO)
        self.tela.blit(pecas_titulo, (painel_x + painel_largura // 2 - pecas_titulo.get_width() // 2, pecas_y))

        # Linha divisória abaixo do título
        linha_y = pecas_y + 25
        pygame.draw.line(self.tela, TERCIARIO,
                         (painel_x + 50, linha_y),
                         (painel_x + painel_largura - 50, linha_y), 1)

        # Peças do jogador (humano) - à esquerda
        jogador_y = linha_y + 15
        jogador_texto = self.fonte_pequena.render("JOGADOR:", True, ACENTO)
        jogador_numero = self.fonte_media.render(f"{pecas_humano}", True, SUCESSO)

        self.tela.blit(jogador_texto, (painel_x + 50, jogador_y))
        self.tela.blit(jogador_numero, (painel_x + 140, jogador_y))

        # Peças da IA - à direita
        ia_texto = self.fonte_pequena.render("IA:", True, ACENTO)
        ia_numero = self.fonte_media.render(f"{pecas_ia}", True, DESTAQUE)

        self.tela.blit(ia_texto, (painel_x + painel_largura - 200, jogador_y))
        self.tela.blit(ia_numero, (painel_x + painel_largura - 150 - ia_numero.get_width(), jogador_y))

        # Linha separadora entre jogador e IA
        separador_x = painel_x + painel_largura // 2
        pygame.draw.line(self.tela, TERCIARIO,
                         (separador_x, jogador_y - 5),
                         (separador_x, jogador_y + 30), 1)

        # Botões do painel - MELHOR POSICIONADOS
        self.botao_menu.rect.y = ALTURA - 400
        self.botao_reiniciar.rect.y = ALTURA - 350

        self.botao_menu.rect.x = ALTURA - 50
        self.botao_reiniciar.rect.x = ALTURA - 50

        self.botao_menu.desenhar(self.tela)
        self.botao_reiniciar.desenhar(self.tela)

    def desenhar_resultado(self):
        self.desenhar_fundo_degradê()

        # Moldura centralizada e alinhada
        moldura_largura = 600
        moldura_altura = 400
        moldura_rect = pygame.Rect(LARGURA // 2 - moldura_largura // 2, 200, moldura_largura, moldura_altura)

        # Fundo com sombra
        pygame.draw.rect(self.tela, (20, 20, 20), moldura_rect.move(4, 4), border_radius=20)
        pygame.draw.rect(self.tela, PRIMARIO, moldura_rect, border_radius=20)
        pygame.draw.rect(self.tela, TERCIARIO, moldura_rect, 3, border_radius=20)

        if self.vencedor == "Humano":
            mensagem = "VITÓRIA!"
            cor = SUCESSO
            subtitulo = "Parabéns! Você venceu a IA!"
        else:
            mensagem = "DERROTA"
            cor = DESTAQUE
            subtitulo = "A IA foi mais esperta desta vez!"

        # Mensagem principal
        msg_surf = self.fonte_grande.render(mensagem, True, cor)
        self.tela.blit(msg_surf, (LARGURA // 2 - msg_surf.get_width() // 2, 250))

        # Subtítulo
        sub_surf = self.fonte_media.render(subtitulo, True, ACENTO)
        self.tela.blit(sub_surf, (LARGURA // 2 - sub_surf.get_width() // 2, 310))

        # Peças finais
        pecas_humano = sum(1 for linha in self.tab for p in linha if p in (HUMANO, DAMA_H))
        pecas_ia = sum(1 for linha in self.tab for p in linha if p in (IA, DAMA_IA))

        # Estatísticas - ALINHADAS CENTRALMENTE
        stats = [
            f"Tempo total: {int(self.tempo_total // 60):02d}:{int(self.tempo_total % 60):02d}",
            f"Seus movimentos: {self.movimentos_humano}",
            f"Movimentos da IA: {self.movimentos_ia}",
            f"Suas capturas: {self.capturas_humano}",
            f"Capturas da IA: {self.capturas_ia}",
            "",  # Linha em branco para separação
        ]

        stats_start_y = 350
        for i, texto in enumerate(stats):
            if texto:  # Só desenhar se não for string vazia
                cor_texto = ACENTO if i < 6 else TERCIARIO
                texto_surf = self.fonte_media.render(texto, True, cor_texto)
                self.tela.blit(texto_surf, (LARGURA // 2 - texto_surf.get_width() // 2, stats_start_y + i * 35))

        # Botões - ALINHADOS E ESPAÇADOS CORRETAMENTE
        self.botao_menu_resultado.desenhar(self.tela)
        self.botao_jogar_novamente.desenhar(self.tela)

    def verificar_vencedor(self):
        # Contagem precisa de peças
        h = sum(1 for linha in self.tab for p in linha if p in (HUMANO, DAMA_H))
        i = sum(1 for linha in self.tab for p in linha if p in (IA, DAMA_IA))

        if h == 0:
            self.vencedor = "IA"
            return True
        if i == 0:
            self.vencedor = "Humano"
            return True

        return False

    def executar(self):
        while True:
            self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado == MENU:
                        for i, botao in enumerate(self.botoes_dificuldade):
                            if botao.verificar_clique(mouse_pos):
                                self.dificuldade = i + 1
                                for j, b in enumerate(self.botoes_dificuldade):
                                    b.cor_normal = SUCESSO if j == i else SECUNDARIO

                        if self.botao_iniciar.verificar_clique(mouse_pos):
                            self.estado = JOGANDO
                            self.resetar_jogo()

                    elif self.estado == JOGANDO:
                        if mouse_pos[0] < TABULEIRO_LADO and mouse_pos[1] < TABULEIRO_LADO:
                            if self.turno == HUMANO:
                                x, y = mouse_pos
                                l, c = y // TAM_QUAD, x // TAM_QUAD

                                if self.selecionado:
                                    for mov in gerar_movimentos(self.tab, HUMANO):
                                        if mov[0][0] == self.selecionado and mov[0][-1] == (l, c):
                                            self.capturas_humano += len(mov[1])
                                            self.movimentos_humano += 1
                                            aplicar(self.tab, mov)
                                            self.turno = IA
                                            break
                                    self.selecionado = None
                                    self.destaques = []
                                elif self.tab[l][c] in (HUMANO, DAMA_H):
                                    self.selecionado = (l, c)
                                    self.destaques = [mov[0][-1] for mov in gerar_movimentos(self.tab, HUMANO)
                                                      if mov[0][0] == self.selecionado]

                        if self.botao_menu.verificar_clique(mouse_pos):
                            self.estado = MENU
                        if self.botao_reiniciar.verificar_clique(mouse_pos):
                            self.resetar_jogo()

                    elif self.estado == RESULTADO:
                        if self.botao_menu_resultado.verificar_clique(mouse_pos):
                            self.estado = MENU
                        if self.botao_jogar_novamente.verificar_clique(mouse_pos):
                            self.estado = JOGANDO
                            self.resetar_jogo()

            # Atualizar hover
            if self.estado == MENU:
                for botao in self.botoes_dificuldade:
                    botao.verificar_hover(mouse_pos)
                self.botao_iniciar.verificar_hover(mouse_pos)
            elif self.estado == JOGANDO:
                self.botao_menu.verificar_hover(mouse_pos)
                self.botao_reiniciar.verificar_hover(mouse_pos)
            elif self.estado == RESULTADO:
                self.botao_menu_resultado.verificar_hover(mouse_pos)
                self.botao_jogar_novamente.verificar_hover(mouse_pos)

            # Lógica do jogo
            if self.estado == JOGANDO:
                if self.turno == IA:
                    mov_ia = jogada_ia(self.tab, self.dificuldade)
                    if mov_ia:
                        self.capturas_ia += len(mov_ia[1])
                        self.movimentos_ia += 1
                        aplicar(self.tab, mov_ia)
                    self.turno = HUMANO

                if self.verificar_vencedor():
                    self.estado = RESULTADO

            # Desenhar
            if self.estado == MENU:
                self.desenhar_menu()
            elif self.estado == JOGANDO:
                self.desenhar_fundo_degradê()
                tabuleiro_rect = pygame.Rect(20, 20, TABULEIRO_LADO, TABULEIRO_LADO)
                pygame.draw.rect(self.tela, PRIMARIO, tabuleiro_rect, border_radius=15)
                pygame.draw.rect(self.tela, TERCIARIO, tabuleiro_rect, 3, border_radius=15)

                desenhar_tabuleiro(self.tela, self.tab, self.destaques)
                self.desenhar_painel_lateral()
            elif self.estado == RESULTADO:
                self.desenhar_resultado()

            pygame.display.flip()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
