from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import first_request, get_all_routes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('init/', first_request),
    path('rutas-procesos/', get_all_routes),
    path('kanban/', include('apps.kanban.urls')),
    path('tareo/', include('apps.tareo.urls')),
    path('seleccion/', include('apps.seleccion.urls')),
    path('capacidad/', include('apps.capacidad.urls')),
    path('supervisor/', include('apps.supervisor.urls')),
]
