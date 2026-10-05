class Pago:
    def __init__(self, monto_usd, medio_pago):
        self._monto_usd = monto_usd
        self._medio_pago = medio_pago

    @property
    def monto(self):
        return self._monto_usd

    @property
    def medio_pago(self):
        return self._medio_pago
