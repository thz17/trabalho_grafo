def carregar_grafo(caminho):
 # Dicionário principal que vai guardar o mapa: { "ORIGEM": [("DESTINO", PESO), ...] }
    grafo = {}
    with open(caminho, "r", encoding="utf-8") as arq:
        for linha in arq:
            # Ignora linhas em branco para não dar erro de split
            if not linha.strip():
                continue
                # Pega os valores da linha: origem (a), destino (b) e o peso (distância em metros)
            a, b, peso = linha.split()
            peso = int(peso)
            # Como o corredor é de mão dupla, adiciona a rota nos dois sentidos
            grafo.setdefault(a, []).append((b, peso))
            grafo.setdefault(b, []).append((a, peso))
    return grafo

if __name__ == "__main__":
    # Teste rápido direto no terminal para ver se o grafo carregou direito
    grafo = carregar_grafo("arestas.txt")
    print(f"Total de portas: {len(grafo)}")
    print(f"Portas carregadas: {list(grafo.keys())}")
    
    # Teste rápido da BFS a partir do LABTEC
    visitados = set()
    fila = ["LABTEC"]
    visitados.add("LABTEC")
    while fila:
        atual = fila.pop(0)
        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
    print(f"Portas alcançadas pelo LABTEC: {len(visitados)} de {len(grafo)}")
