# Generated by Django 4.2.1 on 2023-06-01 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_comment_options_alter_project_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Link do projeto'),
        ),
    ]
