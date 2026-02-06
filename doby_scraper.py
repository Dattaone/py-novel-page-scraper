import logging
from base_scraper import BaseScraper 
from selenium.webdriver.common.by import By


class DobyScraper(BaseScraper):
    def scrape_list_chapters(self):
        try:
            # extraer todo ul
            div_element = self.get_element(By.CLASS_NAME, "eplister eplisterfull")
            uls = div_element.find_elements(By.TAG_NAME, "ul")
            links = []

            for link in links :
                href = link.get_attribute("href")
                links.append(href)

            # elminir last and first
            links = links[2:]

            links.reverse()
            return links

        except Exception as e:
            logging.error(f"Error al extraer la lista: {e}")
            return []
        
    def scrape_chapter(self):
        try:
            content = self.get_element(By.CLASSS_NAME, "epcontent entry-content", timeout=30).text.strip()
            return content
        except Exception as e:
            logging.error(f"Error al extraer capítulo(scrape_chapter) {e}")
            return ""
        
        
    def scrape(self, url, start=None, end=None):
        try:
            # iniciar driver
            self.start_driver()
            # entrar a url
            self.driver.get(url)
            # extraer lista de capitulos links
            chapters = self.scrape_list_chapters()
            # end o no ned
            if end is None:
                end = len(chapters)
            if start is None:
                start = 1
            # bucle sacando todo el texto del cap y almacenarlo
            for _, link in enumerate(chapters[start-1:end],start):
                self.wait_random()
                self.driver.get(link)

                text = self.scrape_chapter()
                #text = self.format_text(text)
                self.novel_text += text + "\n\n"
            logging.info("Final scrape function")
        except Exception as e:
            logging.error(f"Error general en scrape: {e}")
        finally:
            self.close_driver()
            return self.novel_text