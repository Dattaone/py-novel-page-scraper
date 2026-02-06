import time
import logging
import random
import shutil
import tempfile
import winreg
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from text_processor import TextProcessor

class BaseScraper:
    """Clase base con la lógica común para scrapers con Selenium."""

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.novel_text = ""
        self.tp = TextProcessor()

    def find_chrome_version():
        
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Google\Chrome\BLBeacon"
        )

        version, _ = winreg.QueryValueEx(key, "version")
        return version.split(".")[0]


    def start_driver(self):
        """Inicia el navegador con configuraciones comunes."""
        import os

        # borrar esto sino funca
        udc_profile = os.path.join(os.getenv("APPDATA"), "undetected_chromedriver")

        if os.path.exists(udc_profile):
            shutil.rmtree(udc_profile)
        #y tambien esto
        self.temp_profile = tempfile.mkdtemp()


        options = uc.ChromeOptions()

        # genera User-Agent aleatorio
        try:
            ua = UserAgent()
            self.user_agent = ua.random
            logging.info(f"🕵️ Usando User-Agent aleatorio: {self.user_agent}")
        except Exception as e:
            self.user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
            logging.warning(f"No se pudo generar User-Agent dinámico: {e}")
            logging.info(f"Usando User-Agent por defecto: {self.user_agent}")

        options.add_argument(f"user-agent={self.user_agent}")

        #aqui se mete lo de ariba, asi que tambien sino funca eliminar
        options.add_argument(f"--user-data-dir={self.temp_profile}")

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-application-cache")

        version = self.find_chrome_version()

        
        self.driver = uc.Chrome(options=options, version_main=version)


    def close_driver(self):
        """Cierra el navegador por completo y libera archivos."""

        # Intentar cerrar el driver correctamente
        try:
            if getattr(self, "driver", None):
                self.driver.delete_all_cookies()  # <- limpia cookies si aún está abierto
                self.driver.quit()
        except:
            pass
        
        # Asegurar que Python ya no tiene referencia
        self.driver = None

        # Borrar perfil temporal si existe
        temp_profile = getattr(self, "temp_profile", None)
        if temp_profile:
            try:
                shutil.rmtree(temp_profile, ignore_errors=True)
            except:
                pass

        # Dar tiempo a Windows para liberar los archivos
        time.sleep(1.5)



    def get_element(self, by, value, timeout=30):
        """Espera a que un elemento aparezca y lo devuelve."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )


    def get_elements(self, by, value, timeout=20):
        """Devuelve una lista de elementos."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((by,value))
        )

    def click_element(self, by, value, timeout=30):
        try:
            old_url = self.driver.current_url
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            ).click()

            new_url = self.driver.current_url
            if old_url == new_url:
                logging.warning("El clic no tuvo efecto - la URL no cambió.")
                return False
            
            return True
        except Exception as e:
            logging.info(f"Error al intenter clickear el elemento: {e}")
            return False



    def wait_random(self, min_seconds=1, max_seconds=3):
        """Pausa aleatoria para simular comportamiento humano."""
        time.sleep(random.uniform(min_seconds, max_seconds))


    def scrape(self, url: str):
        """Método abstracto para que las subclases lo implementen."""
        raise NotImplementedError("Las subclases deben implementar este método.")

