# Generated by Django 5.0.1 on 2024-01-30 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_pull', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='size_prediction',
            new_name='predicted_size',
        ),
        migrations.AddField(
            model_name='record',
            name='predicted_colour',
            field=models.CharField(default='not available', max_length=255),
        ),
        migrations.AddField(
            model_name='record',
            name='predicted_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='colour',
            field=models.CharField(default='not available', max_length=255),
        ),
        migrations.AlterField(
            model_name='record',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
