from django.db import models


class Measurement(models.Model):
    """
    Measurement model
    """

    # Date and time of the measurement
    measurement_datetime = models.DateTimeField()

    # Device ID
    device_id = models.CharField(max_length=255)

    # Device manufacturer
    device_manufacturer = models.CharField(max_length=255)

    # Device type
    device_type = models.CharField(max_length=255)

    # Device version
    device_version = models.CharField(max_length=255)

    # The dimension of the measurement
    measurement_dimension = models.CharField(max_length=255)

    # Value of the newest measurement
    measurement_value = models.IntegerField()

    # Value of the measurement at the duedate
    measurement_at_duedate = models.IntegerField()

    # The due date
    duedate_datetime = models.DateTimeField()
