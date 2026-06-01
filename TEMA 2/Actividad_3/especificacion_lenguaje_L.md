# ⚡ Actividad III: Diseño de un Lenguaje de Dominio Específico (DSL)

**Arquitectura y Diseño del Lenguaje:** Shirley Cedeño

## 1. Definición del Entorno Físico: Sistema ECO-GRID
El sistema ECO-GRID constituye una arquitectura avanzada de Gestión de Energía para Microredes Inteligentes (Smart Microgrids), diseñada para supervisar, optimizar y proteger el flujo de energía en entornos industriales con alta demanda operativa. El propósito fundamental de esta infraestructura es garantizar la continuidad del servicio mediante la gestión eficiente de fuentes renovables y sistemas de almacenamiento, minimizando el estrés térmico y los riesgos eléctricos.

### 1.1 Componentes de Hardware Controlados:
El software ECO-GRID actúa como el "cerebro" lógico que interactúa con la siguiente infraestructura física a través de las primitivas de nuestro lenguaje:

* Paneles Solares (Captación): Fuentes primarias de generación fotovoltaica que inyectan energía al sistema. El sistema monitorea el flujo de generación en tiempo real.

* Baterías de Litio (Almacenamiento): Sistema de almacenamiento de energía (ESS) crítico para la estabilidad de la red. Requieren una monitorización estricta de sus estados de carga para maximizar su vida útil.

* Sensores Térmicos: Dispositivos de seguridad instalados en los contenedores de baterías. Su función es reportar variaciones de temperatura que podrían derivar en fallos catastróficos o fugas térmicas.

* Inversores (Conversión): Equipos responsables de la conversión de corriente continua a alterna y el acoplamiento de la energía generada con la red industrial o externa.

* Relés (Actuadores): Elementos electromecánicos de alta potencia que permiten la conmutación de líneas. Son el músculo físico del sistema, permitiendo aislar sectores de consumo o redirigir el flujo eléctrico bajo demanda o emergencia.

### 1.2 ¿Por qué ECO-GRID necesita un lenguaje DSL?
Dado que este entorno físico opera bajo condiciones de estrés crítico, la gestión manual es propensa a errores humanos. Nuestro Lenguaje L (ECO-GRID) fue diseñado específicamente para que cualquier operador de planta pueda configurar las reglas de seguridad, automatizar la refrigeración y gestionar los cortes de carga de forma rápida, legible y, sobre todo, segura.

--- 

## 2. Especificación Léxica y Morfológica (Manual de Referencia)

El Lenguaje L (ECO-GRID) está diseñado bajo una filosofía de legibilidad extrema para operadores de plantas eléctricas. Prescinde de delimitadores estrictos de cierre de línea y adopta un vocabulario nativo en español para mitigar errores de sintaxis en entornos de estrés operativo. A continuación, se detalla el comportamiento del analizador léxico conceptual y el diccionario de primitivas de hardware del lenguaje.

### 2.1. Alfabeto Aceptado
Para la escritura del código fuente y nombramiento de identificadores, el lenguaje reconoce los caracteres del alfabeto latino en minúsculas y mayúsculas (`a-z`, `A-Z`), dígitos numéricos (`0-9`) y el carácter de subrayado (`_`). Adicionalmente, el analizador léxico admite espacios en blanco, comillas dobles (`"`) y signos de puntuación de la codificación estándar (ASCII/UTF-8) **exclusivamente** para la encapsulación y formación de cadenas de texto.

### 2.2. Listado Exhaustivo de Tokens Válidos
El escáner del código fuente clasifica todas las cadenas de texto del programa en las siguientes categorías de tokens (Token Classes):

#### TOKEN `LIT_NUM` (Literales Numéricos)
Representa valores constantes numéricos. Acepta números enteros para cálculos de capacidad y números de punto flotante para mediciones térmicas de precisión.
* **Ejemplo de uso:**
  ```eco
  limiteTemperatura = 55.5
  capacidadMinima = 20
  ```

#### TOKEN `LIT_BOOL` (Literales Booleanos)
Representan estados lógicos discretos de los componentes. Se prescinde de los tradicionales `true/false` adoptando palabras clave en español adaptadas al control de actuadores.
* **Valores aceptados:** `encendido`, `apagado`.
* **Ejemplo de uso:**
  ```eco
  estadoRele = encendido
  ```

