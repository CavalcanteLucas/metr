from celery import shared_task


@shared_task
def generate_report():
    print('Report generated.')
    return True
