from rest_framework import serializers
from .models import  Route, Reason, Process, Stop, Client, Order, Priority, Color, FabricType, FabricFamily, QualityType, QualityField

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ('code', 'name', 'description')

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ('machinery_code', 'code', 'start_datetime', 'estimated_completion_datetime', 'real_completion_datetime')
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields =('code', 'email', 'name', 'phone', 'address', 'abbreviated_name', 'short_name', 'created_at', 'updated_at')
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =('code', 'client_code', 'creation_date', 'delivery_deadline_date', 'created_at', 'updated_at')

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields =('code', 'name', 'created_at', 'updated_at')

class FabricTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricType
        fields =('code', 'name', 'description', 'created_at', 'updated_at')

class FabricFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricFamily
        fields =('code', 'name', 'description', 'created_at', 'updated_at')
        
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields =('code', 'description', 'hexadecimal', 'rgb', 'created_at', 'updated_at')

class QualityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityType
        fields = ('code', 'name', 'created_at', 'updated_at')

class QualityFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityField
        fields = ('code','type_quality_code','name','description','standard_value','min_approval','max_approval','min_alert','max_alert','evaluable', 'created_at', 'updated_at')

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('code', 'description', 'created_at', 'updated_at')

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('code', 'name', 'created_at', 'updated_at')

class FabricRollSerializer(serializers.Serializer):
    code = serializers.CharField()
    kilograms = serializers.FloatField()
    state = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    batch_code = serializers.SerializerMethodField()
    fabric_code = serializers.SerializerMethodField()
    
    def get_batch_code(self, obj):
        return obj.fabric_batch_code.batch_code.code

    def get_fabric_code(self, obj):
        return obj.fabric_batch_code.fabric_code.code

class MachineryProcessSerializer(serializers.Serializer):
    codigo_proceso_maquinaria = serializers.CharField(source='code')
    velocidad = serializers.FloatField(source='speed_kg')
    codigo_maquinaria = serializers.CharField(source='machinery_code.code')
    maquina = serializers.SerializerMethodField()
    codigo_proceso = serializers.SerializerMethodField()
    proceso = serializers.SerializerMethodField()
    codigo_tela = serializers.SerializerMethodField()
    
    def get_codigo_tela(self, obj):
        return obj.fabric_process_code.fabric_code.code

    def get_codigo_proceso(self, obj):
        return obj.fabric_process_code.process_code.code

    def get_proceso(self, obj):
        return obj.fabric_process_code.process_code.name

    def get_maquina(self, obj):
        return obj.machinery_code.description

class RoutePointSerializer(serializers.Serializer):
    codigo = serializers.CharField(source='code')
    ruta_codigo = serializers.SerializerMethodField()
    proceso_codigo = serializers.SerializerMethodField()
    proceso_nombre = serializers.SerializerMethodField()
    secuencia = serializers.CharField(source='sequence')
    
    def get_ruta_codigo(self, obj):
        return obj.route_code.code

    def get_proceso_codigo(self, obj):
        return obj.process_code.code

    def get_proceso_nombre(self, obj):
        return obj.process_code.name