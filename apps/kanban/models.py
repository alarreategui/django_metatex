from django.db import models
from apps.tareo.models import Machinery, Parameter
# from apps.authentication.models import User
from django.contrib.auth.models import User
from django.utils import timezone
import os

STATUS = [
    ('A', 'Activo'),
    ('I', 'Inactivo')
]

TYPE_REASON = [
    (1, 'Parada no programada'),
    (2, 'Parada programada'),
    (3, 'Llamada supervisor'),
]

class QualityType(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'tipo_calidad'
        
class Client(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    email = models.CharField(db_column='correo', max_length=255, blank=True, null=True)
    name = models.CharField(db_column='nombre', max_length=255)
    phone = models.CharField(db_column='telefono', blank=True, null=True, max_length=20)
    address = models.CharField(db_column='direccion', max_length=255, blank=True, null=True)
    abbreviated_name = models.CharField(db_column='nombre_abreviado', max_length=255, blank=True, null=True)
    short_name = models.CharField(db_column='nombre_corto', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'cliente'
        
class Order(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    client_code = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='cliente_codigo')
    creation_date = models.DateTimeField(db_column='fecha_creacion', blank=True, null=True)
    delivery_deadline_date = models.DateTimeField(db_column='fecha_limite_entrega', blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'pedido'
   
class Item(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    order_code = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='pedido_codigo')
    delivery_deadline = models.DateTimeField(db_column='fecha_limite_entrega')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'partida'
        
class FabricType(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255, blank=True, null=True)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tipo_tejido'        

class FabricFamily(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255, blank=True, null=True)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'familia_tejido'

class Route(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'ruta'

class Color(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    hexadecimal = models.CharField(db_column='hexadecimal', max_length=255, blank=True, null=True)
    rgb = models.CharField(db_column='rgb', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'color'

class Fabric(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    color_code = models.ForeignKey(Color, on_delete=models.CASCADE, db_column='color_codigo')
    fabric_type_code = models.ForeignKey(FabricType, on_delete=models.CASCADE, db_column='tipo_tejido_codigo')
    fabric_family_code = models.ForeignKey(FabricFamily, on_delete=models.CASCADE, db_column='familia_tejido_codigo')
    route_code = models.ForeignKey(Route, on_delete=models.CASCADE, db_column='ruta_codigo', blank=True, null=True)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    technical_sheet = models.FileField(db_column='ficha_tecnica', upload_to="files/fabric/technical_sheet/", blank=True, null=True)
    instructions = models.FileField(db_column='instrucciones', upload_to="files/fabric/instructions/", blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    # def __str__(self):
    #     return "%s (%s)" % (
    #         self.code,
    #         ", ".join(print("route") for route in self.route_code.all()),
    # ) 

    def save(self, *args, **kwargs):
        try:
            if not self.code:
                super().save(*args, **kwargs)
            else:
                original = self.__class__.objects.get(code=self.code)
                if self.technical_sheet != original.technical_sheet:
                    original_filename, original_extension = os.path.splitext(str(self.technical_sheet))
                    technical_sheet_name = f"fabric_{self.code}_technical_sheet{original_extension}"
                    self.technical_sheet.name = technical_sheet_name
                if self.instructions != original.instructions:
                    original_filename, original_extension = os.path.splitext(str(self.instructions))
                    instructions_name = f"fabric_{self.code}_instructions{original_extension}"
                    self.instructions.name = instructions_name
            self.updated_at = timezone.now()
            super().save(*args, **kwargs)
        except:
            self.updated_at = timezone.now()
            super().save(*args, **kwargs)

    class Meta:
        db_table = 'tela'

class Zone(models.Model):
    code = models.CharField(max_length=4, primary_key=True, db_column='codigo')
    description = models.CharField(max_length=50, db_column='descripcion')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)    
        
    class Meta:
        db_table = 'zona'

class Container(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    zone_code = models.ForeignKey(Zone, on_delete=models.CASCADE, db_column='zona_codigo', blank=True, null=True)
    model = models.CharField(db_column='modelo', max_length=255, blank=True, null=True)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    image = models.ImageField(db_column='imagen/container/', blank=True, null=True)
    state = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)        
    
    class Meta:
        db_table = 'contenedor'

class Reason(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255)
    # type_reason = models.IntegerField(db_column='estado', choices=TYPE_REASON)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'razon'

class Priority(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'prioridad'
        
class FabricBatch(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    batch_code = models.ForeignKey(Item, on_delete=models.CASCADE, db_column='partida_codigo')
    fabric_code = models.ForeignKey(Fabric, on_delete=models.CASCADE, db_column='tela_codigo')
    priority_code = models.ForeignKey(Priority, on_delete=models.CASCADE, db_column='prioridad_codigo', blank=True, null=True)
    process_quantity = models.IntegerField(db_column='cantidad_procesar')
    unit_of_measure = models.CharField(db_column='unidad_medida', max_length=255)
    target_date = models.DateTimeField(db_column='fecha_objetivo')
    destination_type = models.CharField(db_column='tipo_destino', max_length=255, blank=True, null=True)
    packaging_type = models.CharField(db_column='tipo_embalaje', max_length=255, blank=True, null=True)
    production_type = models.CharField(db_column='tipo_produccion', max_length=255, blank=True, null=True)
    observations = models.CharField(db_column='observaciones', max_length=255, blank=True, null=True)    
    instructions = models.FileField(db_column='instrucciones', upload_to="files/fabric_batch/instructions/", blank=True, null=True)
    STATE = [
        ('A', 'Activo'),
        ('F', 'Finalizada')
    ]
    state = models.CharField(db_column='estado', max_length=1, choices=STATE, default='A')
    # fin_tenido= models.CharField(db_column='FinTenido', max_length=255, blank=True, null=True)
    # fin_estimado = models.CharField(db_column='FinEstimado', max_length=255, blank=True, null=True)
    # fin_humedo = models.CharField(db_column='FinHumedo', max_length=255, blank=True, null=True)
    # ancho = models.IntegerField(db_column='ancho')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'partida_tela'
        unique_together = (('batch_code', 'fabric_code'),)

class FabricRoll(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    fabric_batch_code = models.ForeignKey(FabricBatch, on_delete=models.CASCADE, db_column='partida_tela_codigo')
    kilograms = models.FloatField(db_column='kilos')
    state = models.CharField(db_column='estado', max_length=1, choices=STATUS, default='A')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'rollo_tela'

class Process(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    name = models.CharField(db_column='nombre', max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'proceso'

class QualityField(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    type_quality_code = models.ForeignKey(QualityType, on_delete=models.CASCADE, db_column='tipo_calidad_codigo')
    process_code = models.ForeignKey(Process, on_delete=models.CASCADE, db_column='proceso_codigo', blank=True, null=True)
    name = models.CharField(db_column='nombre', max_length=255)
    description = models.CharField(db_column='descripcion', max_length=255, blank=True, null=True)
    standard_value = models.FloatField(db_column='valor_estandar', blank=True, null=True)
    min_approval = models.FloatField(db_column='minimo_aprobacion', blank=True, null=True)
    max_approval = models.FloatField(db_column='maximo_aprobacion', blank=True, null=True)
    min_alert = models.FloatField(db_column='minimo_alerta', blank=True, null=True)
    max_alert = models.FloatField(db_column='maximo_alerta', blank=True, null=True)
    evaluable = models.FloatField(db_column='evaluable', blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'campo_calidad'

class QualityValues(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    quality_field_code = models.ForeignKey(QualityField, on_delete=models.CASCADE, db_column='campo_calidad_codigo')
    value = models.FloatField(db_column='valor')
    result = models.FloatField(db_column='resultado', blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'valor_calidad'

class FabricProcess(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    process_code = models.ForeignKey(Process, on_delete=models.CASCADE, db_column='proceso_codigo')
    fabric_code = models.ForeignKey(Fabric, on_delete=models.CASCADE, db_column='tela_codigo')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'proceso_tela'
        
class Stop(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    machinery_code = models.ForeignKey(Machinery, on_delete=models.CASCADE, db_column='maquinaria_codigo')
    reason_code = models.ForeignKey(Reason, on_delete=models.CASCADE, db_column='razon_codigo')
    start_datetime = models.DateTimeField(db_column='fecha_hora_inicio')
    estimated_completion_datetime = models.DateTimeField(db_column='fecha_hora_estimada_finalizacion', blank=True, null=True) 
    real_completion_datetime = models.DateTimeField(db_column='fecha_hora_finalizacion_real', blank=True, null=True)
    type_reason = models.IntegerField(db_column='estado', choices=TYPE_REASON, default = 1)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'parada'
        
class ArticleProcessPDF(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    instructions_pdf = models.FileField(db_column='pdf_indicaciones', upload_to="files/article_process_pdf/instructions_pdf/", blank=True, null=True)
    recipe_pdf = models.FileField(db_column='pdf_receta', upload_to="files/article_process_pdf/recipe_pdf/", blank=True, null=True)
    recommendations_pdf = models.FileField(db_column='pdf_recomendaciones', upload_to="files/article_process_pdf/recommendations_pdf/", blank=True, null=True)
    required_instructions = models.BooleanField(db_column='obligatorio_indicaciones', blank=True, null=True)
    required_recipe = models.BooleanField(db_column='obligatorio_receta', blank=True, null=True)
    required_recommendations = models.BooleanField(db_column='obligatorio_recomendaciones', blank=True, null=True)
    read_instructions = models.BooleanField(db_column='leido_indicaciones', blank=True, null=True, default=False)
    read_recipe = models.BooleanField(db_column='leido_receta', blank=True, null=True, default=False)
    read_recommendations = models.BooleanField(db_column='leido_recomendaciones', blank=True, null=True, default=False)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'partida_articulo_proceso_pdf'
        
class RoutePoint(models.Model):
    code = models.AutoField(db_column='codigo', primary_key=True)
    process_code = models.ForeignKey(Process, on_delete=models.CASCADE, db_column='proceso_codigo')
    route_code = models.ForeignKey(Route, on_delete=models.CASCADE, db_column='ruta_codigo')
    sequence = models.IntegerField(db_column='secuencia')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'punto_ruta'
        
class ProcessMachinery(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    machinery_code = models.ForeignKey(Machinery, on_delete=models.CASCADE, db_column='maquinaria_codigo')
    fabric_process_code = models.ForeignKey(FabricProcess, on_delete=models.CASCADE, db_column='proceso_tela_codigo')
    speed_kg = models.FloatField(db_column='velocidad_kg', blank=True, null=True)
    speed_mts = models.FloatField(db_column='velocidad_mts', blank=True, null=True)
    cost_dollars_kg = models.FloatField(db_column='costo_dolares_kg', blank=True, null=True)
    cost_dollars_mts = models.FloatField(db_column='costo_dolares_mts', blank=True, null=True)
    supplies = models.FileField(db_column='insumos',  upload_to="files/process_machinery/supplies/", blank=True, null=True)
    specifications = models.FileField(db_column='especificaciones',  upload_to="files/process_machinery/specifications/", blank=True, null=True)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'proceso_maquinaria'
        
class SelectedPath(models.Model):
    code = models.CharField(db_column='codigo', primary_key=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='usuario_usuario', blank=True, null=True)
    quality_values_code = models.ForeignKey(QualityValues, on_delete=models.CASCADE, db_column='valor_calidad_codigo', blank=True, null=True)
    machinery_process_code = models.ForeignKey(ProcessMachinery, on_delete=models.CASCADE, db_column='proceso_maquinaria_codigo')
    pdf_code = models.ForeignKey(ArticleProcessPDF, on_delete=models.CASCADE, db_column='partida_articulo_proceso_pdf_codigo', blank=True, null=True)
    fabric_batch_code = models.ForeignKey(FabricBatch, on_delete=models.CASCADE, db_column='partida_tela_codigo')
    sequence = models.IntegerField(db_column='secuencia')
    start_real_datetime = models.DateTimeField(db_column='fecha_hora_inicio_real', blank=True, null=True)
    end_real_datetime = models.DateTimeField(db_column='fecha_hora_fin_real', blank=True, null=True)
    start_estimated_datetime = models.DateTimeField(db_column='fecha_hora_inicio_estimada', blank=True, null=True)
    end_estimated_datetime = models.DateTimeField(db_column='fecha_hora_fin_estimado', blank=True, null=True)
    incoming_fabric_quantity = models.FloatField(db_column='cantidad_tela_entrante', blank=True, null=True)
    outgoing_fabric_quantity = models.FloatField(db_column='cantidad_tela_saliente', blank=True, null=True)
    unit = models.CharField(db_column='unidad', blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'trayecto_seleccionado'
        
class ContainerSelectedTrajectory(models.Model):
    selected_trajectory_code = models.ForeignKey(SelectedPath, on_delete=models.CASCADE, db_column='trayecto_seleccionado_codigo')
    container_code = models.ForeignKey(Container, on_delete=models.CASCADE, db_column='contenedor_codigo')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'contenedor_trayecto_seleccionado'
        unique_together = (('selected_trajectory_code', 'container_code'),)

class ParameterStart(models.Model):
    code = models.CharField(max_length=50, db_column='codigo')
    value = models.FloatField(db_column='valor')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, db_column='parametro')
    selected_route = models.ForeignKey(SelectedPath, on_delete=models.CASCADE, db_column='trayecto_seleccionado')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'parametro_partida'

class ParameterFabricProcess(models.Model):
    code = models.CharField(max_length=50, db_column='codigo')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, db_column='parametro')
    machinery_process_code = models.ManyToManyField(ProcessMachinery, db_column='proceso_maquinaria_codigo', related_name='parameters')
    value = models.FloatField(db_column='valor')
    state = models.CharField(max_length=50, db_column='estado')
    created_at = models.DateTimeField(db_column='creacion', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='modificacion', auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'parametro_tela_proceso_maquina'