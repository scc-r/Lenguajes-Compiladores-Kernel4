const std = @import("std");

// Función pura: matemática estricta para la conjetura de Collatz
fn collatz(n: u64) u64 {
    var count: u64 = 0;
    var current = n;

    while (current != 1) {
        if (current % 2 == 0) {
            current /= 2;
        } else {
            current = current * 3 + 1;
        }
        count += 1;
    }

    return count;
}

pub fn main() void {
    std.debug.print("[Zig] Iniciando procesamiento intensivo (Collatz)...\n", .{});

    // Límite establecido para la prueba de carga
    const limite_n: u64 = 10_000_000;
    var max_secuencia: u64 = 0;

    // Bucle principal de procesamiento
    var i: u64 = 1;
    while (i < limite_n) : (i += 1) {
        const longitud = collatz(i);
        if (longitud > max_secuencia) {
            max_secuencia = longitud;
        }
    }

    std.debug.print("✅ Procesamiento completado.\n", .{});
    std.debug.print("🔢 Maxima longitud de secuencia encontrada: {}\n", .{max_secuencia});
}
