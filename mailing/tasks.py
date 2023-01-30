from .models import Mailing
from service.sends_out_messages import mailing_subscribers
from email_service.celeryapp import app

from celery.utils.log import get_task_logger
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(bind=True, retry_backoff=True)
def launches_mailing(self, mailing_id,):
    mailing = Mailing.objects.get(pk=mailing_id)
    if mailing:
        if mailing.to_send:
            mailing_subscribers(mailing_id)
        else:
            logger.info(
                "The mailing time has been changed, the task has been moved to {}".format(mailing.mailling_start_at)
            )
            return self.retry(eta=mailing.mailling_start_at)

    else:
        logger.info("Mailing list or client has been deleted")
