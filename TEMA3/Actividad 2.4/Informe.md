# Actividad 2.4: De la Expresión al Autómata (Caso Práctico: Ajedrez)

**Institución:** Universidad Nacional Experimental de Guayana (UNEG)  
**Materia:** Lenguajes y Compiladores  
**Profesor:** Ing. Félix Márquez  
**Estudiante:** Shirley Cedeño  

---

### Introducción y Contextualización Teórica

El estudio de los lenguajes formales y las gramáticas en este Tema 3 nos proporciona las herramientas matemáticas para entender cómo las computadoras procesan secuencias de símbolos con total certeza. Para materializar estos conceptos abstractos (alfabetos, palabras y reglas sintácticas), esta actividad propone la construcción de un analizador desde sus bases fundamentales mediante la dualidad técnica de la **Expresión Regular** y el **Autómata Finito**.

A nivel conceptual, estos dos términos representan las dos caras de la misma moneda en los lenguajes regulares (Tipo 3 de la Jerarquía de Chomsky):
* **La Expresión Regular** funciona como la definición descriptiva y algebraica del lenguaje; establece formalmente *qué* cadenas de texto pertenecen al sistema válido.
* **El Autómata Finito** es la contraparte operativa y algorítmica; representa la máquina abstracta ideal para leer caracteres en tiempo lineal y evaluar, paso a paso, si se cumplen las condiciones dictadas por la expresión.

El ajedrez se presenta como un escenario idóneo para aplicar esta teoría. Lejos de ser un juego caótico, el ajedrez se rige por un sistema estrictamente estructurado donde cada jugada representa una instrucción precisa. Para registrar estas partidas de forma universal, la comunidad informática y de ajedrez estandarizó la notación **PGN (Portable Game Notation)**, la cual convierte las acciones del tablero en un lenguaje de texto con su propio alfabeto y morfología.

Sin embargo, para los objetivos de un analizador léxico puro, procesar la totalidad del PGN real implicaría una complejidad excesiva. El PGN completo incluye metadatos, comentarios anidados en paréntesis, variantes históricas y desambiguaciones que requieren memoria contextual, lo que desplazaría el problema hacia gramáticas más complejas (Tipo 2 o Tipo 1). Por lo tanto, para mantener el sistema dentro de las fronteras de un **Lenguaje Regular puro**, procesable por un escáner de memoria limitada y alta eficiencia, es metodológicamente necesario diseñar un **subconjunto PGN simplificado**. Este enfoque aísla la esencia morfológica de los movimientos y capturas básicos, permitiendo demostrar con rigor científico cómo se transita con éxito desde la abstracción de una expresión regular hasta la implementación física de un autómata en código.

---

## 2.4.1 y 2.4.2 - Definición del Subconjunto PGN Simplificado

A partir del marco conceptual establecido, se delimitan las reglas formales del lenguaje regular específico que procesará nuestro sistema, reduciendo el espectro del PGN a sus componentes morfológicos atómicos.

### Alfabeto Formal ($\Sigma$) y Clases de Caracteres
En la teoría de lenguajes, un alfabeto es un conjunto finito de símbolos. Sin embargo, modelar una transición matemática individual para cada pieza o columna resultaría en una explosión combinatoria inmanejable. Para simplificar nuestro modelo, el alfabeto original se ha optimizado agrupándolo en Clases de Caracteres, uniendo bajo una misma etiqueta los símbolos que comparten el mismo comportamiento morfológico:

* **$P$ (Piezas Mayores):** `[K, Q, R, B, N]`
* **$C$ (Columnas):** `[a, b, c, d, e, f, g, h]`
* **$F$ (Filas):** `[1, 2, 3, 4, 5, 6, 7, 8]`
* **$X$ (Captura):** `[x]`
* **$J$ (Jaque):** `[+]`

### Estructuras Léxicas Válidas
Basados en el alfabeto definido, las "palabras" aceptadas por nuestro lenguaje regular siguen cuatro estructuras base (con la adición opcional del estado terminal de jaque `+`):
1. **Movimiento Simple de Peón:** Columna + Fila (Ej: `e4`)
2. **Movimiento Simple de Pieza:** Pieza + Columna + Fila (Ej: `Nf3`)
3. **Captura con Pieza:** Pieza + `x` + Columna + Fila (Ej: `Bxc6`)
4. **Captura con Peón:** Columna Origen + `x` + Columna Destino + Fila Destino (Ej: `exd5`)

---

## 2.4.3 - Proceso de Diseño de la Expresión Regular (Regex)

En la teoría de lenguajes, una Expresión Regular es una notación algebraica y declarativa que define exactamente qué cadenas pertenecen a un Lenguaje Regular (Tipo 3). No es una fórmula arbitraria, sino el resultado de un proceso de síntesis lógica.

Para diseñar nuestra Regex, no partimos de la fórmula final, sino que deconstruimos los casos de uso definidos en el subconjunto PGN mediante un enfoque "Bottom-Up" (de abajo hacia arriba):

**Paso 1: El núcleo obligatorio (Destino)**
Todo movimiento de ajedrez, sin importar qué pieza se mueva o si hay captura, tiene un denominador común irrefutable: siempre debe indicar la casilla de destino. Por lo tanto, nuestro núcleo sintáctico es la concatenación de una columna y una fila:
* Fragmento base: `[a-h][1-8]`

**Paso 2: El prefijo de la pieza y la captura (Origen)**
A la izquierda de la casilla de destino, el lenguaje presenta variaciones morfológicas que debemos agrupar en una disyunción lógica (operador `|`):
* Si es una pieza mayor, inicia con su letra identificadora, seguida de una captura opcional: `[KQRBN]x?`
* Si es un peón que captura, inicia obligatoriamente con su columna de origen seguida de la 'x': `[a-h]x`
* Si es un peón avanzando, no hay prefijo (es vacío).
* Agrupamos estas posibilidades en un bloque opcional: `([KQRBN]x?|[a-h]x)?`

