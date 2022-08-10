# Generated by Django 3.2.15 on 2022-08-10 13:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0003_auto_20220810_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='follow_requests',
            field=models.ManyToManyField(blank=True, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='pages', to='pages.Tag'),
        ),
    ]
