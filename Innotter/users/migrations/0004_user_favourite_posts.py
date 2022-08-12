# Generated by Django 3.2.15 on 2022-08-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20220812_1252'),
        ('users', '0003_alter_user_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_posts',
            field=models.ManyToManyField(blank=True, related_name='favourites', to='pages.Post'),
        ),
    ]
