# Generated by Django 4.2.1 on 2023-06-24 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_projectsdate_end_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsIdeas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.CharField(max_length=255, verbose_name='Ideia de projeto')),
                ('idea_level', models.CharField(max_length=255, verbose_name='Nível')),
                ('idea_explanation', models.TextField(verbose_name='Explicação')),
                ('idea_deadline', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.projectsdate', verbose_name='Prazo da ideia')),
            ],
        ),
    ]