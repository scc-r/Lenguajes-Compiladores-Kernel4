# Actividad 2.4: De la Expresión al Autómata (Caso Práctico: Ajedrez)

**Institución:** Universidad Nacional Experimental de Guayana (UNEG)  
**Materia:** Lenguajes y Compiladores  
**Profesor:** Ing. Félix Márquez  
**Estudiante:** Shirley Cedeño  

---

## 2.4.1 y 2.4.2 - Definición del Subconjunto PGN Simplificado

Para el desarrollo de este analizador léxico, se ha definido un subconjunto estricto de la notación PGN (Portable Game Notation) que evalúa exclusivamente los desplazamientos simples y las capturas de piezas y peones. Se han excluido deliberadamente eventos complejos como enroques, promociones y desambiguaciones de casillas, garantizando así un lenguaje regular puro (Tipo 3 en la Jerarquía de Chomsky) procesable sin necesidad de memoria de pila.

### Alfabeto Formal ($\Sigma$) y Clases de Caracteres
Para evitar la explosión combinatoria en las transiciones, el alfabeto se agrupa en las siguientes clases formales:
* **$P$ (Piezas Mayores):** `[K, Q, R, B, N]`
* **$C$ (Columnas):** `[a, b, c, d, e, f, g, h]`
* **$F$ (Filas):** `[1, 2, 3, 4, 5, 6, 7, 8]`
* **$X$ (Captura):** `[x]`
* **$J$ (Jaque):** `[+]`

### Estructuras Léxicas Válidas
1. **Movimiento Simple de Peón:** Columna + Fila (Ej: `e4`)
2. **Movimiento Simple de Pieza:** Pieza + Columna + Fila (Ej: `Nf3`)
3. **Captura con Pieza:** Pieza + `x` + Columna + Fila (Ej: `Bxc6`)
4. **Captura con Peón:** Columna Origen + `x` + Columna Destino + Fila Destino (Ej: `exd5`)

*Nota: Todos los movimientos definidos pueden finalizar de manera opcional con el estado terminal de jaque (`+`).*

---

## 2.4.3 - Diseño de la Expresión Regular (Regex)

La expresión regular que modela matemáticamente el subconjunto PGN descrito se define como:

`^([KQRBN]x?|[a-h]x)?[a-h][1-8]\+?$`

**Desglose Estructural:**
* `^` y `$`: Delimitadores estrictos de inicio y fin de cadena.
* `([KQRBN]x?|[a-h]x)?`: Grupo inicial (opcional). Evalúa una pieza mayor con posible captura, o un peón con captura obligatoria.
* `[a-h][1-8]`: Grupo de destino (obligatorio). Define la coordenada exacta en la matriz del tablero.
* `\+?`: Grupo terminal (opcional). Evalúa el símbolo literal de suma para el jaque.

---

## 2.4.4 - Autómata Finito Determinístico (AFD)

### Definición Formal (Quíntupla)
El AFD resultante se define matemáticamente mediante $M = (Q, \Sigma, \delta, q_0, F)$:
* **$Q$ (Estados):** $\{q_0, q_1, q_2, q_3, q_4, q_5, q_6, q_E\}$
* **$\Sigma$ (Alfabeto):** $\{P, C, F, X, J\}$
* **$q_0$ (Estado Inicial):** $q_0$
* **$F$ (Estados de Aceptación):** $\{q_5, q_6\}$

### Tabla de Transiciones ($\delta$)

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

> **Nota Técnica de Diseño:** Para preservar la legibilidad del diagrama de estados en este documento, el estado sumidero ($q_E$) y sus transiciones asociadas han sido omitidos gráficamente. Se asume de manera implícita que cualquier transición no definida explícitamente desde un estado dado conduce directamente a $q_E$, desencadenando el rechazo inmediato de la cadena por error léxico.
