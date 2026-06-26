from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.academy_home, name='academy_home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
