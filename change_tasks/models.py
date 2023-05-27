import os
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=40, verbose_name='Заголовок поста')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение поста', upload_to='news/images')
    data = models.DateField(default=datetime.date.today, verbose_name='Дата нашего поста')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Новости'


class ListProject(models.Model):
    name = models.CharField(max_length=250, verbose_name="Заголовок проекта")
    description = models.TextField(
        max_length=5000, blank=True, verbose_name="Описание проекта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список проектов'
        verbose_name_plural = 'Список проектов'


class Tasks(models.Model):
    Standard = models.ForeignKey(ListProject, on_delete=models.CASCADE, verbose_name="Проект")
    created_by = models.ManyToManyField(User, verbose_name="Задача создана пользователем")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата выдачи")
   
    name = models.CharField(max_length=250, verbose_name="заголовок задачи")
    description = models.TextField(
        max_length=5000, blank=True, verbose_name="Описание задачи")

    assigned_to = models.ManyToManyField(User, blank=True, related_name='tasks_assigned', verbose_name="Исполнитель")
    is_hidden = models.BooleanField(default=False)
    file = models.FileField(upload_to='tasks/files',
                           verbose_name="пдф документ", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'


class TaskAssignment(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="имя")
    email = models.EmailField(max_length=250, verbose_name="майл")
    phone = models.CharField(max_length=100, verbose_name="телефон")
    subject = models.CharField(max_length=100, verbose_name="сообщение")
    date_posted = models.DateTimeField(
        default=timezone.now, verbose_name="дата обращения")
    answer_contact = models.CharField(
        max_length=100, verbose_name="ответ администратора", default='')
    contact_info = models.ForeignKey(User, on_delete=models.CASCADE,
                                     null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"















# код ниже не используется
def save_lesson_files(instance, filename):
    upload_to = 'file/'
    ext = filename.split('.')[-1]

    if instance.tasks_id:
        filename = 'task_files/{}/{}.{}'.format(
            ext)
        if os.path.exists(filename):
            new_name = str(instance.name) + str('1')
            filename = 'task_images/{}/{}.{}'.format(
                instance.name, new_name, ext)
    return os.path.join(upload_to, filename)
# конец кода