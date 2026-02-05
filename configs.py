LARGURA, ALTURA = 1200, 900  # AUMENTADO SIGNIFICATIVAMENTE
TABULEIRO_LADO = 700  # Tabuleiro maior
LINHAS, COLUNAS = 8, 8
TAM_QUAD = TABULEIRO_LADO // COLUNAS
FPS = 60

# Novo esquema de cores - Moderno e elegante
PRIMARIO = (34, 40, 49)      # Azul escuro quase preto
SECUNDARIO = (57, 62, 70)    # Cinza azulado
TERCIARIO = (0, 173, 181)    # Turquesa brilhante
ACENTO = (238, 238, 238)     # Branco suave
DESTAQUE = (255, 107, 107)   # Coral/vermelho claro
SUCESSO = (46, 204, 113)     # Verde suave
AVISO = (241, 196, 15)       # Amarelo dourado
INFO = (52, 152, 219)        # Azul claro

# Cores do tabuleiro
CLARO = (240, 217, 181)      # Bege claro elegante
ESCURO = (101, 67, 33)       # Marrom chocolate
DESTAQUE_MOV = (130, 224, 170, 150)  # Verde translúcido
SELECAO = (52, 152, 219, 180)         # Azul translúcido

# Cores das peças
BRANCO = (245, 245, 245)     # Branco puro
PRETO = (30, 30, 30)         # Preto suave
COROA_CLARA = (255, 215, 0)  # Dourado
COROA_ESCURA = (192, 192, 192) # Prata

# Peças
VAZIO = 0
HUMANO = 1
IA = 2
DAMA_H = 3
DAMA_IA = 4

# Dificuldades - AUMENTADAS
FACIL = 1    # Profundidade 3
MEDIO = 2    # Profundidade 5
DIFICIL = 3  # Profundidade 8

# Estados do jogo
MENU = 0
JOGANDO = 1
RESULTADO = 2
