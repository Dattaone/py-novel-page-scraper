from pypdf import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
import fitz
import os

class PDFCompress:
    def __init__(self, original_pdf_path, translated_text_path, output_pdf_path):
        self.original_pdf_path = original_pdf_path
        self.translated_text_path = translated_text_path
        self.output_pdf_path = output_pdf_path

    def compress_pdf(self, file_name, output_name, quality='screen'):
        reader = PdfReader(f"{file_name}.pdf")
        writer = PdfWriter()

        try:
            for page in reader.pages:
                writer.add_page(page)
            
            with open(f"{output_name}.pdf", "wb") as f:
                writer.write(f)
            print(f"El pdf {output_name}.pdf se creo exitosamente")
        except Exception as e:
            print(f"Error al querer comprimir el archivo: {e}")

    def get_pdftext(self,):
        pass
        
def get_text_from_pdf(filename):
    try:
        doc = fitz.open(f"{filename}.pdf")
    except Exception as e:
        print(f"No se pudo abrir el archivo '{filename}.pdf': {e}")
        return
    translated_text = ""
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        translated_text += span["text"]

    try:
        with open(f"{filename}.txt", "w", encoding="utf-8") as file:
            file.write(translated_text)
        print(f"Archivo '{filename}.txt' creado con éxito.")
    except Exception as e:
        print(f"Error al crear el archivo: {e}")

    print(f"Se creo exitosamente el archivo {filename}.txt")


if __name__ == "__main__":
    file_name = "Yuri Tama - From Third Wheel to Trifecta - Volume 01 [J-Novel Club][Premium_LNWNCentral]"
    translated_pdf = "23"
    output_name = "Yuri Tama Vol1 parseado"

    #get_text_pdf(translated_pdf)

    text = extract_text(f"{file_name}.pdf")
    with open("23.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Texto extraído con pdfminer.")

    #get_text_from_pdf(translated_pdf)

    """ compress = PDFCompress(file_name, output_name)
    compress.compress_pdf(file_name, output_name) """