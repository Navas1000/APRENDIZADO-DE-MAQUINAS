'''
Grupo:

José Pascoal Martins - 22002728
André Pádua da Costa - 22010866
Gustavo Mota - 22010798
Mateus Navarro Bella Cruz - 21004097
'''

import numpy as np
import random

# Define o objetivo e converte os elementos para string para evitar problemas de tipo
objetivo = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 'x']])

# Função para verificar se o jogo é válido (se é solúvel)
def jogo_valido(jogo):
    jogo_flat = jogo.flatten()
    jogo_sem_x = jogo_flat[jogo_flat != 'x']
    inversoes = 0
    for i in range(len(jogo_sem_x)):
        for j in range(i + 1, len(jogo_sem_x)):
            if jogo_sem_x[i] > jogo_sem_x[j]:
                inversoes += 1
    return inversoes % 2 == 0

# Função sucessora para fazer o movimento
def sucessor(jogo, atual, row_x, col_x):
    # Faz uma cópia do jogo
    novo_jogo = jogo.copy()
    row_atual, col_atual = np.where(novo_jogo == atual)
    row_atual, col_atual = row_atual[0], col_atual[0]
    novo_jogo[row_x, col_x], novo_jogo[row_atual, col_atual] = novo_jogo[row_atual, col_atual], novo_jogo[row_x, col_x]
    return novo_jogo

# Função para verificar se o estado atual é o estado final
def eh_estado_final(jogo, objetivo):
    return np.array_equal(jogo, objetivo)

# Gera o jogo e verifica se é válido
while True:
    jogo = objetivo.flatten()
    random.shuffle(jogo)
    jogo = np.reshape(jogo, (3, 3))
    if jogo_valido(jogo):
        break

print("Seu objetivo é chegar em: \n", objetivo)


# Loop principal do jogo
while not eh_estado_final(jogo, objetivo):  # Utiliza a função de retorno booleana
    posicao_x = np.where(jogo == 'x')

    print("Jogo atual:")
    print(jogo)
    print()

    row_x, col_x = posicao_x[0][0], posicao_x[1][0]

    adjacent_elements = []
    if row_x > 0:
        adjacent_elements.append(jogo[row_x - 1, col_x])
    if row_x < 2:
        adjacent_elements.append(jogo[row_x + 1, col_x])
    if col_x > 0:
        adjacent_elements.append(jogo[row_x, col_x - 1])
    if col_x < 2:
        adjacent_elements.append(jogo[row_x, col_x + 1])

    print("Você pode mover:", adjacent_elements)

    atual = input("Escolha um número para mover: ")
    print()

    # Verifica se o movimento é válido e faz a troca usando a função sucessor
    if atual in adjacent_elements:
        jogo = sucessor(jogo, atual, row_x, col_x)
    else:
        print("Movimento inválido! Tente novamente.")

print("Parabéns! Você completou o jogo.")