# Generated by Django 2.0.13 on 2019-07-11 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0009_auto_20190711_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='provImage',
            field=models.ImageField(default='providerImage/default-user.png', upload_to='providerImage/'),
        ),
    ]
