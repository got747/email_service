# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    first_name = models.CharField(
        verbose_name='First name',
        max_length=50)
    second_name = models.CharField(
        verbose_name='Second name',
        max_length=50)
    birthday = models.DateField(verbose_name='Birthday')
    subscriber_email = models.EmailField(verbose_name='Email', unique=True, max_length=100)

    def __str__(self):
        return ('Subscriber: {} \n birthday: {}  \n subscriber_email: {}'
                .format(self.second_name, self.birthday, self.subscriber_email))

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

class Mailing(models.Model):
    SEND_ALL_SUBSCRIBERS='all'

    mailling_start_at = models.DateTimeField(verbose_name='Mailing start')
    subject = models.CharField(verbose_name='Subject of the mailing', max_length=50, blank=True)
    template_name = models.CharField(verbose_name='Template name', max_length=30)

    @property
    def to_send(self):
        return self.mailling_start_at < timezone.now()

    def __str__(self):
        return ('Mailing: {} \n start: {} \n template name: {}'
                .format(self.id, self.mailling_start_at, self.template_name))

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

class Message(models.Model):

    SENT = 'SENT'
    NO_SENT = 'NO_SENT'
    ChoicesStatuses = (
        (SENT, 'SENT'),
        (NO_SENT, 'NO_SENT')
    )

    READ = 'READ'
    NOT_READ = 'NOT_READ'
    ChoicesREAD = (
        (READ, 'READ'),
        (NOT_READ, 'NOT_READ')
    )

    sent_at = models.DateTimeField(verbose_name='Time of sending', auto_now=True)
    created_date = models.DateTimeField(verbose_name='Time of create', auto_now_add=True )
    sending_status = models.CharField(
        verbose_name='Status of sending',
        max_length=10,
        choices=ChoicesStatuses,
        default=NO_SENT,
    )
    read_status = models.CharField(
        verbose_name='Status of reading',
        max_length=10,
        choices=ChoicesREAD,
        default=NOT_READ,
    )
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, null=True)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return ('Message: {} \n sent_at: {} \n sending status: {} \n read status: {} \n subscriber: {} \n mailing: {}'
                .format(self.id, self.sent_at , self.sending_status , self.read_status , self.subscriber , self.mailing ))

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

class Subscription(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
