import logging
from src.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By


class CzbookScraper(BaseScraper):
    def scrape_list_chapters(self):
        try:
            ul_element = self.get_element(By.ID, "chapter-list")
            links = []
            anchors = ul_element.find_elements(By.TAG_NAME, "a")

            for a in anchors:
                href = a .get_attribute("href")

                if isinstance(href, str) and href.startswith("http"):
                    links.append(href)

            return links
        except Exception as e:
            logging.error(f"[Error Scrape List Chapters]: {e}")
            return []
        
    def scrape_chapter(self):
        try:
            el = self.get_element(By.CSS_SELECTOR, ".content", timeout=30)
            html = el.get_attribute("innerHTML")
            logging.info(html[:500])
            return el.text
        except Exception as e:
            logging.error(f"[Error Scrape Chapter]: {e}")
    
    def scrape(self, url, start=1, end=None):
        try:
            self.start_driver()
            self.driver.get(url)
            self.wait_random()

            chapters = self.scrape_list_chapters()

            if end is None:
                end = len(chapters)
            if start is None:
                start = 1

            for i, link in enumerate(chapters[start-1:end],start):
                self.driver.get(link)
                self.wait_random()

                text = self.scrape_chapter()
                logging.info(f"Capitulo {i} extraído.")
                self.set_novel_text(text + "\n\n")

                
            logging.info("Se extrajeron todos los capítulos.")
        except Exception as e:
            logging.error(f"[Error Scrape czbooks]: {e}")
        finally:
            self.close_driver()
            return ""
