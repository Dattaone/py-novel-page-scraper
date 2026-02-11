import requests
import random

# Lista de proxies
proxies_list = [
    'http://157.254.53.50:80',
    'http://72.10.160.173:7003',
    'http://18.223.25.15:80',
    'http://197.255.126.69:80',
    'http://13.38.153.36:80',
]

# URL objetivo
url = 'https://www.ddxs.com/manweilidewaiguawanjia/'

# Encabezados
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36',
}

# Probar proxies
for proxy in proxies_list:  
    try:
        print(f"Usando proxy: {proxy}")
        proxies = {'http': proxy, 'https': proxy}
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        print("¡Solicitud exitosa!")
        print(response.text[:500])  # Muestra solo los primeros 500 caracteres
        break  # Sal del bucle si funciona
    except requests.exceptions.RequestException as e:
        print(f"Proxy fallido ({proxy}): {e}")











# https://www.ddxs.com/manweilidewaiguawanjia/
""" from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecución sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")

service = Service(ChromeDriverManager().install())

# Iniciar el navegador
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.ddxs.com/manweilidewaiguawanjia/")

# Obtener el contenido
html = driver.page_source
print(html)
driver.quit()
 """


""" cookies = {
    'HMACCOUNT': '39B8878C14DA7E38',
    "Hm_lpvt_120ab3aad23c26d06ff4fefe5da67bc2": "1738021510",
    "Hm_lvt_120ab3aad23c26d06ff4fefe5da67bc2": "1738021510",
    "cf_clearance": ".6DTlttXPap1g.VQqxZAJ72mFCe6hdOO4jCKT_WR7Gc-1738021513-1.2.1.1-.lIXc8oR9YJGZIBNdCtmxQwVqPxctgnuBqV9YMTACMQwPlKmR4QSpOgN6ulE5XTspdokCmRo_BWxPwNfEA6.AzT6rYefm51OiwrvVhN1RHQKwmeSgcP0KB2OB9irlzOWBE8KC7jK0xi3Ipr9egrPwKc3zNvareVDpAsQpY1.SfjmItzE6Ix6zni.Zg3ZMw5YPOGSSJRw3MF6Vq1_Qzb9jqnJ9BioT9686cGsTfPIniWLMpgKtVPmIiVow80._Lst5kSDq_zps83GuHTMMs663Q1q8MkiNsEUCLcu7vBD4Qo"
} """