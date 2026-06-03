# ⏱️ Actividad II: Estudio Morfológico, Sintáctico y Benchmarking
**Desarrollado por:** [Rayc Yanez]

## 1. Análisis Morfológico (Léxico) y Sintáctico

**Nota técnica preliminar:** La tokenización analizada en esta sección corresponde a la teoría de lenguajes formales (donde un analizador léxico o *scanner* agrupa secuencias de caracteres en *tokens* o unidades atómicas de significado para el compilador). Este proceso es estrictamente determinista y gramatical, difiriendo por completo de la tokenización probabilística o por sub-palabras empleada en el Procesamiento de Lenguaje Natural (PLN) para modelos de inteligencia artificial.

### 1.1. Zig
- **Análisis Morfológico:** Zig posee un analizador léxico estricto y minimalista. Sus **palabras reservadas** (como `fn`, `while`, `if`, `else`, `var`, `const`) están limitadas para evitar ambigüedades. Las **reglas de identificadores** exigen comenzar con una letra o guion bajo, seguido de caracteres alfanuméricos (`[a-zA-Z_][a-zA-Z0-9_]*`). Los **literales** numéricos soportan tipado fuerte implícito (ej. `0`, `1`) y los literales de cadena utilizan comillas dobles. Los elementos irrelevantes (espacios en blanco, tabulaciones y saltos de línea) son ignorados por el compilador, ya que Zig depende de **delimitadores explícitos**: utiliza llaves `{}` para definir bloques de alcance léxico (*scope*) y el punto y coma `;` para la terminación de sentencias.
- **Análisis Sintáctico:** A continuación, la notación formal (EBNF) de las estructuras de control empleadas:
  ```ebnf
  <Subprograma> ::= "fn" <Identificador> "(" [ <ListaParametros> ] ")" <TipoRetorno> "{" <BloqueInstrucciones> "}"
  <BucleWhile>  ::= "while" "(" <ExpresionBooleana> ")" "{" <BloqueInstrucciones> "}"
  <Condicional> ::= "if" "(" <ExpresionBooleana> ")" "{" <BloqueInstrucciones> "}" 
                    [ "else" "{" <BloqueInstrucciones> "}" ]
  ```

### 1.2. Python
- **Análisis Morfológico:** El escáner léxico de CPython tiene una característica arquitectónica única: **el espacio en blanco es sintácticamente significativo**. A diferencia de los otros lenguajes evaluados, Python no ignora la indentación; el analizador léxico inyecta *tokens* invisibles llamados `INDENT` y `DEDENT` para marcar el inicio y fin de los bloques, eliminando la necesidad de llaves. Sus **palabras reservadas** incluyen `def`, `while`, `if`, `else`. Los **literales** numéricos son tratados como objetos de precisión arbitraria por defecto. El delimitador explícito principal es los dos puntos `:` que anuncia la apertura de un nuevo bloque indentado.
- **Análisis Sintáctico:** Representación formal de sus estructuras, destacando la obligatoriedad de los tokens de indentación:
  ```ebnf
  <Subprograma> ::= "def" <Identificador> "(" [ <ListaParametros> ] "):" <NUEVA_LINEA> <INDENT> <BloqueInstrucciones> <DEDENT>
  <BucleWhile>  ::= "while" <ExpresionBooleana> ":" <NUEVA_LINEA> <INDENT> <BloqueInstrucciones> <DEDENT>
  <Condicional> ::= "if" <ExpresionBooleana> ":" <NUEVA_LINEA> <INDENT> <BloqueInstrucciones> <DEDENT> 
                    [ "else" ":" <NUEVA_LINEA> <INDENT> <BloqueInstrucciones> <DEDENT> ]
  ```

### 1.3. Rust
- **Análisis Morfológico:** El análisis léxico de Rust está diseñado para garantizar la seguridad de memoria desde la fase de compilación. Las **palabras reservadas** (`fn`, `while`, `if`, `let`, `mut`) definen rígidamente la inmutabilidad por defecto. Las **reglas de identificadores** siguen el estándar alfanumérico ASCII/Unicode. Los **literales** son estrictos e infieren el tipo si no se sufijan (ej. `i32`, `u64`). El tratamiento de elementos irrelevantes es tradicional: los espacios y saltos de línea se ignoran. Utiliza **delimitadores explícitos** (`{}` para bloques y `;` para sentencias). Una particularidad léxica es que el *scanner* no requiere (ni recomienda) paréntesis aislantes alrededor de las expresiones booleanas en sus estructuras de control.
- **Análisis Sintáctico:** Notación formal evidenciando la ausencia de paréntesis en las condiciones de evaluación:
  ```ebnf
  <Subprograma> ::= "fn" <Identificador> "(" [ <ListaParametros> ] ")" [ "->" <TipoRetorno> ] "{" <BloqueInstrucciones> "}"
  <BucleWhile>  ::= "while" <ExpresionBooleana> "{" <BloqueInstrucciones> "}"
  <Condicional> ::= "if" <ExpresionBooleana> "{" <BloqueInstrucciones> "}" 
                    [ "else" ( <Condicional> | "{" <BloqueInstrucciones> "}" ) ]
  ```

