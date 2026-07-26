import sys
import re
import json
from google import genai
from google.genai import types

# ==========================================
# 1. CONFIGURACIÓN DEL LLM ACTUALIZADO
# ==========================================
# El nuevo SDK inicializa el cliente directamente
client = genai.Client(api_key="INGRESA_TU_API_KEY_AQUI")  # <--- Reemplaza con tu API Key real

class AsistenteIA:
    def __init__(self):
        self.sugerencias = []
        self.palabras_clave = ['print', 'if', 'else', 'true', 'false']
        self.modelo = 'gemini-3.1-flash-lite'

    def evaluar_confianza_lexica(self, lexema):
        if lexema in self.palabras_clave or not client:
            return lexema

        # NUEVO PROMPT: Texto plano estricto separado por comas (CSV style), cero JSON.
        prompt = f"""
        Eres el analizador léxico de un compilador de UnegScript. 
        El usuario escribió el identificador '{lexema}'. 
        ¿Es un error tipográfico de una de estas palabras clave: {self.palabras_clave}?
        Evalúa la confianza (0.0 a 1.0) de que sea un error tipográfico.
        Responde ÚNICAMENTE con texto plano en este formato exacto: PALABRA,CONFIANZA
        Ejemplo si crees que es un error tipográfico: print,0.95
        Ejemplo si crees que es una variable intencional: {lexema},0.0
        No agregues saludos, ni explicaciones, ni comillas.
        """
        try:
            # Eliminamos la exigencia de application/json, dejamos que responda texto libre
            response = client.models.generate_content(model=self.modelo, contents=prompt)
            
            # Limpiamos la respuesta y la separamos por la coma
            resultado = response.text.strip()
            partes = resultado.split(',')
            
            correccion = partes[0].strip()
            confianza = float(partes[1].strip())

            if confianza >= 0.8 and correccion in self.palabras_clave:
                self.sugerencias.append(f"Sugerencia: '{lexema}' → '{correccion}' (Confianza IA: {confianza})")
                return correccion
            return lexema
        except Exception as e:
            print(f"\n[!] Error de API en Lexer: {e}") # <--- Ahora veremos por qué falla
            return lexema

    def asistir_error_sintactico(self, esperado, encontrado, contexto):
        if not client: return
        
        # Freno de mano: si ya tenemos 2 sugerencias de estructura, no gastamos más cuota
        if len(self.sugerencias) >= 2:
            self.sugerencias.append(f"Sugerencia (Parser local): Revisa el token '{encontrado}' cerca de '{contexto}'")
            return
            
        prompt = f"""
        Eres el parser de un compilador. Error sintáctico: se esperaba '{esperado}' pero se encontró '{encontrado}'.
        Contexto cercano: "{contexto}".
        Genera una sugerencia de reparación técnica en una sola línea. No uses formato markdown.
        """
        try:
            response = client.models.generate_content(model=self.modelo, contents=prompt)
            self.sugerencias.append(f"Sugerencia IA (Parser): {response.text.strip()}")
        except Exception as e:
            self.sugerencias.append(f"Sugerencia IA (Parser): Error cerca de '{encontrado}'.")

# ==========================================
# 2. LEXER TRADICIONAL (Autómata Finito)
# ==========================================
class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    def __repr__(self):
        return f"<{self.tipo}: {self.valor}>"

class LexerHibrido:
    def __init__(self, codigo, ia):
        self.codigo = codigo
        self.pos = 0
        self.ia = ia
        self.tokens = []
        
        self.reglas = [
            ('NUMERO', r'\d+'),
            ('CADENA', r'"[^"]*"'),
            ('IGUAL', r'='),
            ('MAYOR', r'>'),
            ('MENOR', r'<'),
            ('PUNTO_COMA', r';'),
            ('PAR_IZQ', r'\('),
            ('PAR_DER', r'\)'),
            ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),
            ('ESPACIO', r'[ \t\n\r]+'),
        ]

    def tokenizar(self):
        while self.pos < len(self.codigo):
            match = None
            for tipo, regex in self.reglas:
                patron = re.compile(regex)
                match = patron.match(self.codigo, self.pos)
                if match:
                    valor = match.group(0)
                    self.pos = match.end()
                    
                    if tipo != 'ESPACIO':
                        if tipo == 'IDENTIFICADOR':
                            valor_corregido = self.ia.evaluar_confianza_lexica(valor)
                            if valor_corregido in self.ia.palabras_clave:
                                tipo = 'KEYWORD'
                                valor = valor_corregido
                        self.tokens.append(Token(tipo, valor))
                    break
            if not match:
                raise SyntaxError(f"Lexer: Carácter ilegal en la posición {self.pos}")
        
        self.tokens.append(Token('EOF', ''))
        return self.tokens

