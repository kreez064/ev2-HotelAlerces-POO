# 🏨 Sistema de Gestión Hotelera - Hotel Los Alerces
**Evaluación 2 - Programación Orientada a Objetos (POO)**

Este proyecto consiste en el desarrollo de un sistema integral de gestión para el **Hotel Los Alerces**, desarrollado en Python aplicando los principios fundamentales de la **Programación Orientada a Objetos (POO)**, modularidad, diseño desacoplado y buenas prácticas de desarrollo.

---

## 📌 Descripción del Proyecto

El sistema modela las operaciones clave de un hotel, incluyendo la administración de habitaciones, gestión de reservas, control de consumos adicionales durante la estadía, procesamiento de pagos con anticipos mínimos y asignación de roles para el personal (recepcionistas y servicio de limpieza/housekeeping).

---

## 🚀 Pilares y Conceptos de POO Aplicados

### 1. Herencia y Jerarquía de Clases
- **Jerarquía de Personas y Empleados:**
  - `Persona` (Clase Base): Define atributos comunes como RUT, nombre, teléfono y correo.
  - `Huesped` (Especialización): Hereda de `Persona` e incorpora validación de documento (RUT / Pasaporte).
  - `Empleado` (Especialización): Extiende a `Persona` añadiendo cargo y usuario.
  - `Recepcionista` y `CamareraHousekeeping`: Subclases de `Empleado` con responsabilidades específicas (gestión de check-in / pagos y cambio de estado de limpieza de habitaciones, respectivamente).
- **Jerarquía de Habitaciones:**
  - `Habitacion` (Clase Base): Define número, piso, precio base y disponibilidad.
  - Subclases polimórficas: `HabitacionIndividual`, `HabitacionDoble` y `HabitacionSuite`.

### 2. Polimorfismo
- Cada tipo de habitación sobrescribe o implementa el método `obtener_capacidad()`, permitiendo un comportamiento dinámico según el tipo específico de habitación instanciada.

### 3. Encapsulamiento
- Todos los atributos internos de las clases se manejan de manera privada/protegida (convención `_atributo`) y se exponen de forma segura mediante decoradores `@property` de Python, evitando la modificación directa e inconsistente del estado de los objetos.

### 4. Composición y Agregación
- La clase `Reserva` coordina múltiples entidades del dominio:
  - **Líneas de detalle:** `DetalleReserva` (habitación asociada, noches y subtotal).
  - **Consumos de servicios:** `Consumo` asociado a un `Servicio` (minibar, spa, etc.).
  - **Transacciones de pago:** `Pago` asociado a un `MedioPago` (tarjeta, efectivo, transferencia).

### 5. Reglas de Negocio y Manejo de Excepciones Personalizadas
- **`HabitacionOcupadaError`:** Impide reservar una habitación que ya se encuentra ocupada o asignada a otra reserva activa.
- **`AnticipoInsuficienteError`:** Bloquea la operación de *check-in* si el huésped no ha pagado al menos el 50% del total del alojamiento.
- **Validación de Datos:** Validación de longitud mínima y consistencia en el documento de identidad del huésped (`ValueError`).

### 6. Integración de Indicadores Externos
- Clase `IndicadorExterno` que permite la conversión de tarifas y consumos expresados en dólares (USD) a pesos chilenos (CLP) en base al tipo de cambio de referencia.

---

## 📁 Estructura del Repositorio

```text
ev2-HotelAlerces-POO/
├── README.md                   # Documentación general del proyecto
├── main.py                     # Script principal de prueba y demostración
└── model/                      # Paquete con los módulos y modelos del sistema
    ├── __init__.py             # Inicializador del paquete model
    ├── persona.py              # Clase base Persona
    ├── huesped.py              # Clase Huesped con validación de documento
    ├── empleado.py             # Clase base Empleado
    ├── recepcionista.py        # Clase Recepcionista (check-in, pagos)
    ├── camarera_housekeeping.py# Clase CamareraHousekeeping (gestión limpieza)
    ├── habitacion.py           # Clase base Habitacion
    ├── habitacion_individual.py# Subtipo Habitación Individual
    ├── habitacion_doble.py     # Subtipo Habitación Doble
    ├── habitacion_suite.py     # Subtipo Habitación Suite
    ├── detalle_reserva.py      # Detalle de estadía y tarifas
    ├── servicio.py             # Servicios adicionales disponibles (spa, minibar, etc.)
    ├── consumo.py              # Registro de consumo de servicios
    ├── medio_pago.py           # Medios de pago aceptados
    ├── pago.py                 # Registro de transacciones de pago
    ├── indicador_externo.py    # Conversor de moneda externa (USD -> CLP)
    ├── reserva.py              # Entidad transaccional Reserva
    └── excepciones.py          # Excepciones personalizadas del negocio
```

---

## 💻 Instrucciones de Ejecución

Para ejecutar la demostración completa del sistema y verificar el cumplimiento de todas las reglas de negocio y captura de excepciones:

```bash
python main.py
```

### 📋 Flujo de la Demostración (`main.py`):
1. **Demostración de Polimorfismo:** Instanciación y consulta de capacidades en diferentes subtipos de habitación.
2. **Validación de Huéspedes:** Creación correcta de huésped y captura controlada de documento inválido.
3. **Roles y Permisos de Empleados:** Asignación de tareas según el rol (Recepcionista / Camarera).
4. **Transacción Completa:** Creación de reserva, adición de noches en suite, consumos adicionales (Spa y Minibar) y cálculo del total en USD y CLP.
5. **Control de Reglas de Negocio:**
   - Intento fallido de reservar una habitación ya ocupada (*HabitacionOcupadaError* capturada).
   - Intento fallido de realizar *check-in* sin el 50% de anticipo (*AnticipoInsuficienteError* capturada).
   - Registro del pago requerido y confirmación exitosa del *check-in*.