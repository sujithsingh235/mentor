# Generated by Django 2.2.13 on 2020-07-25 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_forum', '0014_auto_20200719_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='tag_with_question_id',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('tag', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='questions',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
