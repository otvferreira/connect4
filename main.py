import pygame
import sys
import math
import time
from construtor import create_board, draw_board
from minimax import minimax
from alfabeta import alfabeta
from minimax import coluna_valida, proxima_linha_livre, jogada_vencedora, locais_validos

# Configurações do jogo
ROW_COUNT = 7  # Alterado para 7 linhas
COLUMN_COUNT = 8  # Alterado para 8 colunas
SQUARESIZE = 100
PECA_JOGADOR = 2
PECA_IA = 1
JOGADOR = 0
IA = 1

# Cores
PRETO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

# Inicialização do Pygame
pygame.init()

# Configuração da tela
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)

# Configurar o ícone do Cruzeiro
icon_cruzeiro = pygame.image.load("cruzeiro.png")
icon_cruzeiro = pygame.transform.scale(icon_cruzeiro, (50, 50))  # Ajusta o tamanho do ícone
pygame.display.set_icon(icon_cruzeiro)  # Define o ícone na janela
pygame.display.set_caption("Connect 4 - Cruzeiro")

# Fonte para mensagens
fonte = pygame.font.SysFont("monospace", 75)

# Carregar a imagem do Cruzeiro para uso como peça do jogador
peca_cruzeiro = pygame.transform.scale(icon_cruzeiro, (SQUARESIZE - 10, SQUARESIZE - 10))

# Inicializa o jogo
tabuleiro = create_board()
fim_de_jogo = False
turno = JOGADOR
profundidade = 4
algoritmo_ia = minimax
# algoritmo_ia = alfabeta

# Desenha o tabuleiro inicial
draw_board(tabuleiro, screen, width, height)

# Loop principal do jogo
while not fim_de_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

        if evento.type == pygame.MOUSEMOTION:
            if not fim_de_jogo:  # Apenas desenha se o jogo não acabou
                pygame.draw.rect(screen, PRETO, (0, 0, width, SQUARESIZE))
                pos_x = evento.pos[0]
                if turno == JOGADOR:
                    screen.blit(peca_cruzeiro, (pos_x - SQUARESIZE // 2, SQUARESIZE // 2 - SQUARESIZE // 2))
                pygame.display.update()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if not fim_de_jogo:  # Impede ações após o jogo acabar
                pygame.draw.rect(screen, PRETO, (0, 0, width, SQUARESIZE))

                if turno == JOGADOR:
                    pos_x = evento.pos[0]
                    coluna = int(math.floor(pos_x / SQUARESIZE))

                    if coluna_valida(tabuleiro, coluna):
                        linha = proxima_linha_livre(tabuleiro, coluna)
                        tabuleiro[linha][coluna] = PECA_JOGADOR

                        if jogada_vencedora(tabuleiro, PECA_JOGADOR):
                            mensagem = fonte.render("Jogador venceu!", 2, AZUL)
                            screen.blit(mensagem, (40, 10))
                            fim_de_jogo = True
                            pygame.display.update()  # Atualiza a mensagem na tela
                            break

                        turno = IA
                        draw_board(tabuleiro, screen, width, height)

    # Movimento da IA
    if turno == IA and not fim_de_jogo:
        inicio = time.time()
        coluna, _ = algoritmo_ia(tabuleiro, profundidade, -math.inf, math.inf, True)
        fim = time.time()

        print(f"Tempo gasto pelo algoritmo {algoritmo_ia.__name__}: {fim - inicio:.4f} segundos")

        if coluna_valida(tabuleiro, coluna):
            linha = proxima_linha_livre(tabuleiro, coluna)
            tabuleiro[linha][coluna] = PECA_IA

            if jogada_vencedora(tabuleiro, PECA_IA):
                mensagem = fonte.render("IA venceu!", 1, AMARELO)
                screen.blit(mensagem, (40, 10))
                fim_de_jogo = True
                pygame.display.update()  # Atualiza a mensagem na tela

            turno = JOGADOR
            draw_board(tabuleiro, screen, width, height)

# Aguarda interação para fechar o jogo
while True:
    for evento in pygame.event.get():
        if evento.type in [pygame.QUIT, pygame.KEYDOWN]:
            pygame.quit()
            sys.exit()