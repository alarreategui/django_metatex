from django.db import models  
from django.utils import timezone
import os
 
  
# class Client(models.Model):
#     code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
#     email = models.CharField(db_column='correo', max_length=255, blank=True, null=True)
#     name = models.CharField(db_column='nombre', max_length=255)
#     phone = models.CharField(db_column='telefono', blank=True, null=True, max_length=20)
#     address = models.CharField(db_column='direccion', max_length=255, blank=True, null=True)
#     abbreviated_name = models.CharField(db_column='nombre_abreviado', max_length=255, blank=True, null=True)
#     short_name = models.CharField(db_column='nombre_corto', max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
#     updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

#     def save(self, *args, **kwargs):
#         self.updated_at = timezone.now()
#         super().save(*args, **kwargs)
        
#     class Meta:
#         db_table = 'cliente'
