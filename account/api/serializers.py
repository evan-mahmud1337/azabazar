from django.db.models import fields
from rest_framework import serializers
from account.models import Account, Profile
from rest_framework.exceptions import ValidationError
from agents.models import Agent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('address','nid_number','phone_number','username',  'refer', 'email')
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('username', 'phone_number', 'address', 'user')
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        username = self.data['user']['username']
        user = Account.objects.get(username=username)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid:
            user_serializer.update(user, user_data)
        instance.save()
        return instance
class AgentSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)
    class Meta:
        model = Agent
        fields = ('__all__')
class RegisterSerializer(serializers.ModelSerializer):
    nid_number = serializers.CharField(default='', max_length=30)
    class Meta:
        model = Account
        fields = ('username', 'phone_number', 'address', 'nid_number','refer','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def validate_refer(self, value):
        if not Account.objects.filter(phone_number=value).exists():
            raise ValidationError('referer doesnot exist')
        return value
    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account