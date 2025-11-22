from collections import deque
from grafo import BRANCO, LARANJA, VERDE, Vertice, Grafo


class AlgoritmosGrafo:

    @staticmethod
    def bfs(grafo:Grafo, inicio: Vertice, pasta, passo_unico=False, pausar=True):
        for v in grafo.vertices():
            v.cor = BRANCO
            v.distancia = float("inf")
            v.predecessor = None

        inicio.cor = LARANJA
        inicio.distancia = 0
        inicio.predecessor = None

        fila = deque([inicio])
        contador = 1
        contador = grafo.desenhar_passo(
            pasta, contador, f"BFS: inicial {inicio.id}",
            passo_unico, prefixo="BFS", pausar=pausar
        )

        while fila:
            u = fila.popleft()
            for v in grafo.adjacentes(u):
                if v.cor == BRANCO:
                    v.cor = LARANJA
                    v.distancia = u.distancia + 1
                    v.predecessor = u
                    fila.append(v)
                    contador = grafo.desenhar_passo(
                        pasta, contador, f"BFS: {v.id} descoberto",
                        passo_unico, prefixo="BFS", pausar=pausar
                    )
            u.cor = VERDE
            contador = grafo.desenhar_passo(
                pasta, contador, f"BFS: {u.id} finalizado",
                passo_unico, prefixo="BFS", pausar=pausar
            )

    @staticmethod
    def dfs(grafo:Grafo, pasta, passo_unico=False, pausar=True):
        for v in grafo.vertices():
            v.cor = BRANCO
            v.predecessor = None
        tempo = [0]
        contador = 1
        for v in grafo.vertices():
            if v.cor == BRANCO:
                contador = AlgoritmosGrafo.dfs_visit(
                    grafo, v, tempo, pasta, contador,
                    passo_unico, pausar
                )
        return contador

    @staticmethod
    def dfs_visit(grafo:Grafo, u, tempo, pasta, contador, passo_unico=False, pausar=True):
        tempo[0] += 1
        u.tempo_descoberta = tempo[0]
        u.cor = LARANJA
        contador = grafo.desenhar_passo(
            pasta, contador, f"DFS: {u.id} descoberto",
            passo_unico, prefixo="DFS", pausar=pausar
        )
        for v in grafo.adjacentes(u):
            if v.cor == BRANCO:
                v.predecessor = u
                contador = AlgoritmosGrafo.dfs_visit(
                    grafo, v, tempo, pasta, contador,
                    passo_unico, pausar
                )
        u.cor = VERDE
        tempo[0] += 1
        u.tempo_finalizacao = tempo[0]
        contador = grafo.desenhar_passo(
            pasta, contador, f"DFS: {u.id} finalizado",
            passo_unico, prefixo="DFS", pausar=pausar
        )
        return contador

    @staticmethod
    def componentes_conexas_busca(grafo:Grafo):
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
    def componentes_conexas_unionfind(grafo:Grafo):
        parent = {}
        rank = {}

        def make_set(v):
            parent[v] = v
            rank[v] = 0

        def find_set(v):
            if parent[v] != v:
                parent[v] = find_set(parent[v])
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

        for v in grafo.vertices():
            make_set(v)

        for u, v in grafo.arestas():
            union(u, v)

        componentes = {}
        for v in grafo.vertices():
            raiz = find_set(v)
            if raiz not in componentes:
                componentes[raiz] = []
            componentes[raiz].append(v)

        return list(componentes.values())
    
    @staticmethod
    def conexo(grafo:Grafo):
        visitados = set()

        def dfs(v):
            visitados.add(v)
            for adj in grafo.adjacentes(v):
                if adj not in visitados:
                    dfs(adj)

        inicio = next((v for v in grafo.vertices() if grafo.adjacentes(v)), None)
        if not inicio:
            return True

        dfs(inicio)

        for v in grafo.vertices():
            if grafo.adjacentes(v) and v not in visitados:
                return False

        return True

    @staticmethod
    def euleriano(grafo:Grafo):
        if not AlgoritmosGrafo.conexo(grafo):
            return False
        
        for v in grafo.vertices():
            if len(grafo.adjacentes(v)) % 2 != 0:
                return False

        return True

    @staticmethod
    def get_ciclo_euleriano(grafo:Grafo):
        if not AlgoritmosGrafo.euleriano(grafo):
            return None

        ciclo = []
        stack = []
        arestas_restantes = {v: set(grafo.adjacentes(v)) for v in grafo.vertices()}

        atual = next(v for v in grafo.vertices() if arestas_restantes[v])

        while stack or arestas_restantes[atual]:
            if not arestas_restantes[atual]:
                ciclo.append(atual)
                atual = stack.pop()
            else:
                stack.append(atual)
                vizinho = arestas_restantes[atual].pop()
                arestas_restantes[vizinho].remove(atual)
                atual = vizinho

        ciclo.append(atual)
        return ciclo