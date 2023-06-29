import csv
from datetime import datetime

from celery import shared_task
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from django.conf import settings

from .models import Measurement


def write_to_csv(file_path: str, measurements: list[Measurement]) -> None:
    """
    Writes a list of measurements to a CSV file.
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(
            [
                'measurement_datetime',
                'device_id',
                'device_manufacturer',
                'device_type',
                'device_version',
                'measurement_dimension',
                'measurement_value',
                'measurement_at_duedate',
                'duedate_datetime',
            ]
        )
        for measurement in measurements:
            writer.writerow(
                [
                    measurement.measurement_datetime,
                    measurement.device_id,
                    measurement.device_manufacturer,
                    measurement.device_type,
                    measurement.device_version,
                    measurement.measurement_dimension,
                    measurement.measurement_value,
                    measurement.measurement_at_duedate,
                    measurement.duedate_datetime,
                ]
            )


def upload_to_google_drive(file_path: str) -> None:
    """
    Uploads a file to Google Drive.
    """
    credentials = service_account.Credentials.from_service_account_file(
        settings.KEY_FILE_LOCATION
    )
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=scoped_credentials)

    filename = f"Measurements report by {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')}"
    file_metadata = {'name': filename, 'parents': [settings.BUCKET_ID]}
    media = MediaFileUpload(file_path, mimetype='text/plain')
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields='id')
        .execute()
    )
    print(f"File created successfully with ID: {file.get('id')}")


@shared_task
def generate_report() -> None:
    try:
        measurements = Measurement.objects.all()
        report_file = 'tmp.csv'

        write_to_csv(report_file, measurements)
        upload_to_google_drive(report_file)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return False

    print('Report generated successfully.')
    return True
