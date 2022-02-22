from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from notifications.models import Client, Distribution, MessageDetail
from notifications.serializers import ClientSerializer, DistributionSerializer


class DistributionViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = DistributionSerializer
    queryset = Distribution.objects.all()

    @action(methods=['GET'], detail=False, url_path='statistics')
    def statistics(self, request, *args, **kwargs):
        return Response({
            'waiting': MessageDetail.percentage_by_status('waiting'),
            'sent': MessageDetail.percentage_by_status('sent'),
            'error': MessageDetail.percentage_by_status('error'),
            'time_is_over': MessageDetail.percentage_by_status('time_is_over'),
        })


class ClientViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
