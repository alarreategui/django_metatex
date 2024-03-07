from django.urls import path
from apps.supervisor import views as sup

urlpatterns = [ 
    # # path('clientes/', sup.ClientListView.as_view(), name='client2-list'),
    path('maquinasparadas/', sup.MaquinasParadasListView.as_view(), name='maquinas-paradas-list'), 
    path('maquinasinactivasprogramadas/', sup.MaquinasInactivasListView.as_view(), name='maquinas-inactivas-list'), 
    path('paradasmotivos/', sup.ParadasMotivosListView.as_view(), name='paradas-motivos-list'), 
    path('maquinasinactivasprogramadas/<str:codigo>', sup.MaquinasInactivasListView.as_view(), name='maquinas-inactivas-list'), 
    path('motivoprioridadxpartida/', sup.MotivoPrioridadPartidasListView.as_view(), name='motivoprioridad-partida-list'), 
    path('partida/', sup.ListaPartidaListView.as_view(), name='lista-de-parada'), 
    path('partidas/<str:partidacodpartida>/', sup.ListaPartidasListView.as_view(), name='partida-id-list'), 
    path('motivosprioridad/', sup.MotivosPrioridadListView.as_view(), name='motivos-list'), 
    path('parametros/par-pro-tel/<str:codigo>', sup.ParametrosPartidaMaquinaListByCodRealizadoView.as_view(), name='parametros-partida-maquina-list'),  
    path('motivoscambio/', sup.MotivosCambioListView.as_view(), name='motivos-cambio-list'), 
    path('motivocambiovalorxprocesopartida/', sup.MotivoCambioValorParTelasListView.as_view(), name='cambio-valor-parametro-list'), 
]