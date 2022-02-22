from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from notifications.models import Client, Distribution, MessageDetail
from settings import DATETIME_FORMAT


class DistributionSerializer(serializers.ModelSerializer):
    time_start_notification = serializers.DateTimeField(format=DATETIME_FORMAT)
    time_finish_notification = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = Distribution
        fields = '__all__'

    def validate(self, attrs):
        time_start_notification = attrs.get('time_start_notification')
        time_finish_notification = attrs.get('time_finish_notification')
        if time_start_notification > time_finish_notification:
            raise ValidationError('time_start_notification cannot be greater than or equal to time_finish_notification')
        return attrs

    def create(self, validated_data):
        distribution = super().create(validated_data)
        MessageDetail.objects.create(distribution=distribution)
        return distribution


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
