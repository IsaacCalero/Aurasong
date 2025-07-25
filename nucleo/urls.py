from django.urls import path
from .views import inicio, canciones_importadas

urlpatterns = [
    path('', inicio, name='inicio'),
    path('canciones/', canciones_importadas, name='canciones'),  
]
