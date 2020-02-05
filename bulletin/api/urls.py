from django.urls import path

from bulletin.api import views

urlpatterns = [
    path('', views.BulletinList.as_view(), name='bulletin-list'),
]