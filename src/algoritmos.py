from collections import deque
from grafo import BRANCO, LARANJA, VERDE, Vertice, Grafo


class AlgoritmosGrafo:

    @staticmethod
    def bfs(grafo, inicio: Vertice, pasta, passo_unico=False, pausar=True):
        for v in grafo.vertices():
            v.cor = BRANCO
            v.distancia = float("inf")
            v.predecessor = None

        inicio.cor = LARANJA
        inicio.distancia = 0
        inicio.predecessor = None

        fila = deque([inicio])
        contador = 1
        contador = grafo.desenhar_passo(pasta, contador, f"BFS: inicial {inicio.id}", passo_unico, prefixo="BFS", pausar=pausar)

        while fila:
            u = fila.popleft()
            for v in grafo.adjacentes(u):
                if v.cor == BRANCO:
                    v.cor = LARANJA
                    v.distancia = u.distancia + 1
                    v.predecessor = u
                    fila.append(v)
                    contador = grafo.desenhar_passo(pasta, contador, f"BFS: {v.id} descoberto", passo_unico, prefixo="BFS", pausar=pausar)
            u.cor = VERDE
            contador = grafo.desenhar_passo(pasta, contador, f"BFS: {u.id} finalizado", passo_unico, prefixo="BFS", pausar=pausar)

    @staticmethod
    def dfs(grafo, pasta, passo_unico=False, pausar=True):
        for v in grafo.vertices():
            v.cor = BRANCO
            v.predecessor = None
        tempo = [0]
        contador = 1
        for v in grafo.vertices():
            if v.cor == BRANCO:
                contador = AlgoritmosGrafo.dfs_visit(grafo, v, tempo, pasta, contador, passo_unico, pausar)
        return contador

    @staticmethod
    def dfs_visit(grafo, u, tempo, pasta, contador, passo_unico=False, pausar=True):
        tempo[0] += 1
        u.tempo_descoberta = tempo[0]
        u.cor = LARANJA
        contador = grafo.desenhar_passo(pasta, contador, f"DFS: {u.id} descoberto", passo_unico, prefixo="DFS", pausar=pausar)
        for v in grafo.adjacentes(u):
            if v.cor == BRANCO:
                v.predecessor = u
                contador = AlgoritmosGrafo.dfs_visit(grafo, v, tempo, pasta, contador, passo_unico, pausar)
        u.cor = VERDE
        tempo[0] += 1
        u.tempo_finalizacao = tempo[0]
        contador = grafo.desenhar_passo(pasta, contador, f"DFS: {u.id} finalizado", passo_unico, prefixo="DFS", pausar=pausar)
        return contador

    @staticmethod
    def imprimir_caminho(origem: Vertice, destino: Vertice):
        if destino == origem:
            print(origem.id, end=" ")
        elif destino.predecessor is None:
            print(f"Não existe caminho de {origem.id} para {destino.id}", end=" ")
        else:
            AlgoritmosGrafo.imprimir_caminho(origem, destino.predecessor)
            print(destino.id, end=" ")

    @staticmethod
    def imprimir_tabela_vertices(grafo):
        print("\n| Vértice | Cor     | Distância | Predecessor | Descoberta | Finalização |")
        print("|" + "-"*8 + "|" + "-"*9 + "|" + "-"*10 + "|" + "-"*13 + "|" + "-"*11 + "|" + "-"*13 + "|")
        for v in grafo.vertices():
            pred = v.predecessor.id if v.predecessor else "-"
            desc = v.tempo_descoberta if v.tempo_descoberta else "-"
            fim = v.tempo_finalizacao if v.tempo_finalizacao else "-"
            print(f"| {v.id:^7} | {v.cor:^7} | {v.distancia:^9} | {pred:^11} | {desc:^9} | {fim:^11} |")
