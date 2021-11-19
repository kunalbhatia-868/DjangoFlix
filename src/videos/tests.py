from django.test import TestCase
from .models import Video

# Create your tests here.


class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="This is my Title")

    def test_valid_title(self):
        title = "This is my Title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        title = "This is my Title"
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 1)
