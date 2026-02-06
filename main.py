import logging
from shuba_scraper import ShubaScraper
from readnovel_scraper import ReadnovelScraper
from wtr_scraper import WtrScraper
from keyboard_interface import KeyboardInterface
from text_processor import TextProcessor


# Configuración del log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ki = KeyboardInterface()
tp = TextProcessor()


def run_scraper(scraper_class, headless=True, needs_chapter_range=False, url_modifier=None):
    """
    Ejecuta un scraper genérico según el tipo de clase pasada.

    Args:
        scraper_class: Clase del scraper a utilizar.
        needs_chapter_range (bool): Indica si el scraper permite definir rango de capítulos.
        url_modifier (callable): Función opcional que modifica la URL antes de usarla.
    """
    novel = ""
    try:
        scraper = scraper_class(headless=headless)

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
        
        novel = scraper.scrape(url, start=start, end=end)
        
        # Guardar resultados
        logging.info("Creando el Docx espere....")
        tp.create_docx_from_text(novel, f"{filename}.docx")
    except KeyboardInterrupt:
        logging.warning("⛔ Scrapeo interrumpido por el usuario.")
        try:
            # Intentar recuperar texto parcial del scraper
            partial = getattr(scraper, "novel_text", "")
            if partial:
                tp.create_text_file(partial, "novel_autosave.txt")
                logging.info("⚠️ Se guardó una copia de seguridad en 'novel_autosave.txt'.")
            else:
                logging.info("No había progreso que guardar.")
        except Exception as e:
            logging.error(f"No se pudo guardar el progreso: {e}")
    except Exception as e:
        logging.error(f"❌ Error inesperado: {e}")
        if novel:
            tp.create_text_file(novel, "novel_autosave.txt")
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


def main():
    """Selector principal entre los diferentes scrapers."""
    ki.clear()
    option = ki.vertical_select(
        "📚 Selecciona la fuente de la novela:\n",
        ["Shuba", "ReadNovel", "WTR-Lab"]
    )

    if option.lower() == "shuba":
        run_scraper(ShubaScraper, headless=False, needs_chapter_range=True, url_modifier=modify_shuba_url)
    elif option.lower() == "readnovel":
        run_scraper(ReadnovelScraper, headless=True, needs_chapter_range=False, url_modifier=modify_readnovel_url)
    elif option.lower() == "wtr-lab":
        run_scraper(WtrScraper, headless=False, needs_chapter_range=False)


if __name__ == "__main__":
    main()
    input("\n Presiona Enter para salir...")
