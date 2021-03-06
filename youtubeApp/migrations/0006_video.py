# Generated by Django 2.2 on 2022-01-04 10:44

from django.db import migrations, models
import django.db.models.deletion
import youtubeApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeApp', '0005_auto_20220103_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to=youtubeApp.models.video_upload_path)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='youtubeApp.User')),
            ],
        ),
    ]
