# Generated by Django 2.0.13 on 2019-06-27 08:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catname', models.CharField(max_length=100, unique=True)),
                ('desc', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='provider',
            fields=[
                ('provid', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.PositiveIntegerField(default=1000000000, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(1999999999)])),
                ('password', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=300)),
                ('adminid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.admin')),
                ('catname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.category')),
            ],
        ),
    ]
