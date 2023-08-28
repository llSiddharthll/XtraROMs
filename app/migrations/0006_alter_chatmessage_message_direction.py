# Generated by Django 4.1.2 on 2023-08-28 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_chatmessage_message_direction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='message_direction',
            field=models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')], default='outgoing', max_length=10),
        ),
    ]