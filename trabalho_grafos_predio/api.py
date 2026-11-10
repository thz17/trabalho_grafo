from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra

# Inicializa a aplicação FastAPI
app = FastAPI(title="Rotas do Prédio - Senac", version="1.0")

# Carrega o grafo globalmente a partir do arquivo de arestas ao subir o servidor
grafo = carregar_grafo("arestas.txt")

@app.get("/portas")
def get_portas():
    """Retorna a lista de todas as portas/vértices disponíveis no grafo do prédio."""
    return {"portas": list(grafo.keys())}

@app.get("/vizinhos/{porta}")
def get_vizinhos(porta: str):
    """Retorna os vizinhos diretos de uma porta específica e os pesos (distâncias em metros)."""
    porta = porta.upper()
    if porta not in grafo:
        raise HTTPException(status_code=404, detail="Porta não encontrada")
    return {
        "porta": porta,
        "vizinhos": [{"porta": v, "peso": p} for v, p in grafo[porta]]
    }

@app.get("/rota")
def get_rota(origem: str, destino: str, algoritmo: str):
    """Calcula a rota entre duas portas utilizando o algoritmo escolhido (bfs, dfs, gulosa ou dijkstra)."""
    origem = origem.upper()
    destino = destino.upper()
    algoritmo = algoritmo.lower()
    
    # Valida se os pontos existem no grafo carregado
    if origem not in grafo or destino not in grafo:
        raise HTTPException(status_code=404, detail="Origem ou destino não encontrados")
        
    # Direciona para a função do algoritmo correspondente
    if algoritmo == "bfs":
        caminho, custo, visitados = bfs(grafo, origem, destino)
    elif algoritmo == "dfs":
        caminho, custo, visitados = dfs(grafo, origem, destino)
    elif algoritmo == "gulosa":
        caminho, custo, visitados = gulosa(grafo, origem, destino)
    elif algoritmo == "dijkstra":
        caminho, custo, visitados = dijkstra(grafo, origem, destino)
    else:
        raise HTTPException(status_code=400, detail="Algoritmo inválido. Use bfs, dfs, gulosa ou dijkstra")
        
    return {
        "algoritmo": algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": "metros",
        "visitados": visitados
    }

@app.get("/comparar")
def get_comparar(origem: str, destino: str):
    """Compara o desempenho, caminho e custo de todos os quatro algoritmos lado a lado."""
    origem = origem.upper()
    destino = destino.upper()
    
    # Valida se os pontos existem
    if origem not in grafo or destino not in grafo:
        raise HTTPException(status_code=404, detail="Origem ou destino não encontrados")
        
    resultados = {}
    # Roda iterativamente todos os algoritmos para montar o comparativo
    for algo_nome, algo_func in [("bfs", bfs), ("dfs", dfs), ("gulosa", gulosa), ("dijkstra", dijkstra)]:
        caminho, custo, visitados = algo_func(grafo, origem, destino)
        resultados[algo_nome] = {
            "caminho": caminho,
            "custo": custo,
            "visitados_count": len(visitados)
        }
        
    return {
        "origem": origem,
        "destino": destino,
        "comparacao": resultados
    }
