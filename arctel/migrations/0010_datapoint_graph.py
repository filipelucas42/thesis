# Generated by Django 4.0.3 on 2022-05-28 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arctel', '0009_alter_datapoint_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='graph',
            field=models.CharField(choices=[('mobile', 'mobile penetration rate')], default='mobile', max_length=255),
        ),
    ]