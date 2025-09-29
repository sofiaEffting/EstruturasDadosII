import os
import shutil
from grafo import Grafo
from algoritmos import AlgoritmosGrafo

# ==========================
# Pergunta inicial
# ==========================
resposta_salvar_passos = input("Deseja salvar cada passo como imagem separada? (s/n): ").strip().lower()
passo_unico = resposta_salvar_passos != 's'
pausar_passos = True

# ==========================
# Casos de teste
# ==========================
casos = [
    {
        "nome": "Caso 1 - Grafo simples não-dirigido",
        "dirigido": False,
        "arestas": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")],
        "inicio_bfs": "A"
    },
    {
        "nome": "Caso 2 - Grafo dirigido",
        "dirigido": True,
        "arestas": [("1", "2"), ("1", "3"), ("2", "4"), ("3", "4"), ("4", "5")],
        "inicio_bfs": "1"
    },
    {
        "nome": "Caso 3 - Grafo com ciclo",
        "dirigido": False,
        "arestas": [("X", "Y"), ("Y", "Z"), ("Z", "X"), ("Z", "W")],
        "inicio_bfs": "X"
    }
]

pasta_principal = "imagens_grafos"
os.makedirs(pasta_principal, exist_ok=True)

for i, caso in enumerate(casos, start=1):
    print("\n" + "="*40)
    print(f"{caso['nome']}")
    print("="*40)

    pasta_caso = os.path.join(pasta_principal, f"caso{i}")
    os.makedirs(pasta_caso, exist_ok=True)

    g = Grafo(dirigido=caso["dirigido"])
    for u, v in caso["arestas"]:
        g.insereA(u, v)

    # Grafo inicial
    print("\n--- Grafo inicial ---")
    print(g)
    g.desenhar_passo(pasta_caso, 1, "Grafo inicial", passo_unico, prefixo="Grafo", pausar=pausar_passos)

    # BFS
    inicio = g.get_vertice(caso["inicio_bfs"])
    print("\n--- BFS passo a passo ---")
    AlgoritmosGrafo.bfs(g, inicio, pasta_caso, passo_unico, pausar=pausar_passos)
    AlgoritmosGrafo.imprimir_tabela_vertices(g)
    print("\nCaminhos a partir de", inicio.id)
    for v in g.vertices():
        print(f"{inicio.id} -> {v.id}: ", end="")
        AlgoritmosGrafo.imprimir_caminho(inicio, v)
        print()

    # DFS
    print("\n--- DFS passo a passo ---")
    AlgoritmosGrafo.dfs(g, pasta_caso, passo_unico, pausar=pausar_passos)
    AlgoritmosGrafo.imprimir_tabela_vertices(g)
    print("\nCaminhos a partir de", inicio.id)
    for v in g.vertices():
        print(f"{inicio.id} -> {v.id}: ", end="")
        AlgoritmosGrafo.imprimir_caminho(inicio, v)
        print()

# Pergunta final sobre manter imagens
manter = input(f"\nDeseja manter as imagens na pasta '{pasta_principal}'? (s/n): ").strip().lower()
if manter != 's':
    shutil.rmtree(pasta_principal)
    print("Todas as imagens foram deletadas.")
