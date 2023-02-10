from celery.utils.log import get_task_logger
from django import template
from django.core import mail
from smtplib import SMTPException

from mailing.models import Message, Subscriber, Mailing
from mailing.serializers import SubscriberSerializer
from email_service.celeryapp import app

from django.core.mail import EmailMessage

from email_service.settings import EMAIL_ADMIN, DEFAULT_DOMAIN

logger = get_task_logger(__name__)

def mailing_subscribers(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)

    messages_for_subscribers = get_messages_for_subscribers(mailing.id
                                            , mailing.template_name
                                            , mailing.subject)

    connection = mail.get_connection()

    try:
        connection.open()
        connection.send_messages(messages_for_subscribers)
        connection.close()
    except SMTPException as exc:
        logger.error("Mailing id: {} is error {}".format(mailing.id, exc))
    else:
        logger.info("Mailing id: {}, Sending status: 'Sent'".format(mailing.id))

        Message.objects.filter(mailing_id=mailing.id).update(
                    sending_status=Message.SENT
                )

def get_messages_for_subscribers(mailing_id, mail_template_name, mail_subject):
    messages_for_subscribers = set()

    subscribers = Mailing.objects.get(pk=mailing_id).subscribers.all()

    if subscribers:
        for subscriber in subscribers:
            message = Message.objects.create(
                    sending_status = Message.NO_SENT,
                    read_status = Message.NOT_READ,
                    subscriber_id = subscriber.id,
                    mailing_id = mailing_id
                )
            url_tracking = '{}/api/tracking/{}'.format(DEFAULT_DOMAIN, message.id)
            message = template.loader.get_template('email_templates/{}.html'.format(mail_template_name)).render({
                    'subscriber': SubscriberSerializer(subscriber).data,
                    'settings' : {'URL_TRACKING' : url_tracking}})

            mail = EmailMessage(
                    subject=mail_subject,
                    body=message,
                    from_email=EMAIL_ADMIN,
                    to=[subscriber.subscriber_email],
                    reply_to=[EMAIL_ADMIN],
                )
            mail.content_subtype = "html"
            messages_for_subscribers.add(mail)
    return messages_for_subscribers