#### TOKEN `LIT_CADENA` (Literales de Texto)
Representan secuencias estáticas de caracteres (strings). El analizador léxico reconocerá como texto plano cualquier cadena que se encuentre encapsulada estrictamente entre comillas dobles (`"`). 
* **Ejemplo de uso:**
  ```eco
  mensajeError = "Fuga térmica detectada en contenedor"
  ```

#### TOKEN `LIT_NIVEL` (Literales de Criticidad)
Representan los estados fijos de severidad y urgencia operativa configurados en el sistema de mensajería de la planta. El escáner los reconocerá como palabras reservadas de valor constante.
* **Valores aceptados:** `info`, `advertencia`, `critico`.
* **Ejemplo de uso:**
  ```eco
  nivelUrgencia = critico
  ```

#### TOKEN `ID` (Identificadores)
Nombres definidos por el usuario para variables, colecciones, sensores o sectores específicos de la microred. Para diferenciarlos visualmente de las funciones nativas del sistema, deben iniciar obligatoriamente con una letra minúscula y utilizar estrictamente la convención de escritura `camelCase`.
* **Ejemplo de uso:**
  ```eco
  bateriaNorte1 = 100
  sectorIndustrial = apagado
  ```

#### TOKEN `ESTRUCTURA` (Palabras de Control de Flujo)
Palabras reservadas por el lenguaje para definir la arquitectura lógica del programa (condicionales, iteraciones y manejo de errores). Deben escribirse obligatoriamente en MAYÚSCULAS para resaltar visualmente la jerarquía del código frente a las variables del operador.
* **Valores aceptados:** `SI`, `ENTONCES`, `SINO`, `FIN_SI`, `MIENTRAS`, `EJECUTAR`, `FIN_MIENTRAS`, `PARA_CADA`, `EN`, `FIN_PARA`, `INTENTAR`, `EN_CASO_DE_FALLA`, `FIN_INTENTAR`.
* **Comando de interrupción (`ROMPER`):** Palabra reservada que fuerza la salida inmediata y absoluta del hilo de ejecución de cualquier bucle iterativo, omitiendo las condiciones restantes.

#### TOKEN `OP` (Operadores de Expresión)
Símbolos y palabras reservadas reconocidos por el analizador léxico para ejecutar operaciones aritméticas, evaluaciones de relación, álgebra booleana y manipulación de cadenas de texto.
* **Asignación:** `=` (Operador único para almacenar valores en identificadores).
* **Aritméticos:** `+` (Suma), `-` (Resta), `*` (Multiplicación), `/` (División) y `%` (Módulo).
* **Concatenación de Cadenas:** El operador `+` presenta sobrecarga para unir texto con identificadores o resultados numéricos. **Regla de precedencia:** Las operaciones matemáticas dentro de una concatenación deben ir entre paréntesis `()`.
* **Relacionales:** `>` (Mayor), `<` (Menor), `>=` (Mayor o igual), `<=` (Menor o igual), `==` (Igualdad estricta), `!=` (Diferencia).
* **Lógicos:** `Y`, `O`, `NO`.
* **Ejemplo de uso:**
  ```eco
  SI (tempActual > limiteSeguro) ENTONCES
      emitir_alerta(critico, "Límite superado por: " + (tempActual - limiteSeguro) + " grados.")
  ```

#### TOKEN `DELIM` (Delimitadores y Símbolos Especiales)
Definen la separación de sentencias e instrucciones, así como la encapsulación de argumentos y colecciones de hardware.
* **Salto de línea (tecla Enter):** Actúa como el único delimitador válido para indicar el final de una instrucción (carácter interno `\n`).
* `,` **(Coma):** Actúa como separador secuencial. Se utiliza para dividir múltiples argumentos dentro de una función o separar los elementos individuales al declarar un vector.
* `[` y `]`: Delimitadores para declarar o indexar vectores (agrupaciones de hardware).
* `(` y `)`: Delimitadores con triple función. Sirven para agrupar expresiones lógicas, pasar parámetros a funciones nativas, y aislar operaciones matemáticas para forzar su precedencia de ejecución (vital al utilizar concatenación de cadenas).
* **Ejemplo de uso:**
  ```eco
  bateriasCriticas = [bateria1, bateria2, bateria3]
  emitir_alerta(critico, "Falla en sector")
  ```

