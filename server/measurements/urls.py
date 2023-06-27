from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.MeasurementCreateAPIView.as_view(),
        name='measurements-create',
    ),
]
