# Generated by Django 2.2.5 on 2019-09-17 02:31

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', localflavor.us.models.USStateField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CanterburyTales.courses.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('published', models.DateField()),
                ('description', models.TextField()),
                ('audience', models.ManyToManyField(to='CanterburyTales.courses.Audience')),
                ('authors', models.ManyToManyField(to='CanterburyTales.courses.User')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CanterburyTales.courses.Organization')),
                ('tags', models.ManyToManyField(to='CanterburyTales.courses.Tag')),
            ],
        ),
    ]