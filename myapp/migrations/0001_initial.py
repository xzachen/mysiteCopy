# Generated by Django 2.0.2 on 2018-05-04 13:42

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APPUser',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'appuser',
                'ordering': ['userid'],
            },
            managers=[
                ('maneger', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CollectionNote',
            fields=[
                ('cnid', models.AutoField(primary_key=True, serialize=False)),
                ('noteid', models.IntegerField()),
                ('cuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-cnid'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=20)),
                ('schoolYear', models.CharField(max_length=20)),
                ('term', models.CharField(max_length=20)),
                ('credit', models.FloatField()),
                ('intstartSection', models.IntegerField()),
                ('endSection', models.IntegerField()),
                ('startWeek', models.IntegerField()),
                ('endWeek', models.IntegerField()),
                ('dayOfWeek', models.IntegerField()),
                ('classroom', models.CharField(max_length=20)),
                ('teacher', models.CharField(max_length=20)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.APPUser')),
            ],
            options={
                'db_table': 'appcourse',
                'ordering': ['cid'],
            },
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('meta_description', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
                ('auther', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'note',
                'ordering': ['-date'],
            },
        ),
    ]
