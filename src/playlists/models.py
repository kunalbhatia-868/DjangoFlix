from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.aggregates import Avg,Max,Min
from django.utils import timezone
from django.db.models.signals import pre_save,post_save
from djangoflix.db.models import PublishStateOptions,PlaylistTypeChoices
from djangoflix.db.receivers import publish_state_pre_save,slugify_pre_save
from videos.models import Video
from categories.models import Category
from tags.models import TaggedItem
from ratings.models import Rating
# Create your models here.

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=timezone.now()
        )

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model,using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured_playlist(self):
        return self.get_queryset().filter(type=PlaylistTypeChoices.choices)

class Playlist(models.Model):
    parent=models.ForeignKey("self",blank=True,null=True,on_delete=models.SET_NULL)
    parent_order=models.IntegerField(default=1)
    category=models.ForeignKey(Category,blank=True,null=True,related_name='playlists',on_delete=models.SET_NULL)
    title = models.CharField(max_length=220)
    type=models.CharField(max_length=3,choices=PlaylistTypeChoices.choices,default=PlaylistTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video=models.ForeignKey(Video,null=True,blank=True,related_name='playlist_featured',on_delete=models.SET_NULL)
    videos=models.ManyToManyField(Video,blank=True,related_name="playlist_item",through='PlaylistItem')
    active = models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    tags=GenericRelation(TaggedItem,related_query_name='playlist')
    ratings=GenericRelation(Rating,related_query_name='playlist')

    objects=PlaylistManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active

    def get_avg_rating(self):
        return Playlist.objects.filter(id=self.id).aggregate(Avg('ratings__value'))

    def get_rating_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(max=Max('ratings__value'),min=Min('ratings__value'))

    def get_short_display(self):
        return ""



class TvShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True,type=PlaylistTypeChoices.SHOW)

class TvShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False,type=PlaylistTypeChoices.SEASON)


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=PlaylistTypeChoices.MOVIE)

class MovieProxy(Playlist):
    objects=MovieProxyManager()
    class Meta:
        proxy=True
        verbose_name='Movie'     
        verbose_name_plural='Movies'

    def save(self,*args,**kwargs):
        self.type=PlaylistTypeChoices.MOVIE
        super().save(*args,**kwargs) 


class TvShowProxy(Playlist):
    objects=TvShowProxyManager()
    class Meta:
        proxy=True
        verbose_name='TV Show'     
        verbose_name_plural='TV Shows'    

    def save(self,*args,**kwargs):
        self.type=PlaylistTypeChoices.SHOW
        super().save(*args,**kwargs)     

    @property
    def seasons(self):
        return self.playlist_set.published()

    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"

class TvShowSeasonProxy(Playlist):
    objects=TvShowSeasonProxyManager()
    class Meta:
        proxy=True   
        verbose_name='Season'     
        verbose_name_plural='Seasons'   

    def save(self,*args,**kwargs):
        self.type=PlaylistTypeChoices.SEASON
        super().save(*args,**kwargs)        



class PlaylistItem(models.Model):
    playlist=models.ForeignKey(Playlist,on_delete=models.CASCADE)
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    order=models.IntegerField(default=1)

    class Meta:
        ordering=['order','-timestamp']

pre_save.connect(publish_state_pre_save, sender=TvShowProxy)
pre_save.connect(slugify_pre_save, sender=TvShowProxy)

pre_save.connect(publish_state_pre_save, sender=TvShowSeasonProxy)
pre_save.connect(slugify_pre_save, sender=TvShowSeasonProxy)

pre_save.connect(publish_state_pre_save, sender=MovieProxy)
pre_save.connect(slugify_pre_save, sender=MovieProxy)

pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)        