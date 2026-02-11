import logging
from src.scrapers.base_scraper import BaseScraper 
from selenium.webdriver.common.by import By


class DobyScraper(BaseScraper):
    def scrape_list_chapters(self):
        try:
            div_element = self.get_element(
                By.CSS_SELECTOR,
                ".eplister"   # una clase está bien
            )

            links = []
            anchors = div_element.find_elements(By.TAG_NAME, "a")

            for a in anchors:
                href = a.get_attribute("href")

                if isinstance(href, str) and href.startswith("http"):
                    links.append(href)

            links = links[2:]
            links.reverse()
            return links

        except Exception as e:
            logging.error(f"[Error Scrape List]: {e}")
            return []
        
    def scrape_chapter(self):
        try:
            content = self.get_element(By.CLASS_NAME, "epcontent", timeout=30).text.strip()
            return content
        except Exception as e:
            logging.error(f"[Error Scrape Chapter]: {e}")
            return ""
        
        
    def scrape(self, url, start=1, end=None):
        try:
            # iniciar driver
            self.start_driver()
            self.driver.get(url)

            chapters = self.scrape_list_chapters()
            # end o no ned
            if end is None:
                end = len(chapters)
            if start is None:
                start = 1

            # bucle sacando todo el texto del cap y almacenarlo
            for i, link in enumerate(chapters[start-1:end],start):
                self.driver.get(link)
                self.wait_random()

                text = self.scrape_chapter()
                logging.info(f"Capitulo {i} extraído.")
                #text = self.format_text(text)
                self.novel_text += text + "\n\n"
            logging.info("Se han extraído todos los capítulos.")
        except Exception as e:
            logging.error(f"[Error Scrape doby]: {e}")
        finally:
            self.close_driver()
            return self.novel_text