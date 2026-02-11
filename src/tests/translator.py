from deep_translator import GoogleTranslator
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TextTranslator:
    def __init__(self, target_lang='es'):
        self.target_lang = target_lang


    def translate(self, text):
        chunks = self.chunk_text(text)
        translated_text = ""
        counter = 0

        for chunk in chunks:
            try:
                counter += 1
                translated_text += GoogleTranslator(target=self.target_lang).translate(chunk) + "\n"
                time.sleep(2)  # Espera 2 segundos entre solicitudes para evitar bloqueos
                logging.info(f"Traduciendo: {counter} de {len(chunks)}")
            except Exception as e:
                logging.error(f"Error al traducir un fragmento: {e}")
                continue

        return translated_text
    
    def chunk_text(self, text, max_length=1200):
        sentences = text.split("。")
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks



""" def get_text():
    file_path = "木叶：这个宇智波只想躺平.txt"

    # Número de caracteres que deseas leer (ajusta según lo que necesites)
    num_characters_to_read = 1000  

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            first_part = file.read(num_characters_to_read)
            return first_part
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encontró.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")



try:
    text = get_text()
    translated_text = GoogleTranslator(target='es').translate(text)
    print(translated_text)
except Exception as e:
    print(f"Error al traducir: {e}") """
