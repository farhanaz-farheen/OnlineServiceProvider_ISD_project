# Generated by Django 2.0.13 on 2019-08-24 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_search_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='search_history',
            name='custid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customer'),
        ),
    ]