### 1.4. JavaScript
- **Análisis Morfológico:** El escáner del motor V8 (ECMAScript) es altamente permisivo. Sus **palabras reservadas** empleadas incluyen `function`, `while`, `if`, `let`, `const`. Las **reglas de identificadores** permiten caracteres estándar y símbolos especiales como `$` o `_`. Los **literales** numéricos, históricamente, se tokenizan siempre como flotantes de doble precisión (IEEE 754), a menos que se declare explícitamente el sufijo `n` para *BigInt*. Emplea **delimitadores explícitos** (`{}` para bloques). Una característica crítica de su analizador léxico es el mecanismo ASI (*Automatic Semicolon Insertion*), donde el compilador infiere e inyecta virtualmente el delimitador `;` al final de una línea si el programador lo omite, aunque el espacio en blanco en general sea ignorado.
- **Análisis Sintáctico:** Notación formal de la jerarquía de estructuras de control en su paradigma base:
  ```ebnf
  <Subprograma> ::= "function" <Identificador> "(" [ <ListaParametros> ] ")" "{" <BloqueInstrucciones> "}"
  <BucleWhile>  ::= "while" "(" <ExpresionBooleana> ")" "{" <BloqueInstrucciones> "}"
  <Condicional> ::= "if" "(" <ExpresionBooleana> ")" <InstruccionOBloque> 
                    [ "else" <InstruccionOBloque> ]
  ```
---

## 2. Benchmarking en Procesamiento Intensivo

**Algoritmo Seleccionado:** Conjetura de Collatz aplicando un límite estricto de estrés de **10,000,000 de iteraciones** consecutivas (evaluando los enteros en el rango de $1$ a $10^7$). Cada lenguaje calcula la longitud de la secuencia matemática para cada elemento y actualiza el registro de la longitud máxima encontrada de forma secuencial.
* **Resultado de control (Secuencia máxima validada):** `685` pasos (idéntico en los cuatro entornos, lo que valida la integridad matemática del escenario de pruebas).

**Entorno de Pruebas (Hardware/Software):**
* **Arquitectura del Sistema:** Computador portátil HP ProBook 450 G6
* **CPU:** Intel Core i5-8265U @ 1.60GHz (hasta 3.90 GHz con Turbo Boost, 4 núcleos / 8 hilos)
* **Memoria RAM:** 16GB DDR4 @ 2400 MHz
* **Sistema Operativo:** Windows 11 Pro (64 bits)
* **Metodología de Medición:** * *Métricas Internas:* Capturadas mediante APIs nativas de introspección de cada lenguaje (`time.perf_counter()` y `tracemalloc` en Python; `performance.now()` y `process.memoryUsage().heapUsed` en JavaScript/Node.js; `std.time.Instant` en Rust).
  * *Métricas Externas (OS):* Auditadas mediante un script de supervisión en `PowerShell` ejecutado de manera concurrente, capturando la propiedad de hardware `WorkingSet64` (RAM física asignada al proceso) con un intervalo de muestreo agresivo de 10 milisegundos y un cronómetro de precisión de la clase `System.Diagnostics.Stopwatch`.

---

### 2.1. Tabla de Tiempos y Memoria (Matriz Empírica)

| Lenguaje de Programación | Paradigma Dominante | Mecanismo de Ejecución y Compilación | Tiempo de Ejecución Interno (ms) | Tiempo de Ejecución Real OS (ms) | Consumo de Memoria Interno (Heap) | Consumo de Memoria Pico Real OS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zig** | Imperativo / Estructurado | Compilación Nativa (LLVM - O ReleaseFast) | *N/D* | 1,408.49 ms | 0.00 MB | 3.04 MB |
| **Rust** | Multiparadigma | Compilación Nativa (LLVM - O) | 1,472.96 ms | 1,491.01 ms | 0.00 MB | 4.31 MB |
| **JavaScript** | Multiparadigma | Compilación JIT / V8 Engine (Node.js) | 16,730.80 ms | 16,810.30 ms | 4.70 MB | 39.05 MB |
| **Python** | Multiparadigma | Interpretado Puro (CPython / VM) | 1,574,755.27 ms | 1,574,808.59 ms | 0.00 MB | 11.89 MB |

