# Generated by Django 2.2.13 on 2020-07-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20200729_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news_model',
            name='published_at',
            field=models.DateTimeField(blank=True),
        ),
    ]
