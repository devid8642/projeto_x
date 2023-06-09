# Generated by Django 4.2.2 on 2023-06-30 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.CharField(max_length=255, verbose_name='Ideia de projeto')),
                ('level', models.CharField(choices=[('1', 'Fácil'), ('2', 'Médio'), ('3', 'Difícil')], max_length=255, verbose_name='Nível')),
                ('stack', models.CharField(choices=[('1', 'Backend'), ('2', 'Frontend'), ('3', 'Fullstack')], max_length=255, null=True, verbose_name='Stack')),
                ('explanation', models.TextField(verbose_name='Explicação')),
                ('start_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data inicial')),
            ],
            options={
                'verbose_name': 'Project Idea',
                'verbose_name_plural': 'Projects Ideas',
                'db_table': 'projects_ideas',
            },
        ),
    ]
