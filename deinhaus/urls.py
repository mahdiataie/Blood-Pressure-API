"""
URL configuration for deinhaus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from database_api.views import TestView, MeasuresListView, LatestMeasuresAPIView, MeasurementCountAPIView, HouseholdCountView, TotalMeasurementsView, HouseholdWarningView, WithingsMeasureCreateView
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserRegistrationView, CustomAuthToken
from database_api.utils import update_blood_pressure_warnings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TestView.as_view(), name='test'),
    path('api-auth/', include('rest_framework.urls')),
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


]
