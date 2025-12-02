"""
Arquivo contendo uma coleção completa de casos de teste para todos os algoritmos.

Cada caso tem o formato:

{
    "nome": "...",
    "dirigido": False/True,
    "arestas": [(u, v), (u, v, peso), ...],
    "origem": "A",            # opcional
    "vertice_inicial": "A"    # opcional (Prim)
}

Você pode carregar esse arquivo no seu main.
"""

casos_teste = [

    # ======================================================================
    # 1. GRAFOS SIMPLES PARA BFS / DFS
    # ======================================================================

    {
        "nome": "Grafo Simples Pequeno",
        "dirigido": False,
        "arestas": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    },

    {
        "nome": "Grafo em Linha (Path Graph)",
        "dirigido": False,
        "arestas": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]
    },

    {
        "nome": "Grafo Estrela (Star Graph)",
        "dirigido": False,
        "arestas": [("C", "A"), ("C", "B"), ("C", "D"), ("C", "E")]
    },

    {
        "nome": "Grafo Ciclo Simples",
        "dirigido": False,
        "arestas": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
    },

    # ======================================================================
    # 2. GRAFOS DIRECIONADOS
    # ======================================================================

    {
        "nome": "Grafo Direcionado Simples",
        "dirigido": True,
        "arestas": [("A", "B"), ("B", "C"), ("C", "A")]
    },

    {
        "nome": "DAG - Grafo Acíclico Direcionado",
        "dirigido": True,
        "arestas": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    },

    {
        "nome": "Grafo Direcionado com Componentes Desconexas",
        "dirigido": True,
        "arestas": [("A", "B"), ("C", "D"), ("D", "E")]
    },

    # ======================================================================
    # 3. GRAFOS PARA EULERIANO
    # ======================================================================

    {
        "nome": "Grafo Euleriano Pequeno",
        "dirigido": False,
        "arestas": [("A", "B"), ("B", "C"), ("C", "A")]
    },

    {
        "nome": "Grafo Não Euleriano (grau ímpar)",
        "dirigido": False,
        "arestas": [("A", "B"), ("B", "C"), ("C", "D")]
    },

    {
        "nome": "Grafo Euleriano Grande",
        "dirigido": False,
        "arestas": [
            ("A","B"),("B","C"),("C","D"),("D","E"),("E","F"),
            ("F","A"),("A","C"),("C","E"),("E","A")
        ]
    },

    # ======================================================================
    # 4. GRAFOS PARA DIJKSTRA / FLOYD-WARSHALL
    # ======================================================================

    {
        "nome": "Completo com Pesos Positivos",
        "dirigido": False,
        "arestas": [
            ("A","B",2), ("A","C",3), ("A","D",1),
            ("B","C",4), ("B","D",2),
            ("C","D",5)
        ],
        "origem": "A"
    },

    {
        "nome": "Grafo com Pesos Negativos (sem ciclo negativo)",
        "dirigido": True,
        "arestas": [
            ("A","B",2), ("B","C",-1), ("C","D",3), ("A","D",10)
        ],
        "origem": "A"
    },

    {
        "nome": "Grafo com Ciclo Negativo",
        "dirigido": True,
        "arestas": [
            ("A","B",1), ("B","C",2), ("C","A",-4)
        ],
        "origem": "A"
    },

    {
        "nome": "Grafo Desconexo Pesado",
        "dirigido": False,
        "arestas": [
            ("A","B",5),
            ("C","D",7)
        ],
        "origem": "A"
    },

    # ======================================================================
    # 5. GRAFOS PARA MST (Kruskal e Prim)
    # ======================================================================

    {
        "nome": "MST Completo Pequeno",
        "dirigido": False,
        "arestas": [
            ("A","B",4), ("A","C",3),
            ("B","C",1), ("B","D",2),
            ("C","D",4)
        ],
        "vertice_inicial": "A"
    },

    {
        "nome": "MST Grande",
        "dirigido": False,
        "arestas": [
            ("A","B",10), ("A","C",20), ("B","C",5), ("B","D",8),
            ("C","E",7), ("D","E",12), ("D","F",6), ("E","F",3)
        ],
        "vertice_inicial": "A"
    },

    {
        "nome": "MST com Subgrafos Desconexos",
        "dirigido": False,
        "arestas": [
            ("A","B",1), ("B","C",3),
            ("D","E",2)
        ],
        "vertice_inicial": "A"
    },

    # ======================================================================
    # 6. GRAFOS MAIORES (para BFS/DFS performance)
    # ======================================================================

    {
        "nome": "Grafo Grade 3x3",
        "dirigido": False,
        "arestas": [
            ("1","2"),("2","3"),
            ("4","5"),("5","6"),
            ("7","8"),("8","9"),
            ("1","4"),("4","7"),
            ("2","5"),("5","8"),
            ("3","6"),("6","9")
        ]
    },

    {
        "nome": "Grafo Linha Longa (10 vértices)",
        "dirigido": False,
        "arestas": [
            ("0","1"),("1","2"),("2","3"),("3","4"),("4","5"),
            ("5","6"),("6","7"),("7","8"),("8","9")
        ]
    },

    {
        "nome": "Grafo Aleatório Grande (20 vértices)",
        "dirigido": False,
        "arestas": [
            ("1","2"),("1","5"),("2","3"),("2","7"),("3","4"),
            ("4","10"),("5","6"),("6","7"),("7","8"),("8","9"),
            ("9","10"),("10","11"),("11","12"),("12","14"),("14","15"),
            ("15","16"),("16","18"),("18","19"),("19","20")
        ]
    }
]
