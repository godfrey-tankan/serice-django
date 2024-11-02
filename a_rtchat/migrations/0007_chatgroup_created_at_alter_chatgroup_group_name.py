# Generated by Django 5.0.6 on 2024-07-19 10:14

import django.utils.timezone
import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0006_reviews_alter_chatgroup_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
    ]