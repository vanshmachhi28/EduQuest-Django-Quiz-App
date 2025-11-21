from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserGameProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_game_profile(sender, instance, created, **kwargs):
    if created:
        UserGameProfile.objects.create(user=instance)


