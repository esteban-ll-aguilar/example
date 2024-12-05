from queue import PriorityQueue
from typing import List, Tuple, Optional, Dict, Set

class Path:
    def __init__(self, nodes: List[int], distance: float):
        self.nodes = nodes
        self.distance = distance
        
    def __str__(self) -> str:
        return f"{'→'.join(map(str, [n+1 for n in self.nodes]))} (dist: {self.distance})"

class DijkstraAlgorithm:
    def __init__(self, size: int):
        self.size = size
        self.graph = None
        self.alternative_paths: Dict[Tuple[int, int], List[Path]] = {}
        
    def initialize(self, graph: List[List[float]]):
        self.graph = graph
        self.alternative_paths.clear()
        
    def find_paths(self, start: int, end: int, max_alternatives: int = 3) -> List[Path]:
        """Encuentra múltiples caminos entre dos nodos usando una variante de Dijkstra."""
        paths: List[Path] = []
        visited_sets: List[Set[int]] = []
        
        # Encontrar el primer camino
        first_path = self._dijkstra_single_path(start, end)
        if first_path:
            paths.append(first_path)
            visited_sets.append(set(first_path.nodes))
            
            # Buscar caminos alternativos
            while len(paths) < max_alternatives:
                # Intentar encontrar un camino que use diferentes nodos
                alternative = self._find_alternative_path(start, end, visited_sets)
                if not alternative:
                    break
                paths.append(alternative)
                visited_sets.append(set(alternative.nodes))
                
        return paths
        
    def _dijkstra_single_path(self, start: int, end: int) -> Optional[Path]:
        """Implementación base de Dijkstra usando cola de prioridad."""
        distances = [float('inf')] * self.size
        distances[start] = 0
        parents = [-1] * self.size
        pq = PriorityQueue()
        pq.put((0, start))
        visited = set()
        
        print(f"\n🔍 Buscando camino de {start + 1} a {end + 1}")
        
        while not pq.empty():
            current_dist, current = pq.get()
            
            if current in visited:
                continue
                
            visited.add(current)
            print(f"\n📍 Visitando nodo {current + 1}")
            
            if current == end:
                break
                
            # Explorar vecinos
            for neighbor in range(self.size):
                if (self.graph[current][neighbor] > 0 and 
                    neighbor not in visited):
                    distance = current_dist + self.graph[current][neighbor]
                    
                    if distance < distances[neighbor]:
                        old_dist = "∞" if distances[neighbor] == float('inf') else distances[neighbor]
                        distances[neighbor] = distance
                        parents[neighbor] = current
                        pq.put((distance, neighbor))
                        print(f"  ↪ Actualizando distancia a {neighbor + 1}: {old_dist} → {distance}")
        
        if distances[end] == float('inf'):
            return None
            
        # Reconstruir el camino
        path = []
        current = end
        while current != -1:
            path.append(current)
            current = parents[current]
        path.reverse()
        
        return Path(path, distances[end])
        
    def _find_alternative_path(self, start: int, end: int, 
                             visited_sets: List[Set[int]]) -> Optional[Path]:
        """Encuentra un camino alternativo evitando nodos ya usados."""
        # Crear una copia del grafo para modificar pesos
        temp_graph = [row[:] for row in self.graph]
        
        # Penalizar caminos que usan nodos ya visitados
        for visited_set in visited_sets:
            for node in visited_set:
                for i in range(self.size):
                    if temp_graph[i][node] != float('inf'):
                        temp_graph[i][node] *= 2  # Duplicar el peso
                        
        # Ejecutar Dijkstra con el grafo modificado
        dijkstra = DijkstraAlgorithm(self.size)
        dijkstra.initialize(temp_graph)
        path = dijkstra._dijkstra_single_path(start, end)
        
        # Verificar si el camino es suficientemente diferente
        if path:
            path_set = set(path.nodes)
            overlap = False
            for visited_set in visited_sets:
                if len(path_set.intersection(visited_set)) > 2:  # Permitir algo de superposición
                    overlap = True
                    break
            if not overlap:
                # Recalcular la distancia real usando el grafo original
                real_distance = 0
                for i in range(len(path.nodes) - 1):
                    real_distance += self.graph[path.nodes[i]][path.nodes[i + 1]]
                return Path(path.nodes, real_distance)
        return None

def crear_matriz_adyacencia(V: int) -> List[List[float]]:
    return [[0 if i == j else float('inf') for j in range(V)] for i in range(V)]

def print_matrix(matrix: List[List[float]], titulo: str):
    n = len(matrix)
    print(f"\n{titulo}")
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
            print("\n🚀 Algoritmo de Dijkstra - Múltiples Caminos")
            V = int(input("\nIngrese el número de vértices: "))
            if V <= 0:
                print("❌ El número de vértices debe ser positivo")
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
                        print("❌ Error: Ingrese origen destino y distancia")
                        continue
                        
                    origen = int(partes[0]) - 1
                    destino = int(partes[1]) - 1
                    peso = int(partes[2])
                    es_direccional = len(partes) > 3 and partes[3].lower() == 'd'
                    
                    if origen < 0 or origen >= V or destino < 0 or destino >= V:
                        print(f"❌ Error: Los nodos deben estar entre 1 y {V}")
                        continue
                    if peso < 0:
                        print("❌ Error: La distancia no puede ser negativa")
                        continue
                        
                    grafo[origen][destino] = peso
                    if not es_direccional:
                        grafo[destino][origen] = peso
                except ValueError:
                    print("❌ Error: Los valores deben ser números")
            
            print_matrix(grafo, "📊 Matriz de Adyacencia")
            
            while True:
                try:
                    origen = int(input("\nIngrese el nodo de origen (1 a " + str(V) + "): ")) - 1
                    destino = int(input("Ingrese el nodo de destino (1 a " + str(V) + "): ")) - 1
                    
                    if origen < 0 or origen >= V or destino < 0 or destino >= V:
                        print(f"❌ Error: Los nodos deben estar entre 1 y {V}")
                        continue
                        
                    if origen == destino:
                        print("ℹ️ El origen y destino son el mismo nodo. La distancia es 0.")
                        continue
                        
                    break
                except ValueError:
                    print("❌ Por favor ingrese números válidos")
            
            # Crear instancia y encontrar caminos
            dijkstra = DijkstraAlgorithm(V)
            dijkstra.initialize(grafo)
            paths = dijkstra.find_paths(origen, destino)
            
            if not paths:
                print(f"\n❌ No existe un camino entre el nodo {origen + 1} y el nodo {destino + 1}")
            else:
                print("\n✨ Caminos encontrados:")
                for i, path in enumerate(paths, 1):
                    print(f"\n🛣️  Camino {i}:")
                    print(f"   {path}")
            
            if input("\n¿Otro cálculo? (s/n): ").lower() != 's':
                break
                
        except ValueError:
            print("❌ Por favor ingrese valores numéricos válidos")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
