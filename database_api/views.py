from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import WithingsMeasureTypeSerializer, WithingsMeasureSerializer, HouseholdCountSerializer, TotalMeasurementsSerializer, WarningSerializer
from .models import WithingsMeasureType, WithingsMeasure, BloodPressureWarning
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime


class TestView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = WithingsMeasureType.objects.all()
        serializer = WithingsMeasureTypeSerializer(qs, many=True)
        return Response(serializer.data)


class MeasuresListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the first 5 objects from the table
        queryset = WithingsMeasure.objects.all()[:5]
        serializer = WithingsMeasureSerializer(queryset, many=True)
        return Response(serializer.data)


class LatestMeasuresAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # If the user is not an admin, get the UUID from the user's information

            queryset = WithingsMeasure.objects.select_related(
                'measuretype_withings')
            queryset = queryset.order_by('-timestamp')
        # If the user is not an admin, filter the queryset based on the user's uuid
            if not request.user.is_staff:
                queryset = queryset.filter(uuid=request.user.uuid)
            else:
                uuid = request.GET.get('uuid')
                if uuid:
                    queryset = queryset.filter(uuid=uuid)

            measure_type = request.GET.get('measure_type')
            if measure_type:
                queryset = queryset.filter(
                    measuretype_withings__measuretype=measure_type)

            date_str = request.GET.get('date')
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(timestamp__date=date)

            measures = queryset[:50]
            response_data = []
            for measure in measures:
                measure_type = measure.measuretype_withings.measuretype
                value = float(measure.value) * 10 ** int(measure.unit)
                description = measure.measuretype_withings.description
                response_data.append({
                    'id': measure.id,
                    'measure_type': measure_type,
                    'description': description,
                    'value': value,
                    'timestamp': measure.timestamp,
                    'houseid': measure.uuid
                })

            return Response(response_data)

        return Response({'error': 'Authentication credentials were not provided.'}, status=401)


class MeasurementCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uuid = request.GET.get('uuid')
        measure_type = request.GET.get('measure_type')

        queryset = WithingsMeasure.objects.all()

        if uuid:
            queryset = queryset.filter(uuid=uuid)
        if measure_type:
            queryset = queryset.filter(measuretype_withings=measure_type)

        measurement_count = queryset.count()

        return Response({'count': measurement_count})


class HouseholdCountView(APIView):
    def get(self, request):
        # Count the number of unique UUIDs in the WithingsMeasures model
        household_count = WithingsMeasure.objects.values(
            'uuid').distinct().count()

        # Create the serializer instance with the count data
        serializer = HouseholdCountSerializer(
            {'household_count': household_count})

        return Response(serializer.data)


class TotalMeasurementsView(APIView):
    def get(self, request):
        # Count all the rows in the WithingsMeasures model
        total_measurements = WithingsMeasure.objects.count()

        # Create the serializer instance with the count data
        serializer = TotalMeasurementsSerializer(
            {'total_measurements': total_measurements})

        return Response(serializer.data)


class HouseholdWarningView(APIView):
    def get(self, request):
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            if not request.user.is_staff:
                uuid = request.user.uuid
            else:
                uuid = request.query_params.get('uuid', None)
                if not uuid:
                    return Response({'error': 'UUID parameter is missing in the request.'}, status=400)

        # Filter BloodPressureWarning by the provided UUID

            warnings = BloodPressureWarning.objects.filter(uuid=uuid)
            warnings = warnings.order_by('-timestamp')
        # Serialize the warnings data
            serializer = WarningSerializer(warnings, many=True)

            return Response(serializer.data)


class WithingsMeasureCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = WithingsMeasureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
