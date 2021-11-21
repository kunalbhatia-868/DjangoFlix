from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save,slugify_pre_save
# Create your models here.

class VideoQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=timezone.now()
        )

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model,using=self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=220,unique=True)
    active = models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    
    objects=VideoManager()

    def get_playlists_ids(self):
        return list(self.playlist_featured.all().values_list('id',flat=True))

    @property
    def is_published(self):
        return self.active


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"


pre_save.connect(publish_state_pre_save,sender=Video)
pre_save.connect(slugify_pre_save,sender=Video)

pre_save.connect(publish_state_pre_save,sender=VideoAllProxy)
pre_save.connect(slugify_pre_save,sender=VideoAllProxy)

pre_save.connect(publish_state_pre_save,sender=VideoPublishedProxy)
pre_save.connect(slugify_pre_save,sender=VideoPublishedProxy)