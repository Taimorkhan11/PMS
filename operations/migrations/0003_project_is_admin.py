# Generated by Django 5.1.1 on 2024-09-30 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_alter_project_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
