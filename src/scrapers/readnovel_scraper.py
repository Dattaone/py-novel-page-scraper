import logging
from selenium.webdriver.common.by import By
from src.scrapers.base_scraper import BaseScraper

class ReadnovelScraper(BaseScraper):
    def scrape_list_chapters(self):
        try:
            div_element = self.get_element(By.CLASS_NAME, "panel-body")
            logging.info(div_element)
            links = div_element.find_elements(By.CSS_SELECTOR, "div div ul li a")
            return [a.get_attribute("href") for a in links]
        except Exception as e:
            logging.error(f"Error al extraer la lista: {e}")
            return []
        
    def scrape_chapter(self):
        try:
            content = self.get_element(By.ID, "chr-content").text.strip()

            return content
        except Exception as e:
            logging.error(f"Error al extraer Capítulo: {e}")
            return ""
    
    def scrape(self, url:str, start=None, end=None):
        try:
            self.start_driver()
            self.driver.get(url)
            links = self.scrape_list_chapters()
            first_chapter = links[0]

            self.driver.get(first_chapter)
            conter = 1
            while True:
                
                self.novel_text += self.scrape_chapter()
                self.novel_text += "\n\n"
                logging.info(f"Capítulo {conter} extraído.")
                conter += 1 
                if not self.click_element(By.ID, "next_chap"):
                    break
                
        except Exception as e:
            logging.error(f"Error al extraer: {e}")
        finally:
            self.close_driver()
            return self.novel_text