from django.db.models.signals import post_delete
from django.dispatch import receiver
from v1.property.models import Property as PropertyModel, PropertyMedia


@receiver(post_delete, sender=PropertyModel)
def delete_main_image_after_row_delete(sender, instance, **kwargs):
    if instance:
        instance.main_image.delete(save=False)


@receiver(post_delete, sender=PropertyMedia)
def delete_extra_media_after_row_delete(sender, instance, **kwargs):
    if instance:
        
        instance.media.delete(save=False)
