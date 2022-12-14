# Generated by Django 4.1.3 on 2022-11-09 19:14

from django.db import migrations, models
import message_service.models


class Migration(migrations.Migration):

    dependencies = [
        ('message_service', '0004_message_metadata_message_private_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='metadata',
            field=models.JSONField(blank=True, default=dict, encoder=message_service.models.CustomJsonEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='private_metadata',
            field=models.JSONField(blank=True, default=dict, encoder=message_service.models.CustomJsonEncoder, null=True),
        ),
    ]
