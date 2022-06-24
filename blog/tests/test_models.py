from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from ..models import Blog, BlogFoto
from django.conf import settings
import shutil


class BlogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        Blog.objects.create(user=user, text='Текст записи блога')

    def test_user_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Автор')

    def test_created_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'Дата записи')

    def test_text_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Текст записи')

    def test_get_absolute_url(self):
        blog = Blog.objects.get(id=1)
        url = blog.get_absolute_url()
        self.assertURLEqual(url, '/blog/1/', msg_prefix='Неправильный URL страницы просмотра записи блога')


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class BlogFotoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_foto = SimpleUploadedFile('image.jpg', b'fff', content_type='image/jpeg')
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        blog = Blog.objects.create(user=user, text='Текст записи блога')
        BlogFoto.objects.create(blog=blog, foto=test_foto, description='test_foto')

    def test_foto_label(self):
        foto = BlogFoto.objects.get(id=1)
        field_label = foto._meta.get_field('foto').verbose_name
        self.assertEqual(field_label, 'Фотография')

    def test_description_label(self):
        foto = BlogFoto.objects.get(id=1)
        field_label = foto._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Подпись')

    def test_path_for_foto(self):
        foto = BlogFoto.objects.get(id=1)
        path_foto = foto.foto.url
        self.assertEqual(path_foto, '/media/blog/nik/image.jpg')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()

