from django.db import models
# Create your models here.

class PublishStateOptions(models.TextChoices):
        # constant = Db_Value,User Display Value
        PUBLISH = "PU", "Publish"
        DRAFT = "DR", "Draft"
        # UNLISTED='UN','Unlisted'
        # PRIVATE='PR','Private'

class PlaylistTypeChoices(models.TextChoices):
        MOVIE='MOV','Movie'
        SHOW='TVS','Tv Show'
        SEASON='SEA','Season'
        PLAYLIST='PLA','Playlist'