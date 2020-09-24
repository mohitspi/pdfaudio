# Generated by Django 3.1.1 on 2020-09-24 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20200921_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='audio',
        ),
        migrations.AddField(
            model_name='audio',
            name='document_audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.document'),
        ),
    ]