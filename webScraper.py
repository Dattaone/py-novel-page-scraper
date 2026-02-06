import chardet
import logging
import os
import requests
import random
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import Optional, List

import requests.compat

# Configura el logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def get_random_headers():
    try:
        user_agent = UserAgent().random
    except Exception:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    return {'User-Agent': user_agent}

def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    try:
        response = requests.get(url, headers=get_random_headers(), timeout=timeout)
        response.raise_for_status()

        # Detect codifiked Chinesse or not
        detected = chardet.detect(response.content)
        response.encoding = detected['encoding'] or 'utf-8'
        return response.text
    except requests.exceptions.RequestException as err:
        logging.error(f"Error fetching {url}: {err}")
        return None

def extract_links(soup: BeautifulSoup, url: str, tag: str, class_: Optional[str] = None, id_: Optional[str] = None) -> List[str]:
    kwargs = {}
    if class_:
        kwargs['class_'] = class_
    if id_:
        kwargs['id'] = id_
    container = soup.find(tag, **kwargs)

    links = []
    for a in container.find_all('a', href=True):
        href = a['href']
        if href.startswith('/'):
            href = f"{get_base_url(url)}{href}"
        links.append(href)
    return links

def get_base_url(url):
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def extract_text(soup: BeautifulSoup, tag: str, class_: Optional[str] = None, id_: Optional[str] = None) -> List[str]:
    kwargs = {}
    if class_:
        kwargs['class_'] = class_
    if id_:
        kwargs['id'] = id_

    elements = soup.find_all(tag, **kwargs)
    return [e.get_text(separator="\n", strip=True) for e in elements if e.get_text(strip=True)]

def delete_file_if_exists(filename: str) -> bool:
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False

def save_text_file(filename: str, text_list: List[str]):
    if delete_file_if_exists(filename):
        logging.info(f"Archivo existente '{filename}' eliminado.")
    with open(filename, 'w', encoding='utf-8') as f:
        for line in text_list:
            f.write(line + "\n")
    logging.info(f"Archivo guardado: {filename}")

def extract_title(soup: BeautifulSoup, tag: str, class_: str) -> str:
    title_tag = soup.find(tag, class_=class_)
    return title_tag.get_text(strip=True) if title_tag else False



def scrape_novel(
    url: str,
    filename: str,
    tag_links: str,
    class_links: Optional[str],
    tag_content: str,
    class_content: Optional[str],
    tag_title: Optional[str] = None,
    class_title: Optional[str] = None,
    sleep_range: tuple = (1, 3)
):
    links = []
    for i in range(20):
        links.append(f"https://wtr-lab.com/es/serie-25922/douluo-peerless-how-did-i-become-an-evil-soul-master/chapter-{i+1}")
    
    all_text = []
    chapter_count = 1
    for link in links:
        full_url = requests.compat.urljoin(url,link)
        html = fetch_url(full_url)
        if html is None:
            logging.warning(f"No se pudo obtener la subpágina: {full_url}")
            continue

        #if chapter_count > 5: break

        soup = BeautifulSoup(html, 'html.parser')
        texts = extract_text(soup, tag_content, class_content)

        title = extract_title(soup, tag_title, class_title) if tag_title else f"Capítulo {chapter_count}"
        title = title if title else f"Capítulo {chapter_count}"

        for text in texts:
            if text and text.strip() and text not in all_text:
                all_text.append(f"{title}: ")
                all_text.append(text.strip())
                all_text.append("\n")

        delay = random.uniform(*sleep_range)
        logging.info(f"Esperando {delay:.2f} segundos antes del siguiente request...")
        time.sleep(delay)
        chapter_count += 1
    
    save_text_file(filename, all_text)


# ------------------- USO ------------------------

if __name__ == "__main__":
    scrape_novel(
        url= "https://wtr-lab.com/es/serie-25922/douluo-peerless-how-did-i-become-an-evil-soul-master?tab=toc",
        filename       = "prueba.txt",
        tag_links       = "div",
        class_links     = "toc-list accordion-body",
        tag_content     = "div",
        class_content   = "chapter-body menu-target font-nunito fs-16 lh-150  terms-bold",
        tag_title       = "h3",
        class_title     = "chapter-title"
    )


    """ scrape_list_of_novel(
        url="https://ixdzs8.com/sort/",
        filename="novela.txt",
        conter=18,
        tag_content="li",
        class_content="burl"
    ) """

    """ scrape_novels(
        url="https://jpxs123.com/tongren/index_11.html",
        filename="novela.txt",
        tag_links="div",
        class_links="page",
        tag_content="div",
        class_content="infos"
    ) """

    """ scrape_description_novels(
        url="https://jpxs123.com/tongren/2865.html",
        filename="naruto.txt",
        tag_links="ul",
        class_links="clearfix",
        tag_content="div",
        class_content="read_chapterDetail",
        tag_title="h1",
        class_title=""
    ) """