from django.db import models
from django.utils import timezone
from apps.authentication.models import Employee
import os

STATUS = [
    ('A', 'Activo'),
    ('I', 'Inactivo')
]

ROLE = [
    (1, 'Operario'),
    (2, 'Auxioliar')
]

class BehavioralField(models.Model):
    TYPE_CHOICES = [
        (1, 'Características Individuales'),
        (2, 'Mejora Continua'),
    ]
    code = models.AutoField(db_column='codigo', primary_key=True)
    name = models.CharField(db_column='nombre', max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    type_behavioral_field = models.IntegerField(db_column='tipo', choices=TYPE_CHOICES)
    state = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'campo_conductual'
        
class TechnicalField(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    name = models.CharField(db_column='nombre', max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    state = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'campo_tecnico'

class BaseMachinery(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255, null=True, blank=True)
    auxiliary_roll_number = models.IntegerField(db_column='numero_rol_auxiliar', blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'maquinaria_base'
        
class Machinery(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    base_machinery_code = models.ForeignKey(BaseMachinery, on_delete=models.CASCADE, db_column='maquinaria_base_codigo', null=True, blank=True)
    description = models.CharField(db_column='descripcion', max_length=255)
    image = models.ImageField(db_column='imagen', upload_to='images/machinery/', null=True, blank=True)
    LINE = [
        ('A', 'Abierta'),
        ('T', 'Tubular'),
        ('H', 'Ambas')
    ]
    line = models.CharField(db_column='linea', blank=True, null=True, choices=LINE, max_length=1)
    state = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    class Meta:
        db_table = 'maquinaria'
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
class Shift(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    start_time = models.TimeField(db_column='hora_inicio')
    end_time = models.TimeField(db_column='hora_fin')
    state = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'turno'

class MachineryGroup(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    start_date = models.DateTimeField(db_column='fecha_inicio')
    end_date = models.DateTimeField(db_column='fecha_fin')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'grupo_maquinaria'      

class MachineryConfiguration(models.Model):
    WEIGHT = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta')
    ]
    code = models.AutoField(db_column='codigo', primary_key=True)
    machinery_code =  models.ForeignKey(Machinery, on_delete=models.CASCADE, db_column='maquinaria_codigo')
    machinery_group_code =  models.ForeignKey(MachineryGroup, on_delete=models.CASCADE, db_column='grupo_maquinaria_codigo')
    weight = models.IntegerField(db_column='peso', choices=WEIGHT)
    shift_quantity =  models.IntegerField(db_column='cantidad_turnos')
    percentage_utilization =  models.FloatField(db_column='porcentaje_utilizacion')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'configuracion_maquina'
    
class WorkLog(models.Model):
    TYPE_CREATION = [
        (1, 'Algoritmo automatico'),
        (2, 'Modificacion de un usuario')
    ]
    code = models.AutoField(db_column='codigo', primary_key=True)
    shift_code = models.ForeignKey(Shift, on_delete=models.CASCADE, db_column='turno_codigo')
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='empleado_codigo')
    machinery_group_code = models.ForeignKey(MachineryGroup, on_delete=models.CASCADE, db_column='grupo_maquinaria_codigo')
    start_date = models.DateTimeField(db_column='fecha_inicio')
    end_date = models.DateTimeField(db_column='fecha_fin')
    role = models.IntegerField(db_column='rol', choices=ROLE)
    type_work_log = models.IntegerField(db_column='tipo', choices=TYPE_CREATION)
    status = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tareo'      
    
class BehavioralEvaluation(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    behavioral_field_code = models.ForeignKey(BehavioralField, on_delete=models.CASCADE, db_column='campo_conductual_codigo')
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='empleado_codigo')
    score = models.FloatField(db_column='puntuaje', default=0)
    status = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'evaluacion_conductual'
        
class OperatorMachineBase(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    machinery_base_code = models.ForeignKey(BaseMachinery, on_delete=models.CASCADE, db_column='maquinaria_base_codigo')
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='empleado_codigo')
    role = models.IntegerField(db_column='rol', choices=ROLE)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'operario_maquinaria_base'
        unique_together = (('machinery_base_code', 'employee_code'),)
           
class TechnicalEvaluation(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    operator_machine_base_code = models.ForeignKey(OperatorMachineBase, on_delete=models.CASCADE, db_column='operario_maquinaria_base_codigo')
    technical_fields_code = models.ForeignKey(TechnicalField, on_delete=models.CASCADE, db_column='campo_tecnico_codigo')
    score = models.FloatField(db_column='puntuaje')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'evaluacion_tecnica'

class Parameter(models.Model):
    code = models.CharField(max_length=50, db_column='codigo')
    name = models.CharField(max_length=100, db_column='nombre')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'parametro'

class MachineParameter(models.Model):
    PREFERENCE = [
        (0, 'Nula'),
        (1, 'Muy baja'),
        (2, 'Baja'),
        (3, 'Media'),
        (4, 'Alta'),
        (5, 'Muy alta'),
    ]
    code = models.CharField(max_length=50, db_column='codigo')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, db_column='parametro')
    machinery = models.ManyToManyField(Machinery, db_column='maquinaria', related_name='parameters')
    minimum = models.FloatField(db_column='minimo')
    maximum = models.FloatField(db_column='maximo')
    unit = models.CharField(max_length=10, db_column='unidad')
    preference = models.IntegerField(db_column='preferencia', choices=PREFERENCE)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'parametro_maquina'