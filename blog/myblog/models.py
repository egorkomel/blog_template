from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model): # создаем класс Post (таблицу в БД) и поля
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # создаем отношение с табл. User
    tag = models.CharField(max_length=200)

    def __str__(self):  # нужна, чтобы в админке посты отображались по title, а не по id
        return self.title
