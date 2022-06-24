from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Blog, BlogFoto
from .forms import FotoForm, FileForm
import csv
from datetime import datetime


class ListBlog(ListView):
    model = Blog
    template_name = 'blog/list_blog.html'


class DetailBlog(DetailView):
    model = Blog
    template_name = 'blog/detail_blog.html'


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/create_blog.html'
    fields = ['text', ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('next_url') == 'edit':
            return reverse('edit_blog', args=[self.object.id])
        return super().get_success_url()


class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog/edit_blog.html'
    fields = ['text', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['foto_form'] = FotoForm()
        context['fotos'] = self.object.foto.all()
        return context

    def get(self, request: HttpRequest, *args, **kwargs):

        author = get_object_or_404(Blog, id=kwargs['pk']).user
        if author != request.user:
            return HttpResponseForbidden(request)

        return super().post(self, request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):

        current_blog = get_object_or_404(Blog, id=kwargs['pk'])
        if current_blog.user != request.user:
            return HttpResponseForbidden(request)

        files = request.FILES.getlist('files')
        if files:
            for file in files:
                img = BlogFoto(blog=current_blog, foto=file)
                img.save()

        return super().post(self, request, *args, **kwargs)


class EditFoto(LoginRequiredMixin, UpdateView):
    model = BlogFoto
    template_name = 'blog/edit_foto.html'
    fields = ['description']

    def get_object(self):
        foto = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if foto.blog.user != self.request.user:
            raise PermissionDenied
        return foto

    def get_success_url(self):
        return reverse('edit_blog', args=[self.object.blog.id])


class DeleteFoto(LoginRequiredMixin, DeleteView):
    model = BlogFoto
    template_name = 'blog/delete_foto.html'

    def get_object(self):
        foto = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if foto.blog.user != self.request.user:
            raise PermissionDenied
        return foto

    def get_success_url(self):
        return reverse('edit_blog', args=[self.object.blog.id])


def decode_file(file):
    try:
        return file.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file.decode('windows-1251')
        except UnicodeDecodeError:
            return None


@login_required
def upload_multi_entries(request: HttpRequest):
    message = None

    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            file = file_form.cleaned_data['file']
            if file.content_type == 'text/csv':
                file = decode_file(file.read())
                if file:
                    n = 0
                    file_csv = csv.reader(file.split('\n'), delimiter=';', quotechar='"')
                    for row in file_csv:
                        if len(row) == 2:
                            blog = Blog(
                                user=request.user,
                                created=datetime.strptime(row[0], '%Y-%m-%d'),
                                text=row[1],
                            )
                            blog.save()
                            n += 1
                    message = _('Успешно! Количество добавленных записей: %(n)d') % {'n': n}

                else:
                    file_form.add_error(None, _('Неизвестная кодировка файла. Используйте UTF-8 или Windows-1251'))

            else:
                file_form.add_error(None, _('Файл не csv'))

    else:
        file_form = FileForm()

    return render(request, 'blog/upload_csv.html', {'form': file_form, 'message': message})
