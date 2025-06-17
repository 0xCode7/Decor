from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import transaction

from authentication.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'full_name', 'mobile_number', 'date_of_birth')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        full_name = validated_data.pop('full_name')
        mobile_number = validated_data.pop('mobile_number')
        date_of_birth = validated_data.pop('date_of_birth')

        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )

            # Get the first name and last name
            full_name = full_name.split()
            user.first_name = full_name[0]
            user.last_name = ' '.join(full_name[1:]) if len(full_name) > 1 else ''
            user.save()

            # Update the profile
            Profile.objects.create(
                user=user,
                mobile_number=mobile_number,
                date_of_birth=date_of_birth
            )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}
