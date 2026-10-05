class IndicadorExterno:
    def __init__(self, fuente="Banco Central de Chile", moneda_origen="USD", valor_clp=950.0):
        self.fuente = fuente
        self.moneda_origen = moneda_origen
        self.valor_clp = valor_clp

    def convertir_a_clp(self, monto_usd):
        return monto_usd * self.valor_clp
