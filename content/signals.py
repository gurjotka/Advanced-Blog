from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Post, Notification


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"New post created: '{instance.title}'"
        )


@receiver(post_delete, sender=Post)
def delete_post_notification(sender, instance, **kwargs):
    Notification.objects.create(
        message=f"Post deleted: '{instance.title}'"
    )