import sys
import time
from lark import Lark

# 1. Gramática Definitiva Simplificada con Token Único de Texto
gramatica_docker = r"""
especificacion_red: "networks" ":" NL lista_redes

lista_redes: definicion_red+
definicion_red: TEXTO ":" NL bloque_propiedades
bloque_propiedades: propiedad+

propiedad: atributo_directo | seccion_anidada

atributo_directo: "driver" ":" TEXTO NL
                | "internal" ":" BOOLEANO NL
                | "attachable" ":" BOOLEANO NL
                | "enable_ipv6" ":" BOOLEANO NL

seccion_anidada: "ipam" ":" NL bloque_ipam
               | "labels" ":" NL lista_pares
               | "driver_opts" ":" NL lista_pares

bloque_ipam: ("driver" ":" TEXTO NL)? "config" ":" NL lista_subredes

lista_subredes: elemento_subred+
elemento_subred: "-" "subnet" ":" IP_RANGO NL ("gateway" ":" IP_RANGO NL)?

lista_pares: par_clave_valor+
par_clave_valor: TEXTO ":" TEXTO NL

# Tokens terminales ultra-estrictos
BOOLEANO: "true" | "false"
IP_RANGO: /[0-9a-fA-F:\.]+(\/[0-9]+)?/

# Unificamos todo texto (claves, valores, paths, nombres) en una sola regla robusta
TEXTO: /"[^"]*"/ | /[a-zA-Z0-9_\-\.\/]+/

# Saltos de línea obligatorios
NL: /(\r?\n)+/

# Ignoramos estrictamente espacios y tabulaciones horizontales
%ignore /[ \t]+/
"""

parser = Lark(gramatica_docker, start='especificacion_red', parser='earley')

def main():
    if len(sys.argv) < 2:
        print("Uso: python parser_python.py <ruta_al_archivo.yml>")
        return

    archivo = sys.argv[1]
    try:
        with open(archivo, 'r') as f:
            texto_yaml = f.read() + "\n"
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {archivo}")
        return

    print(f"--- Evaluando {archivo} ---")

    try:
        arbol_ast = parser.parse(texto_yaml)
        print("=> AST: ¡Análisis en Python Exitoso!")
    except Exception as e:
        print("\n[!] Error Sintáctico detectado:")
        print(e)
        return

    iteraciones = 10000
    print(f"Iniciando bucle de estrés de {iteraciones} iteraciones...")
    
    tiempo_inicio = time.time()
    for _ in range(iteraciones):
        parser.parse(texto_yaml)
        
    tiempo_fin = time.time()
    tiempo_total_ms = (tiempo_fin - tiempo_inicio) * 1000

    print(f"--> Tiempo total de ejecución (Python): {tiempo_total_ms:.2f} ms\n")

if __name__ == '__main__':
    main()