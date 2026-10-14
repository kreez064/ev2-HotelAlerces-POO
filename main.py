"""
=============================================================================
SISTEMA DE GESTIÓN HOTELERA - HOTEL LOS ALERCES
Evaluación Sumativa N°3 - Programación Orientada a Objetos y Persistencia
Integrantes: Kevin Rivera y Elias Espinoza
=============================================================================
Demostración completa e integrada:
1. Inicialización automática de la base de datos SQLite (hotel.db).
2. Consumo resiliente de API externa de tipo de cambio (mindicador.cl).
3. Operaciones CRUD completas mediante la capa DAO (HuespedDAO y ReservaDAO).
4. Validación robusta de entradas mediante decoradores @setter en el Modelo.
5. Transacción completa del dominio hotelero (Reserva, Habitaciones, Consumos).
6. Control de reglas de negocio mediante excepciones personalizadas y solución de estados.
7. Finalización continua y robusta sin caídas del sistema.
=============================================================================
"""
import sys

# Asegurar codificación utf-8 en terminales de diferentes sistemas operativos
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dao.conexion import inicializar_bd
from dao.huesped_dao import HuespedDAO
from dao.reserva_dao import ReservaDAO
from services.indicador_service import IndicadorService
from model.huesped import Huesped
from model.habitacion_individual import HabitacionIndividual
from model.habitacion_doble import HabitacionDoble
from model.habitacion_suite import HabitacionSuite
from model.reserva import Reserva
from model.servicios import Servicio
from model.medio_pago import MedioPago
from model.recepcionista import Recepcionista
from model.camarera_housekeeping import CamareraHousekeeping
from model.excepciones import HabitacionOcupadaError, AnticipoInsuficienteError


