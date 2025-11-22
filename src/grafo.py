import networkx as nx
import matplotlib.pyplot as plt
import os

# Cores dos vértices
BRANCO = "BRANCO"
LARANJA = "LARANJA"
VERDE = "VERDE"


class Vertice:
    def __init__(self, id):
        self.id = id
        self.cor = BRANCO
        self.predecessor = None
        self.distancia = float("inf")
        self.tempo_descoberta = None
        self.tempo_finalizacao = None

    def getId(self):
        return self.id

    def getCor(self):
        return self.cor

    def getPredecessor(self):
        return self.predecessor

    def getDistancia(self):
        return self.distancia

    def getTempoDescoberta(self):
        return self.tempo_descoberta

    def getTempoFinalizacao(self):
        return self.tempo_finalizacao

    def setId(self, id):
        self.id = id

    def setCor(self, cor):
        self.cor = cor

    def setPredecessor(self, pred):
        self.predecessor = pred

    def setDistancia(self, dist):
        self.distancia = dist

    def setTempoDescoberta(self, tempo):
        self.tempo_descoberta = tempo

    def setTempoFinalizacao(self, tempo):
        self.tempo_finalizacao = tempo

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Vertice({self.id})"

class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adj = {} 

    def getDirigido(self):
        return self.dirigido

    def getAdj(self):
        return self.adj

    def setDirigido(self, dirigido):
        self.dirigido = dirigido

    def setAdj(self, adj):
        self.adj = adj

    def getOrdem(self):
        return len(self.adj)

    def getTamanho(self):
        if self.dirigido:
            return sum(len(vizinhos) for vizinhos in self.adj.values())
        else:
            return sum(len(vizinhos) for vizinhos in self.adj.values()) // 2

    def vertices(self):
        return list(self.adj.keys())

    def arestas(self):
        lista = []
        for u, vizinhos in self.adj.items():
            for v in vizinhos:
                if self.dirigido or (v, u) not in lista:
                    lista.append((u, v))
        return lista

    def insereV(self, id):
        if id not in [v.id for v in self.adj]:
            v = Vertice(id)
            self.adj[v] = []
            return v
        return self.get_vertice(id)

    def removeV(self, v: Vertice):
        if v in self.adj:
            for u in list(self.adj.keys()):
                if v in self.adj[u]:
                    self.adj[u].remove(v)
            del self.adj[v]

    def insereA(self, u_id, v_id, peso=None):
        u = self.get_vertice(u_id)
        v = self.get_vertice(v_id)
        if u is None:
            u = self.insereV(u_id)
        if v is None:
            v = self.insereV(v_id)
        self.adj[u].append(v)
        if not self.dirigido:
            self.adj[v].append(u)

    def removeA(self, u: Vertice, v: Vertice):
        if v in self.adj.get(u, []):
            self.adj[u].remove(v)
        if not self.dirigido and u in self.adj.get(v, []):
            self.adj[v].remove(u)

    def getA(self, u: Vertice, v: Vertice):
        if v in self.adj.get(u, []):
            return (u, v)
        if not self.dirigido and u in self.adj.get(v, []):
            return (v, u)
        return None

    def adjacentes(self, v: Vertice):
        return self.adj[v]

    def grauE(self, v: Vertice):
        if not self.dirigido:
            return len(self.adj[v])
        return sum(1 for u in self.adj if v in self.adj[u])

    def grauS(self, v: Vertice):
        return len(self.adj[v])

    def grau(self, v: Vertice):
        if self.dirigido:
            return self.grauE(v) + self.grauS(v)
        return len(self.adj[v])

    def verticesA(self, aresta):
        return aresta

    def oposto(self, v: Vertice, aresta):
        u, w = aresta
        if v == u:
            return w
        elif v == w:
            return u
        return None

    def arestasE(self, v: Vertice):
        return [(u, v) for u in self.adj if v in self.adj[u]]

    def arestasS(self, v: Vertice):
        return [(v, u) for u in self.adj[v]]

    def get_vertice(self, id):
        for v in self.adj.keys():
            if v.id == id:
                return v
        return None

    def __str__(self):
        texto = "Grafo dirigido\n" if self.dirigido else "Grafo não-dirigido\n"
        for v, vizinhos in self.adj.items():
            texto += f"{v.id} -> {[u.id for u in vizinhos]}\n"
        return texto

    def desenhar_passo(self, pasta, contador, titulo="", passo_unico=False, prefixo="passo", pausar=True):
        G = nx.DiGraph() if self.dirigido else nx.Graph()
        for v in self.vertices():
            G.add_node(v.id)
        for v in self.vertices():
            for u in self.adjacentes(v):
                G.add_edge(v.id, u.id)

        cor_map = {BRANCO: "white", LARANJA: "orange", VERDE: "green"}
        node_colors = [cor_map.get(v.cor, "lightblue") for v in self.vertices()]
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(6, 6))
        nx.draw(G, pos, with_labels=True, node_size=1200,
                node_color=node_colors, font_size=12, font_weight="bold",
                edgecolors="black")
        if titulo:
            plt.title(titulo)

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
