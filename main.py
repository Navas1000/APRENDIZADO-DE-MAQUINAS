# Importando as bibliotecas necessárias
import numpy as np   # Biblioteca para cálculos numéricos, incluindo funções matemáticas como a distância euclidiana
import random        # Biblioteca para geração de números aleatórios
import matplotlib.pyplot as plt  # Biblioteca para visualização de gráficos
import time          # Biblioteca para medir o tempo de execução do código

# Função para calcular a distância Euclidiana entre dois pontos (p1 e p2)
def distancia_euclidiana(p1, p2):
    # A fórmula da distância Euclidiana em duas dimensões é:
    # sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Função para calcular a aptidão de uma rota (distância total percorrida)
def aptidao(rota, pontos):
    distancia_total = 0
    # A rota é uma lista de índices dos pontos; percorre todos os pontos da rota.
    for i in range(len(rota)):
        # Soma a distância entre os pontos consecutivos
        distancia_total += distancia_euclidiana(pontos[rota[i - 1]], pontos[rota[i]])
    return distancia_total

# Função para gerar uma população inicial de rotas aleatórias
def gerar_populacao(tam_populacao, num_pontos):
    populacao = []
    # Cria uma população de tamanho tam_populacao com rotas aleatórias
    for _ in range(tam_populacao):
        # A rota é uma permutação aleatória dos pontos, com números de 0 a num_pontos-1
        populacao.append(random.sample(range(num_pontos), num_pontos))
    return populacao

# Função de seleção: escolhe dois pais com base na aptidão (quanto menor a distância, maior a aptidão)
def selecao(populacao, pontos):
    # A aptidão é inversamente proporcional à distância: quanto menor a distância, maior a aptidão
    valores_aptidao = [1 / aptidao(ind, pontos) for ind in populacao]
    aptidao_total = sum(valores_aptidao)  # Soma total das aptidões
    # Probabilidades para cada indivíduo serem selecionados como pais
    probabilidades = [f / aptidao_total for f in valores_aptidao]
    # Escolhe um indivíduo com base nas probabilidades
    return populacao[np.random.choice(len(populacao), p=probabilidades)]

# Função de crossover: combina dois pais para criar um filho (particiona a rota de forma cruzada)
def cruzamento(pai1, pai2):
    tamanho = len(pai1)
    # Sorteia dois índices para definir a região que será copiada do pai1
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho  # Inicializa a rota do filho com None (vazia)
    # Copia a parte da rota de pai1 para o filho
    filho[inicio:fim] = pai1[inicio:fim]

    # Preenche o restante da rota com os elementos do pai2
    indice_p2 = 0
    for i in range(tamanho):
        if filho[i] is None:
            # Garante que não haja repetição de pontos na rota
            while pai2[indice_p2] in filho:
                indice_p2 += 1
            filho[i] = pai2[indice_p2]
    
    return filho

# Função de mutação: troca aleatoriamente dois elementos da rota
def mutacao(rota, taxa_mutacao):
    # Se um número aleatório for menor que a taxa de mutação, realiza a mutação
    if random.random() < taxa_mutacao:
        # Escolhe dois índices aleatórios da rota
        i, j = random.sample(range(len(rota)), 2)
        # Troca os elementos desses índices
        rota[i], rota[j] = rota[j], rota[i]

# Função para executar o algoritmo genético
def algoritmo_genetico(pontos, tam_populacao=100, geracoes=500, taxa_mutacao=0.01, plotar=False):
    num_pontos = len(pontos)  # Número de pontos a serem visitados
    # Gera uma população inicial
    populacao = gerar_populacao(tam_populacao, num_pontos)
    melhor_rota = None  # Melhor rota encontrada até o momento
    melhor_distancia = float('inf')  # Inicializa a melhor distância com um valor muito alto
    
    # Armazena o histórico de aptidão para visualização
    historico_aptidao = []

    # Loop sobre as gerações
    for geracao in range(geracoes):
        nova_populacao = []

        # Cria a nova população usando o crossover e mutação
        for _ in range(tam_populacao):
            # Seleção de dois pais
            pai1 = selecao(populacao, pontos)
            pai2 = selecao(populacao, pontos)

            # Crossover para gerar um novo filho
            filho = cruzamento(pai1, pai2)

            # Mutação do filho
            mutacao(filho, taxa_mutacao)

            nova_populacao.append(filho)

        # Atualiza a população para a nova geração
        populacao = nova_populacao

        # Encontra o melhor indivíduo (menor distância) da nova geração
        melhor_rota_atual = min(populacao, key=lambda ind: aptidao(ind, pontos))
        melhor_distancia_atual = aptidao(melhor_rota_atual, pontos)

        # Se a melhor distância atual for melhor que a anterior, atualiza a melhor rota
        if melhor_distancia_atual < melhor_distancia:
            melhor_rota = melhor_rota_atual
            melhor_distancia = melhor_distancia_atual

        # Armazena a melhor distância da geração atual
        historico_aptidao.append(melhor_distancia)

        # Exibe o progresso a cada 50 gerações
        if geracao % 50 == 0:
            print(f"Geração {geracao} | Melhor distância: {melhor_distancia}")
        
        # Plotar a rota em cada 50 gerações, se solicitado
        if plotar and geracao % 50 == 0:
            plotar_rota(melhor_rota_atual, pontos, geracao)

    return melhor_rota, melhor_distancia, historico_aptidao

