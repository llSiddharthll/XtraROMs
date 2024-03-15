# Generated by Django 5.0 on 2024-03-09 23:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomROM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('device', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images')),
                ('link', models.URLField(max_length=225)),
                ('details', models.TextField()),
                ('upload_date', models.DateField(auto_now=True)),
                ('boot_link', models.URLField(blank=True, max_length=225, null=True)),
                ('comments', models.ManyToManyField(blank=True, related_name='rom_comments', to='main.comment')),
                ('credits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.credits')),
                ('likes', models.ManyToManyField(related_name='liked_roms', to='main.like')),
            ],
        ),
        migrations.CreateModel(
            name='CustomMOD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images')),
                ('link', models.URLField()),
                ('details', models.TextField()),
                ('upload_date', models.DateField(auto_now=True)),
                ('comments', models.ManyToManyField(blank=True, related_name='mod_comments', to='main.comment')),
                ('credits', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.credits')),
                ('likes', models.ManyToManyField(related_name='liked_mods', to='main.like')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_authorized', models.BooleanField(default=False)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pictures/akatsuki_logo_xwqj26.png', null=True, upload_to='profile_picture/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]