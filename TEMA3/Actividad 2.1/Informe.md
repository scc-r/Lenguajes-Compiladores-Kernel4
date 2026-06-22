
Universidad Nacional Experimental de Guayana
Materia: Lenguajes y Compiladores
Profesor: Ing. Félix Márquez
Estudiante: Angel Rodriguez

# 2.2.1.- Relación Gramática-Lenguaje: Concepto, Ejemplo y Mecanismo

## El Concepto de la Relación
En las ciencias de la computación, un alfabeto ($\Sigma$) es un conjunto finito de símbolos, y una palabra o cadena es una secuencia finita de estos. Un lenguaje formal ($L$) es el conjunto matemático de todas las cadenas válidas bajo ciertas reglas.  

La gramática formal ($G$), por su parte, es el motor generador o el "manual de instrucciones". No es el lenguaje en sí, sino el mecanismo finito que define cómo construir un conjunto potencialmente infinito de cadenas válidas. Decimos que una gramática $G$ define a un lenguaje $L$ (denotado como $L(G)$) si y solo si el lenguaje está compuesto exactamente por todas las cadenas de terminales que la gramática puede generar. 

## Mecanismo de Generación: La Derivación 

Formalmente, una gramática se define por una cuádrupla $G = (V_N, V_T, P, S)$, donde:

* $V_N$: Conjunto de variables o símbolos No Terminales (estructuras sintácticas intermedias). 

* $V_T$ : Conjunto de símbolos Terminales (los caracteres reales del alfabeto $\Sigma$). 

* $P$: Conjunto finito de Reglas de Producción (de la forma $\alpha \rightarrow \beta$). 

* $S$: El Símbolo Inicial ($S \in V_N$), desde donde comienza todo. 

 El mecanismo mediante el cual se pasa de la gramática al lenguaje es la derivación. Consiste en aplicar recursivamente las reglas de producción: se toma una cadena, se busca un símbolo no terminal y se reemplaza por el lado derecho de una producción aplicable. Este proceso se repite en pasos sucesivos ($\Rightarrow \dots \Rightarrow$) hasta que la cadena esté compuesta únicamente por símbolos terminales ($V_T$), momento en el cual la palabra oficialmente pertenece al lenguaje.  


## Ejemplo practico

Imaginemos un lenguaje super simplicado para definir asignaciones de variables en programacion donde:

Símbolo inicial: S

Producciones:

S -> <identificador> "=" <numero>

<identificador> -> "x" | "y"

<numero> -> "1" | "2"

Mecanismo en acción (Derivación de la cadena x = 2):

### $$S \Rightarrow <identificador> "=" <numero> \Rightarrow x "=" <numero> \Rightarrow x = 2$$


# 2.2.2.- Jerarquía de Chomsky

Propuesta por Noam Chomsky, esta jerarquía clasifica las gramáticas en 4 niveles (del Tipo 0 al Tipo 3). A medida que el número del tipo aumenta, las restricciones sobre las reglas de producción son más estrictas, pero el poder computacional necesario para reconocerlas disminuye.

A continuación se detallan los 4 tipos acompañados de su representación en BNF (Backus-Naur Form). 
El BNF esta diseñado exclusivamente para expresar sintaxis libre de contexto, es decir tipo 2, por lo que para los tipos 0 y 1 se adaptara la notacion para ilustrar las restricciones semanticas o de contexto.
Nota técnica: BNF está diseñado intrínsecamente para expresar sintaxis libre de contexto (Tipo 2), por lo que para los Tipos 0 y 1 se adaptará la notación para ilustrar las restricciones semánticas o de contexto.

## 1. Tipo 0: Gramáticas No Restringidas (Lenguajes Recursivamente Enumerables)

Estas no tienen restricciones en sus reglas de producción. Cualquier cadena de no terminales y terminales puede transformarse en cualquier otra combinación. Son equivalentes en poder a una Máquina de Turing.

Ejemplo en Notación BNF (Adaptada conceptualmente): Se permite que el lado izquierdo tenga múltiples símbolos y cambie el contexto de forma libre.

```BNF
;; Modifica el contexto de manera desestructurada
<A> <B> ::= <C> "x"
<C>     ::= "a"
```

## 2. Tipo 1: Gramáticas Sensibles al Contexto (Lenguajes Sensibles al Contexto)

Las producciones son de la forma $\alpha A \beta \rightarrow \alpha \gamma \beta$. El símbolo no terminal $A$ solo puede ser reemplazado por $\gamma$ si está rodeado por el "contexto" de $\alpha$ y $\beta$. Además, el lado derecho no puede ser más corto que el izquierdo ($|\alpha| \le |\beta|$). Son reconocidos por Autómatas Linealmente Acotados.

Ejemplo en Notación BNF (Representando el contexto): Un caso clásico es el lenguaje matemático $L = \{a^n b^n c^n \mid n \ge 1\}$.

```BNF
;; El reemplazo de un elemento depende de sus vecinos directos
<Contexto_A> <Variable> <Contexto_B> ::= <Contexto_A> "bloque_valido" <Contexto_B>
```

## 3. Tipo 2: Gramáticas Libres de Contexto (Lenguajes Libres de Contexto)

El lado izquierdo de cualquier regla de producción debe ser únicamente un solo símbolo no terminal. No importa qué caracteres rodeen a este símbolo; la sustitución siempre es válida. Es el esqueleto que define la sintaxis de los lenguajes de programación modernos (estructuras anidadas, paréntesis, bloques de código) y se procesa mediante Autómatas de Pila (Parsers).  

Ejemplo en Notación BNF (Estructura de un bloque if-else):

```BNF
<sentencia_if> ::= "if" "(" <condicion> ")" <bloque> <opcional_else>
<opcional_else> ::= "else" <bloque> | ""
<condicion>     ::= "true" | "false"
<bloque>        ::= "{" "instrucciones" "}"
```

## 4. Tipo 3: Gramáticas Regulares (Lenguajes Regulares)

Son las más restrictivas, Las reglas solo permiten un no terminal a la izquierda, y a la derecha un terminal seguido (o precedido) por máximo un no terminal (lineales a la derecha o a la izquierda). Son las que dan vida a las Expresiones Regulares (Regex) y se procesan eficientemente con Autómatas Finitos para el análisis léxico (identificación de tokens).  

Ejemplo en Notación BNF (Definición léxica de un Identificador/Variable):

```BNF
<identificador> ::= <letra> | <letra> <resto_id>
<resto_id>      ::= <letra> <resto_id> | <digito> <resto_id> | <letra> | <digito>
<letra>         ::= "a" | "b" | "c"
<digito>        ::= "0" | "1" | "2"
```