from .empleado import Empleado

class Recepcionista(Empleado):
    def __init__(self, rut, nombre, telefono, correo, usuario):
        super().__init__(rut, nombre, telefono, correo, "Recepcionista", usuario)

    def hacer_check_in(self, reserva):
        reserva.realizar_check_in()
        return f"Check-in realizado con éxito por recepcionista {self.nombre} para la Reserva #{reserva.id_reserva}."

    def registrar_pago_reserva(self, reserva, monto, medio_pago):
        pago = reserva.registrar_pago(monto, medio_pago)
        return f"Pago de ${monto} USD registrado con {medio_pago.nombre} por {self.nombre}."
