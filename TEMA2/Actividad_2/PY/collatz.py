import time
import tracemalloc

def calcular_collatz():
    LIMITE = 10000000
    print("[Python] Iniciando procesamiento intensivo (Collatz)...")
    
    # Iniciar monitoreo de memoria y tiempo
    tracemalloc.start()
    tiempo_inicio = time.perf_counter()
    
    max_secuencia = 0
    
    for i in range(1, LIMITE + 1):
        n = i
        longitud = 0
        
        while n > 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = (3 * n) + 1
            longitud += 1
            
        if longitud > max_secuencia:
            max_secuencia = longitud

    # Detener cronómetros
    tiempo_fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    tiempo_total_ms = (tiempo_fin - tiempo_inicio) * 1000
    memoria_mb = peak / (1024 * 1024)
    
    print("✅ Procesamiento completado.")
    print(f"⏱️  Tiempo de ejecución: {tiempo_total_ms:.2f} ms")
    print(f"🔢 Máxima longitud de secuencia encontrada: {max_secuencia}")
    print(f"🧠 Consumo de Memoria Pico: {memoria_mb:.2f} MB")

if __name__ == '__main__':
    calcular_collatz()