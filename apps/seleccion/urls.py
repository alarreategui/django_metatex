from django.urls import path
from apps.seleccion import views as sl

urlpatterns = [ 
    path('clientes/', sl.ClientListView.as_view(), name='client2-list'),
    path('cliente/<str:code>/', sl.ClientRetrieveUpdateAPIView.as_view(), name='client2-retrieve-update'), 
    path('prueba/', sl.pruebaView.as_view(), name='prueba-list'),
]