
import requests
from nucleo.models import Cancion

class DeezerImportador:
    BASE_URL = "https://api.deezer.com/search?q=artist:'{artista}'"

    def __init__(self, artista):
        self.artista = artista.strip()
        self.resultados = []

    def buscar_canciones(self):
        url = self.BASE_URL.format(artista=self.artista)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"No se pudo conectar con Deezer: {response.status_code}")
        self.resultados = response.json().get("data", [])

    def guardar_en_bd(self):
        nuevas = 0
        for item in self.resultados:
            titulo = item.get("title")
            artista_nombre = item["artist"].get("name")
            preview = item.get("preview")

            if not Cancion.objects.filter(titulo=titulo, artista=artista_nombre).exists():
                Cancion.objects.create(
                    titulo=titulo,
                    artista=artista_nombre,
                    url_preview=preview,
                )
                nuevas += 1

        return nuevas

    def importar(self):
        self.buscar_canciones()
        cantidad = self.guardar_en_bd()
        return cantidad
