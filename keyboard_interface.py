import os
import msvcrt
import re
import sys

from urllib.parse import urlparse

class KeyboardInterface:
    def __init__(self):
        pass


    def get_input_url(
            self, 
            statement="Ingresar la url: "
            ) -> str:
        """
        Muestra un mensaje(statement).
        Extrae y valora si el ingresado por el usuario es una url.

        Args:
            statement (str): Pregunta o texto de cabecera.

        Returns:
            str: Url ingresada por el usuario.
        """
        while True:
            url = input(statement).strip()
            parsed = urlparse(url)
            if all([parsed.scheme, parsed.netloc]):
                break
        return url


    def get_input_filename(
            self,
            statement="Ingresa nombre para el archivo.\n"
            ) -> str:
        """
        Muestra un mensaje(statement).
        Extrae y valora si el ingresado por el usuario es un nombre válido.

        Args:
            statement (str): Pregunta o texto de cabecera.

        Returns:
            str: Nombre del archivo ingresada por el usuario modificado.
        """
        filename = input(statement).strip()
        return self.sanitize_filename(filename)


    def sanitize_filename(self, filename: str) -> str:
        """Reemplaza caracteres prohibidos con guiones bajos"""
        return re.sub(r'[\\/*?:"<>|]', "_", filename).strip()


    def clear(self):
        """Limpia la consola según el sistema operativo."""
        os.system('cls' if os.name == 'nt' else 'clear')


    def clear_last_line(self):
        """Mueve el cursor una línea arriba y borra solo esa línea."""
        sys.stdout.write("\033[F")  # Mover cursor una línea arriba
        sys.stdout.write("\033[K")  # Borrar toda la línea
        sys.stdout.flush()

    def horizontal_select(
        self,
        statement="¿Deseas extraer la novela completa?",
        options=["Sí", "No"]
    ):
        """
        Muestra un menú horizontal en consola con flechas ← → y selecciona con Enter.
        Solo actualiza la última línea sin limpiar toda la consola.

        Args:
            statement (str): Pregunta o texto de cabecera.
            options (list[str]): Lista de opciones para elegir.

        Returns:
            str: Opción seleccionada.
        """
        index = 0

        print(statement)

        while True:
            # Mostrar las opciones en línea horizontal
            menu = "   ".join(
                [f"[{opt}]" if i == index else f" {opt} "
                 for i, opt in enumerate(options)]
            )
            sys.stdout.write("\r" + menu)  # Reescribe la misma línea
            sys.stdout.flush()

            key = msvcrt.getch()

            if key == b'\xe0':  # Teclas especiales (flechas)
                key = msvcrt.getch()
                if key == b'K':  # Flecha izquierda
                    index = (index - 1) % len(options)
                elif key == b'M':  # Flecha derecha
                    index = (index + 1) % len(options)
            elif key == b'\r':  # Enter
                print()  # salto de línea final
                return options[index]

    def vertical_select(self, title: str, options: list[str]) -> str:
        """
        Muestra un menú en consola con flechas ↑ ↓ y selecciona con Enter.
        
        Args:
            title (str): Mensaje principal o pregunta.
            options (list[str]): Lista de opciones para elegir.

        Returns:
            str: La opción seleccionada.
        """
        index = 0

        while True:
            self.clear()
            print(title + "\n")
            for i, option in enumerate(options):
                if i == index:
                    print(f"> {option} <")
                else:
                    print(f"  {option}")

            key = msvcrt.getch()

            if key == b'\xe0':  # Teclas especiales (flechas)
                key = msvcrt.getch()
                if key == b'H':  # Flecha arriba
                    index = (index - 1) % len(options)
                elif key == b'P':  # Flecha abajo
                    index = (index + 1) % len(options)
            elif key == b'\r':  # Enter
                print()
                selected = options[index]
                return selected

    def get_chapter_range(self) -> tuple[int, int | None]:
        """
        Pide al usuario el rango de capítulos (inicio y fin).
        Si el usuario deja vacío el final, se asume que es hasta el último.
        """
        while True:
            try:
                start_input = input("Capítulo inicial (por defecto 1): ").strip()
                start = int(start_input) if start_input else 1

                end_input = input("Capítulo final (Enter para todos): ").strip()
                end = int(end_input) if end_input else None

                if start < 1:
                    print("❌ El capítulo inicial debe ser 1 o mayor.")
                    continue
                if end is not None and end < start:
                    print("❌ El capítulo final no puede ser menor que el inicial.")
                    continue

                return start, end
            except ValueError:
                print("❌ Ingresa solo números válidos.")

   