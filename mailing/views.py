# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import HttpResponse ,HttpRequest
from rest_framework import status

from .models import Subscriber, Mailing, Message
from .serializers import SubscriberSerializer, MailingSerializer, MailingListSerializer

from PIL import Image

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_classes = {
        'create': MailingSerializer,
        'list' : MailingListSerializer,
        'retrieve': MailingListSerializer,
        'partial_update': MailingSerializer
    }

    default_serializer_class = MailingListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

@api_view(["GET"])
def image_load(request, pk=0):
    if request.method =='GET':
        red = Image.new('RGB', (20, 20))
        response = HttpResponse(content_type="image/png" , status = status.HTTP_200_OK)
        Message.objects.filter(pk=pk).update(
                    read_status=Message.READ
                )
        red.save(response, "PNG")
        return response
