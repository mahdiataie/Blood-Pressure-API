from rest_framework import serializers
from .models import WithingsMeasureType, WithingsMeasure, BloodPressureWarning


class WithingsMeasureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithingsMeasureType
        fields = '__all__'


class WithingsMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithingsMeasure
        fields = '__all__'


class HouseholdCountSerializer(serializers.Serializer):
    household_count = serializers.IntegerField()


class TotalMeasurementsSerializer(serializers.Serializer):
    total_measurements = serializers.IntegerField()


class WarningSerializer(serializers.ModelSerializer):
    # Create a custom field for the measurement type name
    measuretype_name = serializers.SerializerMethodField()

    class Meta:
        model = BloodPressureWarning
        fields = ('timestamp', 'uuid', 'value',
                  'warning_code', 'measuretype_name')

    def get_measuretype_name(self, obj):
        # Get the corresponding name of the measurement type withing number
        try:
            return WithingsMeasureType.objects.get(measuretype=obj.measuretype_withings).description
        except WithingsMeasureType.DoesNotExist:
            return None