def main():
    print("=" * 75)
    print("       SISTEMA DE GESTION HOTELERA - HOTEL LOS ALERCES (EVALUACION N°3)")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # 1. INICIALIZACIÓN AUTOMÁTICA DE LA BASE DE DATOS
    # -------------------------------------------------------------------------
    print("\n[1] INICIALIZACION DE LA BASE DE DATOS SQLITE")
    print("-" * 75)
    inicializar_bd()
    print("[OK] Base de datos 'hotel.db' inicializada correctamente.")
    print("[OK] Tablas verificadas/creadas: 'huespedes', 'reservas', 'detalles_reserva'.")

    # -------------------------------------------------------------------------
    # 2. CONSUMO DE API EXTERNA (INDICADOR SERVICE)
    # -------------------------------------------------------------------------
    print("\n[2] CONSUMO DE API EXTERNA (MINDICADOR.CL)")
    print("-" * 75)
    indicador_service = IndicadorService()
    print("Consultando el valor del dolar observado (timeout=5.0 s)...")
    valor_dolar = indicador_service.obtener_valor_dolar()
    print(f"[OK] Tasa de cambio obtenida y aplicada: ${valor_dolar:,.2f} CLP por 1 USD.")

    # -------------------------------------------------------------------------
    # 3. OPERACIONES CRUD EN BASE DE DATOS MEDIANTE CAPA DAO
    # -------------------------------------------------------------------------
    print("\n[3] DEMOSTRACION DE OPERACIONES CRUD CON LA CAPA DAO")
    print("-" * 75)
    huesped_dao = HuespedDAO()
    reserva_dao = ReservaDAO()

    # Pre-limpieza para garantizar repetibilidad en pruebas sucesivas
    huesped_dao.eliminar("99887766-5")
    huesped_dao.eliminar("11223344-5")
    huesped_dao.eliminar("12345678-9")

    # 3.1 C - Create
    print("\n--- 3.1 CREATE (Creacion de Registros) ---")
    huesped1 = Huesped("12345678-9", "Kevin Rivera", "+56912345678", "kevin@hotel.cl", "12345678-9")
    huesped2 = Huesped("11223344-5", "Elias Espinoza", "+56987654321", "elias@hotel.cl", "11223344-5")
    huesped_temp = Huesped("99887766-5", "Huesped Temporal", "+56900000000", "temp@hotel.cl", "99887766-5")

    huesped_dao.crear(huesped1)
    huesped_dao.crear(huesped2)
    huesped_dao.crear(huesped_temp)
    print(f"[OK] Huespedes insertados con exito en la base de datos:")
    print(f"   • {huesped1.nombre} (RUT: {huesped1.rut})")
    print(f"   • {huesped2.nombre} (RUT: {huesped2.rut})")
    print(f"   • {huesped_temp.nombre} (RUT: {huesped_temp.rut})")

    # 3.2 R - Read by ID / RUT
    print("\n--- 3.2 READ (Lectura por Identificador Unico) ---")
    huesped_leido = huesped_dao.obtener_por_rut("12345678-9")
    print(f"[OK] Huesped recuperado por RUT '12345678-9':")
    print(f"   Nombre: {huesped_leido.nombre} | Correo: {huesped_leido.correo} | Telefono: {huesped_leido.telefono}")

    # 3.3 R - Read All
    print("\n--- 3.3 READ ALL (Lectura de Todos los Registros) ---")
    todos = huesped_dao.obtener_todos()
    print(f"[OK] Total de huespedes en base de datos: {len(todos)}")
    for h in todos:
        print(f"   - {h.nombre} | RUT: {h.rut} | Doc: {h.documento}")

    # 3.4 U - Update
    print("\n--- 3.4 UPDATE (Actualizacion de Registros) ---")
    huesped1.telefono = "+56999881122"
    huesped1.correo = "kevin.actualizado@hotel.cl"
    huesped_dao.actualizar(huesped1)
    huesped_actualizado = huesped_dao.obtener_por_rut("12345678-9")
    print(f"[OK] Datos actualizados en BD para '{huesped1.nombre}':")
    print(f"   Nuevo Telefono: {huesped_actualizado.telefono} | Nuevo Correo: {huesped_actualizado.correo}")

    # 3.5 D - Delete
    print("\n--- 3.5 DELETE (Eliminacion Segura con Parametros) ---")
    eliminado = huesped_dao.eliminar("99887766-5")
    print(f"[OK] Registro temporal con RUT '99887766-5' eliminado correctamente: {eliminado}")
    total_despues = len(huesped_dao.obtener_todos())
    print(f"[OK] Total de huespedes restantes en BD: {total_despues}")

    # -------------------------------------------------------------------------
    # 4. DEMOSTRACIÓN DE VALIDACIÓN EN EL MODELO (@documento.setter)
    # -------------------------------------------------------------------------
    print("\n[4] DEMOSTRACION DE VALIDACION EN EL MODELO (RUT / PASAPORTE)")
    print("-" * 75)
    print("Probando instanciacion de huesped con documento invalido (longitud < 8 caracteres)...")
    try:
        huesped_fallido = Huesped("1-9", "Pedro Invalido", "+569000", "p@email.com", "123")
    except ValueError as e:
        print(f"[OK] EXCEPCION CAPTURADA CONTROLADAMENTE (ValueError):")
        print(f"   Detalle: {e}")

    print("\nProbando asignacion de documento vacio mediante @documento.setter...")
    try:
        huesped1.documento = "   "
    except ValueError as e:
        print(f"[OK] EXCEPCION CAPTURADA CONTROLADAMENTE (ValueError):")
        print(f"   Detalle: {e}")

    # -------------------------------------------------------------------------
    # 5. TRANSACCIÓN COMPLETA (RESERVA, HABITACIONES, CONSUMOS Y PERSISTENCIA)
    # -------------------------------------------------------------------------
    print("\n[5] INSTANCIACION DE TRANSACCION COMPLETA DEL DOMINIO")
    print("-" * 75)
    hab_ind = HabitacionIndividual(101, 1, 50.0)
    hab_doble = HabitacionDoble(201, 2, 90.0)
    hab_suite = HabitacionSuite(301, 3, 200.0)

    print("Demostracion de Polimorfismo en Habitaciones:")
    for hab in [hab_ind, hab_doble, hab_suite]:
        print(f"   - Habitacion {hab.numero}: {hab.obtener_capacidad()} | Tarifa base: ${hab.precio_base} USD")

    reserva1 = Reserva(1001, huesped1)
    detalle1 = reserva1.agregar_detalle(hab_suite, noches=3, tarifa_noche=200.0)
    print(f"\n[OK] Detalle anadido a la Reserva #{reserva1.id_reserva}:")
    print(f"   {detalle1}")

    spa = Servicio(1, "Servicio Spa Termal", 45.0)
    minibar = Servicio(2, "Consumo Frigobar Gourmet", 15.0)
    reserva1.agregar_consumo(spa, cantidad=1)
    reserva1.agregar_consumo(minibar, cantidad=2)

    print("[OK] Consumos adicionales agregados a la estadia:")
    for consumo in reserva1.consumos:
        print(f"   - {consumo}")

    total_usd = reserva1.calcular_total_general()
    total_clp = total_usd * valor_dolar
    print(f"\n[OK] Monto Total General Reserva: ${total_usd:,.2f} USD")
    print(f"[OK] Monto Equivalente en Pesos Chilenos (Dolar @ ${valor_dolar:,.2f} CLP): ${total_clp:,.0f} CLP")

    print("\nPersistiendo Reserva y sus lineas de Detalle en SQLite mediante ReservaDAO...")
    reserva_dao.guardar_reserva(reserva1)
    reserva_en_bd = reserva_dao.obtener_por_id(1001)
    print(f"[OK] Reserva #{reserva_en_bd['id_reserva']} persistida exitosamente en SQLite.")
    print(f"   Estado en BD: {reserva_en_bd['estado']} | Total Alojamiento: ${reserva_en_bd['total_alojamiento']} USD")
    print(f"   Lineas de detalle almacenadas en BD: {len(reserva_en_bd['detalles'])}")

    # -------------------------------------------------------------------------
    # 6. PRUEBA DE REGLAS DE NEGOCIO Y EXCEPCIONES PERSONALIZADAS
    # -------------------------------------------------------------------------
    print("\n[6] PRUEBA DE REGLAS DE NEGOCIO Y EXCEPCIONES PERSONALIZADAS")
    print("-" * 75)
    recepcionista = Recepcionista("11111111-1", "Ana Gomez", "+569111", "ana@hotel.cl", "agomez")
    camarera = CamareraHousekeeping("22222222-2", "Maria Lopez", "+569222", "maria@hotel.cl", "mlopez")
    print(f"Personal asignado:")
    print(f"   - {recepcionista.nombre} - Cargo: {recepcionista.cargo}")
    print(f"   - {camarera.nombre} - Cargo: {camarera.cargo}")

    # Regla 1: HabitacionOcupadaError
    print("\n[REGLA DE NEGOCIO 1] Intentando reservar la Habitacion 301 (ya asignada a Reserva 1001)...")
    try:
        reserva_duplicada = Reserva(1002, huesped2)
        reserva_duplicada.agregar_detalle(hab_suite, noches=2, tarifa_noche=200.0)
    except HabitacionOcupadaError as e:
        print("[OK] EXCEPCION CAPTURADA EXITOSAMENTE (HabitacionOcupadaError):")
        print(f"   {e}")

    # Regla 2: AnticipoInsuficienteError
    print("\n[REGLA DE NEGOCIO 2] Intentando Check-In sin cumplir el 50% de anticipo minimo...")
    try:
        recepcionista.hacer_check_in(reserva1)
    except AnticipoInsuficienteError as e:
        print("[OK] EXCEPCION CAPTURADA EXITOSAMENTE (AnticipoInsuficienteError):")
        print(f"   {e}")

    # Solución de estado: Pago de anticipo
    anticipo_requerido = reserva1.calcular_total_alojamiento() * 0.5
    print(f"\n[SOLUCION DE ESTADO] Registrando pago del anticipo exigido (${anticipo_requerido:,.2f} USD)...")
    tarjeta = MedioPago(1, "Tarjeta de Credito Corporativa")
    mensaje_pago = recepcionista.registrar_pago_reserva(reserva1, monto=anticipo_requerido, medio_pago=tarjeta)
    print(f"[OK] {mensaje_pago}")

    print("\nReintentando Check-In con el anticipo satisfecho...")
    try:
        mensaje_checkin = recepcionista.hacer_check_in(reserva1)
        print(f"[OK] {mensaje_checkin}")

        # Sincronización del nuevo estado en la base de datos
        reserva_dao.guardar_reserva(reserva1)
        reserva_actualizada = reserva_dao.obtener_por_id(1001)
        print(f"[OK] Base de datos sincronizada: Reserva #{reserva_actualizada['id_reserva']} en estado '{reserva_actualizada['estado']}'.")
    except AnticipoInsuficienteError as e:
        print(f"Falla inesperada: {e}")

    # -------------------------------------------------------------------------
    # 7. MENSAJE FINAL CONFIRMANDO EJECUCIÓN SIN CAÍDAS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("       EL PROGRAMA FINALIZÓ SU EJECUCIÓN CONTINUA SIN CAÍDAS       ")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
