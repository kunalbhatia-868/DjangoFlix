from django.test import TestCase
from .models import Video
from django.utils import timezone

# Create your tests here.


class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="This is my Title")
        Video.objects.create(title="This is my Title",state=Video.VideoStateOptions.PUBLISH)


    def test_valid_title(self):
        title = "This is my Title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        title = "This is my Title"
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs=Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)

    def test_publish_case(self):
        qs=Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
        published_qs=Video.objects.filter(
            state=Video.VideoStateOptions.PUBLISH,
            publish_timestamp__lte=timezone.now()
        )
        self.assertEqual(qs.count(),1)
        self.assertTrue(published_qs.exists())
