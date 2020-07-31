# Generated by Django 2.2.13 on 2020-07-30 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0005_auto_20200421_1533'),
        ('request', '0005_mentee_request_model_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='mentor_request_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_signup.mentee_model')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.mentee_request_model')),
            ],
        ),
    ]
