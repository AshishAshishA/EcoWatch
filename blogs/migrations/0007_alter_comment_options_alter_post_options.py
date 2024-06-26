# Generated by Django 5.0.4 on 2024-04-13 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_post_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': ['created'], 'ordering': ['created']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'get_latest_by': ['created_on'], 'ordering': ['-views']},
        ),
    ]
