# Generated by Django 4.0.5 on 2022-12-27 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournamment', '0006_alter_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='group',
            field=models.ForeignKey(max_length=2, on_delete=django.db.models.deletion.CASCADE, to='tournamment.group'),
        ),
    ]