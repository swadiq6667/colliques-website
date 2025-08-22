from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyUser, CustomerProfile

@receiver(post_save, sender=MyUser)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and instance.role == "Customer":
        CustomerProfile.objects.create(
            user=instance,
            customer_name=f"{instance.first_name} {instance.last_name}",
            customer_email=instance.email
        )
