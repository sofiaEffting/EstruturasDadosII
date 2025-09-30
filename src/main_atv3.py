import os
import shutil
from grafo import Grafo
from algoritmos import AlgoritmosGrafo

resposta_salvar_passos = input("Deseja salvar a imagem do grafo inicial para cada caso? (s/n): ").strip().lower()
salvar_passos = resposta_salvar_passos == 's'

resposta_pausar = input("Deseja pausar após a análise de cada caso de teste? (s/n): ").strip().lower()
pausar_passos = resposta_pausar == 's'


def print_componentes(componentes, nome_algoritmo):
    """Função auxiliar para exibir as componentes conexas."""
    
    componentes_ids = [[v.id for v in comp] for comp in componentes]
    num_componentes = len(componentes)
    e_conexao = num_componentes == 1

    print(f"\n--- Resultado: {nome_algoritmo} ---")

    if e_conexao:
        print("• O grafo É CONEXO (1 componente).")
    else:
        print("• O grafo NÃO É CONEXO.")

    print(f"• Número de Componentes Conexas: {num_componentes}")

    print("• Vértices em cada Componente:")
    for i, comp in enumerate(componentes_ids):
        print(f"  Componente {i+1} (Tamanho {len(comp)}): {sorted(comp)}")
        
    print("-" * 30)
    return e_conexao

casos_conexidade = [
    {
        "nome": "Caso 1 - Grafo Conexo Simples",
        "dirigido": False,
        "arestas": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
    },
    {
        "nome": "Caso 2 - Grafo Desconexo (2 Componentes + Vértice Solto)",
        "dirigido": False,
        "arestas": [("1", "2"), ("2", "3"), ("4", "5")],
        "vertices_soltos": ["6"] 
    },
    {
        "nome": "Caso 3 - Grafo Desconexo (3 Componentes Disjuntas)",
        "dirigido": False,
        "arestas": [("X", "Y"), ("Y", "Z"), ("Z", "X"), ("A", "B"), ("P", "Q")]
    },
    {
        "nome": "Caso 4 - Grafo Composto (Muitos Vértices Conexos)",
        "dirigido": False,
        "arestas": [("S", "T"), ("T", "U"), ("U", "V"), ("W", "X"), ("Y", "Z")],
        "vertices_soltos": ["K"]
    }
]

pasta_principal = "imagens_grafos_conexidade"
if salvar_passos:
    os.makedirs(pasta_principal, exist_ok=True)


for i, caso in enumerate(casos_conexidade, start=1):
    print("\n" + "="*60)
    print(f"TESTE {i}: {caso['nome']}")
    print("="*60)

    g = Grafo(dirigido=caso["dirigido"])
    for u, v in caso["arestas"]:
        g.insereA(u, v)
        
    if "vertices_soltos" in caso:
        for v_id in caso["vertices_soltos"]:
             g.insereV(v_id)

    print(f"\nTotal de Vértices: {g.getOrdem()}, Total de Arestas: {g.getTamanho()}")
    print("Vértices no Grafo: ", sorted([v.id for v in g.vertices()]))
    
    if salvar_passos:
        pasta_caso = os.path.join(pasta_principal, f"caso_conexidade_{i}")
        os.makedirs(pasta_caso, exist_ok=True)
        g.desenhar_passo(pasta_caso, 1, "Grafo Inicial para Conexidade", passo_unico=True, prefixo="Grafo", pausar=False)

    print("\n>>> MÓDULO 1: Algoritmo de Busca (DFS) <<<")
    componentes_dfs = AlgoritmosGrafo.componentes_conexas_busca(g)
    print_componentes(componentes_dfs, "Busca em Profundidade (DFS)")
    
    print("\n>>> MÓDULO 2: Algoritmo Alternativo (Union-Find) <<<")
    componentes_uf = AlgoritmosGrafo.componentes_conexas_unionfind(g)
    print_componentes(componentes_uf, "Union-Find")

    if len(componentes_dfs) != len(componentes_uf):
        print("!! ERRO DE CONSISTÊNCIA: Número de componentes diferente entre os algoritmos!")

    if pausar_passos:
        input("Pressione Enter para continuar para o próximo caso de teste...")

print("\n" + "="*60)
if salvar_passos:
    manter = input(f"Deseja manter as imagens na pasta '{pasta_principal}'? (s/n): ").strip().lower()
    if manter != 's':
        try:
            shutil.rmtree(pasta_principal)
            print("Todas as imagens foram deletadas.")
        except Exception as e:
            print(f"Erro ao deletar pasta: {e}")
    else:
        print(f"Imagens mantidas em '{pasta_principal}'.")