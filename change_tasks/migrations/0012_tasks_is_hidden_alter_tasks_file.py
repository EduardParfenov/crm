# Generated by Django 4.1.6 on 2023-05-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_tasks', '0011_alter_tasks_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='file',
            field=models.FileField(blank=True, upload_to='tasks/files', verbose_name='пдф документ'),
        ),
    ]