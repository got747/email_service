from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Mailing
from .tasks import launches_mailing

@receiver(post_save, sender=Mailing, dispatch_uid="builder_task_on_mailing")
def builder_tasks_on_mailing(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.get(pk=instance.id)

        if mailing.to_send:
            launches_mailing.apply_async((mailing.id,))
        else:
            launches_mailing.apply_async((mailing.id,),eta=mailing.mailling_start_at)


