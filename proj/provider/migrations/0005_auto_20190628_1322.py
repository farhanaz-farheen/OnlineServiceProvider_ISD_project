# Generated by Django 2.0.13 on 2019-06-28 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0004_requested_provider_idimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requested_service',
            old_name='servname',
            new_name='provider',
        ),
        migrations.AddField(
            model_name='requested_service',
            name='serv_idImage',
            field=models.ImageField(blank=True, upload_to='serv_id_image/'),
        ),
        migrations.AddField(
            model_name='requested_service',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='provider.service'),
        ),
    ]