#### TOKEN `COMENTARIO`
Cualquier línea o fragmento de texto precedido por el símbolo de numeral `#`. El analizador léxico descarta automáticamente el resto de los caracteres de esa línea durante la fase de escaneo.
* **Ejemplo de uso:**
  ```eco
  # Desconectar la carga si ocurre una sobretensión
  ```

---

### 2.3. Diccionario de Primitivas de Hardware (Palabras Clave)

El lenguaje incorpora un conjunto cerrado de funciones nativas (`TOKEN PRIMITIVA`) que interactúan directamente con los drivers lógicos y actuadores mecánicos de la planta ECO-GRID. Para distinguirse del código del usuario (`camelCase`), el motor del sistema preserva estas invocaciones nativas en convención `snake_case`.

**`init_grid()`**
* **Descripción:** Inicializa, verifica y calibra todos los controladores lógicos y buses de comunicación de la microred. Debe ser de manera obligatoria la primera instrucción ejecutable de cualquier programa.
* **Retorno:** Ninguno.
* **Pseudo-notación:** `init_grid() <\n>`
* **Ejemplo válido:**
  ```eco
  init_grid()
  ```

**`leer_temperatura(bateriaId)`**
* **Descripción:** Consulta el sensor térmico integrado en una celda o contenedor específico de almacenamiento.
* **Retorno:** Flotante (Valor térmico preciso en grados Celsius °C).
* **Pseudo-notación:** `leer_temperatura( <TOKEN ID_bateria> )`
* **Ejemplo válido:**
  ```eco
  tempActual = leer_temperatura(bancoLitioSur)
  ```

**`estado_carga(bateriaId)`**
* **Descripción:** Retorna el nivel relativo de la energía remanente dentro de un banco de celdas específico.
* **Retorno:** Entero (Valor porcentual acotado en el rango de 0 a 100).
* **Pseudo-notación:** `estado_carga( <TOKEN ID_bateria> )`
* **Ejemplo válido:**
  ```eco
  cargaDisponible = estado_carga(bancoLitioSur)
  ```

**`flujo_actual(sensorId)`**
* **Descripción:** Realiza una lectura instantánea del paso de potencia eléctrica a través de los sensores e inversores de acoplamiento.
* **Retorno:** Entero (Potencia medida en kilovatios [kW]. Los valores positivos representan inyección/generación de energía y negativos consumo).
* **Pseudo-notación:** `flujo_actual( <TOKEN ID_sensor> )`
* **Ejemplo válido:**
  ```eco
  generacionSolar = flujo_actual(sensorPaneles1)
  ```

**`conmutar_linea(sectorId, estado)`**
* **Descripción:** Modifica el estado físico de los relés electromecánicos de alta potencia para conectar o aislar un sector de consumo de la red.
* **Retorno:** Ninguno.
* **Pseudo-notación:** `conmutar_linea( <TOKEN ID_sector> , <TOKEN LIT_BOOL> ) <\n>`
* **Ejemplo válido:**
  ```eco
  # Aislar el área de oficinas de la red principal
  conmutar_linea(sectorOficinas, apagado)
  ```

**`activar_refrigeracion(bateriaId)`**
* **Descripción:** Envía una señal de activación forzada a los extractores y sistemas de enfriamiento auxiliar del contenedor especificado.
* **Retorno:** Ninguno.
* **Pseudo-notación:** `activar_refrigeracion( <TOKEN ID_bateria> ) <\n>`
* **Ejemplo válido:**
  ```eco
  activar_refrigeracion(bancoLitioSur)
  ```

