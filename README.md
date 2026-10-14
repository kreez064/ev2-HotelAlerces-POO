# 🏨 Sistema de Gestión Hotelera - Hotel Los Alerces
**Evaluación Sumativa N°3 - Programación Orientada a Objetos y Persistencia**

---

## 1. Integrantes y Negocio

### 🏢 Negocio: Hotel Los Alerces
**Hotel Los Alerces** es un establecimiento hotelero que requiere una solución integral y modular para automatizar y administrar de forma confiable sus operaciones diarias. El sistema aborda:
- Gestión y categorización de habitaciones con comportamiento polimórfico (Individuales, Dobles y Suites).
- Registro y mantención de huéspedes con validación rigurosa de documentos de identidad (RUT / Pasaporte).
- Administración transaccional de reservas y líneas de detalle de estadía.
- Control de consumos adicionales durante la estancia (servicios de Spa, Frigobar, etc.).
- Procesamiento de pagos, exigencia de anticipos mínimos para check-in y asignación de roles operativos (Recepcionista y Camarera de Housekeeping).
- Persistencia robusta en base de datos local SQLite mediante el patrón Data Access Object (DAO) con transacciones atómicas.
- Integración en tiempo real con indicadores económicos externos para conversión de tarifas (USD a CLP).

### 👥 Equipo de Desarrollo
- **Kevin Rivera**
- **Elias Espinoza**

### 📁 Estructura del Repositorio
El repositorio cuenta con la siguiente estructura limpia y modular:

```text
hotel_los_alerces/
├── model/
│   ├── __init__.py               # Paquete de modelos del dominio
│   ├── persona.py                # Clase base Persona con propiedades y setters
│   ├── huesped.py                # Clase Huesped con validación avanzada de documento
│   ├── empleado.py               # Jerarquía de personal del hotel
│   ├── recepcionista.py          # Subtipo Empleado: Check-in y pagos
│   ├── camarera_housekeeping.py  # Subtipo Empleado: Gestión de limpieza
│   ├── habitacion.py             # Clase base Habitacion
│   ├── habitacion_individual.py  # Subtipo Habitación Individual
│   ├── habitacion_doble.py       # Subtipo Habitación Doble
│   ├── habitacion_suite.py       # Subtipo Habitación Suite
│   ├── reserva.py                # Entidad transaccional Reserva
│   ├── detalle_reserva.py        # Detalle de estadía y noches
│   ├── servicio.py               # Catálogo de servicios adicionales
│   ├── servicios.py              # Exportador y compatibilidad de servicios
│   ├── consumo.py                # Registro de consumos por reserva
│   ├── medio_pago.py             # Tipos de medios de pago
│   ├── pago.py                   # Transacciones de pago
│   ├── indicador_externo.py      # Conversor auxiliar de moneda
│   └── excepciones.py            # Excepciones personalizadas del dominio hotelero
├── dao/
│   ├── __init__.py               # Paquete DAO
│   ├── conexion.py               # Conexión centralizada a SQLite (hotel.db) e inicialización DDL
│   ├── huesped_dao.py            # Operaciones CRUD completas y parametrizadas para Huesped
│   └── reserva_dao.py            # Transacciones atómicas (commit/rollback) para Reserva y DetalleReserva
├── services/
│   ├── __init__.py               # Paquete de servicios de integración
│   └── indicador_service.py      # Consumo resiliente de API mindicador.cl (timeout y fallback)
├── main.py                       # Script principal de demostración continua
├── requirements.txt              # Dependencias del proyecto (requests>=2.31.0)
└── README.md                     # Documentación oficial del proyecto
```

---

## 2. Guía de Instalación y Ejecución

Sigue estos pasos para clonar, configurar y ejecutar el proyecto en tu entorno local:

### Paso 1: Clonar el repositorio
Abre una terminal o consola de comandos y ejecuta:
```bash
git clone https://github.com/kreez064/ev2-HotelAlerces-POO.git
cd ev2-HotelAlerces-POO
```

