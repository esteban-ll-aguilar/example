class FloydWarshall:
    def __init__(self, size):
        self.size = size
        self.dist = None
        self.next = None
        self.has_negative_cycle = False
        
    def initialize(self, graph):
        self.dist = [row[:] for row in graph]
        # Matriz para reconstrucción de caminos
        self.next = [[j if graph[i][j] != float('inf') else -1 
                     for j in range(self.size)] 
                     for i in range(self.size)]
        
    def detect_negative_cycles(self):
        for i in range(self.size):
            if self.dist[i][i] < 0:
                return True
        return False
        
    def get_path(self, start, end):
        if self.next[start][end] == -1:
            return []
            
        path = [start + 1]
        while start != end:
            start = self.next[start][end]
            path.append(start + 1)
        return path
        
    def solve(self, graph):
        self.initialize(graph)
        
        print("\n================ PROCESO DE FLOYD-WARSHALL ================")
        for k in range(self.size):
            print(f"\n⭐ Fase {k + 1}: Evaluando {k + 1} como nodo intermedio")
            changes_in_phase = False
            
            for i in range(self.size):
                for j in range(self.size):
                    if self.dist[i][k] != float('inf') and self.dist[k][j] != float('inf'):
                        new_dist = self.dist[i][k] + self.dist[k][j]
                        
                        if new_dist < self.dist[i][j]:
                            changes_in_phase = True
                            old_dist = "∞" if self.dist[i][j] == float('inf') else self.dist[i][j]
                            self.dist[i][j] = new_dist
                            self.next[i][j] = self.next[i][k]
                            
                            print(f"📌 Actualización: {i+1} → {j+1}")
                            print(f"   Ruta anterior: {old_dist}")
                            print(f"   Nueva ruta: {new_dist} (a través de {k+1})")
            
            if not changes_in_phase:
                print(f"ℹ️ No se encontraron mejoras en esta fase")
            
            if k == self.size - 1:
                self.has_negative_cycle = self.detect_negative_cycles()
                
        return self.dist
        
    def print_all_paths(self):
        print("\n================ TODOS LOS CAMINOS MÁS CORTOS ================")
        if self.has_negative_cycle:
            print("⚠️ ADVERTENCIA: Se detectaron ciclos negativos en el grafo.")
            print("   Los resultados podrían no ser confiables.")
            
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    path = self.get_path(i, j)
                    if path:
                        dist = self.dist[i][j]
                        path_str = " → ".join(map(str, path))
                        print(f"\n🔹 De {i+1} a {j+1}:")
                        print(f"   Distancia: {dist}")
                        print(f"   Camino: {path_str}")
                    else:
                        print(f"\n🔸 No hay camino de {i+1} a {j+1}")

def crear_matriz(n, conexiones):
    matriz = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        matriz[i][i] = 0
    for origen, destino, peso in conexiones:
        matriz[origen][destino] = peso
    return matriz

def print_matrix(matriz, titulo):
    n = len(matriz)
    print(f"\n{titulo}")
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
            print("\n🔄 Algoritmo de Floyd-Warshall")
            n = int(input("Número de nodos: "))
            if n < 2:
                print("❌ Error: Se necesitan al menos 2 nodos")
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
                        print("❌ Error: Ingrese origen destino y distancia")
                        continue
                        
                    origen = int(partes[0]) - 1
                    destino = int(partes[1]) - 1
                    peso = int(partes[2])
                    es_direccional = len(partes) > 3 and partes[3].lower() == 'd'
                    
                    if origen < 0 or origen >= n or destino < 0 or destino >= n:
                        print(f"❌ Error: Los nodos deben estar entre 1 y {n}")
                        continue
                    
                    conexiones.append((origen, destino, peso))
                    if not es_direccional:
                        conexiones.append((destino, origen, peso))
                except ValueError:
                    print("❌ Error: Los valores deben ser números")
            
            if not conexiones:
                print("❌ No se ingresaron conexiones")
                continue
                
            grafo = crear_matriz(n, conexiones)
            print_matrix(grafo, "📊 Matriz de Distancias Original")
            
            # Crear instancia y resolver
            floyd = FloydWarshall(n)
            resultado = floyd.solve(grafo)
            
            print_matrix(resultado, "\n📊 Matriz de Distancias Mínimas")
            floyd.print_all_paths()
            
            if input("\n¿Otro cálculo? (s/n): ").lower() != 's':
                break
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            if input("¿Continuar? (s/n): ").lower() != 's':
                break
