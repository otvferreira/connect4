import numpy as np
import math

ROW_COUNT = 7
COLUMN_COUNT = 8
WINDOW_LENGTH = 4
VAZIO = 0
PECA_JOGADOR = 2
PECA_IA = 1

def minimax(tabuleiro, profundidade, alfa, beta, maximizando):
    locais = locais_validos(tabuleiro)
    terminal = eh_terminal(tabuleiro)

    if profundidade == 0 or terminal:
        if terminal:
            if jogada_vencedora(tabuleiro, PECA_IA):
                return (None, 100000000000000)
            elif jogada_vencedora(tabuleiro, PECA_JOGADOR):
                return (None, -10000000000000)
            else:
                return (None, 0)  # Empate
        else:
            return (None, pontuar_tabuleiro(tabuleiro, PECA_IA))

    if maximizando:  # Turno da IA
        valor = -math.inf
        melhor_coluna = locais[0]
        for coluna in locais:
            linha = proxima_linha_livre(tabuleiro, coluna)
            copia_tabuleiro = tabuleiro.copy()
            copia_tabuleiro[linha][coluna] = PECA_IA
            novo_valor = minimax(copia_tabuleiro, profundidade - 1, alfa, beta, False)[1]
            if novo_valor > valor:
                valor = novo_valor
                melhor_coluna = coluna
        return melhor_coluna, valor
    else:  # Turno do jogador
        valor = math.inf
        melhor_coluna = locais[0]
        for coluna in locais:
            linha = proxima_linha_livre(tabuleiro, coluna)
            copia_tabuleiro = tabuleiro.copy()
            copia_tabuleiro[linha][coluna] = PECA_JOGADOR
            novo_valor = minimax(copia_tabuleiro, profundidade - 1, alfa, beta, True)[1]
            if novo_valor < valor:
                valor = novo_valor
                melhor_coluna = coluna
        return melhor_coluna, valor


def proxima_linha_livre(tabuleiro, coluna):
    for linha in range(ROW_COUNT):
        if tabuleiro[linha][coluna] == 0:
            return linha

def jogada_vencedora(tabuleiro, peca):
    """
    Verifica se a peça fornecida resultou em uma jogada vencedora.
    """
    # Verifica horizontalmente
    for r in range(ROW_COUNT):  # Para cada linha
        for c in range(COLUMN_COUNT - 3):  # Para cada conjunto possível de 4 colunas consecutivas
            if all([tabuleiro[r][c + i] == peca for i in range(WINDOW_LENGTH)]):
                return True

    # Verifica verticalmente
    for c in range(COLUMN_COUNT):  # Para cada coluna
        for r in range(ROW_COUNT - 3):  # Para cada conjunto possível de 4 linhas consecutivas
            if all([tabuleiro[r + i][c] == peca for i in range(WINDOW_LENGTH)]):
                return True

    # Verifica diagonal positiva (\)
    for r in range(ROW_COUNT - 3):  # Para cada linha inicial possível de uma diagonal positiva
        for c in range(COLUMN_COUNT - 3):  # Para cada coluna inicial possível
            if all([tabuleiro[r + i][c + i] == peca for i in range(WINDOW_LENGTH)]):
                return True

    # Verifica diagonal negativa (/)
    for r in range(3, ROW_COUNT):  # Para cada linha inicial possível de uma diagonal negativa
        for c in range(COLUMN_COUNT - 3):  # Para cada coluna inicial possível
            if all([tabuleiro[r - i][c + i] == peca for i in range(WINDOW_LENGTH)]):
                return True

    return False

def avaliar_janela(janela, peca):
    pontuacao = 0
    peca_oponente = PECA_JOGADOR if peca == PECA_IA else PECA_IA

    if janela.count(peca) == 4:
        pontuacao += 100
    elif janela.count(peca) == 3 and janela.count(VAZIO) == 1:
        pontuacao += 5
    elif janela.count(peca) == 2 and janela.count(VAZIO) == 2:
        pontuacao += 2

    if janela.count(peca_oponente) == 3 and janela.count(VAZIO) == 1:
        pontuacao -= 4

    return pontuacao

def pontuar_tabuleiro(tabuleiro, peca):
    pontuacao = 0
    coluna_central = [int(i) for i in list(tabuleiro[:, COLUMN_COUNT // 2])]
    central_count = coluna_central.count(peca)
    pontuacao += central_count * 3

    for linha in range(ROW_COUNT):
        linha_array = [int(i) for i in list(tabuleiro[linha, :])]
        for c in range(COLUMN_COUNT - 3):
            janela = linha_array[c:c + WINDOW_LENGTH]
            pontuacao += avaliar_janela(janela, peca)

    for coluna in range(COLUMN_COUNT):
        coluna_array = [int(i) for i in list(tabuleiro[:, coluna])]
        for linha in range(ROW_COUNT - 3):
            janela = coluna_array[linha:linha + WINDOW_LENGTH]
            pontuacao += avaliar_janela(janela, peca)

    for linha in range(ROW_COUNT - 3):
        for coluna in range(COLUMN_COUNT - 3):
            janela = [tabuleiro[linha + i][coluna + i] for i in range(WINDOW_LENGTH)]
            pontuacao += avaliar_janela(janela, peca)

    for linha in range(ROW_COUNT - 3):
        for coluna in range(COLUMN_COUNT - 3):
            janela = [tabuleiro[linha + 3 - i][coluna + i] for i in range(WINDOW_LENGTH)]
            pontuacao += avaliar_janela(janela, peca)

    return pontuacao

def eh_terminal(tabuleiro):
    return jogada_vencedora(tabuleiro, PECA_JOGADOR) or jogada_vencedora(tabuleiro, PECA_IA) or len(locais_validos(tabuleiro)) == 0

def locais_validos(tabuleiro):
    locais = []
    for coluna in range(COLUMN_COUNT):
        if coluna_valida(tabuleiro, coluna):
            locais.append(coluna)
    return locais

def coluna_valida(tabuleiro, coluna):
    return tabuleiro[ROW_COUNT - 1][coluna] == 0