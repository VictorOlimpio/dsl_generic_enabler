# Generated by Django 3.0 on 2020-07-23 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsl_layer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measures',
            name='week_day',
        ),
        migrations.AddField(
            model_name='measures',
            name='season',
            field=models.FloatField(db_column='season', null=True),
        ),
        migrations.AddField(
            model_name='measures',
            name='weekday',
            field=models.FloatField(db_column='weekday', null=True),
        ),
    ]
