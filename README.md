# 🧩 Laberinth Project

**Python Maze Solver with DFS, BFS and K-Shortest Paths**

This project is a modular maze solver written in Python that implements
classic search algorithms (DFS and BFS) and generates multiple optimal
routes using a K-shortest-paths approach.

It includes a clean architecture, command-line interface (CLI),
performance metrics, and basic consistency tests.

> Este proyecto implementa un solucionador de laberintos en Python
> utilizando distintos algoritmos de búsqueda, con una arquitectura
> modular, soporte de línea de comandos, métricas de rendimiento y pruebas
> básicas de consistencia.

---

## 🔍 Project Summary

**Main objectives:**

1. Find the **optimal solution** (shortest path).
2. Generate **fast alternative routes**.
3. Compare algorithms in terms of **execution time and explored nodes**.

**Focus areas:**

- Algorithmic thinking
- Clean architecture
- Performance measurement
- Command-line usability

---

## 📂 Project Structure

```text
laberinth_proyect/
│
├── __init__.py
├── main.py # Entry Point (Punto de entrada) (CLI)
├── maze_solver.py # DFS, BFS and K-shortest paths
├── maze_render.py # Rendering maze and paths (Renderizado del laberinto y caminos)
├── metrics.py # Time metrics and explored-nodes (Métricas de tiempo y nodos explorados)
├── maze_tests.py # Sanity tests
└── README.md
```

---

## 🧠 Implemented Algorithms

### 1. DFS (Depth-First Search)

- Implemented recursively.
- Finds a **valid path**, but does **not guarantee** the shortest one.
- Useful for comparing deep exploration vs level-based exploration.

### 2. BFS (Breadth-First Search)

- Guarantees the **shortest path** in unweighted mazes.
- Used as the **official optimal solution**.
- Serves as the baseline for performance metrics.

### 3. K-Shortest Paths

- Generates the **K shortest possible valid paths**.
- The first path is always the optimal one (BFS).
- Remaining paths are alternative solutions, sorted by length.

---

## 🖥️ Example Output

```text

Maze with official solution (*), start (S) and exit (E):

█ █ █ █ █ █ █ █ █ █ █ █
S * * * █ . . . . . . █
█ █ █ * █ . █ █ █ █ . █
█ . . * . . . . . . . █
█ █ █ * █ █ █ █ █ . . █
█ . . * * * * * █ . . █
█ . █ █ █ █ █ * █ █ . █
█ . . . . . . * * * . █
█ █ █ █ █ █ . █ █ * █ █
█ . . . . . . . . * * E
█ █ █ █ █ █ █ █ █ █ █ █

------------------------------------------------
OFFICIAL PATH (Shortest Path - BFS)
------------------------------------------------
Total moves: 26

Step-by-step path:
Step 00 | row 01 | col 00
Step 01 | row 01 | col 01
Step 02 | row 01 | col 02
Step 03 | row 01 | col 03
...
Step 26 | row 10 | col 11

------------------------------------------------
ALTERNATIVE PATHS (K-Shortest Paths)
------------------------------------------------
Path 2: 28 moves
Path 3: 30 moves
Path 4: 31 moves

------------------------------------------------
ADVANCED METRICS
------------------------------------------------
BFS:
  Time: 0.214 ms
  Nodes explored: 78

DFS:
  Time: 0.119 ms
  Nodes explored: 121

K-Shortest Paths (k=4):
  Total time: 0.803 ms

================================================
```

---

## 🧩 Design Decisions | Decisiones de diseño

- BFS is used as the official solution because it guarantees the shortest path.
- DFS is included for comparison and educational purposes.
- K-shortest paths are generated to provide alternative valid solutions.
- The project is executed as a Python package to ensure clean imports.

- BFS es utilizado como la solucion oficial porque garantiza el camino mas corto.
- DFS esta incluido para razones comparativas y educativas.
- K-shortest paths son generados para proveer soluciones validas alternativas.
- El projecto es ejecutado como un paquete de Python para asegurar imports limpios.

---

## 🖥️ Program Execution

> ⚠️ Important: the project must be executed **as a Python module**, not as a direct script.

From the project’s parent folder (`Enero_2025`):

### Basic executions

```bash
python -m laberinth_proyect.main
python -m laberinth_proyect.main --k 6
python -m laberinth_proyect.main --metrics
```

## 🚀 Future Improvements

- Implement A\* with heuristics.
- Add animated or step-by-step visualization.
- Load mazes from external files.
- Extend automated testing with `pytest`.

---

## 👤 Author

Developed as an advanced Python project focused on:

- algorithmic problem solving,
- search strategies (DFS, BFS),
- and modular Python project design.
