'''
Grupo:

José Pascoal Martins - 22002728
André Pádua da Costa - 22010866
Gustavo Mota - 22010798
Mateus Navarro Bella Cruz - 21004097
'''

import numpy as np
import random
from collections import deque
import heapq

# Define o objetivo
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
    novo_jogo = jogo.copy()
    row_atual, col_atual = np.where(novo_jogo == atual)
    novo_jogo[row_x, col_x], novo_jogo[row_atual[0], col_atual[0]] = novo_jogo[row_atual[0], col_atual[0]], novo_jogo[row_x, col_x]
    return novo_jogo

# Função para verificar se o estado atual é o estado final
def eh_estado_final(jogo):
    return np.array_equal(jogo, objetivo)

# Função de busca em largura
def busca_em_largura(inicio):
    # Inicializa a fila com o estado inicial e um caminho vazio
    fila = deque([(inicio, [])])
    visitados = {tuple(map(tuple, inicio))}  # Conjunto para rastrear estados visitados
    estados_visitados = 0

    # Loop principal da busca
    while fila:
        atual, caminho_atual = fila.popleft()  # Remove o primeiro estado da fila
        estados_visitados += 1
        
        if eh_estado_final(atual):  # Verifica se o estado atual é o objetivo
            return estados_visitados, caminho_atual + [atual]
        
        posicao_x = np.where(atual == 'x')  # Encontra a posição do espaço vazio
        row_x, col_x = posicao_x[0][0], posicao_x[1][0]
        
        # Lista de movimentos possíveis
        movimentos = [(row_x-1, col_x), (row_x+1, col_x), (row_x, col_x-1), (row_x, col_x+1)]
        
        for row_novo, col_novo in movimentos:
            # Verifica se o movimento está dentro dos limites do tabuleiro
            if 0 <= row_novo < 3 and 0 <= col_novo < 3:
                novo_estado = sucessor(atual, atual[row_novo, col_novo], row_x, col_x)  # Gera um novo estado
                estado_tuple = tuple(map(tuple, novo_estado))  # Converte o novo estado em tupla
                if estado_tuple not in visitados:  # Se o novo estado não foi visitado
                    visitados.add(estado_tuple)  # Marca como visitado
                    fila.append((novo_estado, caminho_atual + [atual]))  # Adiciona à fila

    return "Sem solução", []  # Retorna que não há solução se a fila esvaziar

# Função de busca em profundidade
def busca_em_profundidade(inicio):
    # Inicializa a pilha com o estado inicial e um caminho vazio
    pilha = [(inicio, [])]
    visitados = {tuple(map(tuple, inicio))}  # Conjunto para rastrear estados visitados
    estados_visitados = 0

    # Loop principal da busca
    while pilha:
        atual, caminho_atual = pilha.pop()  # Remove o último estado da pilha
        estados_visitados += 1
        
        if eh_estado_final(atual):  # Verifica se o estado atual é o objetivo
            return estados_visitados, caminho_atual + [atual]
        
        posicao_x = np.where(atual == 'x')  # Encontra a posição do espaço vazio
        row_x, col_x = posicao_x[0][0], posicao_x[1][0]
        
        # Lista de movimentos possíveis
        movimentos = [(row_x-1, col_x), (row_x+1, col_x), (row_x, col_x-1), (row_x, col_x+1)]
        
        for row_novo, col_novo in movimentos:
            # Verifica se o movimento está dentro dos limites do tabuleiro
            if 0 <= row_novo < 3 and 0 <= col_novo < 3:
                novo_estado = sucessor(atual, atual[row_novo, col_novo], row_x, col_x)  # Gera um novo estado
                estado_tuple = tuple(map(tuple, novo_estado))  # Converte o novo estado em tupla
                if estado_tuple not in visitados:  # Se o novo estado não foi visitado
                    visitados.add(estado_tuple)  # Marca como visitado
                    pilha.append((novo_estado, caminho_atual + [atual]))  # Adiciona à pilha

    return "Sem solução", []  # Retorna que não há solução se a pilha esvaziar

