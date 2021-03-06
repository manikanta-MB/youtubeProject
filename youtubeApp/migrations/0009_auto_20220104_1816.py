# Generated by Django 2.2 on 2022-01-04 12:46

from django.db import migrations, models
import youtubeApp.models
import youtubeApp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeApp', '0008_auto_20220104_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to=youtubeApp.models.video_upload_path, validators=[youtubeApp.validators.validate_file_extension]),
        ),
    ]
