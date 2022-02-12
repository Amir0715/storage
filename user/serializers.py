from typing import Dict
from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin')
        read_only_fields = ('is_admin', )


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class UserFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin')

class UserCreateSerializer(serializers.ModelSerializer):

    def validate(self, data: Dict):
        for field in self.Meta.fields:
            if field not in data:
                raise serializers.ValidationError({f'{field}': f'{field} parameter must be in request'})
        return data

    def cteate(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")