from mailing.views import *
from rest_framework import routers
from django.conf.urls import url, include



router = routers.SimpleRouter()
router.register('subscriber', SubscriberViewSet)
router.register('mailing', MailingViewSet)
router.register('subscription', SubscriptionViewSet)
urlpatterns = [
    url(r'^tracking/(?P<pk>[0-9]+)', image_load, name='image_load'),
    url('', include(router.urls)),

]
