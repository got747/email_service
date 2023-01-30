# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Mailing, Message, Subscriber, Subscription

admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(Subscriber)
admin.site.register(Subscription)
