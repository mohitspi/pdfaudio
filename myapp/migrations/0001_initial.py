# Generated by Django 3.1.1 on 2020-09-08 13:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='audio/')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^0?[5-9]{1}\\d{9}$')])),
                ('desc', models.TextField()),
                ('cr_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('membership_type', models.CharField(choices=[('Premium', 'pre'), ('Free', 'free')], default='Free', max_length=30)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_membership', to='myapp.membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('user_membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='myapp.usermembership')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('audio', models.FileField(blank=True, upload_to='audio/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
