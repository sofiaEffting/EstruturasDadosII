# 🧠 Trabalho de Estruturas II — Grafos

Implementação completa de grafos e algoritmos clássicos em Python

Este projeto implementa **um framework completo de grafos em Python**, incluindo:

* Estruturas básicas de **grafos dirigidos e não-dirigidos**
* Representação por lista de adjacência
* Classe `Vertice` com atributos auxiliares de busca
* Desenho do grafo e geração de imagens passo a passo
* **Todos os principais algoritmos de grafos**, incluindo:

  * BFS
  * DFS
  * Componentes conexas (DFS e Union-Find)
  * Verificação de conectividade
  * Detecção de ciclo **Euleriano** + algoritmo de **Hierholzer**
  * Detecção de ciclo **Hamiltoniano** (backtracking)
  * Dijkstra
  * Floyd-Warshall
  * Kruskal
  * Prim
  * Funções auxiliares para grau, adjacências, remoção, etc.

---

## 📂 Estrutura do Projeto

```
trabalho_grafos/
│
├── src/
│   ├── grafo.py             # Implementação das classes Grafo e Vertice
│   ├── algoritmos.py        # Todos os algoritmos de grafos (BFS, DFS, AGM, etc.)
│   ├── casos_teste.py       # Arquivo com diversos grafos de exemplo
│   └── main.py              # Execução principal, menu e geração de imagens
│
├── imagens_bfs/          # (gerada automaticamente) imagens dos passos
├── imagens_dfs/          # (gerada automaticamente) imagens dos passos
├── requirements.txt         # Dependências do projeto
└── README.md
```

---

## ⚙️ Como executar

### 1. Criar ambiente virtual (opcional, mas recomendado)

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o programa principal

```bash
python src/main.py
```

---

## 📘 Funcionalidades implementadas (completo)

### ✔ Estruturas de Grafo

* Representação por lista de adjacência
* Grafos dirigidos e não dirigidos
* Classe Vertice com:

  * cor (BRANCO/LARANJA/VERDE)
  * predecessor
  * distância
  * tempos de descoberta e finalização
* Operações básicas:

  * inserir/remover vértice
  * inserir/remover aresta
  * grau, adjacências, oposto, arestas de entrada/saída

---

## 🔍 Algoritmos implementados

### 🔵 **BFS — Busca em Largura**

* Calcula distância mínima
* Predecessores
* Marca descoberta e finalização
* Desenho passo a passo opcional

### 🔵 **DFS — Busca em Profundidade**

* Registra tempo de descoberta e finalização
* Exploração recursiva
* Utilizado por vários outros algoritmos

### 🔵 **Componentes Conexas**

* Implementação com DFS
* Implementação com **Union-Find** (Disjoint Set)

### 🔵 **Verificação de Conectividade**

* Checa se o grafo é totalmente conectado

---

## 🟣 Ciclos

### 🟠 **Euleriano**

* Verifica se:

  * o grafo é conexo
  * todos os vértices têm grau par
* Geração do ciclo usando o **Algoritmo de Hierholzer**

### 🟢 **Hamiltoniano**

* Backtracking exato O(n!)
* Determina se há ciclo Hamiltoniano
* Retorna o ciclo completo se existir

---

## 🟡 Caminhos mínimos

### 🟣 **Dijkstra**

* Caminho mínimo a partir de uma única origem
* Sem pesos negativos
* Retorna matriz de distâncias e predecessores

### 🟣 **Floyd-Warshall**

* Todos os caminhos mínimos entre todos os pares
* Permite reconstruir caminhos

---

## 🌳 Árvores Geradoras Mínimas

### 🟤 **Kruskal**

* Ordena todas as arestas
* Usa Union-Find para evitar ciclos
* Retorna a AGM e seu custo

### 🟤 **Prim**

* Expande sempre a menor aresta conectada ao conjunto árvore
* Retorna a AGM e seu custo

---

## 🧪 Casos de Teste

O arquivo `casos_teste.py` contém:

* grafos completos
* grafos desconexos
* grafos aleatórios
* grafos eulerianos
* grafos hamiltonianos
* grafos ponderados
* grafos com ciclos complexos
* florestas
* grafos grandes e pequenos

---

## 👩‍💻 Autora

**Sofia Effting**
Ciência da Computação — Instituto Federal Catarinense (IFC) – Campus Blumenau
