from src.ui.keyboard_interface import KeyboardInterface
from src.services.text_processor import TextProcessor

import os
import re
import unicodedata


tp = TextProcessor()
ki = KeyboardInterface()

def extract_docx():

    filename = ki.get_input_filename()
    text = tp.extract_text_from_docx(f"{filename}.docx")
    tp.create_text_file(text, f"{filename}.txt")

def normalize(text):
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def normalize_line(line):
    line = line.strip()
    # Regex para capturar "El capítulo" opcional + número en dígito o palabra + resto del título
    match = re.match(r'^(?:El\s+)?[Cc]apítulo\s+([^\s:]+(?:\s+y\s+[^\s:]+)*)[:\s]*(.*)$', line)
    if not match:
        return line  # no coincide, lo devolvemos tal cual

    numero_raw = match.group(1).strip()  # número en palabra o dígito
    title = match.group(2).strip()       # resto del título

    # Convertir número
    if numero_raw.isdigit():
        numero = int(numero_raw)
    else:
        numero = word_to_number(numero_raw)
    
    if numero is None:
        return line  # no se pudo convertir

    # Devuelve siempre "Capítulo {número}: título"
    if title:
        return f"Capítulo {numero}: {title}"
    else:
        return f"Capítulo {numero}:"



def word_to_number(text):
    text = text.lower().replace("-", " ").strip()
    units = {
        "cero":0,"uno":1,"dos":2,"tres":3,"cuatro":4,"cinco":5,
        "seis":6,"siete":7,"ocho":8,"nueve":9
    }
    specials = {
        "diez":10,"once":11,"doce":12,"trece":13,"catorce":14,"quince":15,
        "diesciséis":16,"diescisiete":17,"diesciocho":18,"diescinueve":19
    }
    tens = {
        "veinte":20,"treinta":30,"cuarenta":40,"cincuenta":50,"sesenta":60,
        "setenta":70,"ochenta":80,"noventa":90
    }

    # veintiuno, veintidós...
    if text.startswith("veinti"):
        unit = text[6:]
        return 20 + units.get(unit,0)

    if " y " in text:
        t,u = text.split(" y ",1)
        return tens.get(t,0) + units.get(u,0)
    
    if text in units:
        return units[text]
    if text in specials:
        return specials[text]
    if text in tens:
        return tens[text]

    return None
    


def split_text_into_chapter_files(text, output_dir, conter= 20):
    os.makedirs(output_dir, exist_ok=True)  # Asegura que el directorio de salida exista
    
    chapters = []
    current_chapter = []
    
    lines = text.split("\n")  # Divide el texto por líneas
    for line in lines:
        line = normalize_line(line)

        if re.match(r"\s*Capítulo\s+\d+", line, re.IGNORECASE):
            if current_chapter:
                chapters.append("\n".join(current_chapter))  # Junta líneas y conserva saltos de línea
                current_chapter = []
        current_chapter.append(line)  # Agrega la línea actual al capítulo en curso
    
    if current_chapter:
        chapters.append("\n".join(current_chapter))  # Agregar el último capítulo
    
    for i in range(0, len(chapters), conter):
        block = chapters[i:i + conter] 
            
        block_start = i 
        block_end = block_start + len(block) - 1
        output_file = os.path.join(output_dir, f"capitulos_{block_start+1}_a_{block_end+1}.txt")
        
        with open(output_file, "w", encoding="utf-8") as output:
            output.write("\n\n".join(block))  # Une los capítulos con doble salto de línea
        

def create_text_file_with_docx(file_name):
    text  =tp.extract_text_from_docx(f"{file_name}.docx")
    tp.create_text_file(text, f"{file_name}.txt")
    print("se creó el txt este")
    return text

def main():
    option = ki.horizontal_select("", ["split", "traducir"])
    file_name = "los setenta"
    rango=20

    if option == "split":
        text =  tp.read_txt_file(f"{file_name}.txt")
        split_text_into_chapter_files(text, f"{file_name} {rango} por {rango}", rango)
        print("ya está")
        return

    if option == "traducir":
        resume = ki.horizontal_select("¿Ya está traducido?", ["Sí", "No"])    
        while resume == "No":
            resume = ki.horizontal_select("¿Ya está traducido?", ["Sí", "No"])    

        text  = create_text_file_with_docx(file_name)
        split_text_into_chapter_files(text, f"{file_name} {rango} por {rango}", rango)
        print("ya mató todo")


def uc_prueba():
    import winreg

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Google\Chrome\BLBeacon"
    )

    version, _ = winreg.QueryValueEx(key, "version")
    print(version.split(".")[0])



if __name__ == "__main__":
    #main()
    uc_prueba()