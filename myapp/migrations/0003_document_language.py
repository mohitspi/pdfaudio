# Generated by Django 3.1.1 on 2020-09-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200908_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='language',
            field=models.CharField(choices=[('hi', 'hi'), ('ml', 'ml'), ('ta', 'ta'), ('te', 'te'), ('kn', 'kn')], default='hi', max_length=30),
        ),
    ]
