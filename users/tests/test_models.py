from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from ..models import Profile
from django.conf import settings
import shutil


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_avatar = SimpleUploadedFile('avatar.jpg', b'fff', content_type='image/jpeg')
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        Profile.objects.create(user=user, about='Автор блога', ava=test_avatar)

    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_about_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('about').verbose_name
        self.assertEqual(field_label, 'О себе')

    def test_ava_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('ava').verbose_name
        self.assertEqual(field_label, 'Фото')

    def test_path_for_foto(self):
        profile = Profile.objects.get(id=1)
        path_foto = profile.ava.url
        self.assertEqual(path_foto, '/media/users/foto/nik.jpg')

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()
