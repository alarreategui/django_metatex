from django.contrib import admin
from .models import User, Role, Employee

admin.site.register(Role)
admin.site.register(Employee)
