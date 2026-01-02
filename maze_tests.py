# ============================================================
# TESTS AUTOMÁTICOS (SANITY CHECKS)
# ============================================================

from __future__ import annotations
from typing import Optional
from .maze_solver import find_goal, bfs_shortest_paths, solve_puzzle_dfs, k_shortest_paths


def run_sanity_tests(
    laberinth: list[list[int]],
    start: tuple[int, int],
    k: int = 4,
    goal_value: int = 9,
    verbose: bool = True
) -> bool:
    """
    Ejecuta tests automáticos para validar:
      1) BFS encuentra camino más corto o igual que DFS (si ambos existen)
      2) k_shortest_paths devuelve caminos:
         - únicos
         - ordenados por movimientos (no-decreciente)
         - válidos (adyacencia, dentro de límites, no atraviesan paredes)
         - terminan en la salida
    Requiere que existan:
      - find_goal
      - bfs_shortest_path
      - solve_puzzle_dfs
      - k_shortest_paths
    """
    goal = find_goal(laberinth, goal_value) #Encuentra la salida (goal = 9)
    if goal is None:
        if verbose:
            print("[TEST] Falló: no existe salida (9) en el laberinto.")
        return False

    # ---- Helpers ----
    rows, cols = len(laberinth), len(laberinth[0])

    def is_valid_cell(pos: tuple[int, int]) -> bool:
        r, c = pos
        return 0 <= r < rows and 0 <= c < cols and laberinth[r][c] != 1 #Valida que la celda existe dentro de la matriz y que no es pared

    def is_adjacent(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 #Manhattan distance = 1 (puedes moverte 1 paso o celda en vertical/horizontal.)
                                                        #No se permiten movimientos diagonales ni saltos

    # ---- Validación de caminos ----
    #Confirma que un camino es válido
    def validate_path(path: list[tuple[int, int]]) -> bool:
        if not path:
            return False #No vacio
        if path[0] != start:
            return False #El camino comienza en el inicio
        if path[-1] != goal:
            return False #El camino no termina en la salida
        
        for p in path: #Cada posicion es valida (no pared, dentro de limites)
            if not is_valid_cell(p):
                return False
            
        for x, y in zip(path, path[1:]): #Cada paso es adyacente al siguiente
            if not is_adjacent(x, y):
                return False
        return True

    ok = True

    # ---- 1) BFS vs DFS ----
    path_bfs = bfs_shortest_paths(laberinth, start, goal)
    path_dfs = solve_puzzle_dfs(laberinth, start[0], start[1])

    if path_bfs is not None: #Si BFS encontro un camino, validarlo
        if not validate_path(path_bfs):
            ok = False
            if verbose:
                print("[TEST] Falló: el camino BFS no es válido.")
    if path_dfs is not None: #Si DFS encontro un camino, validarlo
        if not validate_path(path_dfs):
            ok = False
            if verbose:
                print("[TEST] Falló: el camino DFS no es válido.")

    if path_bfs is not None and path_dfs is not None: #Verificacion "optima": BFS no puede ser peor que DFS
        if len(path_bfs) > len(path_dfs):
            ok = False
            if verbose:
                print("[TEST] Falló: BFS dio un camino MÁS largo que DFS (no debería).")

    # ---- 2) K shortest paths ----
    paths = k_shortest_paths(laberinth, start[0], start[1], k=k, goal_value=goal_value)
    if not paths:
        # si BFS no encontró nada, esto es aceptable; si BFS sí, entonces es fallo
        if path_bfs is not None:
            ok = False
            if verbose:
                print("[TEST] Falló: k_shortest_paths devolvió vacío pero BFS sí encontró camino.")
    else:
        # 2a) Unicidad sin duplicados
        #Convierte cada camino en una tupla (inmutable) para poder almacenarlo en un conjunto/set
        seen = set()
        for p in paths:
            t = tuple(p)
            if t in seen:
                ok = False
                if verbose:
                    print("[TEST] Falló: hay caminos duplicados en k_shortest_paths.")
                break
            seen.add(t)

        # 2b) Orden por movimientos (ascendente)
        lens = [len(p) - 1 for p in paths]
        if any(lens[i] > lens[i+1] for i in range(len(lens)-1)):
            ok = False
            if verbose:
                print("[TEST] Falló: los caminos no están ordenados por movimientos (ascendente).")

        # 2c) Validez individual de cada camino
        for idx, p in enumerate(paths):
            if not validate_path(p):
                ok = False
                if verbose:
                    print(f"[TEST] Falló: el camino #{idx} no es válido.")
                break

        # 2d) El primero debe ser el mismo largo que BFS (óptimo)
        if path_bfs is not None:
            if (len(paths[0]) != len(path_bfs)):
                ok = False
                if verbose:
                    print("[TEST] Falló: paths[0] no coincide en longitud con el BFS (óptimo).")

    if verbose:
        print("[TEST] Resultado:", "OK" if ok else "FALLÓ")

    return ok