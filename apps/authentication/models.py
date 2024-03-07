from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Role(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'rol'

# class User(AbstractUser):
#     created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
#     updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

#     def save(self, *args, **kwargs):
#         self.updated_at = timezone.now()
#         super().save(*args, **kwargs)
        
#     class Meta:
#         db_table = 'usuario'

class Employee(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=8)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_code = models.ForeignKey(Role, models.DO_NOTHING, db_column='rol_codigo')
    dni = models.CharField(db_column='dni', max_length=255, blank=True, null=True)
    name = models.CharField(db_column='nombre', max_length=255)
    phone = models.CharField(db_column='telefono', blank=True, null=True, max_length=20)
    address = models.IntegerField(db_column='direccion', blank=True, null=True)
    photo = models.ImageField(db_column='foto', upload_to='images/empleado/', null=True, blank=True)
    LINE = [
        ('A', 'Abierta'),
        ('T', 'Tubular'),
        ('H', 'Ambas')
    ]
    line = models.CharField(db_column='linea', blank=True, null=True, choices=LINE, max_length=1)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'empleado'


                