*(Nota: N/D indica que el lenguaje se ejecuta nativamente sobre el hardware y el binario no inyecta telemetría interna por diseño para evitar sobrecostos de procesamiento).*

---

### 2.2. Gráfica de Rendimiento
*(Insertar aquí la imagen de la gráfica comparativa generada a partir de los datos de la tabla, tal como lo sugiere el profesor)*.

### 2.3. Análisis Técnico y Discusión de Resultados

El estudio empírico revela un comportamiento asimétrico altamente dependiente de la arquitectura interna de los lenguajes evaluados, evidenciando cómo la gestión de memoria y el mecanismo de ejecución dictan el rendimiento final.

#### 1. El Impacto de la Compilación Nativa (Zig y Rust)
Zig y Rust exhiben una eficiencia superior con tiempos de ejecución inferiores a los 1.5 segundos. Ambos lenguajes emplean **LLVM** como infraestructura de compilación (*backend*). Al procesar un bucle matemático puro e iterativo, el optimizador de LLVM traduce las estructuras de control directamente a instrucciones vectorizadas u optimizadas a nivel de registro de CPU en lenguaje ensamblador x86_64. 

Respecto a la memoria, ambos registran **0.00 MB de uso en el Heap interno** debido a que la complejidad espacial del algoritmo es constante; las variables numéricas mutan dentro de registros de la CPU o en la pila (*Stack*). Sin embargo, al auditar el proceso desde el sistema operativo, Windows asigna **3.04 MB a Zig** y **4.31 MB a Rust**. Este diferencial externo representa el *Working Set* mínimo obligatorio para cargar la imagen binaria en memoria física e inicializar las librerías base. Rust resulta ligeramente más pesado debido a la inclusión nativa de metadatos de seguridad y prevención de pánicos (*panic handlers*).

#### 2. La Arquitectura de Memoria en Entornos Gestionados: JavaScript vs. Python
El análisis de los lenguajes interpretados desvela el enorme impacto del entorno de ejecución sobre los recursos del sistema, posicionando a JavaScript (Node.js) como un entorno significativamente más pesado que Python (CPython) en ambas capas de medición, aunque con resultados diametralmente opuestos en rendimiento:

* **JavaScript (Node.js / Motor V8):** Internamente declara un consumo en el Heap de **4.70 MB**, pero externamente el sistema operativo registra un pico masivo de **39.05 MB** (el más alto de toda la prueba). Esta diferencia abismal obedece a la naturaleza de su motor de compilación **Just-In-Time (JIT)**. Al detectar que el bucle se ejecuta millones de veces (*hot code*), el optimizador de V8 entra en funcionamiento concurrente, consumiendo agresivamente la memoria RAM de Windows para almacenar el código máquina compilado al vuelo. Los 4.70 MB corresponden a las estructuras de datos internas, mientras que los ~34 MB de sobrecosto representan la infraestructura completa de V8 encendida. Gracias a este inmenso sacrificio espacial, JS logra resolver la prueba en apenas ~16.8 segundos.

* **Python (CPython):** Registra un consumo interno perfecto de **0.00 MB** en el Heap, y un peso externo estable de **11.89 MB**. A diferencia de JS, CPython es un intérprete puro sin optimización JIT por defecto. La asignación interna nula se debe a su eficiente motor basado en **Conteo de Referencias (*Reference Counting*)**; al actualizar la variable de cálculo, el intérprete destruye el objeto numérico anterior en microsegundos, manteniendo un perfil dinámico plano. Externamente, cargar el entorno base (`python.exe`) le cuesta a Windows casi 12 MB. Al carecer de compilación al vuelo, este entorno evalúa cada línea secuencialmente, lo que explica por qué, aun siendo mucho más ligero en RAM que JavaScript, penaliza el tiempo de ejecución degradándolo a 26.24 minutos.

#### 3. Conclusión Arquitectónica
Los datos empíricos demuestran que los entornos gestionados introducen un sobrecosto de recursos vinculado a la supervivencia del propio entorno. Para cargas de procesamiento matemático masivo, el compilador JIT de JavaScript intercambia un altísimo consumo de RAM por velocidad, mientras que la abstracción pura de Python conserva mejor la memoria pero se traduce en una penalización de rendimiento de casi **1,100 veces en tiempo** en comparación con soluciones compiladas nativamente como Zig y Rust.
