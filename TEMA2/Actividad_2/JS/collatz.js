const { performance } = require('perf_hooks');

function calcularCollatz() {
    const LIMITE = 10000000; // Nuestros 10 millones oficiales
    console.log(`[JavaScript] Iniciando procesamiento intensivo (Collatz)...`);
    
    let maxSecuencia = 0; // Variable para rastrear la secuencia más larga
    
    const tiempoInicio = performance.now();

    for (let i = 1; i <= LIMITE; i++) {
        let n = i;
        let longitud = 0; // Contador de pasos para el número actual

        while (n > 1) {
            if (n % 2 === 0) {
                n = n / 2;
            } else {
                n = (3 * n) + 1;
            }
            longitud++;
        }

        // Si la longitud de este número es la más grande hasta ahora, la guardamos
        if (longitud > maxSecuencia) {
            maxSecuencia = longitud;
        }
    }

    const tiempoFin = performance.now();
    const tiempoTotal = tiempoFin - tiempoInicio;
    const memoriaUsada = process.memoryUsage().heapUsed / 1024 / 1024;

    console.log(`✅ Procesamiento completado.`);
    console.log(`⏱️  Tiempo de ejecución: ${tiempoTotal.toFixed(2)} ms`);
    console.log(`🔢 Máxima longitud de secuencia encontrada: ${maxSecuencia}`);
    console.log(`🧠 Consumo de Memoria Pico: ${memoriaUsada.toFixed(2)} MB`);
}

calcularCollatz();