import networkx as nx
import matplotlib.pyplot as plt
import os

# Cores dos vértices
BRANCO = "BRANCO"
LARANJA = "LARANJA"
VERDE = "VERDE"


class Vertice:
    def __init__(self, id):
        """
        Inicializa um vértice com um identificador único e atributos padrão.

        Args:
            id: O identificador único do vértice.
        
        Atributos:
            id (str): Identificador do vértice.
            cor: Estado de visitação utilizado por BFS/DFS 
                (BRANCO = não visitado, LARANJA = descoberto, VERDE = finalizado).
            predecessor (Vertice | None): Vértice que precede este no percurso dos algoritmos.
            distancia (float): Distância mínima estimada a partir de uma origem
                (usado em BFS e Dijkstra).
            tempo_descoberta (int | None): Tempo em que o vértice foi descoberto na DFS.
            tempo_finalizacao (int | None): Tempo em que o vértice foi finalizado na DFS.
        """
        self.id = id
        self.cor = BRANCO
        self.predecessor = None
        self.distancia = float("inf")
        self.tempo_descoberta = None
        self.tempo_finalizacao = None

    def getId(self):
        """
        Retorna o identificador do vértice.

        Returns:
            O identificador do vértice.
        """
        return self.id

    def getCor(self):
        """
        Retorna a cor atual do vértice.

        Returns:
            A cor do vértice.
        """
        return self.cor

    def getPredecessor(self):
        """
        Retorna o predecessor do vértice.

        Returns:
            O predecessor do vértice.
        """
        return self.predecessor

    def getDistancia(self):
        """
        Retorna a distância do vértice a partir de uma origem.

        Returns:
            A distância do vértice.
        """
        return self.distancia

    def getTempoDescoberta(self):
        """
        Retorna o tempo de descoberta do vértice.

        Returns:
            O tempo de descoberta do vértice.
        """
        return self.tempo_descoberta

    def getTempoFinalizacao(self):
        """
        Retorna o tempo de finalização do vértice.

        Returns:
            O tempo de finalização do vértice.
        """
        return self.tempo_finalizacao

    def setId(self, id):
        """
        Define o identificador do vértice.

        Args:
            id: O novo identificador do vértice.
        """
        self.id = id

    def setCor(self, cor):
        """
        Define a cor do vértice.

        Args:
            cor: A nova cor do vértice.
        """
        self.cor = cor

    def setPredecessor(self, pred):
        """
        Define o predecessor do vértice.

        Args:
            pred: O novo predecessor do vértice.
        """
        self.predecessor = pred

    def setDistancia(self, dist):
        """
        Define a distância do vértice.

        Args:
            dist: A nova distância do vértice.
        """
        self.distancia = dist

    def setTempoDescoberta(self, tempo):
        """
        Define o tempo de descoberta do vértice.

        Args:
            tempo: O novo tempo de descoberta do vértice.
        """
        self.tempo_descoberta = tempo

    def setTempoFinalizacao(self, tempo):
        """
        Define o tempo de finalização do vértice.

        Args:
            tempo: O novo tempo de finalização do vértice.
        """
        self.tempo_finalizacao = tempo

    def __str__(self):
        """
        Retorna uma representação em string do vértice.

        Returns:
            str: O identificador do vértice como string.
        """
        return str(self.id)

    def __repr__(self):
        """
        Retorna uma representação oficial em string do vértice.

        Returns:
            str: Uma string no formato "Vertice(id)" representando o vértice.
        """
        return f"Vertice({self.id})"

