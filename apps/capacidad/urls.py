from django.urls import path
from apps.capacidad import views as cp

urlpatterns = [ 
    path('prueba/', cp.pruebaView.as_view(), name='prueba-list'),
    path('clientes/', cp.ClientListView.as_view(), name='cliente-list'),
]