from collections import deque
from typing import Optional

# ------------------------------------------------------------
# Utilidad: encontrar la salida (9)
# ------------------------------------------------------------
def find_goal(laberinth, goal_value=9): #Buscar la posición de la salida en el laberinto
    for rows in range(len(laberinth)): 
        for columns in range(len(laberinth[0])):
            if laberinth[rows][columns] == goal_value: #Si es la salida
                return (rows, columns) #Retornar la posición
    return None


# ------------------------------------------------------------
# (Opcional) DFS + Backtracking: excelente para recursividad,
# pero NO garantiza el camino más corto.
# ------------------------------------------------------------
def solve_puzzle_dfs(laberinth, row, column, path=None, visited=None):
    #fila,columna = son las pocisiones actuales
    #path = lista que guarda las pocisiones recorridas
    if path is None:
        path = [] #Signfica que estamos en el inicio del laberinto
    if visited is None:
        visited = set()  #Conjunto para almacenar las posiciones visitadas

    #Verificar si la pocision es valida
    if not (0 <= row < len(laberinth) and 0 <= column < len(laberinth[0])):
        return None  #Fuera de los limites del laberinto
    
    #Verificar si la posicion actual es una pared (1) o ya ha sido visitada
    if laberinth[row][column] == 1 or (row, column) in visited:
        return None  # No es una pocision valida
    
    visited.add((row, column))  #Marcar la pocision como visitada
    path.append((row, column))  #Agregar la pocision actual al camino

    #Caso base: verificar si hemos llegado a la salida (9)
    if laberinth[row][column] == 9:
        return path  #Hemos encontrado la salida
    
    #Explorar las cuatro direcciones posibles: arriba, abajo, izquierda, derecha
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    #Recorrer cada direccion
    for move in directions:
        new_row = row + move[0] #Calcular la nueva fila
        new_column = column + move[1] #Calcular la nueva columna

        #Llamada recursiva para explorar la nueva pocision
        result_path = solve_puzzle_dfs(laberinth, new_row, new_column, path, visited)

        if result_path is not None:
            return result_path  #Si encontramos la salida, retornar el camino
        
    path.pop()  #Eliminar la pocision actual del camino (backtracking)
    visited.discard((row, column))  #Desmarcar la pocision como visitada

    return None  #No se encontro la salida desde esta pocision


# ------------------------------------------------------------
# BFS: camino más corto con soporte de bloqueos (celdas y movimientos [nodos/aristas])
# ------------------------------------------------------------
def bfs_shortest_paths(laberinth, start, goal, blocked_cells=None, blocked_moves=None):
    rows, columns = len(laberinth), len(laberinth[0]) #Dimensiones del laberinto
    blocked_cells = blocked_cells or set()  #Celdas bloqueadas
    blocked_moves = blocked_moves or set()  #Movimientos bloqueados

    (start_row, start_column) = start#Posición de inicio
    (goal_row, goal_column) = goal #Posición de la salida

    if not(0 <= start_row < rows and 0 <= start_column < columns): # Si la posición de inicio no es válida
        return None  #Inicio fuera de los limites
    if not(0 <= goal_row < rows and 0 <= goal_column < columns): # Si la posición de la salida no es válida
        return None  #Salida fuera de los limites
    
    if laberinth[start_row][start_column] == 1 or laberinth[goal_row][goal_column] == 1: #Si inicio o salida es una pared
        return None  #No es una pocision valida
    if start in blocked_cells or goal in blocked_cells: #Si inicio o salida estan bloqueados
        return None  #No es una pocision valida
    
    queue = deque([start])  #Cola para BFS
    parent: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}  #Diccionario para rastrear el camino

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #Arriba, Abajo, Izquierda, Derecha

    while queue: #Mientras haya celdas por explorar
        cur_rows, cur_columns = queue.popleft() #Obtener la siguiente celda

        if (cur_rows, cur_columns) == goal: #Si hemos llegado a la salida
            #Reconstruir el camino desde inicio hasta la salida
            path = [] #Camino encontrado
            current = goal #Posición actual

            while current is not None:#Mientras no lleguemos al inicio
                path.append(current) #Agregar la posición al camino
                current = parent[current] #Mover al padre
            path.reverse() #Invertir el camino para que vaya de inicio a salida

            return path  #Retornar el camino encontrado
        
        for dir_row, dir_column in directions: #Explorar las cuatro direcciones
            new_row = cur_rows + dir_row #Calcular la nueva posición
            new_column = cur_columns + dir_column #Calcular la nueva posición
            new_pos = (new_row, new_column) #Nueva posición como tupla

            if not (0 <= new_row < rows and 0 <= new_column < columns): #Si la nueva posición esta fuera de los limites
                continue  #Ignorar esta posición

            if laberinth[new_row][new_column] == 1: #Si la nueva posición es una pared
                continue  #Ignorar esta posición

            if new_pos in blocked_cells: #Si la nueva posición esta bloqueada
                continue  #Ignorar esta posición

            if ( (cur_rows, cur_columns), new_pos) in blocked_moves: #Si el movimiento esta bloqueado
                continue  #Ignorar este movimiento

            if new_pos not in parent: #Si ya hemos visitado esta posición
                parent[new_pos] = (cur_rows, cur_columns) #Registrar el padre
                queue.append(new_pos) #Agregar la nueva posición a la cola

    return None  #No se encontro un camino a la salida


