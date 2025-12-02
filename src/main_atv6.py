from grafo import Grafo
from algoritmos import AlgoritmosGrafo

# Casos de teste
casos_mst = [
    {
        "nome": "Caso 1 - Grafo Completo com Pesos Pequenos",
        "dirigido": False,
        "arestas": [("A", "B", 2), ("A", "C", 3), ("B", "C", 1), ("B", "D", 4), ("C", "D", 5)],
        "vertice_inicial": "A"
    },
    {
        "nome": "Caso 2 - Grafo com Pesos Maiores",
        "dirigido": False,
        "arestas": [("A", "B", 10), ("A", "C", 15), ("B", "C", 5), ("B", "D", 20), ("C", "D", 25)],
        "vertice_inicial": "A"
    },
    {
        "nome": "Caso 3 - Grafo Desconexo",
        "dirigido": False,
        "arestas": [("A", "B", 1), ("C", "D", 2)],
        "vertice_inicial": "A"
    },
    {
        "nome": "Caso 4 - Grafo com Ciclo",
        "dirigido": False,
        "arestas": [("A", "B", 4), ("B", "C", 6), ("C", "D", 8), ("D", "A", 10), ("A", "C", 5)],
        "vertice_inicial": "A"
    }
]

for caso in casos_mst:
    print(f"\nAnalisando: {caso['nome']}")

    grafo = Grafo(dirigido=caso.get("dirigido", False))
    for u, v, peso in caso["arestas"]:
        grafo.insereV(u)
        grafo.insereV(v)
        grafo.insereA(u, v, peso)

    print("\n>>> Algoritmo de Prim <<<")
    vertice_inicial = grafo.get_vertice(caso["vertice_inicial"])
    mst_prim, custo_prim = AlgoritmosGrafo.prim(grafo, vertice_inicial)
    print("Árvore Geradora Mínima (Prim):")
    for u, v, peso in mst_prim:
        print(f"  {u.id} --({peso})--> {v.id}")
    print(f"Custo Total (Prim): {custo_prim}")

    print("\n>>> Algoritmo de Kruskal <<<")
    mst_kruskal, custo_kruskal = AlgoritmosGrafo.kruskal(grafo)
    print("Árvore Geradora Mínima (Kruskal):")
    for u, v, peso in mst_kruskal:
        print(f"  {u.id} --({peso})--> {v.id}")
    print(f"Custo Total (Kruskal): {custo_kruskal}")

    print("\n>>> Comparação <<<")
    if custo_prim == custo_kruskal:
        print("Os custos das árvores geradoras mínimas são consistentes entre os algoritmos.")
    else:
        print("Inconsistência nos custos das árvores geradoras mínimas!")