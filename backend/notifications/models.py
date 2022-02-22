from django.db import models


SENDING_STATUS = (
    ('waiting', 'Waiting'),
    ('sent', 'Sent'),
    ('error', 'Error'),
    ('time_is_over', 'Time_is_over')
)


class Distribution(models.Model):
    time_start_notification = models.DateTimeField(null=True)
    message = models.TextField()
    time_finish_notification = models.DateTimeField(null=True)
    client_filter = models.CharField(max_length=100)


class Client(models.Model):
    phone = models.CharField(max_length=20)
    mobile_operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=20)
    time_zone = models.IntegerField()


class MessageDetail(models.Model):
    sending_status = models.CharField(
        max_length=60,
        choices=SENDING_STATUS,
        default=SENDING_STATUS[0][0],
    )
    dispatch_time = models.DateTimeField(
        null=True,
        blank=True
    )
    distribution = models.OneToOneField(
        Distribution,
        on_delete=models.CASCADE,
        related_name='message_detail',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='message_detail',
        null=True,
        blank=True
    )

    @classmethod
    def percentage_by_status(cls, status):
        count = cls.objects.filter(sending_status=status).count()
        number_of_all_elements = cls.objects.all().count()
        result = 100 * count / number_of_all_elements
        return result
