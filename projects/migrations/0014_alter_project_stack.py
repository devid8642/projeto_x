# Generated by Django 4.2.1 on 2023-06-28 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_project_stack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='stack',
            field=models.CharField(choices=[('1', 'Backend'), ('2', 'Frontend'), ('3', 'Fullstack')], max_length=255, null=True, verbose_name='Stack utilizada'),
        ),
    ]
