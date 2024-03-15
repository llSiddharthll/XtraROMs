# Generated by Django 5.0 on 2024-03-15 04:50

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_blog_link_alter_blog_written_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='custommod',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='name'),
        ),
        migrations.AddField(
            model_name='customrom',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='name'),
        ),
    ]
