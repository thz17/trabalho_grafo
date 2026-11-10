import heapq

def bfs(grafo, origem, destino):
    """Busca em Largura (BFS): Explora por camadas, priorizando o menor número de portas (saltos)."""
    origem, destino = origem.upper(), destino.upper()
    visitados = []
    fila = [[origem]]  # Fila que guarda os caminhos completos sendo testados (FIFO)
    visitados_set = {origem}
    
    while fila:
        caminho = fila.pop(0)  # Pira o primeiro caminho da fila
        atual = caminho[-1]
        visitados.append(atual)
        
        # Se chegou ao destino, calcula o custo total em metros somando as arestas do caminho
        if atual == destino:
            custo = 0
            for i in range(len(caminho) - 1):
                for v, p in grafo.get(caminho[i], []):
                    if v == caminho[i+1]:
                        custo += p
                        break
            return {"caminho": caminho, "custo": custo, "visitados": visitados}
            
        # Pega os vizinhos e joga novos caminhos na fila para explorar a próxima camada
        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados_set:
                visitados_set.add(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
    return {"caminho": [], "custo": 0, "visitados": visitados}

def dfs(grafo, origem, destino):
    """Busca em Profundidade (DFS): Vai fundo no corredor até bater numa parede sem saída."""
    origem, destino = origem.upper(), destino.upper()
    visitados = []
    pilha = [[origem]]  # Pilha LIFO para explorar a fundo o primeiro ramo que aparecer
    visitados_set = set()
    
    while pilha:
        caminho = pilha.pop()  # Pega o último caminho adicionado
        atual = caminho[-1]
        
        if atual not in visitados_set:
            visitados_set.add(atual)
            visitados.append(atual)
            
            # Se achou o destino, calcula o custo acumulado da rota
            if atual == destino:
                custo = 0
                for i in range(len(caminho) - 1):
                    for v, p in grafo.get(caminho[i], []):
                        if v == caminho[i+1]:
                            custo += p
                            break
                return {"caminho": caminho, "custo": custo, "visitados": visitados}
                
            # Empilha os vizinhos invertidos para manter a ordem correta na pilha
            for vizinho, _ in reversed(grafo.get(atual, [])):
                if vizinho not in visitados_set:
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    pilha.append(novo_caminho)
    return {"caminho": [], "custo": 0, "visitados": visitados}

def gulosa(grafo, origem, destino):
    """Busca Gulosa: Escolhe sempre o vizinho com o menor peso imediato (heurística local)."""
    origem, destino = origem.upper(), destino.upper()
    visitados = []
    fila = [(0, [origem])]  # Fila de prioridade baseada no peso local da aresta
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
                for v, p in grafo.get(caminho[i], []):
                    if v == caminho[i+1]:
                        custo += p
                        break
            return {"caminho": caminho, "custo": custo, "visitados": visitados}
            
        # Ordena os vizinhos pelo menor peso imediato e empilha
        vizinhos_ordenados = sorted(grafo.get(atual, []), key=lambda x: x[1])
        for vizinho, peso in vizinhos_ordenados:
            if vizinho not in visitados_set:
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                heapq.heappush(fila, (peso, novo_caminho))
                
    return {"caminho": [], "custo": 0, "visitados": visitados}

def dijkstra(grafo, origem, destino):
    """Dijkstra: O brabo da precisão. Calcula matematicamente o menor custo acumulado em metros."""
    origem, destino = origem.upper(), destino.upper()
    distancia = {p: float("inf") for p in grafo}  # Inicializa todas as distâncias como infinito
    anterior = {}  # Dicionário para rastrear o caminho de volta (quem levou a quem)
    distancia[origem] = 0
    fila = [(0, origem)]  # Fila de prioridade com os custos acumulados
    finalizadas = set()
    
    while fila:
        d, atual = heapq.heappop(fila)
        
        if atual in finalizadas:
            continue
        finalizadas.add(atual)
        
        if atual == destino:
            break
            
        # Relaxamento das arestas: atualiza se achar um caminho mais curto em metros
        for vizinho, peso in grafo.get(atual, []):
            nova_dist = d + peso
            if nova_dist < distancia.get(vizinho, float("inf")):
                distancia[vizinho] = nova_dist
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))
                
    # Reconstrói o caminho final de trás para frente usando o dicionário 'anterior'
    caminho = []
    atual = destino
    while atual in anterior:
        caminho.insert(0, atual)
        atual = anterior[atual]
    if caminho or origem == destino:
        caminho.insert(0, origem)
        
    visitados = list(finalizadas)
    custo_total = distancia.get(destino, 0) if caminho else 0
    return {"caminho": caminho, "custo": custo_total, "visitados": visitados}