# Função para gerar pontos uniformemente distribuídos no espaço 2D
def gerar_pontos_uniformes(num_pontos):
    # Cria uma lista de pontos aleatórios no intervalo [0, 10] para x e y
    return [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(num_pontos)]

# Função para gerar pontos distribuídos em um círculo
def gerar_pontos_circulares(num_pontos):
    # Distribui os pontos uniformemente em um círculo unitário (raio 1)
    return [(np.cos(2 * np.pi * i / num_pontos), np.sin(2 * np.pi * i / num_pontos)) for i in range(num_pontos)]

# Função para visualizar a rota
def plotar_rota(rota, pontos, geracao=None):
    # Ordena os pontos conforme a rota dada
    pontos_ordenados = [pontos[i] for i in rota] + [pontos[rota[0]]]
    # Plota a rota com linha azul e pontos como círculos
    plt.plot([p[0] for p in pontos_ordenados], [p[1] for p in pontos_ordenados], 'b-', marker='o')
    # Se houver um número de geração, coloca no título
    plt.title(f"Rota na geração {geracao}" if geracao is not None else "Melhor Rota")
    plt.show()

# Função para visualizar a evolução da aptidão
def plotar_evolucao_aptidao(historico_aptidao):
    plt.plot(historico_aptidao)  # Plota a evolução da melhor distância
    plt.title("Evolução da aptidão")
    plt.xlabel("Geração")
    plt.ylabel("Distância")
    plt.show()

# Parâmetros
num_pontos = 8  # Número de pontos a serem visitados
tam_populacao = 100  # Tamanho da população
geracoes = 500  # Número de gerações do algoritmo genético
taxa_mutacao = 0.01  # Taxa de mutação

# Cenário 1: Pontos uniformemente distribuídos
print("Cenário 1: Pontos uniformemente distribuídos")
pontos_uniformes = gerar_pontos_uniformes(num_pontos)
melhor_rota, melhor_distancia, historico_aptidao = algoritmo_genetico(pontos_uniformes, tam_populacao, geracoes, taxa_mutacao, plotar=True)
print(f"Melhor distância (uniforme): {melhor_distancia}")
plotar_rota(melhor_rota, pontos_uniformes)
plotar_evolucao_aptidao(historico_aptidao)

# Cenário 2: Pontos em um círculo
print("Cenário 2: Pontos em um círculo")
pontos_circulares = gerar_pontos_circulares(num_pontos)  # Gera pontos distribuídos uniformemente em um círculo
melhor_rota, melhor_distancia, historico_aptidao = algoritmo_genetico(pontos_circulares, tam_populacao, geracoes, taxa_mutacao, plotar=True)
print(f"Melhor distância (circular): {melhor_distancia}")
plotar_rota(melhor_rota, pontos_circulares)  # Exibe a melhor rota encontrada
plotar_evolucao_aptidao(historico_aptidao)  # Exibe o gráfico de evolução da aptidão

# Bônus: Teste com grande quantidade de pontos (100 pontos em círculo)
print("Bônus: Cenário com 100 pontos em círculo")
pontos_circulares_grandes = gerar_pontos_circulares(100)  # Gera 100 pontos distribuídos em um círculo
inicio_tempo = time.time()  # Registra o tempo de início para medir o tempo de execução
melhor_rota, melhor_distancia, historico_aptidao = algoritmo_genetico(pontos_circulares_grandes, tam_populacao, geracoes, taxa_mutacao)
fim_tempo = time.time()  # Registra o tempo após a execução
print(f"Melhor distância (100 pontos): {melhor_distancia}")  # Exibe a melhor distância para o caso de 100 pontos
print(f"Tempo de execução: {fim_tempo - inicio_tempo:.2f} segundos")  # Exibe o tempo de execução
plotar_evolucao_aptidao(historico_aptidao)  # Exibe o gráfico de evolução da aptidão para o caso com 100 pontos
plotar_rota(melhor_rota, pontos_circulares_grandes)  # Exibe a melhor rota encontrada para o caso com 100 pontos

