from django.urls import path
from . import views as vw

urlpatterns = [
    path('maquinas/', vw.MachineryListView.as_view(), name='machinery-list'),
]
