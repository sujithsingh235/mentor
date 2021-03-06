# Generated by Django 2.2.8 on 2020-04-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homepage', '0002_delete_req'),
    ]

    operations = [
        migrations.CreateModel(
            name='req',
            fields=[
                ('req_id', models.AutoField(primary_key=True, serialize=False)),
                ('mentor_id', models.IntegerField()),
                ('mentee_id', models.IntegerField()),
                ('req_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='pending', max_length=25)),
            ],
        ),
    ]