# ------------------------------------------------------------
# K caminos más cortos (Yen) usando BFS
# paths[0] = oficial (más corto)
# paths[1:] = alternativas siguientes (si existen)
# ------------------------------------------------------------
def k_shortest_paths(laberinth, start_row, start_column, k=4, goal_value=9):
    #Usar BFS para encontrar los k caminos más cortos a la salida
    start = (start_row, start_column)
    goal = find_goal(laberinth, goal_value)#Buscar la posición de la salida
    if goal is None:
        return []  #No hay salida en el laberinto

    first_path = bfs_shortest_paths(laberinth, start, goal) #Encontrar el primer camino más corto
    if first_path is None:
        return []  #No hay camino a la salida
    
    A = [first_path]  #Lista de los k caminos más cortos encontrados
    B = []  #Lista de caminos candidatos
    seen_candidates = set()  #Conjunto para evitar caminos duplicados

    def cost(path): 
        return len(path) - 1  #Movimientos

    for _ in range(1, k): #Encontrar los posibles caminos hasta k
        last_path = A[-1]#Obtener el último camino encontrado
        for i in range(len(last_path) -1): #Recorremos la lista de caminos
            spur_node = last_path[i] #Nodo de desviación
            root_path = last_path[:i + 1] #Camino original hasta el nodo de desviación

            blocked_cells = set(root_path[:-1]) #Eliminar los nodos del camino original excepto el último
            blocked_moves = set() #Conjunto para almacenar caminos eliminados

            for path in A:
                if len(path) > i and path[:i+1] == root_path: #
                    blocked_moves.add((path[i], path[i + 1])) #Eliminar el siguiente nodo del camino original

            spur_path = bfs_shortest_paths(laberinth, start=spur_node, goal=goal, blocked_cells=blocked_cells, blocked_moves=blocked_moves)
            #Encontrar el camino desde el nodo de desviación a la salida
            if spur_path is None: #Si no hay camino desde el nodo de desviación
                continue  #Ignorar este camino

            total_path = root_path + spur_path[1:] #Combinar el camino original con el nuevo camino
            key = tuple(total_path) #Clave única para el camino

            if key in seen_candidates: #Si el camino si ha sido visto antes
                continue  #Ignorar este camino
            seen_candidates.add(key)  #Marcar el camino como visto
            B.append((cost(total_path), total_path))  #Agregar el camino candidato a la lista de candidatos
        if not B: #Si no hay caminos candidatos
            break  #Salir del bucle
        B.sort(key=lambda x: x[0])  #Ordenar los caminos candidatos por costo
        _, best_path = B.pop(0)  #Obtener el camino candidato con el menor costo
        A.append(best_path)  #Agregar el mejor camino a la lista de caminos encontrados

    return A  #Retornar los k caminos más cortos encontrados

