from rest_framework import serializers
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):
        user = User.objects.create_user(
            nombre=validated_data['nombre'],
            correo=validated_data['correo'],
            password=validated_data['password']
           #tipo_usuario =validated_data['tipo_usuario']
        )
        user.save()
        return user
    
# class UserRegistrationSerializer(serializers.Serializer):
#     nombre = serializers.CharField()
#     tipo_usuario = serializers.CharField()
#     password = serializers.CharField()
#     correo = serializers.EmailField()