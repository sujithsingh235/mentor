# Generated by Django 2.2.13 on 2020-07-30 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_auto_20200730_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentee_request_model',
            name='status',
            field=models.CharField(default='pending', max_length=20),
            preserve_default=False,
        ),
    ]
