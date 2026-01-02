# ------------------------------------------------------------
# Impresión del mapa (alineado, bonito, uniforme)
# ------------------------------------------------------------
def print_laberinth(laberinth, path):
    step = {pos: i for i, pos in enumerate(path)}  #Mapa de pasos para el camino
    rows, columns = len(laberinth), len(laberinth[0]) #Dimensiones del laberinto

    W = max(3, len(str(len(path) - 1)))  #Ancho dinamico, minimo 3, y que soporte el mayor indice

    def cell_str(r, c):
        if (r, c) == path[0]:
            return "S".rjust(W)           # " S" Inicio
        if laberinth[r][c] == 9:
            return "E".rjust(W)           # " E" Salida
        if laberinth[r][c] == 1:
            return "█" * W                # "██" Pared
        if (r, c) in step:
            return f"{step[(r, c)]:0{W}d}"  # "00", "01", ... Paso en el camino
        return ".".rjust(W)               # " ." Camino libre

    #Encabezado de columnas
    print("   " + " ".join(f"{c:0{W}d}" for c in range(columns)))
    print("   " + ("-" * (columns * (W + 1) - 1)))

    #Recorrer filas e imprimirlas con su indice
    for r in range(rows): 
        row_cells = [cell_str(r, c) for c in range(columns)]
        print(f"{r:02d}| " + " ".join(row_cells)) 

# ------------------------------------------------------------
# Reportes (oficial)
# ------------------------------------------------------------
def print_path_steps(path): #Imprimir el camino paso a paso
    print(f"\nCamino a la salida (paso a paso):")
    print("-" * 36)
    for i, (row, column) in enumerate(path):
        print(f"Paso {i+1:02d} | fila {row:02d} | columna {column:02d}")

def path_to_directions(path): #Convertir el camino en direcciones
    directions = []
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        if r2 == r1 - 1: directions.append("↑")
        elif r2 == r1 + 1: directions.append("↓")
        elif c2 == c1 - 1: directions.append("←")
        elif c2 == c1 + 1: directions.append("→")
    return directions

def print_directions(directions, per_line=40):
    print("\nDirecciones:")
    print("-" * 36)
    for i in range(0, len(directions), per_line):
        print(" ".join(directions[i:i+per_line]))

def compressed_directions(directions): #Comprimir las direcciones e imprimirlas
    if not directions: # Si la lista de direcciones esta vacia, retornamos la cadena vacia
        return ""
    out = [] #Lista para almacenar las direcciones comprimidas
    current = directions[0] #Direccion actual
    count = 1
    for dir in directions[1:]: #Recorrer las direcciones y contarlas
        if dir == current:
            count += 1
        else: #Si la direccion cambia, guardar la direccion y su conteo
            out.append(f"{current}x{count}")
            current = dir
            count = 1
    out.append(f"{current}x{count}")
    return " ".join(out) #Retornar las direcciones comprimidas como una cadena

def print_summary(path): #Imprimir resumen del camino
    print(f"\nResumen:")
    print("-" * 36)
    print(f"Inicio: {path[0]}")
    print(f"Salida: {path[-1]}")
    print(f"Celdas recorridas: {len(path)}")
    print(f"Movimientos realizados: {len(path) -1}")

# ------------------------------------------------------------
# Resultado oficial completo + opciones reducidas
# ------------------------------------------------------------
def print_solution_official_and_options(laberinth, paths): #Imprimir la solucion oficial y las opciones
    if not paths: #Si no hay caminos encontrados, lo indicamos
        print("No se encontró ningún camino a la salida.")
        return
    
    official_path = paths[0] #Camino mas corto (oficial)
    opt_paths = paths[1:]#Caminos alternativos (opciones)

    #Mostramos por pantalla la solucion oficial y sus detalles

    print("\n" + "=" * 48)
    print(f"SOLUCION OFICIAL (TOP -1) + OPCIONES")
    print("=" * 48)

    #Imprimir la solucion oficial

    print("\nSOLUCION OFICIAL (CAMINO MAS CORTO):")
    print("-" * 48)
    print(f"Movimientos: {len(official_path) - 1} | Celdas: {len(official_path)}\n")

    print_laberinth(laberinth, official_path) #Imprimir el laberinto con el camino oficial
    print_path_steps(official_path) #Imprimir el camino oficial paso a paso

    directions = path_to_directions(official_path)
    print_directions(directions, per_line=40)#Imprimir las direcciones oficiales

    compressed = compressed_directions(directions) #Comprimir las direcciones y las imprimimos
    print("\nDirecciones comprimidas:")
    print("-" * 36)
    print(compressed)

    print_summary(official_path) #Imprimir resumen del camino oficial

    #Imprimir las opciones alternativas (solo metricas + mapa)
    if opt_paths: #si hay caminos alternativos, lo mostramos
        print("\n" + "=" * 48)
        print(f"OPCIONES ALTERNATIVAS")
        print("=" * 48)

        for i, opt_path in enumerate(opt_paths, 1): #Recorrer las opciones alternativas y mostrarlas
            print(f"\nOPCION {i}:")
            print("-" * 48)
            print(f"Movimientos: {len(opt_path) - 1} | Celdas: {len(opt_path)}\n")
            print_laberinth(laberinth, opt_path) 

    else: #Si no hay caminos alternativos, lo indicamos
        print("\nNo hay opciones alternativas disponibles.")

    print("\n" + "=" * 48 + "\n")