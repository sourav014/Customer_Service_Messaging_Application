# Generated by Django 4.1.3 on 2022-11-05 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
