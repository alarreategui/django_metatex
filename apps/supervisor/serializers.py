from rest_framework import serializers
# from .models import  Client 
from apps.kanban.models import Client
from apps.supervisor.models import Disponibilidad, Maquina, Maquinaparada, Motivocambiovalorparametro, Motivocambiovalorparametroxpartelcolsecpromaqpar, Motivoprioridad, Motivoprioridadxpartida,Parada,Operario, Parametromaquina,Partida, Partidatelacolorsecuenciaprocesomaquinaparametro, Tela, Color, Proceso
from apps.supervisor.models import Maquinaparada
from apps.supervisor.models import Partidatelacolorsecuenciaproceso, Partidatelacolorsecuenciaprocesomaquinarealizado

class TelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tela
        fields = ('codtela', 'descripcion')

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('codcolor', 'descripcion')

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = ('codproceso', 'descripcion')

        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields =('code', 'email', 'name', 'phone', 'address', 'abbreviated_name', 'short_name', 'created_at', 'updated_at')

class MaquinaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Maquina
        fields = ('codmaquina','descripcion')
class ParadaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Parada
        fields = ('codparada','descripcion')
class DisponibilidadSerializer(serializers.ModelSerializer):
    codparada = ParadaSerializer() 
    codmaquina = MaquinaSerializer()
    class Meta:
        model = Disponibilidad
        fields = ('coddisponibilidad','fechainicio','fechafin','codparada','codmaquina') 
class DisponibilidadSerializerUpdate(serializers.ModelSerializer):  
    class Meta:
        model = Disponibilidad
        fields = ('coddisponibilidad','codparada') 
class PartidaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Partida
        fields = ('codpartida','prioridad')
class OperarioSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Operario
        fields = ('codoperario','nombre')
class MotivoprioridadSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Motivoprioridad
        fields = ('codmotivoprioridad','descripcion')
class MotivoprioridadxpartidaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Motivoprioridadxpartida
        fields = ('codmotivoprioridadxpartida','motivoprioridadcodmotivoprioridad','partidacodpartida')

class MotivoprioridadSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Motivoprioridad
        fields = ('codmotivoprioridad','descripcion')
class MotivocambioSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Motivocambiovalorparametro
        fields = ('codmotivovalor','descripcion')
class ParametromaquinaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Parametromaquina
        fields = ('codparametromaquina','descripcion','unidad','tipodedato')
        
class MotivoprioridadxpartidaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Motivoprioridadxpartida
        fields = ('codmotivoprioridadxpartida','motivoprioridadcodmotivoprioridad','partidacodpartida')
    def validate(self, data):  
        if 'motivoprioridadcodmotivoprioridad' not in data:
            raise serializers.ValidationError("motivoprioridadcodmotivoprioridad es requerido")
        if 'partidacodpartida' not in data:
            raise serializers.ValidationError("partidacodpartida es requerido")
        return data
class MotivocambiovalorparametroxpartelcolsecpromaqparSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Motivocambiovalorparametroxpartelcolsecpromaqpar
        fields = ('codmotivocambiovalorparametropartida','motivocambiovalorparametrocodmotivovalor','codpartidatelacolorsecuenciaprocesomaquinaparametro')
    def validate(self, data):  
        if 'motivocambiovalorparametrocodmotivovalor' not in data:
            raise serializers.ValidationError("motivocambiovalorparametrocodmotivovalor es requerido")
        if 'codpartidatelacolorsecuenciaprocesomaquinaparametro' not in data:
            raise serializers.ValidationError("codpartidatelacolorsecuenciaprocesomaquinaparametro es requerido")
        return data

class PartidatelacolorsecuenciaprocesomaquinaparametroSerializer(serializers.ModelSerializer):
    # codmaquina = MaquinaSerializer() 
    # codpartida = PartidaSerializer() 
    codparametromaquina = ParametromaquinaSerializer()
    class Meta:
        model = Partidatelacolorsecuenciaprocesomaquinaparametro
        fields = ('codpartidatelacolorsecuenciaprocesomaquinaparametro','codparametromaquina','valorinicial','valoractualizado')
class MaquinaparadaSerializer(serializers.ModelSerializer): 
    codparada = ParadaSerializer() 
    codoperario = OperarioSerializer() 
    codmaquina = MaquinaSerializer() 
    codpartida = PartidaSerializer() 
    class Meta:
        model = Maquinaparada
        fields = ('codmaquinaparada','fechainicio','codparada','codoperario','codmaquina','codpartida')
 
class PartidatelacolorsecuenciaprocesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partidatelacolorsecuenciaproceso
        fields = ('codpartidatelacolorsecuenciaproceso', 'secuencia', 'estado', 'procesoestandar', 'estadocalidad', 'estadobloqueo', 'codtela',    'codcolor',    'codproceso',    'codpartida',    'cantidadkg',    'cantidadmt',    'createdat',    'updatedat')    

class PartidatelacolorsecuenciaprocesorealizadoSerializer(serializers.ModelSerializer):
    # codtela_id = TelaSerializer()
    # colorcodcolor_id = ColorSerializer()
    # procesocodproceso_id = ProcesoSerializer()
    # codpartida_id = PartidaSerializer()
    partidacodpartida = PartidaSerializer()
    colorcodcolor = ColorSerializer()
    procesocodproceso = ProcesoSerializer()
    maquinacodmaquina = MaquinaSerializer()
    codtela = TelaSerializer()

    class Meta:
        model = Partidatelacolorsecuenciaprocesomaquinarealizado
        fields =('codpartidatelacolorsecuenciaprocesomaquinarealizado','secuencia','partidacodpartida','colorcodcolor','procesocodproceso','maquinacodmaquina','codtela')
    