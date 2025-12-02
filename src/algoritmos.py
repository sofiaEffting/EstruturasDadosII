from collections import deque
import heapq
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

    @staticmethod
    def floyd_warshall(grafo):
        vertices = grafo.vertices()
        distancias = {u.id: {v.id: float('inf') for v in vertices} for u in vertices}
        predecessores = {u.id: {v.id: None for v in vertices} for u in vertices}
        
        for u in vertices:
            distancias[u.id][u.id] = 0
            for v, peso in grafo.adjacentes_com_peso(u):
                distancias[u.id][v.id] = peso
                predecessores[u.id][v.id] = u.id
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if distancias[i.id][j.id] > distancias[i.id][k.id] + distancias[k.id][j.id]:
                        distancias[i.id][j.id] = distancias[i.id][k.id] + distancias[k.id][j.id]
                        predecessores[i.id][j.id] = predecessores[k.id][j.id]

        return distancias, predecessores

    @staticmethod
    def dijkstra(grafo, origem):
        distancias = {v: float('inf') for v in grafo.vertices()}
        predecessores = {v: None for v in grafo.vertices()}
        distancias[grafo.get_vertice(origem)] = 0

        fila_prioridade = [(0, grafo.get_vertice(origem))] 

        while fila_prioridade:
            dist_atual, u = heapq.heappop(fila_prioridade)

            if dist_atual > distancias[u]:
                continue

            for v, peso in grafo.adjacentes_com_peso(u):
                nova_dist = distancias[u] + peso
                if nova_dist < distancias[v]:
                    distancias[v] = nova_dist
                    predecessores[v] = u
                    heapq.heappush(fila_prioridade, (nova_dist, v))
        distancias = {v.id: d for v, d in distancias.items()}
        predecessores = {v.id: (p.id if p else None) for v, p in predecessores.items()}

        return distancias, predecessores

    @staticmethod
    def possui_pesos_negativos(grafo: Grafo):
        for u in grafo.vertices():
            for v, peso in grafo.adjacentes_com_peso(u):
                if peso < 0:
                    return True
        return False
    
    @staticmethod
    def kruskal(grafo):
        arestas = []
        for u in grafo.vertices():
            for v, peso in grafo.adjacentes_com_peso(u):
                arestas.append((peso, u, v))
        arestas.sort(key=lambda x: x[0])
        parent = {}
        rank = {}

        def make_set(v):
            parent[v] = v
            rank[v] = 0

        def find(v):
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]

        def union(v1, v2):
            root1 = find(v1)
            root2 = find(v2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        for v in grafo.vertices():
            make_set(v)

        mst = []
        custo_total = 0

        for peso, u, v in arestas:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, peso))
                custo_total += peso

        return mst, custo_total
    
    @staticmethod
    def prim(grafo, vertice_inicial):
        mst = []
        visitados = set()
        fila_prioridade = []
        custo_total = 0

        def adicionar_arestas(v):
            visitados.add(v)
            for adj, peso in grafo.adjacentes_com_peso(v):
                if adj not in visitados:
                    heapq.heappush(fila_prioridade, (peso, v, adj))

        adicionar_arestas(vertice_inicial)

        while fila_prioridade:
            peso, u, v = heapq.heappop(fila_prioridade)
            if v not in visitados:
                mst.append((u, v, peso))
                custo_total += peso
                adicionar_arestas(v)

        return mst, custo_total