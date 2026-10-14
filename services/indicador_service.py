"""
Módulo de servicios para consumo de indicadores económicos externos.
Permite obtener información financiera en tiempo real, como el valor del dólar observado.
"""
from typing import Optional
import requests


class IndicadorService:
    """
    Servicio encargado de consultar APIs externas de indicadores económicos
    con mecanismos de resiliencia (timeout controlado, captura de excepciones y valor por defecto).
    """
    URL_DOLAR = "https://mindicador.cl/api/dolar"
    VALOR_POR_DEFECTO = 950.0
    TIMEOUT = 5.0

    def __init__(self, url: Optional[str] = None, timeout: float = TIMEOUT, valor_por_defecto: float = VALOR_POR_DEFECTO):
        self.url = url or self.URL_DOLAR
        self.timeout = timeout
        self.valor_por_defecto = valor_por_defecto

    def obtener_valor_dolar(self) -> float:
        """
        Consulta el tipo de cambio del dólar en CLP desde mindicador.cl.
        
        Aplica timeout=5.0 s y captura cualquier excepción (requests.RequestException,
        timeout de red, errores de estado HTTP o respuestas con JSON inválido).
        
        En caso de fallo, emite un aviso en consola y retorna el valor por defecto ($950.0 CLP)
        para asegurar que el flujo del sistema hotelero continúe sin caídas.
        
        :return: Valor del dólar en pesos chilenos (float).
        """
        try:
            headers = {
                "User-Agent": "HotelLosAlercesApp/1.0 (SistemaGestionHotelera; Python/requests)"
            }
            # Consulta a la API con timeout crítico de 5.0 segundos
            response = requests.get(self.url, headers=headers, timeout=self.timeout)
            
            # Valida código de respuesta HTTP (lanza HTTPError si status no es 2xx)
            response.raise_for_status()
            
            # Procesa la estructura JSON de la respuesta
            datos = response.json()
            serie = datos.get("serie", [])
            
            if not serie or not isinstance(serie, list) or "valor" not in serie[0]:
                raise ValueError("Estructura JSON inválida: falta el campo 'serie' o 'valor'.")
            
            valor_dolar = float(serie[0]["valor"])
            return valor_dolar

        except requests.exceptions.Timeout as e:
            print(f"[AVISO IndicadorService] Tiempo de espera agotado al consultar API mindicador.cl ({e}). "
                  f"Se usará valor de respaldo: ${self.valor_por_defecto} CLP.")
            return self.valor_por_defecto

        except requests.exceptions.HTTPError as e:
            print(f"[AVISO IndicadorService] Error HTTP al consultar API mindicador.cl ({e}). "
                  f"Se usará valor de respaldo: ${self.valor_por_defecto} CLP.")
            return self.valor_por_defecto

        except (requests.RequestException, ValueError, KeyError, IndexError) as e:
            print(f"[AVISO IndicadorService] Falla en la comunicación o procesamiento de la API ({e}). "
                  f"Se usará valor de respaldo: ${self.valor_por_defecto} CLP.")
            return self.valor_por_defecto
