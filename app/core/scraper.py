import requests
from typing import Optional
from bs4 import BeautifulSoup

from app.settings import Config
from app.app_log import get_logger

logger = get_logger(f"[{Config().APP_NAME} - Scraper Module]")

class ClimaScrap():
    """Clase del objeto scraper para scrapear el clima del día"""

    def __init__(self):
        self.url = Config().URL_BASE
        self.soup = self._get_soup()

    def _get_soup(self) -> Optional[BeautifulSoup]:
        """Obtiene y parsea el HTML de la página del clima."""
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Error al obtener la página del clima: {e}")
            return None

    def _get_card(self) -> Optional[BeautifulSoup]:
        """Busca el card con la información del clima en un objeto de BeautifulSoup"""

        try:
            card = self.soup.find(
                "div", 
                {"class": "CurrentConditions--body--r20G9"}
            )
            logger.debug(f"Obteniendo card de la sopa")

            return card
        except Exception as e:
            logger.error(f"Error al obtener el card en la página: {e}")
            return None

    def get_temperature_average(self) -> Optional[str]:
        """Obtiene la temperatura promedio"""

        try:
            card = self._get_card()
            temperatura_promedio = card.find("span", {"class": "CurrentConditions--tempValue--zUBSz"})
            logger.debug(f"Obteniendo temperatura promedio de la sopa")
            return temperatura_promedio.text
        except Exception as e:
            logger.error(f"Error al obtener la temperatura promedio: {e}")
            return None

    def clima_del_dia(self) -> Optional[str]:
        """Obtiene la previsión del clima del día"""
        try:
            card = self._get_card()
            clima = card.find("div", {"class": "CurrentConditions--phraseValue---VS-k"})
            logger.debug(f"Obteniendo clima del día de la sopa")
            return clima.text
        except Exception as e:
            logger.error(f"Error al obtener el clima del día: {e}")
            return None

    def obtener_temperatura_en_el_dia(self) -> Optional[str]:
        """Obtiene la temperatura promedio"""
        try:
            card = self._get_card()
            temperatura_promedio = card.find("div", {"class": "CurrentConditions--tempHiLoValue--Og9IG"})
            logger.debug(f"Obteniendo temperatura promedio del día de la sopa")
            return temperatura_promedio.text
        except Exception as e:
            logger.error(f"Error al obtener la temperatura promedio del día: {e}")
            return None

    def obtener_temperatura_en_el_noche(self) -> Optional[str]:
        """Obtiene la temperatura promedio"""
        try:
            card = self._get_card()
            temperatura_promedio = card.find("span", {"data-testid": "TemperatureValue"})
            logger.debug(f"Obteniendo temperatura promedio de la noche de la sopa")
            return temperatura_promedio.text
        except Exception as e:
            logger.error(f"Error al obtener la temperatura promedio de la noche: {e}")
            return None