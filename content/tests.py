# blog/tests.py

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User


class PostModelTest(TestCase):
    def test_create_post(self):
        post = Post.objects.create(
            title='Model Test Post',
            content='Test content for model.',
            author='ModelTester',
            published_date=timezone.now(),
            is_published=True
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, 'Model Test Post')
        self.assertTrue(post.is_published)


class PostFormTest(TestCase):
    def test_post_form_valid(self):
        form_data = {
            'title': 'Form Test Post',
            'content': 'Test content for form.',
            'author': 'FormTester',
            'published_date': timezone.now(),
            'is_published': True
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form_data = {
            'title': '',  # invalid
            'content': '',  # invalid
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class PostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_post_view(self):
        response = self.client.post(reverse('create_post'), {
            'title': 'New Post',
            'content': 'Post content',
            'author': 'Test Author',
            'published_date': '2025-08-02',
            'is_published': True
        })
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.status_code, 302)  # Should redirect on success

    def test_create_post_view_get(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')  # Ensure form is in the page


from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from content.models import Post
import tempfile
from PIL import Image
import shutil


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PostImageUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def generate_test_image(self):
        image = Image.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file, format='JPEG')
        temp_file.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=temp_file.read(),
            content_type='image/jpeg'
        )

    def test_create_post_with_image(self):
        image_file = self.generate_test_image()

        response = self.client.post(reverse('create_post'), {
            'title': 'Test Post',
            'content': 'Some content',
            'author': 'testuser',
            'published_date': '2025-08-02',
            'image': image_file,
            'is_published': True
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()
        print(f"Uploaded image name: {post.image.name}")  # 👀 Debug
        self.assertTrue(post.image.name.startswith('post_images/'))