# Heurística para A*
def heuristica(jogo):
    dist = 0
    for i in range(3):
        for j in range(3):
            if jogo[i, j] != 'x':
                valor = int(jogo[i, j]) - 1
                target_row, target_col = divmod(valor, 3)
                dist += abs(target_row - i) + abs(target_col - j)  # Calcula a distância Manhattan
    return dist

# Função de busca A*
def busca_a_star(inicio):
    # Inicializa a fila de prioridade com o estado inicial
    fila = []
    estado_inicial_tuple = tuple(map(tuple, inicio))
    heapq.heappush(fila, (0 + heuristica(inicio), estado_inicial_tuple, []))  # Prioridade inicial
    visitados = {estado_inicial_tuple}  # Conjunto para rastrear estados visitados
    estados_visitados = 0

    # Loop principal da busca
    while fila:
        _, atual_tuple, caminho_atual = heapq.heappop(fila)  # Remove o estado com menor prioridade
        estados_visitados += 1
        
        atual = np.array(atual_tuple)  # Converte de volta para array
        
        if eh_estado_final(atual):  # Verifica se o estado atual é o objetivo
            return estados_visitados, caminho_atual + [atual]
        
        posicao_x = np.where(atual == 'x')  # Encontra a posição do espaço vazio
        row_x, col_x = posicao_x[0][0], posicao_x[1][0]
        
        # Lista de movimentos possíveis
        movimentos = [(row_x-1, col_x), (row_x+1, col_x), (row_x, col_x-1), (row_x, col_x+1)]
        
        for row_novo, col_novo in movimentos:
            # Verifica se o movimento está dentro dos limites do tabuleiro
            if 0 <= row_novo < 3 and 0 <= col_novo < 3:
                novo_estado = sucessor(atual, atual[row_novo, col_novo], row_x, col_x)  # Gera um novo estado
                estado_tuple = tuple(map(tuple, novo_estado))  # Converte o novo estado em tupla
                if estado_tuple not in visitados:  # Se o novo estado não foi visitado
                    visitados.add(estado_tuple)  # Marca como visitado
                    prioridade = estados_visitados + heuristica(novo_estado)  # Calcula a prioridade
                    heapq.heappush(fila, (prioridade, estado_tuple, caminho_atual + [atual]))  # Adiciona à fila

    return "Sem solução", []  # Retorna que não há solução se a fila esvaziar

# Gera o jogo e verifica se é válido
while True:
    jogo = objetivo.flatten()
    random.shuffle(jogo)  # Embaralha as peças
    jogo = np.reshape(jogo, (3, 3))  # Reformata para matriz 3x3
    if jogo_valido(jogo):  # Verifica se o jogo é solúvel
        break

print("Seu objetivo é chegar em: \n", objetivo)

# Loop principal do jogo ou escolha de IA
while True:
    print("\nEscolha uma opção:")
    print("1 - Jogar")
    print("2 - Resolver com IA")
    opcao = input("Opção: ")

    if opcao == '1':
        while not eh_estado_final(jogo):
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

            if atual in adjacent_elements:
                jogo = sucessor(jogo, atual, row_x, col_x)  # Faz o movimento
            else:
                print("Movimento inválido! Tente novamente.")

        print("Parabéns! Você completou o jogo.")

    elif opcao == '2':
        print("\nEscolha a IA para resolver:")
        print("1 - Busca em Largura")
        print("2 - Busca em Profundidade")
        print("3 - Busca A*")
        escolha_ia = input("Opção: ")

        if escolha_ia == '1':
            estados_visitados, caminho_final = busca_em_largura(jogo)  # Chama a busca em largura
        elif escolha_ia == '2':
            estados_visitados, caminho_final = busca_em_profundidade(jogo)  # Chama a busca em profundidade
        elif escolha_ia == '3':
            estados_visitados, caminho_final = busca_a_star(jogo)  # Chama a busca A*
        else:
            print("Opção inválida.")
            continue

        print(f"Quantidade de estados visitados: {estados_visitados}")  # Exibe o número de estados visitados
        print("Passo a passo até o resultado final:")
        for idx, estado in enumerate(caminho_final):  # Exibe cada passo da solução
            print(f"Passo {idx + 1}:")
            print(estado)

        break
    else:
        print("Opção inválida. Tente novamente.")
