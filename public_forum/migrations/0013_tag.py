# Generated by Django 2.2.13 on 2020-07-18 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_forum', '0012_auto_20200717_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20)),
            ],
        ),
    ]
