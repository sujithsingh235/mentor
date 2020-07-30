# Generated by Django 2.2.13 on 2020-07-29 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='news_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('url_to_image', models.URLField()),
                ('content', models.TextField()),
                ('published_at', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
    ]