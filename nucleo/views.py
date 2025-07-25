from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cancion, Emocion, EmocionCancion
from .services.importador_deezer import DeezerImportador

def inicio(request):
    return render(request, 'inicio.html')

#  Vista 1: Importar canciones desde Deezer
def importar_desde_deezer(request):
    artista = request.GET.get('artista', 'Aurora')
    importador = DeezerImportador(artista)
    cantidad = importador.importar()
    return HttpResponse(f"🎧 Se importaron {cantidad} canciones de {artista}")

# Vista 2: Asignar emociones a canciones
def asignar_emocion(request):
    canciones = Cancion.objects.all()
    emociones = Emocion.objects.all()

    if request.method == 'POST':
        cancion_id = request.POST.get('cancion')
        emocion_id = request.POST.get('emocion')

        try:
            cancion = Cancion.objects.get(id=cancion_id)
            emocion = Emocion.objects.get(id=emocion_id)
            EmocionCancion.objects.get_or_create(cancion=cancion, emocion=emocion)
        except Cancion.DoesNotExist:
            return HttpResponse("❌ La canción no existe")
        except Emocion.DoesNotExist:
            return HttpResponse("❌ La emoción no existe")

        return redirect('asignar_emocion')

    return render(request, 'asignar_emocion.html', {
        'canciones': canciones,
        'emociones': emociones
    })

#  Vista 3: Ver canciones con sus emociones asignadas (con filtros)
def relaciones_emocionales(request):
    emociones = Emocion.objects.all()
    artistas = Cancion.objects.values_list('artista', flat=True).distinct()

    filtro_emocion = request.GET.get('emocion')
    filtro_artista = request.GET.get('artista')

    relaciones = EmocionCancion.objects.select_related('cancion', 'emocion').all()

    if filtro_emocion:
        relaciones = relaciones.filter(emocion__id=filtro_emocion)
    if filtro_artista:
        relaciones = relaciones.filter(cancion__artista=filtro_artista)

    return render(request, 'relaciones_emocionales.html', {
        'relaciones': relaciones,
        'emociones': emociones,
        'artistas': artistas
    })

# 🗑️ Vista 4: Eliminar relación emocional con las canciones
def eliminar_relacion(request, id):
    EmocionCancion.objects.filter(id=id).delete()
    return redirect('relaciones_emocionales')

# Vista 5: Editar relación emocional con las canciones 
def editar_relacion(request, id):
    relacion = EmocionCancion.objects.select_related('cancion', 'emocion').get(id=id)
    emociones = Emocion.objects.all()

    if request.method == 'POST':
        nueva_emocion_id = request.POST.get('emocion')
        try:
            nueva_emocion = Emocion.objects.get(id=nueva_emocion_id)
            relacion.emocion = nueva_emocion
            relacion.save()
        except Emocion.DoesNotExist:
            return HttpResponse("❌ Emoción no válida")

        return redirect('relaciones_emocionales')

    return render(request, 'editar_relacion.html', {
        'relacion': relacion,
        'emociones': emociones
    })

def canciones_importadas(request):
    canciones = Cancion.objects.all()
    return render(request, 'canciones.html', {'canciones': canciones})

