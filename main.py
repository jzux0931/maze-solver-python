import argparse
from .maze_solver import k_shortest_paths
from .maze_render import print_solution_official_and_options 
from .maze_tests import run_sanity_tests


def build_laberinth (): #Construir el laberinto
    #0 -> camino libre
    #1 -> pared
    #9 -> salida

    return [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 9],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Laberinto Pro: solución oficial + k alternativas.")
    parser.add_argument("--k", type=int, default=4, help="Cantidad de caminos más cortos a generar (default: 4).")
    parser.add_argument("--start", nargs=2, type=int, default=[1, 0], metavar=("ROW", "COL"),
                        help="Coordenadas de inicio: ROW COL (default: 1 0).")
    parser.add_argument("--no-tests", action="store_true", help="Desactiva sanity tests.")
    parser.add_argument("--metrics", action="store_true", help="Muestra métricas avanzadas (tiempo/nodos).")
    return parser.parse_args()


def main():
    args = parse_args()

    lab = build_laberinth()
    start_row, start_col = args.start[0], args.start[1]

    paths = k_shortest_paths(lab, start_row, start_col, k=args.k)
    print_solution_official_and_options(lab, paths)

    if not args.no_tests:
        run_sanity_tests(lab, (start_row, start_col), k=args.k, verbose=True)

    if args.metrics:
        from .metrics import print_advanced_metrics
        print_advanced_metrics(lab, (start_row, start_col), k=args.k)


if __name__ == "__main__": #Ejecutar la funcion principal
    main() 
