import subprocess
import os

def create_audio_with_textaloud(text, output_path="output.mp3"):
    try:
        # Ruta completa al ejecutable
        textaloud_path = r"C:\Program Files (x86)\TextAloud\TextAloudMP3.exe"

        # Crea un archivo temporal para el texto
        temp_text_file = "temp_text.txt"
        with open(temp_text_file, "w", encoding="utf-8") as file:
            file.write(text)

        # Construye el comando con parámetros específicos
        command = [
            textaloud_path,
            f"/r:{temp_text_file}",    # Archivo temporal con el texto
            f"/f:{output_path}",       # Archivo de salida
            "/voice:Jorge",            # Selecciona la voz 'Jorge'
            "/speed:5",                # Velocidad de la voz
            "/pitch:0",                # Tono de la voz
            "/systemVolume:103"        # Volumen del sistema
        ]

        # Ejecuta el comando
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Muestra el resultado
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"Audio guardado en: {output_path}")
        else:
            print("Error al ejecutar el comando.")

        # Limpia el archivo temporal
        os.remove(temp_text_file)

    except FileNotFoundError:
        print("TextAloud.exe no se encontró. Verifica la ruta.")    
    except Exception as e:
        print(f"Error al ejecutar el comando: {e}")

# Prueba el script
create_audio_with_textaloud(
    text="Este es un ejemplo de texto con Loquendo Jorge.",
    output_path="output.mp3"
)
