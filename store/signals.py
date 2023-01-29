from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import ShopUser


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        # shopuser = ShopUser.objects.create(
        #     user=instance,
        #     first_name=instance.first_name,
        #     last_name=instance.last_name,
        #     email = instance.email
        # )

        shopuser, created = ShopUser.objects.get_or_create(email=instance.email)

        shopuser.user = instance
        shopuser.first_name = instance.first_name
        shopuser.last_name = instance.last_name
        shopuser.save()

        subject = "Welcome to EStore"
        message = "We are glad you are here!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [shopuser.email],
            fail_silently=False,
        )
