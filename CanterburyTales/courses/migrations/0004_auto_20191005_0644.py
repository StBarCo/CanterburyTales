# Generated by Django 2.2.5 on 2019-10-05 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20191002_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lesson_length',
        ),
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.DurationField(null=True),
        ),
    ]