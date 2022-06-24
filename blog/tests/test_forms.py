from django.forms import ClearableFileInput
from django.test import TestCase, SimpleTestCase
from ..forms import FotoForm, FileForm


class FotoFormTest(SimpleTestCase):

    def test_foto_form_field(self):
        form = FotoForm()
        self.assertEqual(form.fields['files'].label, 'Загрузить фото')
        self.assertIsInstance(form.fields['files'].widget, ClearableFileInput)


class FileFormTest(SimpleTestCase):

    def test_foto_form_field(self):
        form = FileForm()
        self.assertEqual(form.fields['file'].label, 'Загрузить файл')
        self.assertEqual(form.fields['file'].help_text, 'Выберите файл .csv')
