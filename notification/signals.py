from django.dispatch import receiver
from django.db.models.signals import post_save

from notification.models import Notification
from django.core.mail import send_mail
from django.conf import settings
import json
from infra.user.models import RegisterStudents

from users.list_email import create_list_email

@receiver(post_save, sender=Notification)
def my_call(sender,instance,created,**kwargs):
    if created:
        object = RegisterStudents.objects.last()
        if object and create_list_email() != None:
            archive = object.archive.open()
            data = json.load(archive)
            send_mail(subject=instance.title,message=instance.text,from_email=settings.EMAIL_HOST_USER,recipient_list=create_list_email())