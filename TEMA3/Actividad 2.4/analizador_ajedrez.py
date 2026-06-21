# ====================================================================
# Analizador Léxico de Subconjunto PGN (Ajedrez)
# Implementación de Autómata Finito Determinístico (AFD)
# ====================================================================

def clasificar_caracter(c):
    """
    Simula las clases de caracteres de nuestro Alfabeto formal (Sigma).
    """
    if c in "KQRBN":
        return "P"  # Piezas Mayores
    elif c in "abcdefgh":
        return "C"  # Columnas
    elif c in "12345678":
        return "F"  # Filas
    elif c == "x":
        return "X"  # Captura
    elif c == "+":
        return "J"  # Jaque
    else:
        return "DESCONOCIDO"

# Tabla de transiciones (delta). 
# Estructura: {(Estado_Actual, Clase_Leida): Estado_Siguiente}
# Nota: Si una transición no está en este diccionario, implícitamente va a qE (Error)
tabla_transiciones = {
    ("q0", "P"): "q1",
    ("q0", "C"): "q2",
    
    ("q1", "C"): "q4",
    ("q1", "X"): "q3",
    
    ("q2", "F"): "q5",
    ("q2", "X"): "q3",
    
    ("q3", "C"): "q4",
    
    ("q4", "F"): "q5",
    
    ("q5", "J"): "q6"
}

def analizar_movimiento(cadena):
    """
    Ejecuta el Autómata Finito Determinístico sobre una cadena de texto.
    """
    estado_actual = "q0"
    
    for caracter in cadena:
        clase = clasificar_caracter(caracter)
        
        # Si el caracter no pertenece al alfabeto, error léxico inmediato
        if clase == "DESCONOCIDO":
            return False, f"Error Léxico: Caracter '{caracter}' no pertenece al alfabeto."
            
        # Buscamos la transición en la tabla. Si no existe, caemos en el sumidero (qE)
        estado_actual = tabla_transiciones.get((estado_actual, clase), "qE")
        
        # Si caemos en el sumidero, rechazamos la cadena inmediatamente
        if estado_actual == "qE":
            return False, f"Error Sintáctico: Transición inválida al leer '{caracter}'."

    # Al terminar de leer la cadena, verificamos si estamos en un Estado de Aceptación
    estados_aceptacion = ["q5", "q6"]
    
    if estado_actual in estados_aceptacion:
        return True, "Movimiento Válido [✓]"
    else:
        return False, "Error: La cadena está incompleta."

# Diccionario para traducir las siglas a español
nombres_piezas = {
    'K': 'El Rey', 
    'Q': 'La Reina', 
    'R': 'La Torre', 
    'B': 'El Alfil', 
    'N': 'El Caballo'
}

def traducir_movimiento(cadena):
    """
    Traduce un movimiento válido de PGN a lenguaje natural humano.
    Asume que la cadena ya pasó exitosamente por el Autómata.
    """
    # 1. Revisamos si hay jaque y lo separamos
    texto_jaque = " y da Jaque al rey oponente" if "+" in cadena else ""
    cadena_limpia = cadena.replace("+", "") # Quitamos el '+' para analizar el resto

    # 2. Revisamos si es una captura
    if "x" in cadena_limpia:
        if cadena_limpia[0].islower(): # Captura de peón (ej. exd5)
            columna_origen = cadena_limpia[0]
            casilla_destino = cadena_limpia[2:]
            return f"Un peón de la columna '{columna_origen}' captura en la casilla {casilla_destino}{texto_jaque}."
        else: # Captura de pieza (ej. Bxc6)
            pieza = nombres_piezas[cadena_limpia[0]]
            casilla_destino = cadena_limpia[2:]
            return f"{pieza} captura en la casilla {casilla_destino}{texto_jaque}."
            
    # 3. Si no es captura, es un movimiento simple
    else:
        if cadena_limpia[0].islower(): # Movimiento de peón (ej. e4)
            return f"Un peón avanza a la casilla {cadena_limpia}{texto_jaque}."
        else: # Movimiento de pieza (ej. Nf3)
            pieza = nombres_piezas[cadena_limpia[0]]
            casilla_destino = cadena_limpia[1:]
            return f"{pieza} se mueve a la casilla {casilla_destino}{texto_jaque}."

# ====================================================================
# Interfaz Interactiva por Terminal
# ====================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("   ANALIZADOR LÉXICO PGN (AJEDREZ) - MODO INTERACTIVO")
    print("   Escriba 'salir' para terminar el programa.")
    print("=====================================================")
    
    while True:
        # Pedimos el movimiento al usuario y limpiamos espacios extra
        movimiento = input("\nIngrese un movimiento de ajedrez: ").strip()
        
        # Condición de salida
        if movimiento.lower() == 'salir':
            print("Cerrando el analizador. ¡Éxito en la defensa!")
            break
            
        # Evitar procesar entradas vacías si el usuario presiona Enter por error
        if movimiento == "":
            continue
            
        # Ejecutar el analizador (Autómata)
        es_valido, msj = analizar_movimiento(movimiento)
        
        # Imprimir el resultado
        if es_valido:
            # Si el autómata lo aprueba, lo traducimos a humano
            traduccion = traducir_movimiento(movimiento)
            print(f" -> [✓] Válido: {traduccion}")
        else:
            # Si falla, mostramos el error léxico/sintáctico
            print(f" -> [X] Rechazado: {msj}")