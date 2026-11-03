import heapq

def bfs(grafo, origem, destino):
    visitados = []
    fila = [[origem]]
    visitados_set = {origem}
    
    while fila:
        caminho = fila.pop(0)
        atual = caminho[-1]
        visitados.append(atual)
        
        if atual == destino:
            custo = 0
            for i in range(len(caminho) - 1):
                for v, p in grafo[caminho[i]]:
                    if v == caminho[i+1]:
                        custo += p
                        break
            return caminho, custo, visitados
            
        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados_set:
                visitados_set.add(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
    return [], 0, visitados

def dfs(grafo, origem, destino):
    visitados = []
    pilha = [[origem]]
    visitados_set = set()
    
    while pilha:
        caminho = pilha.pop()
        atual = caminho[-1]
        
        if atual not in visitados_set:
            visitados_set.add(atual)
            visitados.append(atual)
            
            if atual == destino:
                custo = 0
                for i in range(len(caminho) - 1):
                    for v, p in grafo[caminho[i]]:
                        if v == caminho[i+1]:
                            custo += p
                            break
                return caminho, custo, visitados
                
            for vizinho, _ in reversed(grafo.get(atual, [])):
                if vizinho not in visitados_set:
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    pilha.append(novo_caminho)
    return [], 0, visitados

def gulosa(grafo, origem, destino):
    visitados = []
    fila = [(0, [origem])]
    visitados_set = set()
    
    while fila:
        _, caminho = heapq.heappop(fila)
        atual = caminho[-1]
        
        if atual in visitados_set:
            continue
        visitados_set.add(atual)
        visitados.append(atual)
        
        if atual == destino:
            custo = 0
            for i in range(len(caminho) - 1):
                for v, p in grafo[caminho[i]]:
                    if v == caminho[i+1]:
                        custo += p
                        break
            return caminho, custo, visitados
            
        vizinhos_ordenados = sorted(grafo.get(atual, []), key=lambda x: x[1])
        for vizinho, peso in vizinhos_ordenados:
            if vizinho not in visitados_set:
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                heapq.heappush(fila, (peso, novo_caminho))
                
    return [], 0, visitados

def dijkstra(grafo, origem, destino):
    distancia = {p: float("inf") for p in grafo}
    anterior = {}
    distancia[origem] = 0
    fila = [(0, origem)]
    finalizadas = set()
    
    while fila:
        d, atual = heapq.heappop(fila)
        
        if atual in finalizadas:
            continue
        finalizadas.add(atual)
        
        if atual == destino:
            break
            
        for vizinho, peso in grafo.get(atual, []):
            nova_dist = d + peso
            if nova_dist < distancia[vizinho]:
                distancia[vizinho] = nova_dist
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))
                
    caminho = []
    atual = destino
    while atual in anterior:
        caminho.insert(0, atual)
        atual = anterior[atual]
    if caminho or origem == destino:
        caminho.insert(0, origem)
        
    visitados = list(finalizadas)
    return caminho, distancia[destino], visitados
