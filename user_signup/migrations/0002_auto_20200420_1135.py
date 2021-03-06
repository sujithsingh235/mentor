# Generated by Django 2.2.8 on 2020-04-20 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='sub_field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_field_name', models.CharField(max_length=50)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_signup.field')),
            ],
        ),
        migrations.DeleteModel(
            name='sample',
        ),
        migrations.AddField(
            model_name='mentee_model',
            name='username',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='mentor_model',
            name='pay_per_month',
            field=models.PositiveIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='mentor_model',
            name='username',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AlterField(
            model_name='mentee_model',
            name='field',
            field=models.ForeignKey(default='others', on_delete=django.db.models.deletion.SET_DEFAULT, to='user_signup.field'),
        ),
        migrations.AlterField(
            model_name='mentee_model',
            name='startup',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mentee_model',
            name='sub_field',
            field=models.ForeignKey(default='others', on_delete=django.db.models.deletion.SET_DEFAULT, to='user_signup.sub_field'),
        ),
        migrations.AlterField(
            model_name='mentor_model',
            name='field',
            field=models.ForeignKey(default='others', on_delete=django.db.models.deletion.SET_DEFAULT, to='user_signup.field'),
        ),
        migrations.AlterField(
            model_name='mentor_model',
            name='sub_field',
            field=models.ForeignKey(default='others', on_delete=django.db.models.deletion.SET_DEFAULT, to='user_signup.sub_field'),
        ),
    ]
