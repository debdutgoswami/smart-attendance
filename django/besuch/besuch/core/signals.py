from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Attendance


# signals
@receiver(pre_save, sender=Attendance)
def get_percentage_present(sender, instance: Attendance, **kwargs):
    strength = instance.class_details.strength
    present = instance.total_present
    percentage_present = present / strength * 100
    instance.percentage_present = percentage_present
