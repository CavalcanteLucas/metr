from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import MeasurementSerializer


class MeasurementCreateAPIView(generics.CreateAPIView):
    serializer_class = MeasurementSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.data
        data = {
            'measurement_datetime': request_data.get('data')[0].get('value'),
            'device_id': request_data.get('device').get('identnr'),
            'device_manufacturer': request_data.get('device').get(
                'manufacturer'
            ),
            'device_type': request_data.get('device').get('type'),
            'device_version': request_data.get('device').get('version'),
            'measurement_dimension': request_data.get('data')[1].get(
                'dimension'
            ),
            'measurement_value': request_data.get('data')[1].get('value'),
            'measurement_at_duedate': request_data.get('data')[3].get('value'),
            'duedate_datetime': request_data.get('data')[2].get('value'),
        }
        if data:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            return Response(
                {'detail': 'No data provided.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
