import pygame
import numpy as np

# Configurações do jogo
ROW_COUNT = 7  # Alterado para 7 linhas
COLUMN_COUNT = 8  # Alterado para 8 colunas
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
PECA_JOGADOR = 2  # Representa a peça do jogador
PECA_IA = 1       # Representa a peça da IA

# Cores
BLUE = (0, 100, 0)
BLACK = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def create_board():
    """
    Cria o tabuleiro inicial do jogo como uma matriz 7x8 preenchida com zeros.
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def draw_board(board, screen, width, height):
    """
    Desenha o tabuleiro no Pygame.
    :param board: Matriz representando o estado atual do tabuleiro.
    :param screen: Tela do Pygame onde o tabuleiro será desenhado.
    :param width: Largura da tela.
    :param height: Altura da tela.
    """

    # Carregar a imagem do escudo do Cruzeiro
    escudo_cruzeiro = pygame.image.load("cruzeiro.png")
    escudo_cruzeiro = pygame.transform.scale(escudo_cruzeiro, (SQUARESIZE - 10, SQUARESIZE - 10))  # Redimensionar

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PECA_JOGADOR:
                # Desenha o escudo do Cruzeiro
                screen.blit(
                    escudo_cruzeiro,
                    (c * SQUARESIZE + 5, height - (r + 1) * SQUARESIZE + 5)
                )
            elif board[r][c] == PECA_IA:
                # Desenha a peça da IA (círculo amarelo)
                pygame.draw.circle(
                    screen,
                    (255, 255, 0),  # Amarelo
                    (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS
                )
    pygame.display.update()
