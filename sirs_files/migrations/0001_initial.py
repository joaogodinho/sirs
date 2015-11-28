# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirs_users', '0001_initial'),
    ]

    operations = [
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
