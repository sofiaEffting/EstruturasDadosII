from grafo import Grafo
from algoritmos import AlgoritmosGrafo

casos_dijkstra_fw = [
    {
        "nome": "Caso 1 - Grafo Completo com Pesos Pequenos",
        "dirigido": False,
        "arestas": [("A", "B", 2), ("A", "C", 3), ("B", "C", 1), ("B", "D", 4), ("C", "D", 5)],
        "origem": "A"
    },
    {
        "nome": "Caso 2 - Grafo com Pesos Negativos (Sem Ciclos Negativos)",
        "dirigido": True,
        "arestas": [("A", "B", 4), ("B", "C", 2), ("C", "D", 3), ("D", "A", 1)],
        "origem": "A"
    },
    {
        "nome": "Caso 3 - Grafo Desconexo",
        "dirigido": False,
        "arestas": [("A", "B", 1), ("C", "D", 2)],
        "origem": "A"
    },
    {
        "nome": "Caso 4 - Grafo com Ciclo Negativo (Para Testar Floyd-Warshall)",
        "dirigido": True,
        "arestas": [("A", "B", 1), ("B", "C", 2), ("C", "A", -1)],
        "origem": "A"
    }
]

for caso in casos_dijkstra_fw:
    print(f"\nAnalisando: {caso['nome']}")

    grafo = Grafo(dirigido=caso.get("dirigido", False))

    for u, v, peso in caso["arestas"]:
        grafo.insereV(u)
        grafo.insereV(v)
        grafo.insereA(u, v, peso)

    print("\n>>> Executando Floyd-Warshall <<<")
    distancias_fw, _ = AlgoritmosGrafo.floyd_warshall(grafo)
    print("Distâncias calculadas pelo Floyd-Warshall:")
    for u in distancias_fw:
        for v in distancias_fw[u]:
            print(f"  {u} -> {v}: {distancias_fw[u][v]}")

    if AlgoritmosGrafo.possui_pesos_negativos(grafo):
        print("\n>>> O grafo possui pesos negativos. O algoritmo de Dijkstra não será executado. <<<")
        continue

    print("\n>>> Executando Dijkstra para cada vértice <<<")
    distancias_dijkstra_todos = {}
    for origem in grafo.vertices():
        origem_id = origem.getId()
        distancias_dijkstra, _ = AlgoritmosGrafo.dijkstra(grafo, origem_id)
        distancias_dijkstra_todos[origem_id] = distancias_dijkstra
        print(f"Distâncias calculadas pelo Dijkstra a partir do vértice '{origem_id}':")
        for v, d in distancias_dijkstra.items():
            print(f"  {origem_id} -> {v}: {d}")

    print("\n>>> Comparando os resultados de Dijkstra e Floyd-Warshall <<<")
    consistente = True
    for origem, distancias_dijkstra in distancias_dijkstra_todos.items():
        for destino, distancia_dijkstra in distancias_dijkstra.items():
            if destino not in distancias_fw[origem]:
                consistente = False
                print(f"Inconsistência encontrada: {origem} -> {destino} (Dijkstra: {distancia_dijkstra}, Floyd-Warshall: valor não encontrado)")
            elif distancia_dijkstra != distancias_fw[origem][destino]:
                consistente = False
                print(f"Inconsistência encontrada: {origem} -> {destino} (Dijkstra: {distancia_dijkstra}, Floyd-Warshall: {distancias_fw[origem][destino]})")

    if consistente:
        print("Os resultados de Dijkstra e Floyd-Warshall são consistentes para todos os vértices.")