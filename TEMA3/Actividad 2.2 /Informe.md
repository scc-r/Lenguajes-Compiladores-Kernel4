Aquí el enlace de drive con el archivo DOC: https://docs.google.com/document/d/1T_ez43Aa_JTb-0GcJqnrSvgMz0cv7i2O9M88y8HI35k/edit?usp=sharing

Sección 2.2.1: Derivación y Modelado (Caso Práctico: Dibujo con Genoma)
El presente documento detalla la resolución de la actividad 2.2.1, enfocada en el diseño de una Gramática Libre de Contexto (GLC) que modela herramientas de dibujo bidimensionales. Para evitar ambigüedades en la interpretación, se ha estructurado una traza de ejecución paso a paso (derivación por la izquierda) donde se especifica la regla de producción aplicada y la semántica geométrica exacta de la acción del "trazador" (análogo a un gráfico de tortuga).

1. Definición Formal de la Gramática
Toda gramática G se define matemáticamente como la cuádrupla G = (V, Σ, P, S). A continuación, se definen los parámetros adaptados a nuestro lenguaje de modelado:
Alfabeto de Símbolos Terminales (Σ): Los caracteres del genoma asignados a movimientos elementales. Σ = {a, c, g, t}.
a (Avanzar): Traza una línea recta de longitud K en la dirección actual.
c (Cruzar/Derecha): Rota el ángulo de dirección actual +90° (giro a la derecha).
g (Girar/Izquierda): Rota el ángulo de dirección actual -90° (giro a la izquierda).
t (Trasladar/Retornar): Retrocede una longitud K sobre la línea trazada previamente sin alterar el ángulo de dirección. Es una función de memoria de posición para bifurcaciones.
Conjunto de No Terminales (V): Las macro-instrucciones geométricas. V = {S, Cuadrado, Arbol, Cubo, Cruz, Escalera, L, D, I, R}.
Símbolo Inicial (S): Punto de entrada del analizador.
Conjunto de Producciones (P)
Producción
Regla
Descripción Lógica
P1
S → Cuadrado | Arbol | Cubo | Cruz | Escalera
Derivación principal de las 5 figuras exigidas.
P2
Cuadrado → L D L D L D L
Ciclo cerrado: Lado, giro 90°, repetido 4 veces.
P3
Arbol → L I L R D D L
Bifurcación: Tallo, rama izquierda, retroceso al centro, compensación de ángulo, rama derecha.
P4
Cubo → Cuadrado I L D L D L
Proyección 2D: Cara frontal, sesgo de profundidad y aristas laterales/superiores.
P5
Cruz → L R D L R D L R D L
Centro radial: Línea, retorno al origen, giro 90°, repetido 4 veces en bucle.
P6
Escalera → L D L I L D L I L
Patrón zig-zag: Avance intercalado con giros alternos derecha/izquierda.
P7 a P10
L → a | D → c | I → g | R → t
Resolución léxica de los símbolos No Terminales de acción a los Terminales.


2. Cuadros de Derivación Explicativa (Leftmost Derivation)
Se aplica el reemplazo estricto del símbolo No Terminal ubicado más a la izquierda en cada paso de computación. El símbolo ⇒ indica una derivación lógica hacia el siguiente estado.
Caso A: Cuadrado
Paso
Cadena Derivada
Producción
Acción Geométrica (Semántica)
1
S ⇒ Cuadrado
P1
Llamada a la función de la figura.
2
S ⇒ L D L D L D L
P2
Expansión de la plantilla sintáctica del polígono.
3
S ⇒ a D L D L D L
P7
Avanza: Dibuja el primer lado inferior (base).
4
S ⇒ a c L D L D L
P8
Gira Der: Se orienta hacia arriba.
5
S ⇒ a c a D L D L
P7
Avanza: Dibuja el lado vertical derecho.
6
S ⇒ a c a c L D L
P8
Gira Der: Se orienta hacia la izquierda.
7
S ⇒ a c a c a D L
P7
Avanza: Dibuja el lado superior (techo).
8
S ⇒ a c a c a c L
P8
Gira Der: Se orienta hacia abajo.
9
S ⇒ a c a c a c a
P7
Avanza: Dibuja el lado vertical izquierdo, cerrando el polígono.


