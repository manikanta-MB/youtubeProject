# Generated by Django 2.2 on 2022-01-06 11:33

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeApp', '0011_auto_20220105_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('video_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to='youtubeApp.User')),
            ],
        ),
        migrations.AddConstraint(
            model_name='playlist',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_playlist_per_user'),
        ),
    ]
