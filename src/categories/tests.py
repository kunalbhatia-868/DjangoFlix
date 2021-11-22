from django.test import TestCase
from .models import Category
from playlists.models import Playlist
# Create your tests here.
class CategoryTestCase(TestCase):
    def setUp(self):
        self.cat_a=Category.objects.create(title='Action')
        self.cat_b=Category.objects.create(title='Comedy',active=False)
        self.play_a=Playlist.objects.create(title='New Title',category=self.cat_a)


    def test_is_active(self):    
        self.assertTrue(self.cat_a.active)

    def test_is_not_active(self):    
        self.assertFalse(self.cat_b.active)    

    def test_realted_playlist(self):
        qs=self.cat_a.playlists.all()
        self.assertEqual(qs.count(),1)    