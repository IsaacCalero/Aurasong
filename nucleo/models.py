from django.db import models
from django.contrib.auth.models import User

class Emocion(models.Model):
    nombre = models.CharField(max_length=30)
    intensidad = models.IntegerField() 
    color = models.CharField(max_length=7)  
    def __str__(self):
        return f"{self.nombre} ({self.intensidad})"

class Cancion(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100, blank=True)
    url_preview = models.CharField(max_length=500, blank=True, null=True)
    emociones = models.ManyToManyField(Emocion, related_name='canciones')

    def __str__(self):
        return self.titulo
    

class EmocionCancion(models.Model):
    emocion = models.ForeignKey(Emocion, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('emocion', 'cancion')

    def __str__(self):
        return f"{self.emocion.nombre} ↔ {self.cancion.titulo}"


class ListaReproduccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    estado_base = models.ForeignKey(Emocion, null=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"

class CancionLista(models.Model):
    lista = models.ForeignKey(ListaReproduccion, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    orden_emocional = models.IntegerField()

    def __str__(self):
        return f"{self.lista.nombre} → {self.cancion.titulo} [#{self.orden_emocional}]"
