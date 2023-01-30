from rest_framework import serializers
from django import template
from .models import  Subscriber, Mailing, Subscription

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

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializerEmail(many=True)
    mailing = serializers.PrimaryKeyRelatedField(queryset=Mailing.objects.all())

    class Meta:
        model = Subscription
        fields = ('subscriber', 'mailing')

    def create(self, validated_data):
        subscribers_data = validated_data.get('subscriber')
        mailing = validated_data.get('mailing')
        subscriptions = []
        for subscriber_data in subscribers_data:
            subscriber = Subscriber.objects.get(
                subscriber_email=subscriber_data['subscriber_email']
            )
            subscription = Subscription.objects.create(
                subscriber=subscriber, mailing=mailing
            )
            subscriptions.append(subscription)
        return subscriptions

    def to_representation(self, instance):
        return self.context.get('request').data

class SubscriptionListSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializerEmail()
    mailing = serializers.PrimaryKeyRelatedField(queryset=Mailing.objects.all())

    class Meta:
        model = Subscription
        fields = ('subscriber', 'mailing')

class MailingSerializer(serializers.ModelSerializer):
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
