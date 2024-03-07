from rest_framework import serializers
# from .models import  Client 
from apps.kanban.models import Client, FabricBatch,SelectedPath
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields =('code', 'email', 'name', 'phone', 'address', 'abbreviated_name', 'short_name', 'created_at', 'updated_at')
class SelectedPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedPath
        fields = ('code', 'machinery_process_code', 'fabric_batch_code', 'sequence','start_estimated_datetime','end_estimated_datetime','unit', 'created_at', 'updated_at')
