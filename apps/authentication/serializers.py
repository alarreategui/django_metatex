from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Role, Employee

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        if username and password:
            user = None
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Access denied: wrong username or password.', code='authorization')
        else:
            raise serializers.ValidationError(
                'Both "username" and "password" are required.', code='authorization')
        attrs['user'] = user
        return attrs

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['code', 'description', 'created_at', 'updated_at']
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['code','user','role_code','dni','name','phone','address','photo','line','created_at','updated_at']