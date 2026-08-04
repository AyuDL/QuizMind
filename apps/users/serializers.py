
from rest_framework import serializers
from .models import Users as User

class UserSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    accepted_terms = serializers.BooleanField(required=True)  # Add a field for accepted_terms
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'accepted_terms']

    def create(self, validated_data):
        validated_data.pop('accepted_terms')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'league_point', 'date_joined', 'birth_date']
        read_only_fields = ['id', 'first_name', 'last_name', 'league_point', 'date_joined', 'birth_date']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type' : 'password'})
    password = serializers.CharField(write_only=True, required=True, style={'input_type' : 'password'})