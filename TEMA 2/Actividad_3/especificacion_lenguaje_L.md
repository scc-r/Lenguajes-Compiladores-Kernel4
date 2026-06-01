# ⚡ Actividad III: Diseño de un Lenguaje de Dominio Específico (DSL)
**Arquitectura y Diseño del Lenguaje:** [Tu Nombre]  
**Programación de Escenarios Operativos:** [Nombre del Integrante 4]  

## 1. Definición del Entorno Físico: Sistema ECO-GRID
*(Breve descripción del entorno de Sistema de Gestión de Microredes Eléctricas Inteligentes y Almacenamiento de Energía. Mencionar los componentes de hardware controlados: paneles solares, baterías de litio, inversores, sensores térmicos y relés)*.

---

## 2. Especificación Léxica y Morfológica
*(Detallar cómo el analizador léxico conceptual leerá el código)*.

* **Alfabeto Aceptado:** *(Ej. Caracteres ASCII, letras a-z, A-Z, números 0-9).*
* **Tipos de Datos (Literales):** *(Definir si aceptan enteros para kW, flotantes para temperatura, y booleanos para estados de relés).*
* **Reglas de Identificadores:** *(Ej. Las variables deben iniciar con una letra minúscula y usar snake_case).*
* **Delimitadores y Comentarios:** *(Definir cómo se separan las instrucciones y cuál es el símbolo para los comentarios. Ej. `//` para una línea).*

### 2.1. Palabras Clave Obligatorias y Primitivas de Hardware
*(Listado exhaustivo de los comandos nativos que interactúan con el driver de bajo nivel)*.

* **Inicialización:** `init_grid`
* **Sensores (Lectura):**
  * `leer_temperatura(bateria_id)`
  * `estado_carga(bateria_id)`
  * `flujo_actual(sensor_id)`
* **Actuadores (Escritura/Acción):**
  * `conmutar_linea(sector_id, estado)`
  * `activar_refrigeracion(bateria_id)`

---

## 3. Gramática Sintáctica Abstracta
*(Documentar el orden lógico y las estructuras de control de flujo usando notación matemática o lenguaje natural estructurado)*.

### 3.1. Estructuras Condicionales
*(Definir la sintaxis compacta o estructurada para la toma de decisiones)*.
* **Sintaxis:** `si [condicion] entonces`
      `[instrucciones]`
  `fin_si`

### 3.2. Estructuras Iterativas (Bucles)
*(Definir cómo el lenguaje maneja la monitorización continua)*.
* **Sintaxis:**
  `mientras [condicion] ejecutar`
      `[instrucciones]`
  `fin_mientras`

---

## 4. Resolución de Escenarios Operativos Críticos
*(Los códigos fuente funcionales se encuentran en los archivos adjuntos `.eco` dentro del directorio de esta actividad en el repositorio).*

### 4.1. Escenario Operativo A: Prevención de Fuga Térmica
* **Objetivo:** Monitorización iterativa para prevenir el sobrecalentamiento de las baterías.
* **Lógica Implementada:** *(Tu compañero debe explicar aquí, en lenguaje natural, cómo su script lee la temperatura, y si supera los 55°C, cómo invoca las primitivas para activar refrigeración, desconectar carga solar y desviar consumo a la red comercial)*.
* **Archivo Fuente:** `escenario_A.eco`

### 4.2. Escenario Operativo B: Balance de Carga y Optimización Energética
* **Objetivo:** Toma de decisiones autónoma para inyectar excedentes o aislar sectores críticos.
* **Lógica Implementada:** *(Explicar cómo el script evalúa si la carga es >90% para vender energía a la red, o si es <20% de noche, cómo aísla sectores no esenciales para proteger las áreas críticas).*
* **Archivo Fuente:** `escenario_B.eco`
