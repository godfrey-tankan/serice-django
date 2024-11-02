# Generated by Django 5.0.6 on 2024-11-02 10:00

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0010_alter_chatgroup_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='MessageStatus',
        ),
    ]