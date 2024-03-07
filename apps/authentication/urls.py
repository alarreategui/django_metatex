from django.urls import path
from .views import RoleListView, RoleRetrieveUpdateAPIView, EmployeeListView, EmployeeRetrieveUpdateAPIView

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('rol/<str:code>/', RoleRetrieveUpdateAPIView.as_view(), name='role-retrieve-update'),
    path('empleados/', EmployeeListView.as_view(), name='role-list'),
    path('empleado/<str:code>/', EmployeeRetrieveUpdateAPIView.as_view(), name='employee-retrieve-update'),
]
