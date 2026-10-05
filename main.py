from model.huesped import Huesped
from model.habitacion_individual import HabitacionIndividual
from model.habitacion_doble import HabitacionDoble
from model.habitacion_suite import HabitacionSuite
from model.recepcionista import Recepcionista
from model.camarera_housekeeping import CamareraHousekeeping
from model.reserva import Reserva
from model.servicio import Servicio
from model.medio_pago import MedioPago
from model.indicador_externo import IndicadorExterno
from model.excepciones import HabitacionOcupadaError, AnticipoInsuficienteError

def main():
    print("="*60)
    print("      DEMOSTRACIÓN SISTEMA DE GESTIÓN HOTEL LOS ALERCES      ")
    print("="*60)

    # 1. POLIMORFISMO Y DEMOSTRACIÓN DE SUBTIPOS DE HABITACIÓN
    print("\n--- 1. SUBTIPOS DE HABITACIÓN Y POLIMORFISMO ---")
    hab_ind = HabitacionIndividual(101, 1, 50.0)
    hab_doble = HabitacionDoble(201, 2, 90.0)
    hab_suite = HabitacionSuite(301, 3, 200.0)

    habitaciones = [hab_ind, hab_doble, hab_suite]
    for hab in habitaciones:
        print(f"Habitación {hab.numero}: {hab.obtener_capacidad()}")

    # 2. DEMOSTRACIÓN DE DATO CON VALIDACIÓN (RUT/PASAPORTE)
    print("\n--- 2. CREACIÓN DE HUÉSPED Y VALIDACIÓN DE DOCUMENTO ---")
    try:
        huesped1 = Huesped("12345678-9", "Kevin Rivera", "+56912345678", "kevin@email.com", "12345678-9")
        print(f"Huésped creado exitosamente: {huesped1} | Doc: {huesped1.documento}")
    except ValueError as e:
        print(f"Error de validación: {e}")

    print("\nProbando validación con un documento inválido (menos de 8 caracteres)...")
    try:
        huesped_invalido = Huesped("1-9", "Pedro", "+569000", "p@email.com", "123")
    except ValueError as e:
        print(f"SE CAPTURÓ VALIDACIÓN CORRECTAMENTE: {e}")

    # 3. CREACIÓN DE EMPLEADOS
    print("\n--- 3. PERSONAL Y PERMISOS SEPARADOS ---")
    recepcionista = Recepcionista("11111111-1", "Ana Gomez", "+569111", "ana@hotel.cl", "agomez")
    camarera = CamareraHousekeeping("22222222-2", "Maria Lopez", "+569222", "maria@hotel.cl", "mlopez")
    print(f"Empleado 1: {recepcionista.nombre} - Cargo: {recepcionista.cargo}")
    print(f"Empleado 2: {camarera.nombre} - Cargo: {camarera.cargo}")

    # 4. TRANSACCIÓN CON LÍNEAS DE DETALLE (RESERVA Y CONSUMOS)
    print("\n--- 4. TRANSACCIÓN DE RESERVA Y SERVICIOS ---")
    reserva1 = Reserva(1001, huesped1)
    
    detalle1 = reserva1.agregar_detalle(hab_suite, noches=3, tarifa_noche=200.0)
    print(f"Detalle agregado -> {detalle1}")

    spa = Servicio(1, "Servicio Spa Premium", 45.0)
    minibar = Servicio(2, "Consumo Minibar", 15.0)
    
    reserva1.agregar_consumo(spa, cantidad=1)
    reserva1.agregar_consumo(minibar, cantidad=2)

    print("\nConsumos en la estadía:")
    for c in reserva1.consumos:
        print(f" - {c}")

    total_usd = reserva1.calcular_total_general()
    print(f"Total Reserva en Dólares: ${total_usd} USD")

    dolar = IndicadorExterno(valor_clp=950.0)
    total_clp = dolar.convertir_a_clp(total_usd)
    print(f"Total equivalente en Peso Chileno (Dólar @ ${dolar.valor_clp}): ${total_clp:,.0f} CLP")

    # 5. REGLAS DE NEGOCIO (EXCEPCIONES PROPIAS CAPTURADAS)
    print("\n--- 5. PRUEBA DE REGLAS DE NEGOCIO Y CONTROL DE EXCEPCIONES ---")
    
    print("\n[REGLA 1] Intentando reservar la Habitación 301 que ya está asignada a la Reserva 1001...")
    try:
        reserva_duplicada = Reserva(1002, huesped1)
        reserva_duplicada.agregar_detalle(hab_suite, noches=2, tarifa_noche=200.0)
    except HabitacionOcupadaError as e:
        print(f"EXCEPCIÓN CAPTURADA EXITOSAMENTE (HabitacionOcupadaError):\n -> {e}")

    print("\n[REGLA 2] Intentando hacer Check-In sin registrar el 50% de anticipo...")
    try:
        recepcionista.hacer_check_in(reserva1)
    except AnticipoInsuficienteError as e:
        print(f"EXCEPCIÓN CAPTURADA EXITOSAMENTE (AnticipoInsuficienteError):\n -> {e}")

    print("\nRegistrando pago del 50% de anticipo requerido para corregir la situación...")
    tarjeta = MedioPago(1, "Tarjeta de Crédito")
    print(recepcionista.registrar_pago_reserva(reserva1, monto=300.0, medio_pago=tarjeta))

    print("Reintentando Check-In tras realizar el pago del anticipo...")
    try:
        mensaje_checkin = recepcionista.hacer_check_in(reserva1)
        print(f"ÉXITO: {mensaje_checkin}")
    except AnticipoInsuficienteError as e:
        print(f"Error: {e}")

    print("\n" + "="*60)
    print("   EL PROGRAMA FINALIZÓ SU EJECUCIÓN CONTINUA SIN CAERSE   ")
    print("="*60)

if __name__ == "__main__":
    main()
