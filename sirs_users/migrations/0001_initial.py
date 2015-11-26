# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SecretFile',
            fields=[
                ('name', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('iv', models.CharField(max_length=30)),
                ('key', models.CharField(max_length=50)),
                ('ct', models.TextField()),
                ('owner', models.ForeignKey(to='sirs_users.CustomUser')),
            ],
        ),
    ]
