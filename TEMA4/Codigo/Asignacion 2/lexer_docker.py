import re
import sys

# Definición de los tokens léxicos para Docker
tokens = [
    ('INSTRUCTION', r'\b(FROM|RUN|CMD|COPY|EXPOSE|WORKDIR|ENV)\b'),
    ('IMAGE_NAME', r'[a-zA-Z0-9_-]+:[a-zA-Z0-9_.-]+'),
    ('NUMBER', r'\d+'), 
    ('PATH', r'[\./]?[a-zA-Z0-9_/\.-]+'), 
    ('EQUALS', r'='),
    ('STRING', r'"[^"]*"'),
    ('COMMENT', r'#.*'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]

def lexer(input_text):
    # Compilar todas las expresiones regulares en un solo patrón usando grupos con nombre
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    
    line_num = 1
    line_start = 0
    
    # Escaneo del texto
    for mo in re.finditer(token_regex, input_text):
        kind = mo.lastgroup
        value = mo.group(kind)
        
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue # Ignorar espacios, tabulaciones y comentarios
        elif kind == 'MISMATCH':
            # Control de error léxico indicando línea exacta
            column = mo.start() - line_start
            raise RuntimeError(f"ERROR LÉXICO: '{value}' inesperado en la línea {line_num}, columna {column}")
        else:
            column = mo.start() - line_start
            yield kind, value, line_num, column

def cargar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

if __name__ == '__main__':
    # Permite pasar el archivo por consola o usa uno por defecto
    archivo_entrada = sys.argv[1] if len(sys.argv) > 1 else 'Dockerfile_test'
    
    texto = cargar_archivo(archivo_entrada)
    if texto is not None:
        print(f"--- Analizando archivo: {archivo_entrada} ---")
        try:
            for token in lexer(texto):
                print(token)
            print("--- Análisis completado con éxito ---")
        except RuntimeError as e:
            print(e)