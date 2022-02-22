import requests
from django.utils.timezone import now
from django.conf import settings
from celery_app import app

from notifications.models import Distribution, Client, MessageDetail


@app.task
def send_notifications():
    Distribution.objects.create(message='fun')
    for distribution in Distribution.objects.filter(time_start_notification__lte=now(), time_finish_notification__gte=now()):
        filter_parameters = distribution.client_filter.split(',')
        clients = Client.objects.filter(tag__in=filter_parameters, mobile_operator_code__in=filter_parameters)
        for client in clients:
            send_time = now()
            if send_time > distribution.time_finish_notification:
                sending_status = 'time_is_over'
            else:
                resp = requests.post('https://probe.fbrq.cloud/v1/send/', json={
                    'phone': client.phone,
                    'text': distribution.message
                }, headers={
                    'Authorization': 'Bearer ' + settings.FBRQ_TOKEN
                })

                if resp.status_code == 200:
                    sending_status = 'sent'
                else:
                    sending_status = 'error'

            MessageDetail.objects.create(
                sending_status=sending_status,
                dispatch_time=send_time,
                distribution=distribution,
                client=client
            )
