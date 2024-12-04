def floyd_warshall(graph):                                                                           
    n = len(graph)                                                                              #2                                                           
    dist = [row[:] for row in graph]                                                            #n^2
    
    for k in range(n):                                                                           #n    
        print(f"\n------------------------------------ PASO {k + 1} ------------------")        
        print(f"\nPaso {k + 1} (Usando vértice {k + 1} como intermedio):")
        for i in range(n):                                                                      #n^2  
            for j in range(n):                                                                  #n^3  
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):                   #10n^3
                    nuevo_valor = dist[i][k] + dist[k][j]                                       #6n^3       
                    if nuevo_valor < dist[i][j]:                                                #4n^3   
                        print(f"{dist[i][k]} + {dist[k][j]} = {nuevo_valor} < {dist[i][j] \
                             if dist[i][j] != float('inf') else 'inf'}")                       
                        print(f"Actualizando distancia de {i+1} a {j+1} a {nuevo_valor}")
                        dist[i][j] = nuevo_valor                                                #3n^3
        print("\nMatriz actual:")
        print_solution(dist)                                                                    #1
    return dist                                                                                 #1 

def print_solution(dist):
    n = len(dist)
    print("    ", end="")
    for i in range(n):
        print(f"{i+1:4}", end="")
    print()
    print("   +" + "----" * n)
    
    for i in range(n):
        print(f"{i+1:2} |", end="")
        for j in range(n):
            if dist[i][j] == float('inf'):
                print(" INF", end="")
            else:
                print(f"{dist[i][j]:4}", end="")
        print()

def crear_matriz(n, conexiones):
    matriz = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        matriz[i][i] = 0
    for origen, destino, peso in conexiones:
        matriz[origen][destino] = peso
    return matriz

if __name__ == "__main__":
    while True:
        try:
            print("\nAlgoritmo de Floyd-Warshall")
            n = int(input("Número de nodos: "))
            if n < 2:
                print("Error: Se necesitan al menos 2 nodos")
                continue
                
            print("\nIngrese las conexiones como: origen destino distancia [d]")
            print("Ejemplo: 1 2 5    (conexión de dos vías entre nodos 1 y 2)")
            print("         1 2 5 d  (conexión de una vía del nodo 1 al 2)")
            print("Para terminar ingrese: -1")
            
            conexiones = []
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
                    
                    if origen < 0 or origen >= n or destino < 0 or destino >= n:
                        print(f"Error: Los nodos deben estar entre 1 y {n}")
                        continue
                    if peso < 0:
                        print("Error: La distancia no puede ser negativa")
                        continue
                        
                    conexiones.append((origen, destino, peso))
                    if not es_direccional:
                        conexiones.append((destino, origen, peso))
                except ValueError:
                    print("Error: Los valores deben ser números")
            
            if not conexiones:
                print("No se ingresaron conexiones")
                continue
                
            grafo = crear_matriz(n, conexiones)
            resultado = floyd_warshall(grafo)
            
            print("\n------------------------------------RESULTADOS------------------------------------")
            print("\nDistancias originales:")
            print_solution(grafo)
            print("\nDistancias más cortas:")
            print_solution(resultado)
            
            if input("\n¿Otro cálculo? (s/n): ").lower() != 's':
                break
                
        except Exception as e:
            print(f"Error: {str(e)}")
            if input("¿Continuar? (s/n): ").lower() != 's':
                break
