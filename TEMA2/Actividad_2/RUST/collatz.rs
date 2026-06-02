use std::time::Instant;

// Función pura: usamos mutabilidad explícita (mut) solo donde se requiere
fn collatz(mut n: u64) -> u64 {
    let mut count: u64 = 0;
    
    while n > 1 {
        if n % 2 == 0 {
            n /= 2;
        } else {
            n = n * 3 + 1;
        }
        count += 1;
    }
    
    // Retorno idiomático en Rust (sin 'return' ni ';')
    count
}

fn main() {
    println!("[Rust] Iniciando procesamiento intensivo (Collatz)...");

    const LIMITE_N: u64 = 10_000_000;
    let mut max_secuencia: u64 = 0;

    // Cronómetro nativo de Rust
    let start = Instant::now();

    // Bucle iterativo utilizando rangos inclusivos (1..=LIMITE_N)
    for i in 1..=LIMITE_N {
        let longitud = collatz(i);
        if longitud > max_secuencia {
            max_secuencia = longitud;
        }
    }

    let duration = start.elapsed();
    // Convertimos la duración a milisegundos flotantes para mayor precisión
    let elapsed_ms = duration.as_secs_f64() * 1000.0;

    println!("✅ Procesamiento completado.");
    println!("⏱️  Tiempo de ejecución interno: {:.2} ms", elapsed_ms);
    println!("🔢 Máxima longitud de secuencia encontrada: {}", max_secuencia);
}