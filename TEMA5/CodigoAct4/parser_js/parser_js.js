const fs = require('fs');
const { performance } = require('perf_hooks');

function main() {
    // 1. Capturar los argumentos de la consola
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log("Uso: node parser_js.js <ruta_al_archivo.yml>");
        return;
    }
    const archivo = args[0];
    
    // 2. Leer el archivo
    let textoYaml;
    try {
        // Leemos el archivo y le agregamos un salto de línea por seguridad (como en Python)
        textoYaml = fs.readFileSync(archivo, 'utf8') + "\n";
    } catch (error) {
        console.log(`[!] Error: No se pudo abrir el archivo ${archivo}`);
        return;
    }

    console.log(`--- Evaluando ${archivo} ---`);

    // 3. Validación inicial (1 pasada)
    try {
        analizarFlujo(textoYaml);
        console.log("=> AST: ¡Análisis en JavaScript Exitoso!");
    } catch (error) {
        console.log(`\n[!] Análisis abortado.\n${error.message}`);
        return;
    }

    // 4. Experimento de Rendimiento (Benchmarking)
    const iteraciones = 10000;
    console.log(`Iniciando bucle de estrés de ${iteraciones} iteraciones...`);
    
    // perf_hooks nos da precisión de microsegundos, igual que sys/time.h en C
    const tiempoInicio = performance.now();
    
    for (let i = 0; i < iteraciones; i++) {
        analizarFlujo(textoYaml);
    }
    
    const tiempoFin = performance.now();
    const tiempoTotalMs = tiempoFin - tiempoInicio;

    console.log(`--> Tiempo total de ejecución (Node.js): ${tiempoTotalMs.toFixed(2)} ms\n`);
}

// 5. Motor del Parser: Analizador de Flujo Lineal (Inmune a ambigüedades LALR)
function analizarFlujo(texto) {
    // Dividimos por saltos de línea sin importar el sistema operativo (\r\n o \n)
    const lineas = texto.split(/\r?\n/);
    
    for (let i = 0; i < lineas.length; i++) {
        let linea = lineas[i].trim();
        
        // Ignorar líneas vacías
        if (!linea) continue;

        // Reglas Léxico-Sintácticas combinadas (Expresiones Regulares estrictas)
        const esRaiz       = /^networks:$/.test(linea);
        const esSeccion    = /^[a-zA-Z0-9_\-\.]+?:$/.test(linea); // ej: backend_tier: o ipam:
        const esPropiedad  = /^[a-zA-Z0-9_\-\.]+?:\s*([a-zA-Z0-9_\-\.\/:]+|"[^"]*"|true|false)$/.test(linea);
        const esSubred     = /^-\s+subnet:\s+[0-9a-fA-F:\.]+(\/[0-9]+)?$/.test(linea);
        const esGateway    = /^gateway:\s+[0-9a-fA-F:\.]+(\/[0-9]+)?$/.test(linea);

        // Si la línea no encaja en ninguna de las estructuras de YAML válidas, abortamos
        if (!esRaiz && !esSeccion && !esPropiedad && !esSubred && !esGateway) {
            throw new Error(`Error de Sintaxis en la línea ${i + 1}: Token inesperado cerca de '${linea}'`);
        }
    }
}

// Ejecutar el programa
main();