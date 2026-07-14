# Analizador Léxico para subconjunto de Rust (FLEX)

Este directorio contiene la implementación de un analizador léxico desarrollado mediante el metacompilador FLEX, diseñado para procesar un subconjunto específico de la sintaxis del lenguaje Rust.

## Archivos del Proyecto
* `lexer_rust.l`: Archivo de especificación léxica (Reglas Regex y acciones C).
* `prueba.rs`: Archivo de código fuente en Rust utilizado para las pruebas de validación.

## Requisitos Previos (Entorno Linux)
El analizador fue diseñado para ser compilado en un entorno Unix/Linux. Se requieren los siguientes paquetes:
* `flex` (Fast Lexical Analyzer Generator)
* `gcc` (GNU Compiler Collection)

Para instalar las dependencias en distribuciones basadas en Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install flex gcc -y