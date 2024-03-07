from rest_framework import serializers
# from .models import  Client 
from apps.kanban.models import Client
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields =('code', 'email', 'name', 'phone', 'address', 'abbreviated_name', 'short_name', 'created_at', 'updated_at')
