# Trabalho de Estruturas II - Grafos

Este projeto implementa **grafos em Python** com operações básicas, além de algoritmos de **Busca em Largura (BFS)** e **Busca em Profundidade (DFS)**.
O programa também gera imagens mostrando passo a passo a execução dos algoritmos.

---

## 📂 Estrutura do projeto

trabalho\_grafos/
│
├── src/
│   ├── grafo.py         # Classe Grafo e Vertice
│   ├── algoritmos.py    # Implementação de BFS e DFS
│   └── main.py          # Arquivo principal que executa os casos de teste
│
├── requirements.txt     # Lista de dependências
└── README.md            # Este arquivo

---

## ⚙️ Como executar

### 1. Criar ambiente virtual (recomendado)

No terminal, dentro da pasta do projeto:
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows (PowerShell)

### 2. Instalar dependências

pip install -r requirements.txt

### 3. Executar o programa

python src/main.py

---

## 🖼️ Geração de imagens

Durante a execução, o programa pergunta:

Deseja salvar cada passo como imagem separada? (s/n):

* Se você responder **s**, cada passo dos algoritmos será salvo como uma imagem diferente dentro de subpastas em `imagens_grafos/`.
* Se responder **n**, os arquivos de imagem serão sobrescritos a cada passo. Assim, ao abrir uma única imagem, basta ir pressionando **Enter** no terminal para visualizar a evolução do grafo.

No final, o programa também pergunta:

Deseja manter as imagens na pasta 'imagens\_grafos'? (s/n):

Se responder **n**, todas as imagens geradas serão apagadas automaticamente.

---

## 📊 Funcionalidades implementadas

* Estrutura de **grafo dirigido e não-dirigido**
* Operações com vértices e arestas
* Algoritmo de **Busca em Largura (BFS)**
* Algoritmo de **Busca em Profundidade (DFS)**
* Impressão de tabela com:
  * Cor do vértice
  * Distância
  * Predecessor
  * Tempo de descoberta e finalização
* Geração de imagens em cada passo dos algoritmos

---

## 👩‍💻 Autor

Sofia Effting – Ciência da Computação, IFC - Blumenau

---
