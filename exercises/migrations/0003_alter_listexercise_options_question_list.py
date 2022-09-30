# Generated by Django 4.0.5 on 2022-09-30 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_listexercise'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listexercise',
            options={'ordering': ('-availability',)},
        ),
        migrations.AddField(
            model_name='question',
            name='list',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='exercises.listexercise'),
            preserve_default=False,
        ),
    ]
