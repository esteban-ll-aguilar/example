def dijkstra(graph, start, end):
    n = len(graph)
    # Inicializar distancias y visitados
    dist = [float('inf')] * n
    dist[start] = 0
    prev = [-1] * n
    visited = [False] * n
    
    print(f"\nBuscando camino de {start + 1} a {end + 1}")
    
    # Algoritmo principal
    for _ in range(n):
        # Encontrar el nodo no visitado con menor distancia
        min_dist = float('inf')
        u = -1
        for v in range(n):
            if not visited[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v
        
        if u == -1 or u == end:
            break
        
        visited[u] = True
        print(f"\nVisitando nodo {u + 1}")
        
        # Actualizar distancias de vecinos
        for v in range(n):
            if (not visited[v] and graph[u][v] > 0 and 
                dist[u] + graph[u][v] < dist[v]):
                dist[v] = dist[u] + graph[u][v]
                prev[v] = u
                print(f"Distancia a nodo {v + 1}: {dist[v]}")
    
    # Reconstruir el camino
    if dist[end] == float('inf'):
        return None, None
    
    path = []
    current = end
    while current != -1:
        path.append(current + 1)
        current = prev[current]
    path.reverse()
    
    return dist[end], path

def crear_matriz(n):
    return [[0 if i == j else 0 for j in range(n)] for i in range(n)]

def print_matrix(matriz):
    n = len(matriz)
    print("\nMatriz de adyacencia:")
    print("    ", end="")
    for i in range(n):
        print(f"{i+1:4}", end="")
    print()
    print("   +" + "----" * n)
    
    for i in range(n):
        print(f"{i+1:2} |", end="")
        for j in range(n):
            print(f"{matriz[i][j]:4}", end="")
        print()

if __name__ == "__main__":
    while True:
        try:
            print("\nAlgoritmo de Dijkstra")
            n = int(input("\nNúmero de nodos: "))
            if n <= 0:
                print("Error: El número debe ser positivo")
                continue
            
            grafo = crear_matriz(n)
            
            print("\nIngrese las conexiones como: origen destino distancia [d]")
            print("Ejemplo: 1 2 5    (conexión de dos vías)")
            print("         1 2 5 d  (conexión de una vía)")
            print("Para terminar ingrese: -1")
            
            while True:
                entrada = input("\nConexión: ")
                if entrada == "-1":
                    break
                
                partes = entrada.split()
                if len(partes) < 3:
                    print("Error: Ingrese origen destino y distancia")
                    continue
                
                origen = int(partes[0]) - 1
                destino = int(partes[1]) - 1
                peso = int(partes[2])
                es_direccional = len(partes) > 3 and partes[3].lower() == 'd'
                
                if origen < 0 or origen >= n or destino < 0 or destino >= n:
                    print(f"Error: Los nodos deben estar entre 1 y {n}")
                    continue
                if peso < 0:
                    print("Error: La distancia no puede ser negativa")
                    continue
                
                grafo[origen][destino] = peso
                if not es_direccional:
                    grafo[destino][origen] = peso
            
            print_matrix(grafo)
            
            while True:
                try:
                    origen = int(input("\nNodo de origen (1 a " + str(n) + "): ")) - 1
                    destino = int(input("Nodo de destino (1 a " + str(n) + "): ")) - 1
                    
                    if origen < 0 or origen >= n or destino < 0 or destino >= n:
                        print(f"Error: Los nodos deben estar entre 1 y {n}")
                        continue
                    
                    if origen == destino:
                        print("El origen y destino son iguales. Distancia = 0")
                        continue
                    
                    break
                except ValueError:
                    print("Error: Ingrese números válidos")
            
            distancia, camino = dijkstra(grafo, origen, destino)
            
            print("\nResultado:")
            if distancia is None:
                print(f"No existe camino entre {origen + 1} y {destino + 1}")
            else:
                print(f"Distancia mínima: {distancia}")
                print(f"Camino: {' → '.join(map(str, camino))}")
            
            if input("\n¿Otro cálculo? (s/n): ").lower() != 's':
                break
            
        except ValueError:
            print("Error: Ingrese números válidos")
        except Exception as e:
            print(f"Error: {str(e)}")
