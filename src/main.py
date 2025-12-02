import importlib.util
import os
from grafo import Grafo
from algoritmos import AlgoritmosGrafo

def garantir_pasta(nome):
    os.makedirs(nome, exist_ok=True)

def carregar_casos(caminho):
    if not os.path.isfile(caminho):
        print("X Arquivo não encontrado.")
        return None

    try:
        spec = importlib.util.spec_from_file_location("modulo_casos", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        if not hasattr(modulo, "casos_teste"):
            print("X O arquivo não contém a variável 'casos_teste'.")
            return None

        print(f"✔ {len(modulo.casos_teste)} casos carregados.\n")
        return modulo.casos_teste

    except Exception as e:
        print(f"X Erro ao carregar arquivo: {e}")
        return None

def construir_grafo(caso):
    grafo = Grafo(dirigido=caso.get("dirigido", False))

    for item in caso["arestas"]:
        if len(item) == 2:
            u, v = item
            grafo.insereV(u)
            grafo.insereV(v)
            grafo.insereA(u, v)

        elif len(item) == 3:
            u, v, peso = item
            grafo.insereV(u)
            grafo.insereV(v)
            grafo.insereA(u, v, peso)

    return grafo

def menu_algoritmos(grafo, caso):
    while True:
        print("\n=== MENU DE ALGORITMOS ===")
        print("1 - BFS")
        print("2 - DFS")
        print("3 - Componentes Conexas (DFS)")
        print("4 - Componentes Conexas (Union-Find)")
        print("5 - Verificar se é Conexo")
        print("6 - Verificar Eulerianidade")
        print("7 - Floyd-Warshall")
        print("8 - Dijkstra (uma origem)")
        print("9 - Dijkstra (todas as origens)")
        print("10 - Kruskal (AGM)")
        print("11 - Prim (AGM)")
        print("12 - Verificar se é Hamiltoniano")
        print("13 - Obter ciclo Hamiltoniano")
        print("0 - Voltar")
        opcao = input("Escolha: ")


        if opcao == "0":
            return


        elif opcao == "1":
            inicio = input("Vértice inicial da BFS: ").strip()
            v = grafo.get_vertice(inicio)
            if v:
                garantir_pasta("imagens_bfs")
                AlgoritmosGrafo.bfs(grafo, v, "imagens_bfs", passo_unico=False, pausar=False)
                print("✔ BFS executada e imagens geradas.")
            else:
                print("X Vértice inválido.")


        elif opcao == "2":
            garantir_pasta("imagens_dfs")
            AlgoritmosGrafo.dfs(grafo, "imagens_dfs", passo_unico=False, pausar=False)
            print("✔ DFS executada e imagens geradas.")


        elif opcao == "3":
            comps = AlgoritmosGrafo.componentes_conexas_busca(grafo)
            print("\nComponentes encontradas:")
            for c in comps:
                print(" -", [v.id for v in c])


        elif opcao == "4":
            comps = AlgoritmosGrafo.componentes_conexas_unionfind(grafo)
            print("\nComponentes encontradas:")
            for c in comps:
                print(" -", [v.id for v in c])


        elif opcao == "5":
            print("✔ Conexo" if AlgoritmosGrafo.conexo(grafo) else "X Não conexo")


        elif opcao == "6":
            eh = AlgoritmosGrafo.euleriano(grafo)
            print("✔ É euleriano" if eh else "X Não é euleriano")
            if eh:
                ciclo = AlgoritmosGrafo.get_ciclo_euleriano(grafo)
                print("Ciclo:", " -> ".join([v.id for v in ciclo]))


        elif opcao == "7":
            dist, pred = AlgoritmosGrafo.floyd_warshall(grafo)
            print("\n=== Distâncias ===")
            for u in dist:
                print(u, dist[u])
            print("\n=== Predecessores ===")
            for u in pred:
                print(u, pred[u])


        elif opcao == "8":
            origem = input("Vértice origem: ").strip()
            if grafo.get_vertice(origem) is None:
                print("X Origem inválida.")
                continue
            dist, pred = AlgoritmosGrafo.dijkstra(grafo, origem)
            print("Distâncias:", dist)
            print("Predecessores:", pred)


        elif opcao == "9":
            for v in grafo.vertices():
                print(f"\nOrigem = {v.id}")
                dist, pred = AlgoritmosGrafo.dijkstra(grafo, v.id)
                print("Distâncias:", dist)
                print("Predecessores:", pred)


        elif opcao == "10":
            mst, custo = AlgoritmosGrafo.kruskal(grafo)
            print("\nArestas da AGM (Kruskal):")
            for u, v, p in mst:
                print(f"{u.id} - {v.id}: {p}")
            print("Custo total =", custo)


        elif opcao == "11":
            inicio = caso.get("vertice_inicial")
            if not inicio:
                inicio = input("Vértice inicial: ")
            v0 = grafo.get_vertice(inicio)
            if v0:
                mst, custo = AlgoritmosGrafo.prim(grafo, v0)
                print("\nArestas da AGM (Prim):")
                for u, v, p in mst:
                    print(f"{u.id} - {v.id}: {p}")
                print("Custo total =", custo)
            else:
                print("X Vértice inicial inválido.")

        elif opcao == "12":
            print("Verificando se é Hamiltoniano...")
            if AlgoritmosGrafo.eh_hamiltoniano(grafo):
                print("✔ O grafo é Hamiltoniano!")
            else:
                print("X O grafo NÃO é Hamiltoniano.")

        elif opcao == "13":
            print("Buscando ciclo Hamiltoniano...")
            existe, ciclo = AlgoritmosGrafo.ciclo_hamiltoniano(grafo)
            if existe:
                print("✔ Ciclo encontrado:")
                print(" → ".join(v.id for v in ciclo))
            else:
                print("X Nenhum ciclo Hamiltoniano encontrado.")

def main():
    casos = None

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Carregar arquivo de casos")
        print("2 - Selecionar caso e executar algoritmos")
        print("0 - Sair")
        opcao = input("Escolha: ")


        if opcao == "0":
            print("Encerrando...")
            return


        elif opcao == "1":
            caminho = input("Digite o caminho do arquivo de casos: ").strip()
            casos = carregar_casos(caminho)


        elif opcao == "2":
            if not casos:
                print("X Nenhum arquivo de casos carregado.")
                continue

            print("\nCasos disponíveis:")
            for i, c in enumerate(casos):
                print(f"{i} - {c['nome']}")

            idx = int(input("Escolha o caso: "))
            if idx < 0 or idx >= len(casos):
                print("X Caso inválido.")
                continue

            caso = casos[idx]
            grafo = construir_grafo(caso)

            print(f"\n=== Executando: {caso['nome']} ===")
            menu_algoritmos(grafo, caso)


if __name__ == "__main__":
    main()
