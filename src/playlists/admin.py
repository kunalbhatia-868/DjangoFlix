from django.contrib import admin
from .models import Playlist,PlaylistItem,TvShowProxy,TvShowSeasonProxy,MovieProxy
from djangoflix.db.models import PlaylistTypeChoices
from tags.admin import TaggedItemInline
# Register your models here.


class MovieProxyAdmin(admin.ModelAdmin):
    fields=['title','state','description','video','slug']
    list_display=['title']
    class Meta:
        model=MovieProxy

    def get_queryset(self,request):
        return MovieProxy.objects.all()    

class SeasonEpisodeAdminInline(admin.TabularInline):
    model=PlaylistItem
    extra=0


class SeasonEpisodeAdmin(admin.ModelAdmin):

    inlines=[SeasonEpisodeAdminInline]
    list_display = ['title', 'parent']
    class Meta:
        model=TvShowSeasonProxy

    def get_queryset(self, request):
        return TvShowSeasonProxy.objects.all()

    


class TvShowSeasonProxyInline(admin.TabularInline):
    model=TvShowSeasonProxy
    extra=0
    fields=['parent_order','title','state']


class TvShowProxyAdmin(admin.ModelAdmin):
    def get_queryset(self,request):
        return TvShowProxy.objects.all()
        
    inlines=[TaggedItemInline,TvShowSeasonProxyInline]
    fields=['title','state','description','category','video','slug']
    class Meta:
        model=TvShowProxy  

class PlaylistItemInline(admin.TabularInline):
    model=PlaylistItem
    extra=0


class PlaylistAdmin(admin.ModelAdmin):
    inlines=[PlaylistItemInline]
    class Meta:
        model=Playlist

    def get_queryset(self, request):	
        return Playlist.objects.filter(type=PlaylistTypeChoices.PLAYLIST)    

admin.site.register(Playlist,PlaylistAdmin)
admin.site.register(TvShowProxy,TvShowProxyAdmin)
admin.site.register(TvShowSeasonProxy,SeasonEpisodeAdmin)
admin.site.register(MovieProxy,MovieProxyAdmin)