class Grafo:
    def __init__(self, dirigido=False):
        """
        Inicializa um grafo, que pode ser dirigido ou não.

        Args:
            dirigido (bool, opcional): Indica se o grafo é dirigido. Padrão é False.
        """
        self.dirigido = dirigido
        self.adj = {}

    def getDirigido(self):
        """
        Retorna se o grafo é dirigido.

        Returns:
            bool: True se o grafo for dirigido, False caso contrário.
        """
        return self.dirigido

    def getAdj(self):
        """
        Retorna a lista de adjacência do grafo.

        Returns:
            dict: O dicionário de adjacência do grafo.
        """
        return self.adj

    def setDirigido(self, dirigido):
        """
        Define se o grafo é dirigido.

        Args:
            dirigido (bool): True para grafo dirigido, False para não dirigido.
        """
        self.dirigido = dirigido

    def setAdj(self, adj):
        """
        Define a lista de adjacência do grafo.

        Args:
            adj (dict): O novo dicionário de adjacência.
        """
        self.adj = adj

    def getOrdem(self):
        """
        Retorna a ordem do grafo (número de vértices).

        Returns:
            int: O número de vértices no grafo.
        """
        return len(self.adj)

    def getTamanho(self):
        """
        Retorna o tamanho do grafo (número de arestas).

        Returns:
            int: O número de arestas no grafo.
        """
        if self.dirigido:
            return sum(len(vizinhos) for vizinhos in self.adj.values())
        else:
            return sum(len(vizinhos) for vizinhos in self.adj.values()) // 2

    def vertices(self):
        """
        Retorna a lista de vértices do grafo.

        Returns:
            list: Uma lista contendo os vértices do grafo.
        """
        return list(self.adj.keys())

    def arestas(self):
        """
        Retorna a lista de arestas do grafo.

        Returns:
            list: Uma lista de tuplas representando as arestas do grafo.
                  Cada tupla contém dois vértices (u, v).
        """
        lista = []
        seen = set()
        for u, vizinhos in self.adj.items():
            for (v, _) in vizinhos:
                pair = (u, v)
                key = (u.id, v.id) if self.dirigido else tuple(sorted((u.id, v.id)))
                if key not in seen:
                    lista.append(pair)
                    seen.add(key)
        return lista

    def insereV(self, id):
        """
        Insere um novo vértice no grafo.

        Args:
            id: O identificador do novo vértice.

        Returns:
            Vertice: O vértice recém-criado, ou o vértice existente se o ID já estiver no grafo.
        """
        v_existente = self.get_vertice(id)
        if v_existente is not None:
            return v_existente
        novo = Vertice(id)
        self.adj[novo] = []
        return novo

    def removeV(self, v: Vertice):
        """
        Remove um vértice do grafo, juntamente com todas as arestas associadas a ele.

        Args:
            v (Vertice): O vértice a ser removido.
        """
        if v not in self.adj:
            return
        for u in list(self.adj.keys()):
            self.adj[u] = [(x, p) for (x, p) in self.adj[u] if x != v]
        del self.adj[v]

    def insereA(self, u_id, v_id, peso=1):
        """
        Insere aresta (u_id -> v_id) com peso. Cria vértices se necessário.

        Para grafo não-dirigido, insere também (v -> u) com mesmo peso.

        Args:
            u_id: O identificador do vértice de origem.
            v_id: O identificador do vértice de destino.
            peso (int, opcional): O peso da aresta. Padrão é 1.
        """
        u = self.get_vertice(u_id) or self.insereV(u_id)
        v = self.get_vertice(v_id) or self.insereV(v_id)

        if not any(x == v for (x, _) in self.adj[u]):
            self.adj[u].append((v, peso))

        if not self.dirigido:
            if not any(x == u for (x, _) in self.adj[v]):
                self.adj[v].append((u, peso))

    def removeA(self, u: Vertice, v: Vertice):
        """
        Remove aresta entre u e v (qualquer peso). Para não-dirigido remove
        ambas as direções.

        Args:
            u (Vertice): O vértice de origem.
            v (Vertice): O vértice de destino.
        """
        if u in self.adj:
            self.adj[u] = [(x, p) for (x, p) in self.adj[u] if x != v]
        if not self.dirigido and v in self.adj:
            self.adj[v] = [(x, p) for (x, p) in self.adj[v] if x != u]

    def getA(self, u: Vertice, v: Vertice):
        """
        Retorna uma aresta entre dois vértices, se existir.

        Args:
            u (Vertice): O vértice de origem.
            v (Vertice): O vértice de destino.

        Returns:
            tuple: Uma tupla representando a aresta (u, v) ou (v, u), dependendo do tipo do grafo.
               Retorna None se a aresta não existir.
        """
        if u in self.adj:
            for (x, p) in self.adj[u]:
                if x == v:
                    return (u, v, p)
        if not self.dirigido and v in self.adj:
            for (x, p) in self.adj[v]:
                if x == u:
                    return (v, u, p)
        return None

    def adjacentes(self, v: Vertice):
        """
        Retorna os vértices adjacentes a um vértice dado.

        Args:
            v (Vertice): O vértice para o qual os adjacentes serão retornados.

        Returns:
            list: Uma lista de vértices adjacentes ao vértice dado.
        """
        if v not in self.adj:
            return []
        return [x for (x, _) in self.adj[v]]
    

    def adjacentes_com_peso(self, vertice):
        """
        Retorna os vértices adjacentes a um dado vértice, juntamente com seus pesos.

        Se o peso não for um número inteiro ou de ponto flutuante, assume-se o peso como 1.

        Args:
            vertice (str): O vértice para o qual os adjacentes serão retornados.

        Returns:
            list: Uma lista de tuplas, onde cada tupla contém um vértice adjacente e seu peso.
                  Exemplo: [(v1, peso1), (v2, peso2), ...].
        """
        if vertice not in self.adj:
            return []
        result = []
        for (x, p) in self.adj[vertice]:
            if not isinstance(p, (int, float)):
                p = 1
            result.append((x, p))
        return result

    def grauE(self, v: Vertice):
        """
        Retorna o grau de entrada de um vértice.

        Args:
            v (Vertice): O vértice para o qual o grau de entrada será calculado.

        Returns:
            int: O grau de entrada do vértice.
        """
        if not self.dirigido:
            return len(self.adj.get(v, []))
        return sum(1 for u in self.adj if any(x == v for (x, _) in self.adj[u]))

    def grauS(self, v: Vertice):
        """
        Retorna o grau de saída de um vértice.

        Args:
            v (Vertice): O vértice para o qual o grau de saída será calculado.

        Returns:
            int: O grau de saída do vértice.
        """
        return len(self.adj.get(v, []))

    def grau(self, v: Vertice):
        """
        Retorna o grau total de um vértice.

        Para grafos dirigidos, o grau total é a soma do grau de entrada e do grau de saída.

        Args:
            v (Vertice): O vértice para o qual o grau total será calculado.

        Returns:
            int: O grau total do vértice.
        """
        if self.dirigido:
            return self.grauE(v) + self.grauS(v)
        return len(self.adj.get(v, []))

    def verticesA(self, aresta):
        """
        Retorna os vértices associados a uma aresta.

        Args:
            aresta (tuple): Uma tupla representando a aresta (u, v).

        Returns:
            tuple: A própria aresta, contendo os vértices associados.
        """
        return aresta

    def oposto(self, v: Vertice, aresta):
        """
        Retorna o vértice oposto a um dado vértice em uma aresta.

        Args:
            v (Vertice): O vértice conhecido.
            aresta (tuple): Uma tupla representando a aresta (u, w).

        Returns:
            Vertice: O vértice oposto ao vértice fornecido, ou None se o vértice não estiver na aresta.
        """
        u, w = aresta
        if v == u:
            return w
        elif v == w:
            return u
        return None

    def arestasE(self, v: Vertice):
        """
        Retorna as arestas de entrada de um vértice.

        Args:
            v (Vertice): O vértice para o qual as arestas de entrada serão retornadas.

        Returns:
            list: Uma lista de tuplas representando as arestas de entrada.
        """
        res = []
        for u in self.adj:
            for (x, _) in self.adj[u]:
                if x == v:
                    res.append((u, v))
        return res


    def arestasS(self, v: Vertice):
        """
        Retorna as arestas de saída de um vértice.

        Args:
            v (Vertice): O vértice para o qual as arestas de saída serão retornadas.

        Returns:
            list: Uma lista de tuplas representando as arestas de saída.
        """
        return [(v, x) for (x, _) in self.adj.get(v, [])]

    def get_vertice(self, id):
        """
        Retorna o vértice correspondente ao ID fornecido.

        Args:
            id: O identificador do vértice.

        Returns:
            O vértice correspondente ao ID, ou None se não for encontrado.
        """
        for v in self.adj.keys():
            if v.id == id:
                return v
        return None

    def __str__(self):
        """
        Retorna uma representação em string do grafo.

        Returns:
            str: Uma string que descreve o grafo, indicando se é dirigido ou não,
                 e listando os vértices e seus vizinhos.
        """
        texto = "Grafo dirigido\n" if self.dirigido else "Grafo não-dirigido\n"
        for v, vizinhos in self.adj.items():
            viz_ids = [x.id for (x, _) in vizinhos]
            texto += f"{v.id} -> {viz_ids}\n"
        return texto
    
    def desenhar_passo(self, pasta, contador, titulo="", passo_unico=False, prefixo="passo", pausar=True):
        """
        Desenha o grafo em um estado específico e salva a imagem em um arquivo.

        Args:
            pasta (str): O caminho da pasta onde a imagem será salva.
            contador (int): O número do passo atual, usado para nomear o arquivo.
            titulo (str, opcional): O título do grafo. Padrão é "".
            passo_unico (bool, opcional): Indica se o arquivo deve ser salvo como um único passo.
                                          Padrão é False.
            prefixo (str, opcional): O prefixo do nome do arquivo. Padrão é "passo".
            pausar (bool, opcional): Indica se o programa deve pausar após salvar a imagem.
                                     Padrão é True.

        # Função auxiliar para garantir criação de pastas
        Returns:
            int: O contador incrementado em 1.
        """
        G = nx.DiGraph() if self.dirigido else nx.Graph()

        # adicionar nós
        for v in self.vertices():
            G.add_node(v.id, color=v.cor)

        # adicionar arestas (com peso se houver)
        for u in self.adj:
            for (v, peso) in self.adj[u]:
                # networkx edge labels usam ids (strings/ints)
                G.add_edge(u.id, v.id, weight=peso)

        # layout fixo para estabilidade entre imagens
        pos = nx.spring_layout(G, seed=42)

        # mapear cores
        cor_map = {BRANCO: "white", LARANJA: "orange", VERDE: "green"}
        node_colors = [cor_map.get(self.get_vertice(node), "lightblue")  # fallback (não usado)
                       for node in G.nodes()]  # placeholder; vamos mapear corretamente abaixo

        # build node colors correctly using Vertice objects
        node_colors = []
        for node in G.nodes():
            v_obj = self.get_vertice(node)
            if v_obj is None:
                node_colors.append("lightblue")
            else:
                node_colors.append(cor_map.get(v_obj.cor, "lightblue"))

        plt.figure(figsize=(6, 6))
        nx.draw(G, pos, with_labels=True, node_size=1200,
                node_color=node_colors, font_size=12, font_weight="bold",
                edgecolors="black")

        # desenhar pesos se existirem
        edge_labels = nx.get_edge_attributes(G, "weight")
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        if titulo:
            plt.title(titulo)

        # montar caminho do arquivo
        if passo_unico:
            arquivo = os.path.join(pasta, f"{prefixo}_passo.png")
        else:
            arquivo = os.path.join(pasta, f"{prefixo}_passo_{contador}.png")

        plt.savefig(arquivo)
        plt.close()
        print(f"Imagem salva: {arquivo}")

        if pausar:
            input("Pressione Enter para continuar...")

        return contador + 1