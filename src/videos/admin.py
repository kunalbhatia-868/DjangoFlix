from django.contrib import admin
from .models import VideoAllProxy,VideoPublishedProxy
# Register your models here.

class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display=['title','id','video_id','is_published']
    search_fields=['title']
    list_filter=['active']
    readonly_fields=['id','is_published']

    class Meta:
        model=VideoAllProxy

    # def published(self,obj,*args,**kwargs):
    #     return obj.active    

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display=['title','video_id']
    search_fields=['title']
    # list_filter=['video_id']
    class Meta:
        model=VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)    


admin.site.register(VideoAllProxy,VideoAllProxyAdmin)
admin.site.register(VideoPublishedProxy,VideoPublishedProxyAdmin)
