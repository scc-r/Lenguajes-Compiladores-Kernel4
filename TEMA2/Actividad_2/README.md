# 🚀 Guía de Reproducción de Escenarios Empíricos (Benchmarking)

Este documento proporciona las instrucciones técnicas explícitas para configurar los entornos, instalar las dependencias, compilar los archivos fuente y reproducir los escenarios de pruebas empíricas de estrés matemático basados en la Conjetura de Collatz (10,000,000 de iteraciones) para los lenguajes Zig, Rust, JavaScript (Node.js) y Python.

---

## 🛠️ Instalación y Configuración del Entorno (PowerShell)

Para replicar el entorno de pruebas en Windows, todos los lenguajes y sus entornos de ejecución deben ser instalados nativamente a través de la consola. 

Abra una terminal de **PowerShell** y ejecute los siguientes comandos utilizando el gestor de paquetes de Windows (`winget`):

```powershell
# 1. Instalar el compilador de Zig
winget install zig.zig

# 2. Instalar el entorno de ejecución de JavaScript (Node.js)
winget install OpenJS.NodeJS

# 3. Instalar el intérprete estándar de Python (CPython)
winget install Python.Python.3

# 4. Instalar el gestor de herramientas de Rust (Rustup)
winget install Rustlang.Rustup
```

### Configuración adicional obligatoria para Rust
Para el compilador de **Rust**, es fundamental configurar la cadena de herramientas basada en GNU (`x86_64-pc-windows-gnu`). Esto evita la dependencia del enlazador pesado de Microsoft Visual Studio (`link.exe`), utilizando en su lugar un entorno ligero de compilación adecuado para pruebas empíricas.

Ejecute consecutivamente los siguientes comandos:

```powershell
# Instalar la cadena de herramientas estable de GNU para Windows
rustup toolchain install stable-x86_64-pc-windows-gnu

# Configurar dicha cadena de herramientas como la predeterminada global del sistema
rustup default stable-x86_64-pc-windows-gnu
```

---

## 💻 Instrucciones de Compilación y Ejecución

Para garantizar la precisión e imparcialidad científica del benchmark, la medición del tiempo de ejecución y del consumo de memoria RAM física (Working Set) se realiza de forma externa al código fuente. Se utiliza un script de supervisión en PowerShell que interroga activamente al sistema operativo cada 10 milisegundos, registrando el pico máximo de memoria antes de la finalización del proceso.

### 1. Pruebas en Zig (Compilado Nativo)

Navegue al directorio donde se encuentra el archivo `collatz.zig` y proceda con la compilación del binario aplicando los modificadores de optimización más agresivos del compilador para maximizar el rendimiento de ejecución:

```powershell
cd TEMA2/Actividad_2/ZIG
zig build-exe collatz.zig -O ReleaseFast
```

**Comando de supervisión y ejecución en tiempo real:**
```powershell
$p = Start-Process -FilePath ".\collatz.exe" -PassThru -NoNewWindow; $peak = 0; $sw = [System.Diagnostics.Stopwatch]::StartNew(); while (-not $p.HasExited) { $p.Refresh(); try { if ($p.WorkingSet64 -gt $peak) { $peak = $p.WorkingSet64 } } catch {}; Start-Sleep -Milliseconds 10 }; $sw.Stop(); Write-Host "----------------------------------------"; Write-Host "⏱️ Tiempo OS (ZIG): $($sw.Elapsed.TotalMilliseconds) ms"; Write-Host "🧠 RAM OS Pico: $([math]::Round($peak / 1048576, 2)) MB"; Write-Host "----------------------------------------"
```

### 2. Pruebas en Rust (Compilado Nativo)

Navegue al directorio que contiene el archivo `collatz.rs` y compile el código fuente optimizado para producción utilizando la bandera de optimización nativa del compilador:

```powershell
cd TEMA2/Actividad_2/RUST
rustc -O collatz.rs
```

**Comando de supervisión y ejecución en tiempo real:**
```powershell
$p = Start-Process -FilePath ".\collatz.exe" -PassThru -NoNewWindow; $peak = 0; $sw = [System.Diagnostics.Stopwatch]::StartNew(); while (-not $p.HasExited) { $p.Refresh(); try { if ($p.WorkingSet64 -gt $peak) { $peak = $p.WorkingSet64 } } catch {}; Start-Sleep -Milliseconds 10 }; $sw.Stop(); Write-Host "----------------------------------------"; Write-Host "⏱️ Tiempo OS (RUST): $($sw.Elapsed.TotalMilliseconds) ms"; Write-Host "🧠 RAM OS Pico: $([math]::Round($peak / 1048576, 2)) MB"; Write-Host "----------------------------------------"
```

### 3. Pruebas en JavaScript (Motor JIT - Node.js)

Navegue al directorio que contiene el script `collatz.js`. Debido al modelo de ejecución basado en compilación en tiempo real (Just-In-Time), este entorno no requiere un paso previo de compilación manual.

```powershell
cd TEMA2/Actividad_2/JS
```

**Comando de supervisión y ejecución en tiempo real:**
```powershell
$p = Start-Process -FilePath "node" -ArgumentList "collatz.js" -PassThru -NoNewWindow; $peak = 0; $sw = [System.Diagnostics.Stopwatch]::StartNew(); while (-not $p.HasExited) { $p.Refresh(); try { if ($p.WorkingSet64 -gt $peak) { $peak = $p.WorkingSet64 } } catch {}; Start-Sleep -Milliseconds 10 }; $sw.Stop(); Write-Host "----------------------------------------"; Write-Host "⏱️ Tiempo OS (JS): $($sw.Elapsed.TotalMilliseconds) ms"; Write-Host "🧠 RAM OS Pico: $([math]::Round($peak / 1048576, 2)) MB"; Write-Host "----------------------------------------"
```

### 4. Pruebas en Python (Intérprete Puro)

Navegue al directorio que contiene el script `collatz.py`. Este programa se ejecutará de forma directa bajo el entorno interpretado estándar de CPython.

```powershell
cd TEMA2/Actividad_2/PY
```

**Comando de supervisión y ejecución en tiempo real:**
```powershell
$p = Start-Process -FilePath "python" -ArgumentList "collatz.py" -PassThru -NoNewWindow; $peak = 0; $sw = [System.Diagnostics.Stopwatch]::StartNew(); while (-not $p.HasExited) { $p.Refresh(); try { if ($p.WorkingSet64 -gt $peak) { $peak = $p.WorkingSet64 } } catch {}; Start-Sleep -Milliseconds 10 }; $sw.Stop(); Write-Host "----------------------------------------"; Write-Host "⏱️ Tiempo OS (PYTHON): $($sw.Elapsed.TotalMilliseconds) ms"; Write-Host "🧠 RAM OS Pico: $([math]::Round($peak / 1048576, 2)) MB"; Write-Host "----------------------------------------"
```
