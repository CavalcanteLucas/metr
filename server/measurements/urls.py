from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.MeasurementCreateAPIView.as_view(),
        name='measurements-create',
    ),
    path(
        'report/',
        views.measurement_report_api_view,
        name='measurements-report',
    ),
]
