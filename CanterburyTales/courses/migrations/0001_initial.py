# Generated by Django 2.2.5 on 2019-09-24 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('year_written', models.IntegerField(default=2019)),
                ('posted', models.DateField(null=True)),
                ('description', models.TextField()),
                ('lesson_length', models.IntegerField(null=True)),
                ('audience', models.ManyToManyField(to='courses.Audience')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.Profile')),
                ('tags', models.ManyToManyField(to='courses.Tag')),
                ('upvotes', models.ManyToManyField(default=0, related_name='upvotes', to='profiles.Profile')),
            ],
        ),
    ]
