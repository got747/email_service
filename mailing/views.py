# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import HttpResponse ,HttpRequest
from rest_framework import status

from .models import Subscriber, Mailing, Message, Subscription
from .serializers import SubscriberSerializer, MailingSerializer, SubscriptionCreateSerializer, SubscriptionListSerializer

from PIL import Image

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    http_method_names = ['get', 'post']
    serializer_classes = {
        'create': SubscriptionCreateSerializer,
        'list' : SubscriptionListSerializer,
    }

    default_serializer_class = SubscriptionListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

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
