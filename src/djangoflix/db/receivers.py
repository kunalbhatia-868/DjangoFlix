from django.utils import timezone
from django.utils.text import slugify
from .models import PublishStateOptions
# Create your models here.

def publish_state_pre_save(sender,instance,*args,**kwargs):
    is_publish=instance.state == PublishStateOptions.PUBLISH
    is_draft=instance.publish_timestamp is None
    if (is_publish and is_draft):
            print("save timestamp for published published")
            instance.publish_timestamp=timezone.now()
    elif instance.state == PublishStateOptions.DRAFT:    
        instance.publish_timestamp=None


def slufigy_pre_save(sender,instance,*args,**kwargs):
    title=instance.title
    slug=instance.slug
    if slug is None:
        instance.slug=slugify(title)  