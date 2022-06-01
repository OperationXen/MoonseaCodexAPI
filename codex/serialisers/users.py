from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from codex.models import CodexUser
from codex.serialisers.dm_info import DMLogSerialiser


class CodexUserRegistrationSerialiser(serializers.ModelSerializer):
    """ Serialiser to use for registering new accounts """
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=CodexUser.objects.all(), lookup='iexact')])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CodexUser.objects.all(), lookup='iexact')])
    discord_id = serializers.CharField(required=False, allow_blank=True, validators=[UniqueValidator(queryset=CodexUser.objects.all(), lookup='iexact')])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = CodexUser
        fields = ['username', 'email', 'discord_id', 'password']
        optional_fields = ['discord_id']

    def validate(self, data):
        """ Additional validation of the data passed to the serialiser """
        return data

    def create(self, validated_data):
        """ Create a new user object """
        user = CodexUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class CodexUserSerialiser(serializers.ModelSerializer):
    """ Serialiser for retrieving data about a specific user """
    dm_info = DMLogSerialiser(many=True)

    class Meta:
        model = CodexUser
        fields = ['username', 'email', 'discord_id', 'dm_info']
