# Generated by Django 3.0.3 on 2022-04-26 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('core', '0005_player_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
    ]
