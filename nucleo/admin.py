from django.contrib import admin
from .models import Emocion, Cancion, EmocionCancion

class EmocionCancionAdmin(admin.ModelAdmin):
    list_display = ('emocion', 'cancion')
    search_fields = ('emocion__nombre', 'cancion__titulo')

admin.site.register(Emocion)
admin.site.register(Cancion)
admin.site.register(EmocionCancion, EmocionCancionAdmin)
