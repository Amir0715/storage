from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin')