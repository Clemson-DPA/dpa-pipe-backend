# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('code', models.CharField(help_text=b'A unique code name for this location.', max_length=32, serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'A short descriptive name for this location.', max_length=32)),
                ('description', models.CharField(help_text=b'A longer description of this location.', max_length=256)),
                ('timezone', models.CharField(help_text=b'The timezone of this location.', max_length=32)),
                ('latitude', models.FloatField(help_text=b'The latitude of the location.')),
                ('longitude', models.FloatField(help_text=b'The longitutde of the location.')),
                ('active', models.BooleanField(default=True, help_text=b'True if the location is active, False otherwise.')),
                ('host', models.CharField(help_text=b'Host name for this location.', max_length=256, blank=True)),
                ('filesystem_root', models.CharField(help_text=b'Root path to this locations ptask hierarchy.', max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