### Paso 2: Creación y activación del entorno virtual (Opcional pero recomendado)
- **En Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Paso 3: Instalación de dependencias
Instala la librería oficial requerida especificada en `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar el sistema
Inicia la demostración completa ejecutando:
```bash
python main.py
```

### 📋 Flujo de Demostración Verificado en `main.py`:
1. **Inicialización automática de SQLite (`hotel.db`):** Crea automáticamente las tablas `huespedes`, `reservas` y `detalles_reserva` con integridad referencial activa (`PRAGMA foreign_keys = ON;`).
2. **Consumo de API Externa (`mindicador.cl`):** Consulta el valor del dólar en CLP mediante `IndicadorService` con un timeout controlado de 5.0 segundos y mecanismo de fallback tolerante a fallos.
3. **Operaciones CRUD en la Capa DAO:** Demuestra en vivo la creación (`Create`), consulta por ID (`Read`), listado general (`Read All`), actualización (`Update`) y eliminación segura (`Delete`) en SQLite.
4. **Validación de Entradas con `@setter`:** Captura de forma controlada intentos de ingresar documentos inválidos (menos de 8 caracteres o vacíos) sin colapsar el programa.
5. **Transacción Completa del Dominio:** Instancia habitaciones polimórficas (`Individual`, `Doble`, `Suite`), líneas de `DetalleReserva`, consumos de `Servicio` y persistencia en base de datos.
6. **Control de Reglas de Negocio:**
   - Captura de `HabitacionOcupadaError` al intentar sobre-reservar una habitación ocupada.
   - Captura de `AnticipoInsuficienteError` al intentar hacer check-in sin abonar el 50% de anticipo.
   - Solución del estado mediante el registro del pago exigido y confirmación exitosa del check-in.
7. **Finalización Segura:** Confirmación visual de ejecución continua exitosa.

---

## 3. Decisiones de Seguridad

### 🛡️ Prevención de Inyección SQL (SQL Injection) en la Capa DAO
La inyección de código SQL es una de las vulnerabilidades más críticas en aplicaciones que interactúan con bases de datos relacionales. Ocurre cuando datos no confiables provenientes del usuario son concatenados directamente en la sentencia SQL (`f"SELECT * FROM ... WHERE id = '{input}'"`), permitiendo que un atacante manipule la sintaxis e inserte comandos arbitrarios.

**Medidas técnicas implementadas:**
1. **Uso Exclusivo de Consultas Parametrizadas (`?`):**
   - En todos los métodos de `HuespedDAO` y `ReservaDAO`, sin excepción, las sentencias SQL utilizan marcadores de posición posicionales (`?`), delegando el enlace de datos al motor nativo de SQLite:
     ```python
     # Correcto y seguro:
     sql = "INSERT INTO huespedes (rut, nombre, telefono, correo, documento) VALUES (?, ?, ?, ?, ?)"
     cursor.execute(sql, (huesped.rut, huesped.nombre, huesped.telefono, huesped.correo, huesped.documento))
     ```
   - **Prohibición estricta de concatenación:** En ningún archivo del sistema se utilizan F-strings, formateo `%` ni concatenación con `+` para estructurar sentencias SQL.
2. **Separación de Código y Datos:**
   - El motor de base de datos compila y define el árbol sintáctico de la consulta de manera previa a recibir los valores. Incluso si un usuario ingresara caracteres maliciosos como `' OR '1'='1' --` o `; DROP TABLE huespedes;`, estos son tratados puramente como texto literal (cadenas de datos) y jamás como instrucciones ejecutables.
3. **Integridad Transaccional (ACID):**
   - Las operaciones compuestas, como el registro de una `Reserva` junto con sus múltiples líneas de `DetalleReserva`, se ejecutan dentro de bloques de transacción atómica con `conn.commit()` y `conn.rollback()`, garantizando que ninguna falla técnica deje la base de datos en un estado inconsistente o parcialmente corrupto.

### 🧹 Sanitización y Validación de Entradas mediante Métodos `@setter`
La integridad de los datos en el dominio del negocio se protege a nivel de modelo mediante el principio de encapsulamiento estricto de la POO:

1. **Atributos Protegidos y Acceso Controlado:**
   - Los datos sensibles no se exponen como variables públicas directas, sino como atributos protegidos (`_documento`, `_nombre`, `_telefono`, `_correo`) regulados por decoradores `@property` y `@setter`.
