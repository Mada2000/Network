# Generated by Django 5.0.7 on 2024-11-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follower_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='liked_posts',
            field=models.ManyToManyField(related_name='liked_list', to='network.post'),
        ),
    ]
