import random

class Puzzle8:
    def __init__(self):
        self.estado = self.gerar_estado_solvivel()
        self.objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 'X']
        self.movimentos_realizados = 0
        self.historico_estados = [self.estado.copy()]
        self.debug_mode = False

    def gerar_estado_solvivel(self):
        """Gera um estado inicial válido e solucionável para o 8-puzzle."""
        estado = list(range(1, 9)) + ['X']
        while True:
            random.shuffle(estado)
            if self.eh_solvivel(estado):
                return estado

    def eh_solvivel(self, estado):
        """Verifica se o estado é solucionável."""
        inversoes = 0
        estado_1d = [x for x in estado if x != 'X']
        for i in range(len(estado_1d)):
            for j in range(i + 1, len(estado_1d)):
                if estado_1d[i] > estado_1d[j]:
                    inversoes += 1
        return inversoes % 2 == 0

    def exibir_estado(self):
        """Exibe o estado atual do puzzle de forma legível."""
        print("Estado Atual:")
        for i in range(0, 9, 3):
            print(f"{self.estado[i]} {self.estado[i+1]} {self.estado[i+2]}")
        print(f"Movimentos realizados: {self.movimentos_realizados}")
        print()

    def obter_movimentos_possiveis(self):
        """Retorna uma lista de movimentos possíveis baseados na posição do espaço vazio ('X')."""
        movimentos = []
        posicao_x = self.estado.index('X')
        linha, coluna = divmod(posicao_x, 3)
        
        if coluna < 2: movimentos.append(1)  # Mover para a direita
        if coluna > 0: movimentos.append(-1)  # Mover para a esquerda
        if linha < 2: movimentos.append(3)  # Mover para baixo
        if linha > 0: movimentos.append(-3)  # Mover para cima
        
        return movimentos

    def realizar_movimento(self, movimento):
        """Executa o movimento dado e atualiza o estado do puzzle."""
        posicao_x = self.estado.index('X')
        nova_posicao_x = posicao_x + movimento
        self.estado[posicao_x], self.estado[nova_posicao_x] = self.estado[nova_posicao_x], self.estado[posicao_x]
        self.movimentos_realizados += 1
        self.historico_estados.append(self.estado.copy())

    def eh_estado_objetivo(self):
        """Verifica se o estado atual é o estado final (objetivo)."""
        return self.estado == self.objetivo

    def modo_debug(self):
        """Ativa o modo de depuração para imprimir informações adicionais."""
        self.debug_mode = True
        print("Modo de depuração ativado.")

    def desativar_debug(self):
        """Desativa o modo de depuração."""
        self.debug_mode = False
        print("Modo de depuração desativado.")

    def jogar(self):
        """Função principal para jogar o puzzle."""
        print("Bem-vindo ao 8-Puzzle!")
        self.exibir_estado()
        if self.debug_mode:
            print(f"Estado inicial: {self.estado}")

        while not self.eh_estado_objetivo():
            movimentos = self.obter_movimentos_possiveis()
            mapa_movimentos = {1: "direita", -1: "esquerda", 3: "baixo", -3: "cima"}
            print(f"Movimentos disponíveis: {', '.join(mapa_movimentos[movimento] for movimento in movimentos)}")
            
            movimento = int(input("Escolha um movimento (1 para direita, -1 para esquerda, 3 para baixo, -3 para cima): "))
            if movimento in movimentos:
                self.realizar_movimento(movimento)
                self.exibir_estado()
                if self.debug_mode:
                    print(f"Histórico de estados: {self.historico_estados}")
            else:
                print("Movimento inválido. Tente novamente.")
        
        print("Parabéns! Você resolveu o puzzle!")

if __name__ == "__main__":
    jogo = Puzzle8()
    
    # Ativar o modo de depuração se necessário
    # jogo.modo_debug()
    
    jogo.jogar()