2. **Sanitización y Validación en `Huesped.@documento.setter`:**
   - **Eliminación de espacios superfluos:** Se aplica `strip()` sobre el valor recibido para neutralizar espacios en blanco al inicio o al final.
   - **Verificación de no nulidad y no vacuidad:** Se valida que el valor no sea `None` ni quede como una cadena vacía.
   - **Longitud mínima de consistencia:** Se exige una longitud mínima de 8 caracteres, requerida tanto para un RUT chileno (ej. `12345678-9`) como para números de Pasaporte internacional.
3. **Manejo Controlado de Errores (`ValueError`):**
   - Al detectarse un dato no conforme, el método `@setter` levanta inmediatamente una excepción `ValueError` descriptiva.
   - Esto impide que se construyan objetos en estados inválidos o se almacenen datos corruptos en la persistencia, permitiendo a la capa superior capturar el error y notificar al usuario de forma amigable sin provocar la caída de la aplicación.

---

## 4. Uso de Inteligencia Artificial

Durante el ciclo de desarrollo de la Evaluación N°3, se utilizó Inteligencia Artificial (IA) como copiloto de arquitectura técnica, específicamente al diseñar la comunicación con la API externa de `mindicador.cl` y la persistencia transaccional.

### Caso Concreto: Resiliencia en el Consumo de la API Externa

#### 1. Sugerencia Inicial Entregada por la IA:
La IA propuso inicialmente una implementación estándar y simplificada para consumir la API:
```python
# Propuesta inicial de la IA (descartada por falta de resiliencia):
import requests

def obtener_dolar():
    response = requests.get("https://mindicador.cl/api/dolar")
    data = response.json()
    return data["serie"][0]["valor"]
```

#### 2. Análisis Crítico, Adaptación y Modificaciones Realizadas:
El equipo evaluó la propuesta inicial e identificó múltiples riesgos operacionales:
- **Ausencia de Timeout:** Si el servidor de `mindicador.cl` está caído, sobrecargado o bloquea la conexión, la llamada síncrona `requests.get()` puede quedar colgada indefinidamente, congelando todo el sistema del hotel y afectando la atención de huéspedes.
- **Vulnerabilidad ante caídas de red o JSON inválido:** Si el servicio devuelve un código HTTP 500, un cuerpo HTML de error o formato inesperado, la aplicación arrojaría excepciones no controladas (`KeyError`, `JSONDecodeError`, `ConnectionError`), colapsando la ejecución del sistema.

#### 3. Decisiones Técnicas Adoptadas, Modificadas y Descartadas:
- ✅ **Adoptado:**
  - El endpoint oficial de `mindicador.cl/api/dolar`.
  - La extracción del valor observado a través del primer elemento de la lista `serie`.
- 🛠️ **Modificado y Fortalecido:**
  - **Definición estricta de `timeout=5.0`:** Se fijó un tiempo máximo de espera de 5 segundos para proteger el hilo de ejecución principal.
  - **Encabezado `User-Agent` personalizado:** Para evitar rechazos o bloqueos por firewalls que filtran clientes HTTP no identificados.
  - **Manejo multinivel de excepciones:** Bloque `try/except` que captura específicamente `requests.exceptions.Timeout`, `requests.exceptions.HTTPError`, `requests.RequestException` y errores de parsing (`ValueError`, `KeyError`, `IndexError`).
  - **Mecanismo de Fallback (Graceful Degradation):** En caso de cualquier anomalía de red o API, el sistema emite una advertencia clara por consola y retorna un valor por defecto seguro de **$950.0 CLP**, permitiendo que las reservas, cálculos y conversiones continúen operando con normalidad.
- ❌ **Descartado:**
  - Se descartaron reintentos infinitos (`retry` indefinido) o esperas pasivas sin límite temporal que introdujeran latencia inaceptable para los recepcionistas del hotel.

### Justificación Técnica
La aplicación de patrones de **degradación elegante (Graceful Degradation)** y **diseño tolerante a fallos** asegura que una dependencia externa de red nunca comprometa la estabilidad y disponibilidad de las funciones críticas del negocio hotelero.