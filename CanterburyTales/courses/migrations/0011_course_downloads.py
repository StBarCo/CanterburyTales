# Generated by Django 2.2.5 on 2019-10-18 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20191014_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='downloads',
            field=models.IntegerField(default=0),
        ),
    ]
