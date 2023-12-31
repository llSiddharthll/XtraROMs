# Generated by Django 4.2.4 on 2023-09-29 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('image_url', models.URLField()),
                ('article_id', models.CharField(max_length=255)),
                ('article_title', models.CharField(max_length=255)),
                ('article_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_authorized', models.BooleanField(default=False)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomROM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('device', models.CharField(max_length=50)),
                ('credits', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(upload_to='images')),
                ('link', models.URLField(max_length=225)),
                ('details', models.TextField()),
                ('upload_date', models.DateField(blank=True, null=True)),
                ('boot_link', models.URLField(blank=True, max_length=225, null=True)),
                ('likes', models.ManyToManyField(default=0, related_name='liked_roms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomMOD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images')),
                ('credits', models.CharField(max_length=50, null=True)),
                ('link', models.URLField()),
                ('details', models.TextField()),
                ('upload_date', models.DateField(blank=True, null=True)),
                ('likes', models.ManyToManyField(default=0, related_name='liked_mods', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
