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

        @staticmethod
    def componentes_conexas_busca(grafo):
        for v in grafo.vertices():
            v.cor = BRANCO
            v.predecessor = None

        componentes = []
        for v in grafo.vertices():
            if v.cor == BRANCO:
                componente = []
                AlgoritmosGrafo._dfs_coleta(grafo, v, componente)
                componentes.append(componente)

        return componentes

    @staticmethod
    def _dfs_coleta(grafo, u, componente):
        u.cor = LARANJA
        componente.append(u)
        for v in grafo.adjacentes(u):
            if v.cor == BRANCO:
                AlgoritmosGrafo._dfs_coleta(grafo, v, componente)
        u.cor = VERDE

        @staticmethod
    def componentes_conexas_unionfind(grafo):
        parent = {}
        rank = {}

        def make_set(v):
            parent[v] = v
            rank[v] = 0

        def find_set(v):
            if parent[v] != v:
                parent[v] = find_set(parent[v])  # path compression
            return parent[v]

        def union(u, v):
            ru, rv = find_set(u), find_set(v)
            if ru != rv:
                if rank[ru] < rank[rv]:
                    parent[ru] = rv
                elif rank[ru] > rank[rv]:
                    parent[rv] = ru
                else:
                    parent[rv] = ru
                    rank[ru] += 1

        # inicializa conjuntos
        for v in grafo.vertices():
            make_set(v)

        # une os conjuntos com base nas arestas
        for u, v in grafo.arestas():
            union(u, v)

        # agrupa vértices por representante
        componentes = {}
        for v in grafo.vertices():
            raiz = find_set(v)
            if raiz not in componentes:
                componentes[raiz] = []
            componentes[raiz].append(v)

        return list(componentes.values())

        @staticmethod
    def componentes_conexas_goodman(grafo):
        # Copia do grafo (para não destruir o original)
        H = Grafo(dirigido=grafo.dirigido)
        for v in grafo.vertices():
            H.insereV(v.id)
        for u, v in grafo.arestas():
            H.insereA(u.id, v.id)

        componentes = []

        while H.getOrdem() > 0:
            # pega um vértice qualquer
            v = next(iter(H.vertices()))
            # cria a componente
            componente = [v]
            mudou = True
            while mudou:
                mudou = False
                for u in list(H.adjacentes(v)):
                    # funde v e u
                    novo = Vertice(f"{v.id}_{u.id}")
                    H.adj[novo] = []
                    # adiciona vizinhos de v e u
                    vizinhos = set(H.adjacentes(v) + H.adjacentes(u))
                    vizinhos.discard(u)
                    vizinhos.discard(v)
                    for x in vizinhos:
                        H.adj[novo].append(x)
                        H.adj[x].append(novo)
                        if v in H.adj[x]:
                            H.adj[x].remove(v)
                        if u in H.adj[x]:
                            H.adj[x].remove(u)

                    # remove v e u
                    del H.adj[v]
                    del H.adj[u]

                    v = novo
                    H.adj[v] = list(set(H.adj[v]))  # remove duplicatas
                    componente.append(u)
                    mudou = True
                    break  # volta e tenta fundir de novo

            # remove o vértice final da fusão
            del H.adj[v]
            componentes.append(componente)

        return componentes
