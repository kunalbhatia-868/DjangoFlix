from django.test import TestCase
from .models import Video
from djangoflix.db.models import PublishStateOptions
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.


class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a=Video.objects.create(title="This is my Title",video_id="first")
        self.obj_b=Video.objects.create(title="This is my Title",video_id="second",state=PublishStateOptions.PUBLISH)


    def test_valid_title(self):
        title = "This is my Title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_slug_field(self):
        title=self.obj_a.title
        test_slug=slugify(title)
        self.assertEqual(test_slug,self.obj_a.slug)

    def test_created_count(self):
        title = "This is my Title"
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs=Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)

    def test_publish_case(self):
        qs=Video.objects.filter(state=PublishStateOptions.PUBLISH)
        published_qs=Video.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=timezone.now()
        )
        self.assertEqual(qs.count(),1)
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs=Video.objects.all().published()
        published_qs_2=Video.objects.all().published()
        self.assertEqual(published_qs.count(),published_qs_2.count())
        self.assertTrue(published_qs)
