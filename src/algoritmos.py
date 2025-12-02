from collections import deque
import heapq
from grafo import BRANCO, LARANJA, VERDE, Vertice, Grafo


class AlgoritmosGrafo:
    """Conjunto de algoritmos clássicos para grafos, incluindo buscas,
    conectividade, detecção de ciclos e algoritmos de caminhos mínimos e AGM."""

    @staticmethod
    def bfs(grafo: Grafo, inicio: Vertice, pasta, passo_unico=False, pausar=True):
        """
        Executa a Busca em Largura (BFS) a partir de um vértice inicial.

        A função também desenha os passos da execução em arquivos, caso o grafo
        possua o método `desenhar_passo`.

        Args:
            grafo (Grafo): O grafo onde a BFS será executada.
            inicio (Vertice): Vértice inicial da busca.
            pasta (str): Caminho da pasta para salvar os passos.
            passo_unico (bool, optional): Se True, salva todos os passos em um único arquivo.
                Padrão é False.
            pausar (bool, optional): Se True, pausa a cada passo desenhado.
                Padrão é True.
        """
        for v in grafo.vertices():
            v.cor = BRANCO
            v.distancia = float("inf")
            v.predecessor = None

        inicio.cor = LARANJA
        inicio.distancia = 0

        fila = deque([inicio])
        contador = 1

        contador = grafo.desenhar_passo(
            pasta, contador, f"BFS: inicial {inicio.id}",
            passo_unico, prefixo="BFS", pausar=pausar
        )

        while fila:
            u = fila.popleft()
            for v in [adj for adj, _ in grafo.adjacentes_com_peso(u)]:
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
    def dfs(grafo: Grafo, pasta, passo_unico=False, pausar=True):
        """
        Executa a Busca em Profundidade (DFS) completa no grafo.

        A função chama recursivamente `dfs_visit` para cada vértice não visitado
        e desenha cada etapa da busca caso `desenhar_passo` esteja implementado.

        Args:
            grafo (Grafo): O grafo onde a DFS será realizada.
            pasta (str): Caminho da pasta para salvar imagens dos passos.
            passo_unico (bool, optional): Salva todos os passos em um único arquivo.
                Padrão é False.
            pausar (bool, optional): Pausa após cada passo. Padrão é True.

        Returns:
            int: Contador final de passos utilizados.
        """
        for v in grafo.vertices():
            v.cor = BRANCO
            v.predecessor = None

        tempo = [0]
        contador = 1

        for v in grafo.vertices():
            if v.cor == BRANCO:
                contador = AlgoritmosGrafo.dfs_visit(
                    grafo, v, tempo, pasta, contador, passo_unico, pausar
                )

        return contador

    @staticmethod
    def dfs_visit(grafo: Grafo, u, tempo, pasta, contador, passo_unico=False, pausar=True):
        """
        Visita recursivamente um vértice na DFS.

        Args:
            grafo (Grafo): O grafo sendo explorado.
            u (Vertice): Vértice atual.
            tempo (list): Lista com único inteiro representando o tempo global.
            pasta (str): Pasta para salvar desenhos.
            contador (int): Contador de passos.
            passo_unico (bool, optional): Se deve salvar tudo num único arquivo.
            pausar (bool, optional): Se deve pausar a cada passo.

        Returns:
            int: Novo valor do contador.
        """
        tempo[0] += 1
        u.tempo_descoberta = tempo[0]
        u.cor = LARANJA

        contador = grafo.desenhar_passo(
            pasta, contador, f"DFS: {u.id} descoberto",
            passo_unico, prefixo="DFS", pausar=pausar
        )

        for v in [adj for adj, _ in grafo.adjacentes_com_peso(u)]:
            if v.cor == BRANCO:
                v.predecessor = u
                contador = AlgoritmosGrafo.dfs_visit(
                    grafo, v, tempo, pasta, contador, passo_unico, pausar
                )

        u.cor = VERDE
        tempo[0] += 1
        u.tempo_finalizacao = tempo[0]

        return grafo.desenhar_passo(
            pasta, contador, f"DFS: {u.id} finalizado",
            passo_unico, prefixo="DFS", pausar=pausar
        )
    
    @staticmethod
    def componentes_conexas_busca(grafo: Grafo):
        """
        Retorna as componentes conexas usando DFS simples.

        Args:
            grafo (Grafo): Grafo a ser analisado.

        Returns:
            list[list[Vertice]]: Lista de componentes, cada uma contendo vértices.
        """
        for v in grafo.vertices():
            v.cor = BRANCO
            v.predecessor = None

        componentes = []

        for v in grafo.vertices():
            if v.cor == BRANCO:
                comp = []
                AlgoritmosGrafo._dfs_coleta(grafo, v, comp)
                componentes.append(comp)

        return componentes

    @staticmethod
    def _dfs_coleta(grafo, u, componente):
        """
        Auxiliar da DFS para coletar vértices de uma componente conexa.

        Args:
            grafo (Grafo): O grafo.
            u (Vertice): Vértice atual.
            componente (list): Lista sendo preenchida com os vértices visitados.
        """
        u.cor = LARANJA
        componente.append(u)

        for v in [adj for adj, _ in grafo.adjacentes_com_peso(u)]:
            if v.cor == BRANCO:
                AlgoritmosGrafo._dfs_coleta(grafo, v, componente)

        u.cor = VERDE

    @staticmethod
    def componentes_conexas_unionfind(grafo: Grafo):
        """
        Retorna as componentes conexas utilizando Union-Find.

        Args:
            grafo (Grafo): Grafo a ser analisado.

        Returns:
            list[list[Vertice]]: Lista com cada componente como lista de vértices.
        """
        parent = {}
        rank = {}

        def make_set(v):
            parent[v] = v
            rank[v] = 0

        def find_set(v):
            if parent[v] != v:
                parent[v] = find_set(parent[v])
            return parent[v]

        def union(a, b):
            ra, rb = find_set(a), find_set(b)
            if ra != rb:
                if rank[ra] > rank[rb]:
                    parent[rb] = ra
                elif rank[ra] < rank[rb]:
                    parent[ra] = rb
                else:
                    parent[rb] = ra
                    rank[ra] += 1

        for v in grafo.vertices():
            make_set(v)

        for u, v in grafo.arestas():
            union(u, v)

        comp = {}
        for v in grafo.vertices():
            raiz = find_set(v)
            comp.setdefault(raiz, []).append(v)

        return list(comp.values())

    @staticmethod
    def conexo(grafo: Grafo):
        """
        Verifica se o grafo é conexo.

        Args:
            grafo (Grafo): O grafo a ser analisado.

        Returns:
            bool: True se o grafo é conexo, False caso contrário.
        """
        vertices = grafo.vertices()
        if not vertices:
            return True

        inicio = next((v for v in vertices if grafo.adjacentes(v)), None)

        if not inicio:
            return True

        for v in vertices:
            v.cor = BRANCO

        componente = []
        AlgoritmosGrafo._dfs_coleta(grafo, inicio, componente)

        for v in vertices:
            if grafo.adjacentes(v) and v.cor == BRANCO:
                return False

        return True
    
    @staticmethod
    def euleriano(grafo: Grafo):
        """
        Verifica se o grafo possui um ciclo euleriano.

        Condições:
        - Grafo precisa ser conexo.
        - Todos os vértices precisam ter grau par.

        Args:
            grafo (Grafo): O grafo a ser analisado.

        Returns:
            bool: True se é euleriano, False caso contrário.
        """
        if not AlgoritmosGrafo.conexo(grafo):
            return False

        return all(grafo.grau(v) % 2 == 0 for v in grafo.vertices())

    @staticmethod
    def get_ciclo_euleriano(grafo: Grafo):
        """
        Retorna um ciclo euleriano utilizando o algoritmo de Hierholzer.

        Args:
            grafo (Grafo): O grafo euleriano.

        Returns:
            list[Vertice] | None: Lista representando o ciclo,
            ou None caso o grafo não seja euleriano.
        """
        if not AlgoritmosGrafo.euleriano(grafo):
            return None

        ciclo = []
        stack = []

        adj = {}
        for v in grafo.vertices():
            vizinhos = set()
            for x, _ in grafo.adjacentes_com_peso(v):
                vizinhos.add(x)
            adj[v] = vizinhos

        atual = None
        for v in grafo.vertices():
            if adj[v]:  # se o conjunto não está vazio
                atual = v
                break

        while stack or adj[atual]:
            if not adj[atual]:
                ciclo.append(atual)
                atual = stack.pop()
            else:
                stack.append(atual)
                viz = adj[atual].pop()
                adj[viz].remove(atual)
                atual = viz

        ciclo.append(atual)
        return ciclo
    
    @staticmethod
    def eh_hamiltoniano(grafo: Grafo):
        """
        Verifica se o grafo possui AO MENOS UM ciclo Hamiltoniano.

        Método exato usando backtracking.
        Complexidade: O(n!), adequado para grafos pequenos/médios.

        Args:
            grafo (Grafo)

        Returns:
            bool: True se existe ciclo Hamiltoniano, False caso negativo.
        """
        ciclo_existe, _ = AlgoritmosGrafo.ciclo_hamiltoniano(grafo)
        return ciclo_existe


    @staticmethod
    def ciclo_hamiltoniano(grafo: Grafo):
        """
        Retorna um ciclo Hamiltoniano caso exista.

        Método exato (backtracking). Retorna o ciclo como lista de vértices
        terminando no vértice inicial.

        Args:
            grafo (Grafo)

        Returns:
            tuple:
                - bool: True se encontrou ciclo
                - list[Vertice] | None: ciclo completo (incluindo retorno ao início)
        """
        vertices = grafo.vertices()
        n = len(vertices)

        if n == 0:
            return False, None

        inicio = vertices[0]
        caminho = [inicio]
        visitados = {inicio}

        def backtrack(atual):
            if len(caminho) == n:
                if inicio in grafo.adjacentes(atual):
                    return True
                return False

            for v in grafo.adjacentes(atual):
                if v not in visitados:
                    visitados.add(v)
                    caminho.append(v)

                    if backtrack(v):
                        return True

                    visitados.remove(v)
                    caminho.pop()

            return False

        existe = backtrack(inicio)

        if existe:
            return True, caminho + [inicio]

        return False, None

    @staticmethod
    def floyd_warshall(grafo):
        """
        Executa o algoritmo de Floyd-Warshall para todos os pares de vértices.

        Args:
            grafo (Grafo): Grafo ponderado (sem pesos negativos).

        Returns:
            tuple:
                - dict: distâncias mínimas entre todos os pares.
                - dict: predecessores para reconstrução dos caminhos.
        """

        vertices = grafo.vertices()

        # Inicializar matriz de distâncias
        dist = {}
        for u in vertices:
            dist[u.id] = {}
            for v in vertices:
                dist[u.id][v.id] = float("inf")

        # Inicializar matriz de predecessores
        pred = {}
        for u in vertices:
            pred[u.id] = {}
            for v in vertices:
                pred[u.id][v.id] = None

        # Inicialização: distância para ele mesmo = 0
        for origem in vertices:
            dist[origem.id][origem.id] = 0

            # Preenche distâncias diretas (arestas)
            for destino, peso in grafo.adjacentes_com_peso(origem):
                dist[origem.id][destino.id] = peso
                pred[origem.id][destino.id] = origem.id

        # Etapa principal do algoritmo de Floyd-Warshall
        # k = vértice intermediário
        # i = vértice de origem
        # j = vértice de destino
        # Se passar por k melhora o caminho de i → j, atualiza dist e predecessor
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    caminho_atual = dist[i.id][j.id]
                    caminho_via_k = dist[i.id][k.id] + dist[k.id][j.id]

                    if caminho_via_k < caminho_atual:
                        dist[i.id][j.id] = caminho_via_k
                        pred[i.id][j.id] = pred[k.id][j.id]


        # Retorna matrizes de distâncias e predecessores
        return dist, pred

    @staticmethod
    def dijkstra(grafo, origem):
        """
        Executa o algoritmo de Dijkstra para caminhos mínimos a partir de uma fonte.

        Args:
            grafo (Grafo): Grafo ponderado sem pesos negativos.
            origem (str): ID do vértice inicial.

        Returns:
            tuple:
                - dict: distâncias mínimas (chave = id do vértice).
                - dict: predecessores de cada vértice.
        """
        dist = {v: float("inf") for v in grafo.vertices()}
        pred = {v: None for v in grafo.vertices()}

        origem_v = grafo.get_vertice(origem)
        dist[origem_v] = 0

        fila = [(0, origem_v.id, origem_v)]

        while fila:
            dist_u, _, u = heapq.heappop(fila)

            if dist_u > dist[u]:
                continue

            for v, peso in grafo.adjacentes_com_peso(u):
                nova = dist[u] + peso
                if nova < dist[v]:
                    dist[v] = nova
                    pred[v] = u
                    heapq.heappush(fila, (nova, v.id, v))

        # Converte as chaves (que são objetos Vertice) para seus IDs
        dist_formatado = {}
        for vertice, distancia in dist.items():
            dist_formatado[vertice.id] = distancia

        pred_formatado = {}
        for vertice, predecessor in pred.items():
            pred_formatado[vertice.id] = predecessor.id if predecessor else None

        return dist_formatado, pred_formatado

    @staticmethod
    def possui_pesos_negativos(grafo: Grafo):
        """
        Verifica se o grafo possui alguma aresta com peso negativo.

        Args:
            grafo (Grafo): Grafo a ser analisado.

        Returns:
            bool: True se existe peso negativo, False caso contrário.
        """
        return any(
            peso < 0
            for u in grafo.vertices()
            for _, peso in grafo.adjacentes_com_peso(u)
        )

    @staticmethod
    def kruskal(grafo):
        """
        Calcula a Árvore Geradora Mínima (AGM) usando o algoritmo de Kruskal.

        Ideia geral:
        - Ordena todas as arestas por peso (da menor para a maior)
        - Percorre as arestas, adicionando apenas aquelas que NÃO formam ciclo
        - Usa Union-Find (disjoint set) para detectar ciclos


        Args:
            grafo (Grafo): Grafo ponderado.

        Returns:
            tuple:
                - list[tuple]: Arestas da AGM na forma (u, v, peso).
                - float: Custo total da árvore.
        """
        arestas = [
            (peso, u, v)
            for u in grafo.vertices()
            for v, peso in grafo.adjacentes_com_peso(u)
        ]

        # Ordena as arestas crescentemente pelo peso
        arestas.sort(key=lambda x: x[0])

        parent = {}
        rank = {}
        
        def criar_conjunto(v):
            parent[v] = v
            rank[v] = 0

        def encontrar(v):
            if parent[v] != v:
                parent[v] = encontrar(parent[v])
            return parent[v]

        def unir(a, b):
            ra, rb = encontrar(a), encontrar(b)
            if ra != rb: # se pertencem a conjuntos diferentes
                if rank[ra] > rank[rb]:
                    parent[rb] = ra
                elif rank[ra] < rank[rb]:
                    parent[ra] = rb
                else:
                    parent[rb] = ra
                    rank[ra] += 1

        for v in grafo.vertices():
            criar_conjunto(v)

        mst = [] #lista de arestas da árvore geradora mínima
        custo = 0

        for peso, u, v in arestas:
            if encontrar(u) != encontrar(v):
                unir(u, v)
                mst.append((u, v, peso))
                custo += peso

        return mst, custo


    @staticmethod
    def prim(grafo, vertice_inicial):
        """
        Calcula a Árvore Geradora Mínima (AGM) usando o algoritmo de Prim.

        Args:
            grafo (Grafo): Grafo ponderado.
            vertice_inicial (Vertice): Vértice inicial da AGM.

        Returns:
            tuple:
                - list[tuple]: Arestas da AGM (u, v, peso)
                - float: custo total da AGM
        """
        mst = []
        visitados = set()
        fila = []
        custo = 0

        def adicionar_arestas(v):
            visitados.add(v)
            for adj, peso in grafo.adjacentes_com_peso(v):
                if adj not in visitados:
                    heapq.heappush(fila, (peso, v.id, adj.id, v, adj))

        adicionar_arestas(vertice_inicial)

        while fila:
            peso, _, _, u, v = heapq.heappop(fila)
            if v not in visitados:
                mst.append((u, v, peso))
                custo += peso
                adicionar_arestas(v)

        return mst, custo
