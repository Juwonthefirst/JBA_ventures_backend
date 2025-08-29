from django.db.models.signals import post_delete
from django.dispatch import receiver
from v1.property.models import Property as PropertyModel


@receiver(post_delete, sender=PropertyModel)
def delete_file_after_row_delete(sender, instance, **kwargs):
    if instance:
        instance.file.delete()
