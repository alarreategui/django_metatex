from rest_framework import serializers
from .models import Machinery

class MachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = ('code', 'description', 'state')
