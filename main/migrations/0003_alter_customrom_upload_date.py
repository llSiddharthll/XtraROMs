# Generated by Django 5.0 on 2024-03-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_modcomment_romcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrom',
            name='upload_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
