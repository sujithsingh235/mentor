# Generated by Django 2.2.8 on 2020-04-21 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0004_auto_20200420_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentee_model',
            name='field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_signup.field'),
        ),
        migrations.AlterField(
            model_name='mentee_model',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=25),
        ),
        migrations.AlterField(
            model_name='mentee_model',
            name='sub_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_signup.sub_field'),
        ),
        migrations.AlterField(
            model_name='mentor_model',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=25),
        ),
    ]
