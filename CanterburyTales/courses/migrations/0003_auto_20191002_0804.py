# Generated by Django 2.2.5 on 2019-10-02 12:04

import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='audience',
        ),
        migrations.AddField(
            model_name='course',
            name='audience',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(default=(5, 10)),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Audience',
        ),
    ]
