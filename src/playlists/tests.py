from functools import partial
from typing import Tuple
from django.test import TestCase
from .models import Playlist
from djangoflix.db.models import PublishStateOptions
from django.utils import timezone
from django.utils.text import slugify
from videos.models import Video
# Create your tests here.


class PlaylistModelTestCase(TestCase):
    def create_show_with_seasons(self):
        the_friends=Playlist.objects.create(title='Friends Series')
        friends_1=Playlist.objects.create(title='Friends Season 1',parent=the_friends,parent_order=1)
        friends_2=Playlist.objects.create(title='Friends Season 2',parent=the_friends,parent_order=2)
        friends_3=Playlist.objects.create(title='Friends Season 3',parent=the_friends,parent_order=3)
        friends_4=Playlist.objects.create(title='Friends Season 4',parent=the_friends,parent_order=4)
        self.shows_with_seasons=Playlist.objects.filter(parent__isnull=True)
        self.show=self.shows_with_seasons.last()


    def setUp(self):
        self.video_a=Video.objects.create(title='my title',video_id='asas')
        self.video_b=Video.objects.create(title='my title',video_id='asxssas')
        self.video_c=Video.objects.create(title='my title',video_id='asaxsxsxs')
        
        self.obj_a=Playlist.objects.create(title="This is my Title",video=self.video_a)
        self.obj_b=Playlist.objects.create(title="This is my Title",video=self.video_a,
            state=PublishStateOptions.PUBLISH)
        self.video_qs=Video.objects.all()
        self.obj_b.videos.set(self.video_qs)    
        self.obj_a.save()
        self.create_show_with_seasons()

    def test_show_have_seasons(self):
        self.assertTrue(self.shows_with_seasons.exists())

    def test_new_shows_of_show_created(self):
        season_video_created=self.show.playlist_set.all()
        shows_created=Playlist.objects.filter(parent=self.show.id)
        self.assertTrue(shows_created,season_video_created)    

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video,self.video_a)

    def test_video_playlist(self):
        qs=self.video_a.playlist_featured.all()
        self.assertEqual(qs.count(),2)

    def test_playlist_video_through_model(self):
        v_qs=sorted(list(self.video_qs.values_list('id')))
        video_qs=sorted(list(self.obj_b.videos.all().values_list('id')))
        playlist_item_qs=self.obj_b.playlistitem_set.all().values('video')
        self.assertEqual(video_qs,v_qs,playlist_item_qs)


    def test_playlist_video_items(self):
        count=self.obj_b.videos.all().count()

        self.assertEqual(count,self.video_qs.count())

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
        self.assertEqual(qs.count(), 7)

    def test_draft_case(self):
        qs=Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(),6)

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
