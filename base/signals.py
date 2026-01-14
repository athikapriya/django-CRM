from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Customer
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        
        group, _ = Group.objects.get_or_create(name="customer")
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username,  
            email=instance.email
        )

        logger.info(f"Customer profile created for user: {instance.username}")
