def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    uploaded_extension = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3','.mp4']
    if not uploaded_extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
