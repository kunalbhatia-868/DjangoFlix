from django import db
from django.test import TestCase
from django.contrib.auth import get_user_model
import random
from playlists.models import Playlist
from ratings.models import Rating,RatingChoice
from django.db.models import Avg,Max,Min
# Create your tests here.

User=get_user_model()


class RatingTestCase(TestCase):
    def create_playlist(self):
            items=[]
            self.playlist_count=random.randint(0,500)
            for i in range(0,self.playlist_count):
                items.append(Playlist(title=f'playlist_tv_show_{i}'))
            Playlist.objects.bulk_create(items)
            self.playlists=Playlist.objects.all()

    def create_user(self):
        items=[]
        self.user_count=random.randint(0,500)
        for i in range(0,self.user_count):
            items.append(User(username=f'user_{i}'))
        User.objects.bulk_create(items)
        self.users=User.objects.all()

    def create_ratings(self):
        items=[]
        self.rating_total=[]
        self.rating_count=1000
        for i in range(0,self.rating_count):
            user_obj=self.users.order_by('?').first()
            ply_obj=self.playlists.order_by('?').first()
            rating_val=random.choice(RatingChoice.choices)[0]
            if rating_val is not None:
                self.rating_total.append(rating_val)
            items.append(
                Rating(
                    user=user_obj,
                    content_object=ply_obj,
                    value=rating_val
                )
            )
        Rating.objects.bulk_create(items)
        self.ratings=Rating.objects.all()
    
    def setUp(self):
        self.create_user()
        self.create_playlist()
        self.create_ratings()

    def test_user_count(self):
        qs=User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.user_count)
        self.assertEqual(self.users.count(),self.user_count)


    def test_playlist_count(self):
        qs=Playlist.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.playlist_count)
        self.assertEqual(self.playlists.count(),self.playlist_count)

    def test_rating_count(self):
        qs=Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.rating_count)
        self.assertEqual(self.ratings.count(),self.rating_count)

    def test_rating_random_choices(self):
        value_set=set(Rating.objects.values_list('value',flat=True))
        self.assertTrue(len(value_set)>1)

    def test_rating_agg(self):
        db_avg=Rating.objects.aggregate(average=Avg('value'))['average']
        self.assertIsNotNone(db_avg)
        self.assertTrue(db_avg>0)
        total_sum=sum(self.rating_total)
        passed_avg=total_sum/(len(self.rating_total)*1.0)
        self.assertEqual(passed_avg,db_avg)
        print(passed_avg)
        
    def test_rating_playlist_agg(self):
        item_1=Playlist.objects.aggregate(average=Avg('ratings__value'))['average']
        self.assertIsNotNone(item_1)
        self.assertTrue(item_1>0)
    