import logging
from src.scrapers.shuba_scraper import ShubaScraper
from src.scrapers.readnovel_scraper import ReadnovelScraper
from src.scrapers.wtr_scraper import WtrScraper
from src.scrapers.doby_scraper import DobyScraper
from src.scrapers.czbooks_scraper import CzbookScraper
from src.ui.keyboard_interface import KeyboardInterface
from src.services.text_processor import TextProcessor


# Configuración del log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


SCRAPERS = {
    "shuba": {
        "class": ShubaScraper,
        "headless": False,
        "needs_chapter_range": True,
        "url_modifier": modify_shuba_url
    },
    "readnovel": {
        "class": ReadnovelScraper,
        "headless": True,
        "needs_chapter_range": False,
        "url_modifier": modify_readnovel_url
    },
    "wtr": {
        "class": WtrScraper,
        "headless": False,
        "needs_chapter_range": False,
        "url_modifier": None
    },
    "czbooks": {
        "class": CzbookScraper,
        "headless": False,
        "needs_chapter_range": True,
        "url_modifier": None
    },
    "doby": {
        "class": DobyScraper,
        "headless": True,
        "needs_chapter_range": True,
        "url_modifier": None
    },
}


def get_user_input(needs_chapter_range=False, url_modifier=None):
    """
    Obtiene la entrada del usuario para configurar el scraper.
    """
    
    ki.clear()
    url = ki.get_input_url()
    if url_modifier:
        url = url_modifier(url)

    filename = ki.get_input_filename()

    start = end = None
    if needs_chapter_range:
        option = ki.horizontal_select()
        if option == "No":
            start, end = ki.get_chapter_range()

    return url, filename, start, end

def run_scraper(scraper_class, headless=True, needs_chapter_range=False, url_modifier=None):
    """
    Ejecuta un scraper genérico según el tipo de clase pasada.

    Args:
        scraper_class: Clase del scraper a utilizar.
        needs_chapter_range (bool): Indica si el scraper permite definir rango de capítulos.
        url_modifier (callable): Función opcional que modifica la URL antes de usarla.
    """
    
    try:
        scraper = scraper_class(headless=headless)

        url, filename, start, end = get_user_input(needs_chapter_range, url_modifier)
        
        novel = scraper.scrape(url, start=start, end=end)

        if not novel.strip():
            raise Exception("⚠️ El texto está vacío. No se creará el documento.")
        
        # Guardar resultados
        logging.info("Creando el Docx espere....")
        tp.create_docx_from_text(novel, f"{filename}.docx")
        
        option = ki.horizontal_select("¿También quieres crear un archivo de texto?", ["No", "Si"])
        if option == "Si":
            tp.create_text_file(novel, f"{filename}.txt")
    except Exception as e:
        logging.error(f"❌ [Error en run_scraper]: {e}")
        partial = scraper.get_novel_text()
        if partial:
            tp.create_text_file(partial, "novel_autosave.txt")
            logging.warning("⚠️ Se guardó una copia de seguridad en 'novel_autosave.txt'.")
    finally:
        if scraper and hasattr(scraper, "close_driver"):
            scraper.close_driver()
    

def modify_shuba_url(url: str) -> str:
    """Ajusta URLs que terminan en .html/.htm para Shuba."""
    if url.endswith(".html") or url.endswith(".htm"):
        return url.rsplit(".", 1)[0] + "/"
    return url


def modify_readnovel_url(url: str) -> str:
    """Ajusta URLs para ReadNovel."""
    if not url.endswith(".html"):
        return url.rsplit("#", 1)[0] + "#tab-chapter-title"
    return url + "#tab-chapter-title"


def main(ki: KeyboardInterface, tp: TextProcessor):
    """Selector principal entre los diferentes scrapers."""
    ki.clear()
    option = ki.vertical_select(
        "📚 Selecciona la fuente de la novela:\n",
        ["Shuba", "ReadNovel", "WTR-Lab", "CzBooks", "Doby"]
    )
    
    config = SCRAPERS[option.lower()]
    run_scraper(**config)


if __name__ == "__main__":
    ki = KeyboardInterface()
    tp = TextProcessor()
    main(ki, tp)
    input("\n Presiona Enter para salir...")
