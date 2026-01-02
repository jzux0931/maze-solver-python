from __future__ import annotations

from time import perf_counter
from collections import deque
from typing import Optional

from .maze_solver import find_goal, solve_puzzle_dfs, bfs_shortest_paths, k_shortest_paths


def _bfs_count_nodes(
    laberinth: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> tuple[Optional[list[tuple[int, int]]], int]:
    rows, cols = len(laberinth), len(laberinth[0])
    sr, sc = start
    gr, gc = goal

    if not (0 <= sr < rows and 0 <= sc < cols):
        return None, 0
    if not (0 <= gr < rows and 0 <= gc < cols):
        return None, 0
    if laberinth[sr][sc] == 1 or laberinth[gr][gc] == 1:
        return None, 0

    q = deque([start])
    parent: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
    explored = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        r, c = q.popleft()
        explored += 1

        if (r, c) == goal:
            path: list[tuple[int, int]] = []
            cur: Optional[tuple[int, int]] = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, explored

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if laberinth[nr][nc] == 1:
                continue
            if nxt in parent:
                continue

            parent[nxt] = (r, c)
            q.append(nxt)

    return None, explored


def _dfs_count_nodes(
    laberinth: list[list[int]],
    start: tuple[int, int],
    goal_value: int = 9,
) -> tuple[Optional[list[tuple[int, int]]], int]:
    rows, cols = len(laberinth), len(laberinth[0])
    visited: set[tuple[int, int]] = set()
    path: list[tuple[int, int]] = []
    explored = 0

    def rec(r: int, c: int) -> Optional[list[tuple[int, int]]]:
        nonlocal explored

        if not (0 <= r < rows and 0 <= c < cols):
            return None
        if laberinth[r][c] == 1 or (r, c) in visited:
            return None

        explored += 1
        visited.add((r, c))
        path.append((r, c))

        if laberinth[r][c] == goal_value:
            return list(path)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            res = rec(r + dr, c + dc)
            if res is not None:
                return res

        path.pop()
        visited.discard((r, c))
        return None

    return rec(start[0], start[1]), explored


def print_advanced_metrics(
    laberinth: list[list[int]],
    start: tuple[int, int],
    k: int = 4,
    goal_value: int = 9,
) -> None:
    goal = find_goal(laberinth, goal_value)
    if goal is None:
        print("\n[MÉTRICAS] No existe salida (9) en el laberinto.")
        return

    # BFS tiempo
    t0 = perf_counter()
    bfs_path = bfs_shortest_paths(laberinth, start, goal)
    bfs_time = (perf_counter() - t0) * 1000

    # BFS nodos explorados (con BFS instrumentado)
    t0 = perf_counter()
    _, bfs_nodes = _bfs_count_nodes(laberinth, start, goal)
    bfs_count_time = (perf_counter() - t0) * 1000

    # DFS tiempo
    t0 = perf_counter()
    dfs_path = solve_puzzle_dfs(laberinth, start[0], start[1])
    dfs_time = (perf_counter() - t0) * 1000

    # DFS nodos explorados (instrumentado)
    t0 = perf_counter()
    _, dfs_nodes = _dfs_count_nodes(laberinth, start, goal_value=goal_value)
    dfs_count_time = (perf_counter() - t0) * 1000

    # K-shortest tiempo
    t0 = perf_counter()
    paths = k_shortest_paths(laberinth, start[0], start[1], k=k, goal_value=goal_value)
    k_time = (perf_counter() - t0) * 1000

    def moves(p: Optional[list[tuple[int, int]]]) -> Optional[int]:
        return (len(p) - 1) if p else None

    print("\n" + "=" * 48)
    print("MÉTRICAS AVANZADAS")
    print("=" * 48)
    print(f"Start: {start} | Goal: {goal}")
    print("-" * 48)
    print(f"BFS:         tiempo={bfs_time:.3f} ms | movimientos={moves(bfs_path)}")
    print(f"BFS (conteo): tiempo={bfs_count_time:.3f} ms | nodos_explorados={bfs_nodes}")
    print("-" * 48)
    print(f"DFS:         tiempo={dfs_time:.3f} ms | movimientos={moves(dfs_path)}")
    print(f"DFS (conteo): tiempo={dfs_count_time:.3f} ms | nodos_explorados={dfs_nodes}")
    print("-" * 48)
    print(f"K-shortest (k={k}): tiempo={k_time:.3f} ms | caminos={len(paths)}")
    if paths:
        print(f"  Oficial:   movimientos={len(paths[0]) - 1}")
        if len(paths) > 1:
            print(f"  2da opción: movimientos={len(paths[1]) - 1}")
    print("=" * 48 + "\n")
