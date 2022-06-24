from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListBlog.as_view(), name='main'),
    path('blog/create/', views.CreateBlog.as_view(), name='create_blog'),
    path('blog/<int:pk>/', views.DetailBlog.as_view(), name='detail_blog'),
    path('blog/<int:pk>/edit/', views.UpdateBlog.as_view(), name='edit_blog'),
    path('blog/foto/<int:pk>/edit/', views.EditFoto.as_view(), name='edit_foto'),
    path('blog/foto/<int:pk>/delete/', views.DeleteFoto.as_view(), name='delete_foto'),
    path('blog/upload/', views.upload_multi_entries, name='upload_csv'),
]
