# Generated by Django 4.1.3 on 2022-11-06 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_service', '0002_user_is_staff'),
        ('message_service', '0002_alter_message_created_at_alter_message_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='priority',
            field=models.CharField(choices=[('high', 'high'), ('medium', 'medium'), ('low', 'low')], default='high', max_length=10),
        ),
        migrations.AddField(
            model_name='message',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_messages', to='user_service.user'),
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('query_received', 'query_received'), ('query_in_progress', 'query_in_progress'), ('query_resolved', 'query_resolved'), ('query_rejected', 'query_rejected')], default='query_received', max_length=20),
        ),
    ]