Caso B: Árbol (Bifurcación)
Paso
Cadena Derivada
Producción
Acción Geométrica (Semántica)
1
S ⇒ Arbol
P1
Llamada a la función de la figura.
2
S ⇒ L I L R D D L
P3
Expansión de la plantilla sintáctica.
3
S ⇒ a I L R D D L
P7
Avanza: Dibuja el tronco principal.
4
S ⇒ a g L R D D L
P9
Gira Izq: Inclina el vector hacia la diagonal izquierda.
5
S ⇒ a g a R D D L
P7
Avanza: Dibuja la rama izquierda.
6
S ⇒ a g a t D D L
P10
Retorna: El puntero retrocede la distancia de la rama, ubicándose de nuevo en la punta del tronco, sin cambiar su ángulo (sigue mirando a la izq).
7
S ⇒ a g a t c D L
P8
Gira Der: Cancela la inclinación izquierda, mirando al frente.
8
S ⇒ a g a t c c L
P8
Gira Der: Inclina el vector hacia la diagonal derecha.
9
S ⇒ a g a t c c a
P7
Avanza: Dibuja la rama derecha, completando el árbol.


Caso C: Cubo (Perspectiva 2D)
Paso
Cadena Derivada
Producción
Acción Geométrica (Semántica)
1
S ⇒ Cubo
P1
Llamada a la función de la figura.
2
S ⇒ Cuadrado I L D L D L
P4
Expansión. Llama a un bloque complejo y luego proyecta la fuga visual.
3
S ⇒ a c a c a c a I L D L D L
P2, P7-8
Resolución Macro: Se ejecuta y dibuja la cara frontal completa (Caso A). El puntero queda en el vértice inicial mirando hacia abajo.
4
S ⇒ a c a c a c a g L D L D L
P9
Gira Izq: El puntero se orienta en diagonal (eje Z de fuga isométrico).
5
S ⇒ a c a c a c a g a D L D L
P7
Avanza: Traza la arista inferior de profundidad.
6
S ⇒ a c a c a c a g a c L D L
P8
Gira Der: El puntero se orienta hacia arriba.
7
S ⇒ a c a c a c a g a c a D L
P7
Avanza: Traza la arista vertical trasera (fondo de la cara lateral).
8
S ⇒ a c a c a c a g a c a c L
P8
Gira Der: El puntero se orienta hacia la derecha.
9
S ⇒ a c a c a c a g a c a c a
P7
Avanza: Traza la arista horizontal superior (fondo del techo), dando ilusión 3D.


Caso D: Cruz Simétrica Radial
Paso
Cadena Derivada
Producción
Acción Geométrica (Semántica)
1
S ⇒ Cruz
P1
Llamada a la función de la figura.
2
S ⇒ L R D L R D L R D L
P5
Expansión del patrón radial en cruz.
3
S ⇒ a R D L R D L R D L
P7
Avanza: Dibuja la línea superior (brazo Norte).
4
S ⇒ a t D L R D L R D L
P10
Retorna: Vuelve al origen (nodo central) deslizando sobre la línea trazada.
5
S ⇒ a t c L R D L R D L
P8
Gira Der: Desde el origen, rota 90° (mira al Este).
6
S ⇒ a t c a R D L R D L
P7
Avanza: Dibuja el brazo Este.
7 a 11
... ⇒ a t c a t c a R D L ...
P10, P8, P7
Se repite el retorno al centro, giro de 90° (mira al Sur) y trazo del brazo Sur.
Final
S ⇒ a t c a t c a t c a
P8, P7
Último retorno, giro (mira al Oeste) y traza el brazo final cerrando la simetría.


Caso E: Escalera (Zig-Zag)
Paso
Cadena Derivada
Producción
Acción Geométrica (Semántica)
1
S ⇒ Escalera
P1
Llamada a la función de la figura.
2
S ⇒ L D L I L D L I L
P6
Expansión del patrón alterno.
3
S ⇒ a D L I L D L I L
P7
Avanza: Traza la huella (base) del primer escalón.
4
S ⇒ a c L I L D L I L
P8
Gira Der: Se orienta hacia arriba.
5
S ⇒ a c a I L D L I L
P7
Avanza: Traza la contrahuella (altura) del escalón.
6
S ⇒ a c a g L D L I L
P9
Gira Izq: Se orienta nuevamente hacia el frente (restaura vector original).
7
S ⇒ a c a g a D L I L
P7
Avanza: Traza la huella del segundo escalón.
...
...
...
El patrón de giro derecha → izquierda mantiene el ascenso constante en el plano.
11
S ⇒ a c a g a c a g a
P7
Avanza: Traza el último peldaño, finalizando la iteración.



