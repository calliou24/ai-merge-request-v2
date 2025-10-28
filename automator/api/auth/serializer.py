
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers 

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', "email"]


class RegisterSerializer(serializers.ModelSerializer):
    email=serializers.CharField(required=True)
    password=serializers.CharField(write_only=True, validators=[validate_password])   
    password2=serializers.CharField(write_only=True)

    class Meta: 
        model=User
        fields=['username', "email", 'password', 'password2']

    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError("Passwords does not match")
        
        return validated_data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)