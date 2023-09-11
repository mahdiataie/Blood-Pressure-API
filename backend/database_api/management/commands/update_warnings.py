# update_warnings.py

from django.core.management.base import BaseCommand
from database_api.models import WithingsMeasure, BloodPressureWarning

class Command(BaseCommand):
    help = 'Check all data and create warning records in the BloodPressureWarning table.'

    def handle(self, *args, **options):
        measures = WithingsMeasure.objects.all()

        # List to store measure IDs with warning codes
        measure_ids_with_warnings = []

        # Iterate through all blood pressure measures and update the warnings
        for measure in measures:
            measure_type = measure.measuretype_withings.measuretype
            value = float(measure.value) * 10 ** int(measure.unit)

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

            # Update or create the corresponding BloodPressureWarning record if there is a warning
            if warning_code is not None:
                BloodPressureWarning.objects.update_or_create(
                    id=measure.id,  # Use the id field as the unique identifier
                    defaults={
                        'uuid': measure.uuid,
                        'timestamp': measure.timestamp,
                        'deviceID': measure.deviceID,
                        'measuretype_withings': measure.measuretype_withings.measuretype,
                        'value': value,
                        'unit': measure.unit,
                        'warning_code': warning_code,
                    }
                )
                # Add the measure ID to the list if it has a warning code
                measure_ids_with_warnings.append(measure.id)

        # Delete records with null or None warning codes
        BloodPressureWarning.objects.exclude(id__in=measure_ids_with_warnings).delete()

        self.stdout.write(self.style.SUCCESS('Warning records have been created.'))

