def floyd_warshall(graph):
    n = len(graph)
    # Crear una copia de la matriz de distancias
    dist = [row[:] for row in graph]
    # Matriz para guardar los caminos
    next = [[j if graph[i][j] != float('inf') else -1 
             for j in range(n)] for i in range(n)]
    
    # Algoritmo principal
    for k in range(n):
        print(f"\n--- Usando nodo {k + 1} como intermedio ---")
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next[i][j] = next[i][k]
                        print(f"Nuevo camino: {i+1} → {k+1} → {j+1} = {dist[i][j]}")
    
    return dist, next

def get_path(next, start, end):
    if next[start][end] == -1:
        return []
    path = [start + 1]
    while start != end:
        start = next[start][end]
        path.append(start + 1)
    return path

def crear_matriz(n, conexiones):
    matriz = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        matriz[i][i] = 0
    for origen, destino, peso in conexiones:
        matriz[origen][destino] = peso
    return matriz

def print_matrix(matriz):
    n = len(matriz)
    print("\nMatriz de distancias:")
    print("    ", end="")
    for i in range(n):
        print(f"{i+1:4}", end="")
    print()
    print("   +" + "----" * n)
    
    for i in range(n):
        print(f"{i+1:2} |", end="")
        for j in range(n):
            if matriz[i][j] == float('inf'):
                print(" INF", end="")
            else:
                print(f"{matriz[i][j]:4}", end="")
        print()

if __name__ == "__main__":
    while True:
        try:
            print("\nAlgoritmo de Floyd-Warshall")
            n = int(input("Número de nodos: "))
            if n < 2:
                print("Error: Se necesitan al menos 2 nodos")
                continue
            
            print("\nIngrese las conexiones como: origen destino distancia [d]")
            print("Ejemplo: 1 2 5    (conexión de dos vías)")
            print("         1 2 5 d  (conexión de una vía)")
            print("Para terminar ingrese: -1")
            
            conexiones = []
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
                
                conexiones.append((origen, destino, peso))
                if not es_direccional:
                    conexiones.append((destino, origen, peso))
            
            if not conexiones:
                print("Error: No se ingresaron conexiones")
                continue
            
            grafo = crear_matriz(n, conexiones)
            print("\nMatriz original:")
            print_matrix(grafo)
            
            distancias, siguiente = floyd_warshall(grafo)
            
            print("\nMatriz de distancias mínimas:")
            print_matrix(distancias)
            
            print("\nCaminos más cortos:")
            for i in range(n):
                for j in range(n):
                    if i != j and distancias[i][j] != float('inf'):
                        camino = get_path(siguiente, i, j)
                        print(f"De {i+1} a {j+1}: {' → '.join(map(str, camino))} = {distancias[i][j]}")
            
            if input("\n¿Otro cálculo? (s/n): ").lower() != 's':
                break
            
        except ValueError:
            print("Error: Ingrese números válidos")
        except Exception as e:
            print(f"Error: {str(e)}")
