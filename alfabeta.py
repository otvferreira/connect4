import numpy as np
import math
from minimax import coluna_valida, proxima_linha_livre, jogada_vencedora, locais_validos, pontuar_tabuleiro

ROW_COUNT = 7
COLUMN_COUNT = 8
WINDOW_LENGTH = 4
VAZIO = 0
PECA_JOGADOR = 2
PECA_IA = 1

def alfabeta(tabuleiro, profundidade, alfa, beta, maximizando):
    """
    Implementa o algoritmo Alfa-Beta.
    """
    locais = locais_validos(tabuleiro)
    terminal = jogada_vencedora(tabuleiro, PECA_JOGADOR) or jogada_vencedora(tabuleiro, PECA_IA) or len(locais) == 0

    if profundidade == 0 or terminal:
        if terminal:
            if jogada_vencedora(tabuleiro, PECA_IA):
                return (None, 100000000000000)
            elif jogada_vencedora(tabuleiro, PECA_JOGADOR):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, pontuar_tabuleiro(tabuleiro, PECA_IA))

    if maximizando:
        valor = -math.inf
        melhor_coluna = locais[0]
        for coluna in locais:
            linha = proxima_linha_livre(tabuleiro, coluna)
            copia_tabuleiro = tabuleiro.copy()
            copia_tabuleiro[linha][coluna] = PECA_IA
            novo_valor = alfabeta(copia_tabuleiro, profundidade - 1, alfa, beta, False)[1]
            if novo_valor > valor:
                valor = novo_valor
                melhor_coluna = coluna
            alfa = max(alfa, valor)
            if alfa >= beta:
                break
        return melhor_coluna, valor
    else:
        valor = math.inf
        melhor_coluna = locais[0]
        for coluna in locais:
            linha = proxima_linha_livre(tabuleiro, coluna)
            copia_tabuleiro = tabuleiro.copy()
            copia_tabuleiro[linha][coluna] = PECA_JOGADOR
            novo_valor = alfabeta(copia_tabuleiro, profundidade - 1, alfa, beta, True)[1]
            if novo_valor < valor:
                valor = novo_valor
                melhor_coluna = coluna
            beta = min(beta, valor)
            if alfa >= beta:
                break
        return melhor_coluna, valor
