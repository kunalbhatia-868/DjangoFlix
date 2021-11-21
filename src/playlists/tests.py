from django.test import TestCase
from .models import Playlist
from djangoflix.db.models import PublishStateOptions
from django.utils import timezone
from django.utils.text import slugify
from videos.models import Video
# Create your tests here.


class PlaylistModelTestCase(TestCase):
    def setUp(self):
        self.video_a=Video.objects.create(title='my title',video_id='asas')
        self.video_b=Video.objects.create(title='my title',video_id='asxssas')
        self.video_c=Video.objects.create(title='my title',video_id='asaxsxsxs')
        
        self.obj_a=Playlist.objects.create(title="This is my Title",video=self.video_a)
        self.obj_b=Playlist.objects.create(title="This is my Title",video=self.video_a,
            state=PublishStateOptions.PUBLISH)
        self.obj_b.videos.set([self.video_a,self.video_b,self.video_c])    
        self.obj_a.save()

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video,self.video_a)

    def test_video_playlist(self):
        qs=self.video_a.playlist_featured.all()
        self.assertEqual(qs.count(),2)

    def test_playlist_video_items(self):
        count=self.obj_b.videos.all().count()
        self.assertEqual(count,3)

    def test_video_playlist_ids(self):
        ids=self.obj_a.video.get_playlists_ids()
        actualids=list(Playlist.objects.filter(video=self.video_a).values_list('id',flat=True))
        self.assertEqual(ids,actualids)

    def test_valid_title(self):
        title = "This is my Title"
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_slug_field(self):
        title=self.obj_a.title
        test_slug=slugify(title)
        self.assertEqual(test_slug,self.obj_a.slug)

    def test_created_count(self):
        title = "This is my Title"
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs=Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)

    def test_publish_case(self):
        qs=Playlist.objects.filter(state=PublishStateOptions.PUBLISH)
        published_qs=Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=timezone.now()
        )
        self.assertEqual(qs.count(),1)
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs=Playlist.objects.all().published()
        published_qs_2=Playlist.objects.all().published()
        self.assertEqual(published_qs.count(),published_qs_2.count())
        self.assertTrue(published_qs)
