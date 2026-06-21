 Actividad 2.3: Higiene y Optimización de Gramáticas
**Desarrollado por:** [Rayc Yanez]

1. Patologías de las Gramáticas Formales

En el diseño de compiladores, no basta con que una gramática genere matemáticamente un lenguaje válido. Si la gramática presenta patologías estructurales, los analizadores sintácticos (especialmente los *parsers* descendentes o Top-Down como LL(1)) fallarán al procesar el código, generando bucles infinitos o árboles sintácticos contradictorios. A continuación, se demuestran y optimizan tres casos prácticos.

1.1. Gramática Ambigua

Concepto Teórico: Una gramática se considera ambigua si existe al menos una cadena válida que puede ser generada mediante dos o más árboles de derivación distintos. Esto es un error crítico en ingeniería de software, ya que el compilador tendría múltiples interpretaciones semánticas para una misma línea de código.

Caso Práctico: Evaluación de expresiones aritméticas sin jerarquía de precedencia.
  Gramática Original:
  ```ebnf
  E -> E + E | E * E | id

Demostración de Ambigüedad (Cadena: id + id * id):
A continuación, se demuestra cómo el analizador puede construir dos árboles contradictorios para la misma cadena.

Árbol A: Evaluación incorrecta (Prioriza la suma)

graph TD
    E1((E)) --> E2((E))
    E1 --> Op1((*))
    E1 --> E3((E))
    
    E2 --> E4((E))
    E2 --> Op2((+))
    E2 --> E5((E))
    
    E4 --> id1(id)
    E5 --> id2(id)
    E3 --> id3(id)

Árbol B: Evaluación correcta (Prioriza la multiplicación)

graph TD
    E1((E)) --> E2((E))
    E1 --> Op1((+))
    E1 --> E3((E))
    
    E2 --> id1(id)
    
    E3 --> E4((E))
    E3 --> Op2((*))
    E3 --> E5((E))
    
    E4 --> id2(id)
    E5 --> id3(id)

1.2. Recursividad por la Izquierda
Concepto Teórico: Ocurre cuando un No Terminal (A) puede derivar en una regla que comienza con el mismo No Terminal (A -> Aα). Esta patología colapsa a los analizadores descendentes (Descenso Recursivo), ya que el autómata entra en un bucle infinito intentando expandir A sin llegar a consumir nunca un símbolo terminal de la entrada.

Caso Práctico: Una gramática clásica para sumar términos.

Gramática Patológica:

E -> E + T | T

Algoritmo de Eliminación:
Para una regla de la forma A -> Aα | β (donde β es la base no recursiva y α el sufijo recursivo):

El No Terminal A debe apuntar a la base β seguida de un nuevo No Terminal A'.

El nuevo No Terminal A' manejará el sufijo α seguido de sí mismo, incluyendo la transición vacía (ε) para cerrar el bucle.

Gramática Resultante Optimizada:

E  -> T E'
E' -> + T E' | ε

Conclusión: El lenguaje generado es matemáticamente idéntico, pero el compilador ahora consume obligatoriamente el terminal (T) antes de iterar, previniendo el desbordamiento de memoria (Stack Overflow).

1.3. Factorización por la Izquierda
Concepto Teórico: Esta anomalía se presenta cuando dos o más reglas de producción de un mismo No Terminal comparten un prefijo común idéntico (A -> αβ1 | αβ2). En un analizador predictivo LL(1), el compilador evalúa un solo token hacia adelante (Lookahead). Al ver el prefijo común, el compilador entra en un estado de "no determinismo", incapaz de decidir qué regla aplicar.

Caso Práctico (El problema del "Dangling Else"):
Sentencia condicional en lenguajes estructurados.

Gramática con No Determinismo:

S -> if E then S | if E then S else S | a

El prefijo común que bloquea al analizador es: if E then S.

Algoritmo de Optimización:

Se extrae el prefijo común (α = if E then S).

Se reescribe la producción para que genere el prefijo seguido de un nuevo No Terminal (S'), conservando las rutas independientes (a).

El nuevo No Terminal (S') alojará los sufijos sobrantes.

Gramática Resultante Factorizada:

S  -> if E then S S' | a
S' -> else S | ε

Conclusión: El analizador predictivo ahora procesa el bloque if con total seguridad. Solo al terminar, revisa el siguiente token: si encuentra un else, aplica la ruta de S'; si no, aplica el camino vacío (ε), resolviendo la ambigüedad estructural.


