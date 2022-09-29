# Generated by Django 4.0.5 on 2022-09-29 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('availability', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
            ],
        ),
    ]
