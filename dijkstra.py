def dijkstra(graph, src, dest):
    V = len(graph)
    dist = [float('inf')] * V
    dist[src] = 0
    parent = [-1] * V
    visited = [False] * V

    print(f"\n----------------------- PROCESO DE DIJKSTRA -----------------------")
    print(f"Buscando camino más corto del nodo {src + 1} al nodo {dest + 1}")
    
    for _ in range(V):
        # Encontrar el vértice no visitado con la distancia mínima
        min_dist = float('inf')
        u = -1
        for v in range(V):
            if not visited[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v
        
        if u == -1 or u == dest:  # Si llegamos al destino, podemos terminar
            break
            
        visited[u] = True
        print(f"\nPaso {_ + 1}: Visitando nodo {u + 1}")
        
        # Actualizar las distancias de los vértices adyacentes
        for v in range(V):
            if (not visited[v] and 
                graph[u][v] > 0 and 
                dist[u] + graph[u][v] < dist[v]):
                
                old_dist = dist[v] if dist[v] != float('inf') else "∞"
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u
                print(f"  Actualizando distancia a nodo {v + 1}: {old_dist} → {dist[v]}")
                if v == dest:
                    print(f"  Nuevo camino encontrado al destino: {get_path(parent, v)}")
    
    return dist[dest], parent

def get_path(parent, vertex):
    path = []
    while vertex != -1:
        path.append(vertex + 1)
        vertex = parent[vertex]
    return ' → '.join(map(str, path[::-1]))

def crear_matriz_adyacencia(V):
    return [[0 if i == j else float('inf') for j in range(V)] for i in range(V)]

def print_specific_path(dist, parent, src, dest):
    print("\n------------------- RESULTADO -------------------")
    if dist == float('inf'):
        print(f"\nNo existe un camino entre el nodo {src + 1} y el nodo {dest + 1}")
    else:
        path = get_path(parent, dest)
        print(f"\nCamino más corto del nodo {src + 1} al nodo {dest + 1}:")
        print(f"Distancia: {dist}")
        print(f"Recorrido: {path}")

def print_matrix(matrix):
    n = len(matrix)
    print("    ", end="")
    for i in range(n):
        print(f"{i+1:4}", end="")
    print()
    print("   +" + "----" * n)
    
    for i in range(n):
        print(f"{i+1:2} |", end="")
        for j in range(n):
            if matrix[i][j] == float('inf'):
                print(" INF", end="")
            else:
                print(f"{matrix[i][j]:4}", end="")
        print()

if __name__ == "__main__":
    while True:
        try:
            print("\nAlgoritmo de Dijkstra - Camino más corto entre dos nodos")
            V = int(input("\nIngrese el número de vértices: "))
            if V <= 0:
                print("El número de vértices debe ser positivo")
                continue
                
            grafo = crear_matriz_adyacencia(V)
            
            print("\nIngrese las conexiones como: origen destino distancia [d]")
            print("Ejemplo: 1 2 5    (conexión de dos vías entre nodos 1 y 2)")
            print("         1 2 5 d  (conexión de una vía del nodo 1 al 2)")
            print("Para terminar ingrese: -1")
            
            while True:
                entrada = input("\nConexión: ")
                if entrada == "-1":
                    break
                    
                try:
                    partes = entrada.split()
                    if len(partes) < 3:
                        print("Error: Ingrese origen destino y distancia")
                        continue
                        
                    origen = int(partes[0]) - 1
                    destino = int(partes[1]) - 1
                    peso = int(partes[2])
                    es_direccional = len(partes) > 3 and partes[3].lower() == 'd'
                    
                    if origen < 0 or origen >= V or destino < 0 or destino >= V:
                        print(f"Error: Los nodos deben estar entre 1 y {V}")
                        continue
                    if peso < 0:
                        print("Error: La distancia no puede ser negativa")
                        continue
                        
                    grafo[origen][destino] = peso
                    if not es_direccional:
                        grafo[destino][origen] = peso
                except ValueError:
                    print("Error: Los valores deben ser números")
            
            print("\nMatriz de adyacencia:")
            print_matrix(grafo)
            
            while True:
                try:
                    origen = int(input("\nIngrese el nodo de origen (1 a " + str(V) + "): ")) - 1
                    destino = int(input("Ingrese el nodo de destino (1 a " + str(V) + "): ")) - 1
                    
                    if origen < 0 or origen >= V or destino < 0 or destino >= V:
                        print(f"Error: Los nodos deben estar entre 1 y {V}")
                        continue
                        
                    if origen == destino:
                        print("El origen y destino son el mismo nodo. La distancia es 0.")
                        continue
                        
                    break
                except ValueError:
                    print("Por favor ingrese números válidos")
            
            distancia, padres = dijkstra(grafo, origen, destino)
            print_specific_path(distancia, padres, origen, destino)
            
            if input("\n¿Otro cálculo? (s/n): ").lower() != 's':
                break
                
        except ValueError:
            print("Por favor ingrese valores numéricos válidos")
        except Exception as e:
            print("Error:", str(e))
