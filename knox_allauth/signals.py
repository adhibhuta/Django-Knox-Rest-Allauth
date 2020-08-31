from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from .models import CustomUser as User

@receiver(post_save, sender=SocialAccount)
def create_class(sender, instance, created, **kwargs):
	if created:
		user = User.objects.filter(email=instance.extra_data['email']).first()
		user.name = instance.extra_data['name']
		user.save()
