# Generated by Django 4.2.2 on 2023-06-30 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0001_initial'),
        ('projects', '0014_alter_project_stack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_inspired',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ideas.projectidea', verbose_name='Inspirado em'),
        ),
    ]
