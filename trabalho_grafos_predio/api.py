from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra

app = FastAPI()
grafo = carregar_grafo("arestas.txt")

@app.get("/portas")
def get_portas():
    return {"portas": list(grafo.keys())}

@app.get("/vizinhos/{porta}")
def get_vizinhos(porta: str):
    porta = porta.upper()
    if porta not in grafo:
        raise HTTPException(status_code=404, detail="Porta não encontrada")
    return {
        "porta": porta,
        "vizinhos": [{"porta": v, "peso": p} for v, p in grafo[porta]]
    }

@app.get("/rota")
def get_rota(origem: str, destino: str, algoritmo: str):
    origem = origem.upper()
    destino = destino.upper()
    algoritmo = algoritmo.lower()
    
    if origem not in grafo or destino not in grafo:
        raise HTTPException(status_code=404, detail="Origem ou destinopip install fastapi uvicorn não encontrados")
        
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
    origem = origem.upper()
    destino = destino.upper()
    
    if origem not in grafo or destino not in grafo:
        raise HTTPException(status_code=404, detail="Origem ou destino não encontrados")
        
    resultados = {}
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
