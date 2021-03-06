from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

User=settings.AUTH_USER_MODEL

class RatingChoice(models.IntegerChoices):
    ONE=1 ,'Onw'
    TWO=2 ,'Two'
    THREE=3, 'Three'
    FOUR=4 ,'Four'
    FIVE=5 ,'Five'

    __empty__='Unknown'

class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    value=models.IntegerField(null=True,blank=True,choices=RatingChoice.choices)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    