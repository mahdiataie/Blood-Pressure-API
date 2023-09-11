from rest_framework import serializers
from .models import CustomUser
from database_api.models import WithingsMeasure
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'uuid', 'user_type')

    def validate_uuid(self, value):
        # Check if there is at least one record with the provided UUID in the WithingsMeasure model
        try:
            withings_measure = WithingsMeasure.objects.filter(
                uuid=value).first()
            if withings_measure is None:
                raise serializers.ValidationError('Invalid UUID.')
        except WithingsMeasure.DoesNotExist:
            raise serializers.ValidationError('Invalid UUID.')

        return value

    def create(self, validated_data):
        # Create a new user instance with the provided data
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            uuid=validated_data['uuid'],
            user_type=validated_data['user_type'],
        )
        return user
