from rest_framework import serializers
from django import template
from .models import  Subscriber, Mailing

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"

class SubscriberSerializerEmail(serializers.ModelSerializer):
    subscriber_email = serializers.EmailField()

    def validate(self, data):
        try:
            Subscriber.objects.get(subscriber_email=data.get("subscriber_email"))
        except Subscriber.DoesNotExist:
            raise serializers.ValidationError("Subscriber with this email does not exist.")
        return super(SubscriberSerializerEmail, self).validate(data)

    class Meta:
        model = Subscriber
        fields = ('subscriber_email',)

class MailingListSerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField('get_email')

    def validate(self, data):
        template_name = data.get("template_name")
        try:
            template.loader.get_template("email_templates/{}.html".format(template_name))
        except template.TemplateDoesNotExist:
            raise serializers.ValidationError(
                "There is no mailing template {}".format(template_name)
            )
        return super(MailingSerializer, self).validate(data)

    class Meta:
        model = Mailing
        fields = "__all__"

    def get_email(self, obj):
        return obj.subscribers.values('subscriber_email')

class MailingSerializer(serializers.ModelSerializer):
    subscribers = SubscriberSerializerEmail(many=True, required=False)

    def create(self, validated_data):
        subscriber = validated_data.get('subscribers')
        subscribers = Subscriber.objects.filter(subscriber_email__in=subscriber)
        instance = super().create(validated_data)
        if subscribers.exists():
            instance.add(subscribers)
        return instance

    def update(self, instance, validated_data):
        subscriber = {sub.get('subscriber_email') for sub in validated_data.get('subscribers')}
        subscribers = Subscriber.objects.filter(subscriber_email__in=subscriber).values_list('pk',flat=True)
        if subscribers.exists():
            instance.subscribers.add(*subscribers)
        return instance

    def validate(self, data):
        template_name = data.get("template_name")
        try:
            template.loader.get_template("email_templates/{}.html".format(template_name))
        except template.TemplateDoesNotExist:
            raise serializers.ValidationError(
                "There is no mailing template {}".format(template_name)
            )
        return super(MailingSerializer, self).validate(data)

    class Meta:
        model = Mailing
        fields = "__all__"
