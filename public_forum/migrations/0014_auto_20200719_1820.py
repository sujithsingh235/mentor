# Generated by Django 2.2.13 on 2020-07-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_forum', '0013_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='answer',
            field=models.TextField(),
        ),
    ]
