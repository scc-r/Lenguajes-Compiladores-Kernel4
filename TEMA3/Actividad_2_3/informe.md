# Actividad 2.3: Higiene y Optimización de Gramáticas
**Desarrollado por:** [Rayc Yanez]

## 1. Patologías de las Gramáticas Formales

En el diseño de compiladores, la calidad de una gramática formal no se limita a su capacidad matemática para generar cadenas. Si la estructura posee malformaciones, los analizadores sintácticos predictivos y descendentes colapsarán, generando bucles infinitos o interpretaciones de código inconsistentes. A continuación, se diagnostican y sanean tres casos prácticos fundamentales.

### 1.1. Gramática Ambigua

**Concepto Teórico:** Una gramática es ambigua si existe al menos una cadena en su lenguaje que posee dos o más árboles de derivación independientes. En ingeniería de compiladores, la ambigüedad es una patología crítica: si el *parser* puede estructurar el código de dos formas distintas, el backend generará código de máquina impredecible, rompiendo la certeza del lenguaje.

**Caso Práctico:** Expresiones aritméticas sin jerarquía de precedencia ni asociatividad explícita.
* **Alfabeto ($\Sigma$):** `{ id, +, * }`
* **Variables No Terminales ($V$):** `{ E }`
* **Reglas de Producción ($P$):** ```ebnf
  E -> E + E | E * E | id
Demostración de la Ambigüedad (Cadena de estrés: id + id * id):
A continuación, se demuestra el fallo estructural modelando las dos interpretaciones jerárquicas totalmente divergentes que el compilador puede construir ante la misma entrada:

Árbol de Derivación A: Prioridad de la Multiplicación (Suma en la Raíz)
En esta estructura jerárquica, la suma se ubica en el nodo raíz del árbol, lo que obliga al compilador a evaluar primero los niveles inferiores. Semánticamente, esto equivale a interpretar la instrucción como id + (id * id).


    E1((E)) --- E2((E))
    E1 --- Op1(("+"))
    E1 --- E3((E))
    
    E2 --- id1("[id]")
    
    E3 --- E4((E))
    E3 --- Op2(("*"))
    E3 --- E5((E))
    
    E4 --- id2("[id]")
    E5 --- id3("[id]")
    
    style E1 fill:#1e3a8a,stroke:#000,color:#fff
    style E3 fill:#3b82f6,stroke:#000,color:#fff

    
Árbol de Derivación B: Prioridad de la Suma (Multiplicación en la Raíz)
Debido a la patología de la gramática, el parser puede tomar una ruta de derivación sintáctica alterna, posicionando la multiplicación en el nodo raíz. Esto altera por completo la jerarquía, forzando la evaluación anticipada de la suma, lo que equivale semánticamente a la expresión errónea (id + id) * id.

Code snippet
graph TD
    E1((E)) --- E2((E))
    E1 --- Op1(("*"))
    E1 --- E3((E))
    
    E2 --- E4((E))
    E2 --- Op2(("+"))
    E2 --> E5((E))
    
    E4 --- id1("[id]")
    E5 --- id2("[id]")
    
    E3 --- id3("[id]")
    
    style E1 fill:#1e3a8a,stroke:#000,color:#fff
    style E2 fill:#ef4444,stroke:#000,color:#fff
    
Conclusión del Análisis: La existencia demostrada de estos dos árboles estructurales para una misma palabra confirma la invalidez técnica de la gramática original para un compilador determinista, haciendo obligatoria su reescritura mediante la introducción de nuevos No Terminales que fijen la precedencia.

1.2. Recursividad por la Izquierda
Concepto Teórico: Ocurre cuando una regla de producción permite que un No Terminal se invoque a sí mismo como el primer elemento de su expansión (A -> Aα). Esta malformación introduce un bucle infinito en los analizadores de descenso recursivo, provocando un desbordamiento de la pila (Stack Overflow) al intentar expandir la variable antes de consumir cualquier terminal de entrada.

Caso Práctico: Regla de acumulación sintáctica de términos.

Gramática Patológica:

    E -> E + T | T

Algoritmo de Saneamiento:
Para eliminar la recursividad inmediata de la forma A -> Aα | β:

El No Terminal A debe derivar en la base no recursiva β seguida de una nueva variable de control A'.

El nuevo No Terminal A' hereda el sufijo recursivo α seguido de sí mismo, cerrando el flujo con la transición vacía o Épsilon (ε).

Gramática Resultante Optimizada:


    E  -> T E'
    E' -> + T E' | ε
    
1.3. Factorización por la Izquierda
Concepto Teórico: Esta anomalía se presenta cuando un No Terminal tiene múltiples producciones que comparten el mismo prefijo común (A -> αβ1 | αβ2). Al leer la entrada, un analizador sintáctico predictivo con un solo token de anticipación (Lookahead LL(1)) colisionará en un estado de no determinismo al no poder decidir cuál ruta expandir.

Caso Práctico: El dilema del Dangling Else en condicionales anidados.

Gramática con No Determinismo:

    S -> if E then S | if E then S else S | a
    
El factor común que bloquea la decisión del parser es el prefijo if E then S.

Algoritmo de Optimización:

Se extrae el factor común más largo (α = if E then S).

Se reescribe la producción raíz para generar dicho factor acompañado de un nuevo No Terminal diferido (S'), manteniendo las producciones independientes (a).

El No Terminal secundario resolverá los sufijos restantes, incluyendo la opción vacía (ε).

Gramática Resultante Factorizada:

    S  -> if E then S S' | a
    S' -> else S | ε

### 💡 Actualización para tu Defensa en Video (Fase II):
Al momento de grabar tu exposición frente a la cámara y compartir la pantalla de tu repositorio de GitHub, debes señalar específicamente los diagramas renderizados usando esta argumentación técnica:

> *"Como pueden observar en la pantalla de nuestro repositorio, en la sección 1.1 demuestro visualmente la patología de la ambigüedad gramatical utilizando dos árboles de derivación jerárquica para la misma cadena exacta: `id + id * id`. El problema de diseño radica en que, al carecer de reglas de precedencia, el compilador puede generar el Árbol A, donde la suma queda abajo y la multiplicación se evalúa primero, o el Árbol B, donde la multiplicación queda en la raíz y la suma se evalúa antes. En ingeniería de compiladores, esto representa un fallo catastrófico, ya que el comportamiento semántico del software pasa a ser completamente ambiguo e impredecible en tiempo de ejecución."*