# ==========================================
# 3. PARSER RECURSIVO DESCENDENTE (Lookahead)
# ==========================================
class ParserHibrido:
    def __init__(self, tokens, ia):
        self.tokens = tokens
        self.pos = 0
        self.ia = ia
        self.token_actual = self.tokens[self.pos]

    def avanzar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_actual = self.tokens[self.pos]

    def coincidir(self, tipo_esperado, valor_esperado=None):
        if self.token_actual.tipo == tipo_esperado and (valor_esperado is None or self.token_actual.valor == valor_esperado):
            self.avanzar()
        else:
            ctx = " ".join([t.valor for t in self.tokens[max(0, self.pos-2):min(len(self.tokens), self.pos+2)]])
            self.ia.asistir_error_sintactico(valor_esperado or tipo_esperado, self.token_actual.valor, ctx)
            self.avanzar()

    def parse_programa(self):
        instrucciones = []
        while self.token_actual.tipo != 'EOF':
            nodo = self.parse_instruccion()
            if nodo: instrucciones.append(nodo)
        return {"AST_UnegScript": instrucciones}

    def parse_instruccion(self):
        if self.token_actual.tipo == 'KEYWORD':
            if self.token_actual.valor == 'print':
                return self.parse_print()
            elif self.token_actual.valor == 'if':
                return self.parse_if()
        elif self.token_actual.tipo == 'IDENTIFICADOR':
            return self.parse_asignacion()
        
        token_erroneo = self.token_actual
        self.avanzar()
        return {"Error_Sintaxis": f"Token inesperado estructural: {token_erroneo.valor}"}

    def parse_asignacion(self):
        variable = self.token_actual.valor
        self.coincidir('IDENTIFICADOR')
        self.coincidir('IGUAL')
        valor = self.token_actual.valor
        self.coincidir('NUMERO')
        if self.token_actual.tipo == 'PUNTO_COMA':
            self.coincidir('PUNTO_COMA')
        return {"Asignacion": {"variable": variable, "valor": valor}}

    def parse_print(self):
        self.coincidir('KEYWORD', 'print')
        usa_parentesis = (self.token_actual.tipo == 'PAR_IZQ')
        if usa_parentesis:
            self.coincidir('PAR_IZQ')
            
        contenido = self.token_actual.valor
        self.avanzar()
        
        if usa_parentesis:
            self.coincidir('PAR_DER')
            
        # Recuperación Sintáctica Avanzada: si el usuario mezcló print con asignación erróneamente
        if self.token_actual.tipo == 'IGUAL':
            ctx = f"print {contenido} ="
            self.ia.asistir_error_sintactico("PUNTO_COMA o fin de linea", "=", ctx)
            # Consumimos el '=' y el número siguiente para limpiar el flujo y evitar nodos huérfanos
            self.coincidir('IGUAL')
            self.avanzar() 
            if self.token_actual.tipo == 'PUNTO_COMA': self.coincidir('PUNTO_COMA')
            
        return {"Print": contenido}

    def parse_if(self):
        self.coincidir('KEYWORD', 'if')
        var = self.token_actual.valor
        self.coincidir('IDENTIFICADOR')
        operador = self.token_actual.valor
        self.avanzar()
        limite = self.token_actual.valor
        self.coincidir('NUMERO')
        
        bloque_true = self.parse_instruccion()
        bloque_false = None
        
        if self.token_actual.tipo == 'KEYWORD' and self.token_actual.valor == 'else':
            self.coincidir('KEYWORD', 'else')
            bloque_false = self.parse_instruccion()
            
        return {
            "Condicional": {
                "Condicion": f"{var} {operador} {limite}",
                "Bloque_True": bloque_true,
                "Bloque_False": bloque_false
            }
        }

# ==========================================
# 4. PUNTO DE ENTRADA
# ==========================================
def main():
    if len(sys.argv) < 2:
        print("Uso correcto: python asistente.py <archivo.uneg>")
        return

    archivo = sys.argv[1]
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo_fuente = f.read()
    except FileNotFoundError:
        print(f"[!] Error: No se pudo encontrar el archivo '{archivo}'")
        return

    print(f"--- Procesando archivo: {archivo} ---")
    print(f"Código original: {codigo_fuente.strip()}\n")
    print("[*] Conectando con la API de Google (Generative AI)...")
    
    ia_hibrida = AsistenteIA()
    
    lexer = LexerHibrido(codigo_fuente, ia_hibrida)
    tokens = lexer.tokenizar()
    
    parser = ParserHibrido(tokens, ia_hibrida)
    ast = parser.parse_programa()

    print("\n[✓] TOKENS CORREGIDOS (Token Stream):")
    for t in tokens:
        if t.tipo != 'EOF':
            print(f"  {t}")

    print("\n[✓] ÁRBOL DE SINTAXIS ABSTRACTA (AST JSON):")
    print(json.dumps(ast, indent=2, ensure_ascii=False))

    print("\n[✓] REPORTE DE IA (Fallbacks Aplicados):")
    for sug in ia_hibrida.sugerencias:
        print(f"  - {sug}")

if __name__ == "__main__":
    main()