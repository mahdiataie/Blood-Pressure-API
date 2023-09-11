from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WithingsMeasure, BloodPressureWarning
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=WithingsMeasure)
def update_blood_pressure_warning(sender, instance, created, **kwargs):
    if created:
        # Your logic to check for warnings and update the BloodPressureWarning table here
        measure_type = instance.measuretype_withings.measuretype
        value = float(instance.value) * 10 ** int(instance.unit)

        # Check for high blood pressure based on the defined limits
        if measure_type == 9:  # Diastolic Blood Pressure
            if value > 90:
                warning_code = 'RED' if value > 120 else 'YELLOW'
            else:
                warning_code = None  # No warning code if it doesn't meet the criteria
        else:  # Systolic Blood Pressure
            if value > 140:
                warning_code = 'RED' if value > 180 else 'YELLOW'
            else:
                warning_code = None  # No warning code if it doesn't meet the criteria

         # Send a color notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                instance.uuid,
                {
                    "type": "send_notification",
                    "message": {
                        'uuid': instance.uuid,
                        "timestamp": instance.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        'deviceID': instance.deviceID,
                        'measuretype_name': instance.measuretype_withings.description,
                        'value': value,
                        'warning_code':'GREEN' if warning_code is None else warning_code
                    },
                }
            )
        # Update or create the corresponding BloodPressureWarning record if there is a warning
        if warning_code is not None:
            print('New Warning Added')
            BloodPressureWarning.objects.update_or_create(
                id=instance.id,  # Use the id field as the unique identifier
                defaults={
                    'uuid': instance.uuid,
                    'timestamp': instance.timestamp,
                    'deviceID': instance.deviceID,
                    'measuretype_withings': instance.measuretype_withings.measuretype,
                    'value': value,
                    'unit': instance.unit,
                    'warning_code': warning_code,
                }
            )
 





        
