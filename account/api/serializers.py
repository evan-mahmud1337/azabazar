from django.db.models import fields
from rest_framework import serializers
from account.models import Account, Profile
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'phone_number', 'address', 'nid_number')
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Profile
        fields = ('username', 'phone_number', 'address')
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        username = self.data['user']['username']
        user = Account.objects.get(username=username)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid:
            user_serializer.update(user, user_data)
        instance.save()
        return instance
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'phone_number', 'address')

class RegisterSerializer(serializers.ModelSerializer):
    nid_number = serializers.CharField(default='', max_length=30)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Account
        fields = ('username', 'phone_number', 'address', 'nid_number', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True}}
    def validate_password(self, value):
        data = self.get_initial()
        password = data.get('password2')
        password2 = value
        if password != password2:
            raise ValidationError('Passwords must match')
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get('password')
        password2 = value
        if password != password2:
            raise ValidationError('Passwords must match')
        return value
    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account