**`emitir_alerta(nivelCriticidad, mensaje)`**
* **Descripción:** Envía de forma síncrona una notificación estructurada para ser desplegada inmediatamente en la pantalla de alarmas de la HMI. Permite la concatenación de texto estático con identificadores dinámicos o con el resultado de operaciones aritméticas usando el operador `+`.
* **Retorno:** Ninguno.

  **A. Concatenación directa con variable simple**
  Se utiliza para unir el texto con el valor de un identificador sin ejecutar cálculos matemáticos.
  * **Pseudo-notación:** `emitir_alerta( <TOKEN LIT_NIVEL> , <TOKEN LIT_CADENA> + <TOKEN ID> ) <\n>`
  * **Ejemplo válido:**
    ```eco
    # Envía el texto junto al nombre específico de la batería
    emitir_alerta(critico, "Fuga térmica detectada en: " + bancoLitioSur)
    ```
  **B. Concatenación con operación matemática**
  Requiere el uso obligatorio de paréntesis para aislar la expresión aritmética, forzando al motor a resolver el cálculo antes de unirlo al texto.
  * **Pseudo-notación:** `emitir_alerta( <TOKEN LIT_NIVEL> , <TOKEN LIT_CADENA> + ( <operacion_aritmetica> ) ) <\n>`
  * **Ejemplo válido:**
    ```eco
    # El compilador resuelve primero la resta y luego une el resultado numérico al texto
    emitir_alerta(advertencia, "Límite térmico superado por: " + (tempActual - 55.0))
    ```

**`hora_actual()`**
* **Descripción:** Consulta el reloj interno en tiempo real de los servidores de la planta para la toma de decisiones cronológicas.
* **Retorno:** Entero (Valor numérico de 0 a 23, representando la hora militar local).
* **Pseudo-notación:** `hora_actual()`
* **Ejemplo válido:**
  ```eco
  SI (hora_actual() >= 18 Y hora_actual() <= 23) ENTONCES
      conmutar_linea(sectorIndustrial, apagado)
  FIN_SI
  ```

**`esperar(segundos)`**
* **Descripción:** Pausa la ejecución del hilo de monitorización. Obligatoria en bucles continuos para evitar el colapso del CPU.
* **Retorno:** Ninguno.
* **Pseudo-notación:** `esperar( <TOKEN LIT_NUM_entero> ) <\n>`
* **Ejemplo válido:**
  ```eco
  esperar(60) # Pausa el sistema durante un minuto
  ```

---

## 3. Gramática Sintáctica Abstracta

Una vez que el analizador léxico ha tokenizado el código fuente, el analizador sintáctico de ECO-GRID evalúa el orden lógico de las instrucciones para construir el Árbol de Sintaxis Abstracta (AST). 

Para garantizar que la máquina interprete los comandos sin ambigüedades, se establece el siguiente orden lógico obligatorio, descrito mediante pseudo-notación estructural y lenguaje natural.

### 3.1. Estructura de Declaración y Asignación
Define la regla gramatical para almacenar valores numéricos (`LIT_NUM`), booleanos (`LIT_BOOL`), cadenas de texto (`LIT_CADENA`), agrupaciones de hardware (`vector`) o lecturas de sensores en la memoria del sistema.
* **Orden Lógico Estricto:** La sentencia debe iniciar obligatoriamente con un `TOKEN ID` (en convención `camelCase`), seguido del operador de asignación `=`, seguido de una expresión válida, y finalizar con el delimitador de salto de línea `\n`.
* **Pseudo-notación:**
  `<identificador_camelCase> = <literal | primitiva | operacion | vector> <\n>`
* **Ejemplo válido:**
  ```eco
  temperaturaMaxima = 55.0
  mensajePeligro = "Temperatura crítica alcanzada"
  cargaActual = estado_carga(bateriaPrincipal)
  bateriasNorte = [batNorte1, batNorte2]
  ```

### 3.2. Estructuras Condicionales (Toma de Decisiones)
Regula cómo el sistema evalúa el entorno para ejecutar acciones de respuesta (como apagar un relé si hay sobrecalentamiento). 
* **Orden Lógico Estricto:** Inicia con `SI`, seguido de una condición lógica entre paréntesis `()`, la palabra `ENTONCES` y un salto de línea. El bloque `SINO` es opcional para manejar condiciones contrarias. Todo el bloque se cierra con `FIN_SI`.
* **Pseudo-notación:**
  ```eco
  SI ( <expresion_logica> ) ENTONCES <\n>
      <bloque_instrucciones_verdadero> <\n>
  SINO <\n>
      <bloque_instrucciones_falso> <\n>
  FIN_SI <\n>
  ```
