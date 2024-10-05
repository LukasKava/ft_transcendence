#0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30, blank=True)),
                ('last_name', models.CharField(max_length=30, blank=True)),
				('display_name', models.CharField(max_length=150, blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff' = models.BooleanField(default=False)), 

                # Add other fields as needed
            ],
        ),
    ]