**Paso 3: El sufijo terminal (Jaque)**
Cualquier movimiento legal puede, de forma circunstancial, resultar en un jaque al rey oponente. Al ser opcional, añadimos el símbolo literal de suma al final con el cuantificador de cero o una ocurrencia:
* Fragmento final: `\+?`

**Paso 4: Delimitación estricta de la cadena**
Para que nuestro analizador léxico no acepte "basura" antes o después de la jugada (por ejemplo, rechazar `xxNf3yy`), anclamos la expresión al inicio (`^`) y al final (`$`) de la lectura del token.

**Resultado: La Expresión Regular Definitiva**
Al concatenar los pasos lógicos anteriores, obtenemos la representación matemática exacta de nuestro subconjunto PGN:
`^([KQRBN]x?|[a-h]x)?[a-h][1-8]\+?$`

---

## 2.4.4 - Diseño y Profundización del Autómata Finito Determinístico (AFD)

### ¿Qué es y para qué sirve en la fase de Compilación?
Mientras que la Expresión Regular es una declaración estática de nuestro lenguaje, el Autómata Finito Determinístico (AFD) es el modelo dinámico y algorítmico que permite ejecutarla. En el diseño de compiladores, el AFD actúa como el "motor" del Analizador Léxico (Escáner). 

Su propósito fundamental es leer el código fuente (en nuestro caso, el movimiento de ajedrez) carácter por carácter, transitando entre "estados" lógicos. Su mayor virtud arquitectónica es su **complejidad temporal lineal $O(n)$**: al ser *determinístico*, por cada carácter que lee, la máquina sabe exactamente a qué único estado debe ir. No existe ambigüedad, no requiere una memoria de pila (stack) y jamás necesita retroceder (backtracking) para reevaluar la cadena.

### Metodología de Diseño del Grafo
El diseño de nuestro AFD se construyó mapeando el flujo secuencial de la Expresión Regular hacia un grafo dirigido:
1. **Estado Inicial ($q_0$):** Representa el sistema esperando el primer carácter. Desde aquí se abren dos caminos lógicos: leer una pieza mayor ($P$) que nos lleva a $q_1$, o leer una columna minúscula ($C$) que nos lleva a $q_2$.
2. **Nodos de Tránsito ($q_1, q_2, q_3, q_4$):** Estos estados representan lecturas incompletas. Por ejemplo, en $q_3$ el escáner acaba de leer el símbolo de captura 'x', por lo que "sabe" que el siguiente carácter exigido por la gramática debe ser obligatoriamente una columna ($C$).
3. **Estados de Aceptación ($q_5, q_6$):** Si la lectura de la cadena finaliza estando el autómata en uno de estos estados, el escáner léxico aprueba el token y se lo envía al analizador sintáctico/semántico. El estado $q_5$ representa un movimiento legal limpio, y $q_6$ representa un movimiento legal con jaque.
4. **El Estado Sumidero ($q_E$):** Es el mecanismo de defensa del autómata. Si en cualquier estado se recibe un carácter inesperado (por ejemplo, leer dos 'x' seguidas), el sistema transita a $q_E$, un estado sin salida que garantiza el rechazo del código por "Error Léxico".

### Definición Formal (Quíntupla)
El AFD estructurado se define matemáticamente mediante $M = (Q, \Sigma, \delta, q_0, F)$:
* **$Q$ (Estados):** $\{q_0, q_1, q_2, q_3, q_4, q_5, q_6, q_E\}$
* **$\Sigma$ (Alfabeto de Clases):** $\{P, C, F, X, J\}$
* **$q_0$ (Estado Inicial):** $q_0$
* **$F$ (Estados de Aceptación):** $\{q_5, q_6\}$

### Función y Tabla de Transiciones ($\delta$)
La siguiente matriz documenta el comportamiento determinístico del sistema. Si una celda indica $q_E$, significa que esa transición específica rompe las reglas sintácticas del PGN.

| Estado Actual | Lee $P$ (Pieza) | Lee $C$ (Columna) | Lee $F$ (Fila) | Lee $X$ (Captura) | Lee $J$ (Jaque) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $\rightarrow q_0$ | $q_1$ | $q_2$ | $q_E$ | $q_E$ | $q_E$ |
| $q_1$ | $q_E$ | $q_4$ | $q_E$ | $q_3$ | $q_E$ |
| $q_2$ | $q_E$ | $q_E$ | $q_5$ | $q_3$ | $q_E$ |
| $q_3$ | $q_E$ | $q_4$ | $q_E$ | $q_E$ | $q_E$ |
| $q_4$ | $q_E$ | $q_E$ | $q_5$ | $q_E$ | $q_E$ |
| $* q_5$ | $q_E$ | $q_E$ | $q_E$ | $q_E$ | $q_6$ |
| $* q_6$ | $q_E$ | $q_E$ | $q_E$ | $q_E$ | $q_E$ |
| $q_E$ (Sumidero) | $q_E$ | $q_E$ | $q_E$ | $q_E$ | $q_E$ |

### Diagrama de Estados
![Diagrama AFD Ajedrez](./diagrama_afd_ajedrez.png)

> **Nota Técnica sobre el Diagrama:** Para preservar la legibilidad gráfica del autómata, el estado sumidero ($q_E$) y sus aristas han sido omitidos del esquema. Se asume que cualquier arista faltante en un nodo conduce irrevocablemente al sumidero de error.
