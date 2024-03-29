from django.urls import path
from apps.kanban import views as vk

urlpatterns = [
    path('paradas/', vk.StopListView.as_view(), name='stop-list'),
    path('procesos/', vk.ProcessListView.as_view(), name='process-list'),
    path('clientes/', vk.ClientListView.as_view(), name='client-list'),
    path('cliente/<str:code>/', vk.ClientRetrieveUpdateAPIView.as_view(), name='client-retrieve-update'),
    path('prioridades/', vk.PriorityListView.as_view(), name='priority-list'),
    path('prioridad/<str:code>/', vk.PriorityRetrieveUpdateAPIView.as_view(), name='priority-retrieve-update'),
    path('pedidos/', vk.OrderListView.as_view(), name='order-list'),
    path('pedido/<str:code>/', vk.OrderRetrieveUpdateAPIView.as_view(), name='order-retrieve-update'),
    path('tipo_tejidos/', vk.FabricTypeListView.as_view(), name='fabric_type-list'),
    path('tipo_tejido/<str:code>/', vk.FabricTypeRetrieveUpdateAPIView.as_view(), name='fabric_type-retrieve-update'),
    path('familia_tejidos/', vk.FabricFamilyListView.as_view(), name='fabric_family-list'),
    path('familia_tejido/<str:code>/', vk.FabricFamilyRetrieveUpdateAPIView.as_view(), name='fabric_family-retrieve-update'),
    path('colores/', vk.ColorListView.as_view(), name='color-list'),
    path('color/<str:code>/', vk.ColorRetrieveUpdateAPIView.as_view(), name='color-retrieve-update'),
    path('tipos_calidad/', vk.QualityTypeListView.as_view(), name='quality_type-list'),
    path('tipo_calidad/<str:code>/', vk.QualityTypeRetrieveUpdateAPIView.as_view(), name='quality_type-retrieve-update'),
    path('campos_calidad/', vk.QualityFieldListView.as_view(), name='quality_field-list'),
    path('campo_calidad/<str:code>/', vk.QualityFieldRetrieveUpdateAPIView.as_view(), name='quality_field-retrieve-update'),
    path('razones/', vk.ReasonListView.as_view(), name='reason-list'),
    path('razon/<str:code>/', vk.ReasonRetrieveUpdateAPIView.as_view(), name='reason-retrieve-update'),
    path('rutas/', vk.RouteListView.as_view(), name='route-list'),
    path('ruta/<str:code>/', vk.RouteRetrieveUpdateAPIView.as_view(), name='route-retrieve-update'),
    path('procesos_maquinaria/', vk.MachineryProcessListView.as_view(), name='machinery_process-list'),
    path('rollos_tela/', vk.FabricRollListView.as_view(), name='fabric-roll-list'),
    path('ruta-tela/', vk.FabricRollListView.as_view(), name='route-fabric-list'),
]