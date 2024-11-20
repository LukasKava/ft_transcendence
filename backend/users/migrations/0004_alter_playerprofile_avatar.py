# Generated by Django 4.1.7 on 2024-11-08 11:12

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_playerprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to='avatars/', validators=[users.validators.validate_file_size]),
        ),
    ]
