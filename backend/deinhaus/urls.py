
from django.contrib import admin
from django.urls import path, include
from database_api.views import MeasuresListView, LatestMeasuresAPIView, MeasurementCountAPIView, HouseholdCountView, TotalMeasurementsView, HouseholdWarningView, WithingsMeasureCreateView
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserRegistrationView, CustomAuthToken
from database_api.utils import update_blood_pressure_warnings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomAuthToken.as_view(), name='obtain-token'),
    path('measures/', MeasuresListView.as_view(), name='measures'),
    path('api/measures/latest/', LatestMeasuresAPIView.as_view(),
         name='get_latest_measures'),
    path('api/measures/count/', MeasurementCountAPIView.as_view(),
         name='get_measurement_count'),
    path('api/household/count/', HouseholdCountView.as_view(),
         name='household-count'),
    path('api/measurements/count/', TotalMeasurementsView.as_view(),
         name='total-measurements'),
    path('api/household/warnings/', HouseholdWarningView.as_view(),
         name='household-warnings'),
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/add-measure/', WithingsMeasureCreateView.as_view(), name='add-measure'),
    path('silk/', include('silk.urls', namespace='silk'))


]
