import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from ..models import Blog, BlogFoto


class ListBlogViewTest(TestCase):
    number_of_entries = 15  # количество записей для заполнения базы
    blog_text = 'Текст записи блога '

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        for num in range(cls.number_of_entries):
            Blog.objects.create(user=user, text=f'{cls.blog_text} {num}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/list_blog.html')

    def test_numbers_blog_in_list_view(self):
        resp = self.client.get(reverse('main'))
        self.assertEqual(len(resp.context['blog_list']), self.number_of_entries)

    def test_context_in_blog_list_view(self):
        # Проверка, что выведено определенное количество записей
        resp = self.client.get(reverse('main'))
        self.assertContains(resp, self.blog_text, self.number_of_entries, status_code=200)


class DetailBlogViewTest(TestCase):

    blog_text = 'Текст записи блога '

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        Blog.objects.create(user=user, text=f'{cls.blog_text}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/blog/1/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('detail_blog', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('detail_blog', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/detail_blog.html')

    def test_context_blog_in_detail_view(self):
        resp = self.client.get(reverse('detail_blog', args=[1]))
        self.assertIsNotNone(resp.context.get('blog'), msg='Нет переменной шаблона:')

    def test_context_in_blog_list_view(self):
        # Проверка, что выведена запись блога
        resp = self.client.get(reverse('detail_blog', args=[1]))
        self.assertContains(resp, self.blog_text, 1, status_code=200)

    def test_404_for_non_exist_blog(self):
        resp = self.client.get(reverse('detail_blog', args=[2]))
        self.assertEqual(resp.status_code, 404)


class CreateBlogViewTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.blog_text = 'Новая запись блога'
        cls.test_user = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get('/blog/create/')
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("create_blog")}')

    # Далее все проверки для авторизованного пользователя
    def test_url_exists_at_desired_location(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get('/blog/create/')
        self.assertEqual(resp.status_code, 200)

    def test_url_accessible_by_name(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get(reverse('create_blog'))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get(reverse('create_blog'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/create_blog.html')

    def test_context_in_create_blog(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get(reverse('create_blog'))
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.context.get('form'))
        self.assertIsNotNone(resp.context.get('user'))
        self.assertContains(resp, 'method="post"')

    def test_create_new_blog(self):
        self.client.force_login(self.test_user)
        self.client.post(reverse('create_blog'), data={'text': self.blog_text})
        new_blog = Blog.objects.get(id=1)
        self.assertEqual(new_blog.user, self.test_user)
        self.assertEqual(new_blog.text, self.blog_text)


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class UpdateBlogViewTest(TestCase):

    blog_text_old = None
    author = None

    @classmethod
    def setUpTestData(cls):

        cls.blog_text_old = 'Старая запись блога'
        cls.blog_text_changed = 'Измененная запись блога'
        cls.test_foto = SimpleUploadedFile('image.jpg', b'fff', content_type='image/jpeg')
        cls.author = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        cls.just_user = User.objects.create_user(username='jast_user', password='111', first_name='noname', last_name='no_last_name')
        cls.test_blog = Blog.objects.create(user=cls.author, text=f'{cls.blog_text_old}')

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get('/blog/1/edit/')
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("edit_blog", args=[1])}')

    def test_404_for_non_exist_blog(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('edit_blog', args=[2]))
        self.assertEqual(resp.status_code, 404)

    def test_access_for_author(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('edit_blog', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_access_for_non_author(self):
        self.client.force_login(self.just_user)
        resp = self.client.get(reverse('edit_blog', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_url_exists_at_desired_location(self):
        self.client.force_login(self.author)
        resp = self.client.get('/blog/1/edit/')
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('edit_blog', args=[1]))
        self.assertTemplateUsed(resp, 'blog/edit_blog.html')

    def test_post_change_text(self):
        self.client.force_login(self.author)
        resp = self.client.post(reverse('edit_blog', args=[1]), data={'text': self.blog_text_changed})
        blog = Blog.objects.get(id=1)
        self.assertEqual(blog.text, self.blog_text_changed)

    def test_post_add_foto(self):
        self.client.force_login(self.author)
        self.assertEqual(BlogFoto.objects.all().count(), 0, msg='Должно быть 0 фото')
        resp = self.client.post(reverse('edit_blog', args=[1]),
                                data={'text': self.blog_text_changed, 'files': [self.test_foto]})
        blog = Blog.objects.get(id=1)
        self.assertEqual(blog.text, self.blog_text_changed)
        self.assertEqual(BlogFoto.objects.all().count(), 1,  msg='Должно быть создано 1 фото')
        foto = BlogFoto.objects.get(id=1)
        self.assertEqual(foto.blog, blog, msg='фото не принадлежит нужному блогу')
        self.assertEqual(foto.foto.url, '/media/blog/nik/image.jpg', msg='путь сохранения или имя фото не верны')

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()

@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class EditFotoViewTest(TestCase):

    old_descr = 'Старое описание'
    new_descr = 'Новое описание'
    test_foto = None
    test_blog = None
    author = None

    @classmethod
    def setUpTestData(cls):

        cls.test_foto = SimpleUploadedFile('image.jpg', b'fff', content_type='image/jpeg')
        cls.author = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        cls.just_user = User.objects.create_user(username='jast_user', password='111', first_name='noname', last_name='no_last_name')
        cls.test_blog = Blog.objects.create(user=cls.author, text='Just text')
        cls.test_foto = BlogFoto.objects.create(blog=cls.test_blog, foto=cls.test_foto, description=cls.old_descr)

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('edit_foto', args=[1]))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("edit_foto", args=[1])}')

    def test_404_for_non_exist_foto(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('edit_foto', args=[2]))
        self.assertEqual(resp.status_code, 404)

    def test_access_for_author(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('edit_foto', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_access_for_non_author(self):
        self.client.force_login(self.just_user)
        resp = self.client.get(reverse('edit_foto', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_url_exists_at_desired_location(self):
        self.client.force_login(self.author)
        resp = self.client.get('/blog/foto/1/edit/')
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('edit_foto', args=[1]))
        self.assertTemplateUsed(resp, 'blog/edit_foto.html')

    def test_post_change_description(self):
        self.client.force_login(self.author)
        foto = BlogFoto.objects.get(id=1)
        self.assertEqual(foto.description, self.old_descr)
        resp = self.client.post(reverse('edit_foto', args=[1]), data={'description': self.new_descr})
        foto.refresh_from_db()
        self.assertEqual(foto.description, self.new_descr)
        self.assertRedirects(resp, reverse('edit_blog', args=[1]))

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'files_test' / 'media')
class DeleteFotoViewTest(TestCase):

    test_foto = None
    test_blog = None
    author = None

    @classmethod
    def setUpTestData(cls):

        cls.test_foto = SimpleUploadedFile('image.jpg', b'fff', content_type='image/jpeg')
        cls.author = User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')
        cls.just_user = User.objects.create_user(username='jast_user', password='111', first_name='noname', last_name='no_last_name')
        cls.test_blog = Blog.objects.create(user=cls.author, text='Just text')
        cls.test_foto = BlogFoto.objects.create(blog=cls.test_blog, foto=cls.test_foto, description='description')

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("delete_foto", args=[1])}')

    def test_404_for_non_exist_foto(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('delete_foto', args=[2]))
        self.assertEqual(resp.status_code, 404)

    def test_access_for_author(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertEqual(resp.status_code, 200)

    def test_access_for_non_author(self):
        self.client.force_login(self.just_user)
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertEqual(resp.status_code, 403)

    def test_url_exists_at_desired_location(self):
        self.client.force_login(self.author)
        resp = self.client.get('/blog/foto/1/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.author)
        resp = self.client.get(reverse('delete_foto', args=[1]))
        self.assertTemplateUsed(resp, 'blog/delete_foto.html')

    def test_post_delete_foto(self):
        self.client.force_login(self.author)
        self.assertEqual(BlogFoto.objects.all().count(), 1, msg='Должно быть 1 фото')
        resp = self.client.post(reverse('delete_foto', args=[1]), follow=True)
        self.assertEqual(BlogFoto.objects.all().count(), 0, msg='Должно быть 0 фото')
        self.assertRedirects(resp, reverse('edit_blog', args=[1]))

    @classmethod
    def tearDownClass(cls):
        # удаление временной папки с фото
        shutil.rmtree(settings.MEDIA_ROOT.parent)
        super().tearDownClass()


class UploadMultiEntriesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='nik', password='111', first_name='Иван', last_name='Петров')

    def test_redirect_for_unauthorized_user(self):
        # проверка перенаправления на страницу логина для неавторизованного пользователя
        resp = self.client.get(reverse('upload_csv'))
        self.assertRedirects(resp, f'{reverse("login")}?next={reverse("upload_csv")}')

    # Далее все проверки для авторизованного пользователя
    def test_url_exists_at_desired_location(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get('/blog/upload/')
        self.assertEqual(resp.status_code, 200)

    def test_url_accessible_by_name(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get(reverse('upload_csv'))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(User.objects.get(id=1))
        resp = self.client.get(reverse('upload_csv'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/upload_csv.html')

    def test_upload_file(self):
        data = '2022-06-10;Запись 1\n2022-06-11;Запись 2\n2022-06-11;Запись 3'.encode(encoding='utf-8')
        self.client.force_login(User.objects.get(id=1))
        test_file = SimpleUploadedFile('file.csv', data, content_type='text/csv')
        self.assertEqual(Blog.objects.all().count(), 0, msg='Сначала записей не должно быть')
        self.client.post(reverse('upload_csv'), data={'file': test_file})
        self.assertEqual(Blog.objects.all().count(), 3, msg='Должны создаться две записи')
