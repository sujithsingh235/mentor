# Generated by Django 2.2.13 on 2020-07-22 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemes', '0004_auto_20200722_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheme',
            name='Headed_by',
            field=models.TextField(default='N/A'),
        ),
    ]