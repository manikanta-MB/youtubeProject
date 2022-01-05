# Generated by Django 2.2 on 2022-01-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeApp', '0010_dislike_like'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='dislike',
            constraint=models.UniqueConstraint(fields=('video', 'by_whom'), name='unique_dislikes_per_video_per_user'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('video', 'by_whom'), name='unique_likes_per_video_per_user'),
        ),
    ]