* **Ejemplo válido:**
  ```eco
  SI (temperaturaActual > 55.0) ENTONCES
    conmutar_linea(sectorIndustrial, apagado)
  SINO
      conmutar_linea(sectorIndustrial, encendido)
  FIN_SI
  ```

### 3.3. Estructuras Iterativas (Bucles)
Garantizan la monitorización continua y autónoma del hardware. El lenguaje define dos estructuras jerárquicas sin ambigüedad para ciclos iterativos.

#### A. Bucle Condicional Continuo (`MIENTRAS`)
Se ejecuta indefinidamente mientras la condición evaluada retorne un valor lógico verdadero.
* **Pseudo-notación:**
  ```eco
  MIENTRAS ( <expresion_logica> ) EJECUTAR <\n>
      <bloque_de_instrucciones> <\n>
  FIN_MIENTRAS <\n>
  ```
* **Ejemplo válido (Demostrando control de tiempo, concatenación y ruptura de emergencia):**
  ```eco
  MIENTRAS (estado_carga(bateriaPrincipal) < 100) EJECUTAR
      SI (leer_temperatura(bateriaPrincipal) > 60.0) ENTONCES
          # Se aplica la regla de concatenación de cadenas
          emitir_alerta(critico, "Sobrecalentamiento en carga de: " + bateriaPrincipal)
          ROMPER
      FIN_SI
      esperar(60) # Pausa obligatoria de 1 minuto para no saturar el CPU
  FIN_MIENTRAS
  ```

#### B. Bucle de Colección (`PARA_CADA`)
Estructura específica diseñada para recorrer agrupaciones masivas de hardware (vectores), extrayendo un elemento a la vez para su evaluación individual.
* **Pseudo-notación:**
  ```eco
  PARA_CADA <nuevo_ID> EN <coleccion_ID> EJECUTAR <\n>
      <bloque_de_instrucciones_sobre_elemento> <\n>
  FIN_PARA <\n>
  ```
* **Ejemplo válido:**
  ```eco
  PARA_CADA bat EN bateriasCriticas EJECUTAR
      tempCelda = leer_temperatura(bat)
      activar_refrigeracion(bat)
  FIN_PARA
  ```

### 3.4. Estructura Sintáctica de Resiliencia (Manejo de Errores)
Para evitar la detención total del software ante la pérdida de conexión con un sensor físico, la gramática incorpora una estructura de control de excepciones.
* **Orden Lógico Estricto:** El bloque primario se inicia con `INTENTAR`. Si alguna instrucción falla o devuelve un error de hardware, el flujo salta inmediatamente a la estructura `EN_CASO_DE_FALLA`, ejecutando el bloque de contingencia. Se cierra con `FIN_INTENTAR`.
* **Pseudo-notación:**
  ```eco
  INTENTAR <\n>
      <bloque_de_instrucciones_primarias> <\n>
  EN_CASO_DE_FALLA <\n>
      <bloque_de_contingencia_y_alertas> <\n>
  FIN_INTENTAR <\n>
  ```
* **Ejemplo válido:**
  ```eco
  INTENTAR
      temp = leer_temperatura(bateriaNorte)
  EN_CASO_DE_FALLA
      emitir_alerta(critico, "Fallo de comunicación con el sensor en: " + bateriaNorte)
  FIN_INTENTAR
  ```

---

## 4. Resolución de Escenarios Operativos Críticos
**Programación de Escenarios Operativos:** [Nombre del Integrante 4]  

### 4.1. Escenario Operativo A: Prevención de Fuga Térmica
* **Objetivo:** Monitorización iterativa para prevenir el sobrecalentamiento de las baterías.
* **Lógica Implementada:** *(Tu compañero debe explicar aquí, en lenguaje natural, cómo su script lee la temperatura, y si supera los 55°C, cómo invoca las primitivas para activar refrigeración, desconectar carga solar y desviar consumo a la red comercial)*.
* **Codigo Fuente:** 

### 4.2. Escenario Operativo B: Balance de Carga y Optimización Energética
* **Objetivo:** Toma de decisiones autónoma para inyectar excedentes o aislar sectores críticos.
* **Lógica Implementada:** *(Explicar cómo el script evalúa si la carga es >90% para vender energía a la red, o si es <20% de noche, cómo aísla sectores no esenciales para proteger las áreas críticas).*
* **Codigo Fuente:** 
