# Generated by Django 3.2.9 on 2021-11-21 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0004_alter_playlist_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='videos',
        ),
    ]
