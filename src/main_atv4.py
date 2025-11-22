import os
import shutil
from grafo import Grafo
from algoritmos import AlgoritmosGrafo

def print_resultado_euleriano(eh_euleriano, ciclo, nome_caso):
    """Função auxiliar para exibir os resultados do teste de Eulerianidade."""
    
    print(f"\n--- Resultado: {nome_caso} ---")

    if eh_euleriano:
        print("• O grafo É EULERIANO.")
        print("• Ciclo Euleriano encontrado:")
        print("  ->", " -> ".join([v.id for v in ciclo]))
    else:
        print("• O grafo NÃO É EULERIANO.")
        
    print("-" * 30)


casos_eulerianos = [
    {
        "nome": "Caso 1 - Grafo Euleriano Simples",
        "dirigido": False,
        "arestas": [("A", "B"), ("B", "C"), ("C", "A")]
    },
    {
        "nome": "Caso 2 - Grafo Não Euleriano (Vértice com Grau Ímpar)",
        "dirigido": False,
        "arestas": [("1", "2"), ("2", "3"), ("3", "4")]
    },
    {
        "nome": "Caso 3 - Grafo Euleriano com Ciclo Maior",
        "dirigido": False,
        "arestas": [("X", "Y"), ("Y", "Z"), ("Z", "W"), ("W", "X"), ("X", "Z"), ("Y", "W")]
    }
]

pasta_principal = "imagens_grafos_eulerianos"
os.makedirs(pasta_principal, exist_ok=True)
contador = 0

for caso in casos_eulerianos:
    print(f"\nAnalisando: {caso['nome']}")

    grafo = Grafo(dirigido=caso.get("dirigido", False))

    for u, v in caso["arestas"]:
        grafo.insereV(u)
        grafo.insereV(v)
        grafo.insereA(u, v)

    contador += 1

    grafo.desenhar_passo(pasta_principal, contador, titulo="Grafo Inicial", passo_unico=False, prefixo="Grafo", pausar=False)

    eh_euleriano = AlgoritmosGrafo.euleriano(grafo)
    ciclo = AlgoritmosGrafo.get_ciclo_euleriano(grafo) if eh_euleriano else None

    print_resultado_euleriano(eh_euleriano, ciclo, caso["nome"])


print("\n" + "="*60)
manter = input(f"Deseja manter as imagens na pasta '{pasta_principal}'? (s/n): ").strip().lower()
if manter != 's':
    try:
        shutil.rmtree(pasta_principal)
        print("Todas as imagens foram deletadas.")
    except Exception as e:
        print(f"Erro ao deletar pasta: {e}")
else:
    print(f"Imagens mantidas em '{pasta_principal}'.")