# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of this ptask.', max_length=128, db_index=True)),
                ('description', models.CharField(help_text=b'A description of this ptask.', max_length=1024)),
                ('created', models.DateTimeField(help_text=b'The date this ptask was created.', auto_now_add=True)),
                ('start_date', models.DateField(help_text=b'The date work is to be started on this ptask.')),
                ('due_date', models.DateField(help_text=b'The date work is to be completed on this ptask.')),
                ('priority', models.IntegerField(default=50, help_text=b'PTask priority. Lower number means higher priority.')),
                ('status', models.IntegerField(default=0, help_text=b'The status of work being done on this ptask.', choices=[(0, b'Ready To Begin'), (1, b'In Progress'), (2, b'Completed'), (3, b'On Hold')])),
                ('active', models.BooleanField(default=True, help_text=b'True if ptask is active, False otherwise.')),
                ('spec', models.CharField(help_text=b'Specification for this ptask.', max_length=1024, editable=False, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('creator', models.ForeignKey(help_text=b'The creator of this ptask.', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='ptasks.PTask', help_text=b'The parent ptask of this ptask.', null=True)),
            ],
            options={
                'verbose_name': 'PTask',
                'verbose_name_plural': 'PTasks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PTaskAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(help_text=b'The start date for this user on this ptask.', null=True, blank=True)),
                ('end_date', models.DateField(help_text=b'The end date for this user on this ptask.', null=True, blank=True)),
                ('active', models.BooleanField(default=True, help_text=b'True if ptask is active, False otherwise.')),
                ('spec', models.CharField(help_text=b'Specification for this ptask assignment.', max_length=1024, editable=False, blank=True)),
                ('ptask', models.ForeignKey(related_name=b'assignments', to='ptasks.PTask', help_text=b'The ptask to assign a user to.')),
                ('user', models.ForeignKey(help_text=b'The user to assign to the ptask.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Assignment',
                'verbose_name_plural': 'Assignments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PTaskType',
            fields=[
                ('name', models.CharField(help_text=b'The name of this ptask type.', max_length=32, serialize=False, primary_key=True)),
                ('description', models.CharField(help_text=b'A description of what this ptask type is used for.', max_length=1024)),
                ('level_hint', models.IntegerField(default=1, help_text=b'An integer indicating the level of a ptask')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PTaskVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date this ptask version was created.', auto_now_add=True)),
                ('description', models.CharField(help_text=b'A description of this ptask version.', max_length=1024)),
                ('number', models.IntegerField(help_text=b'The actual version number of this ptask version.')),
                ('spec', models.CharField(help_text=b'Specification for this ptask.', max_length=1024, editable=False, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('creator', models.ForeignKey(help_text=b'The user who created this version.', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, to='locations.Location', help_text=b'The location that owns this version.')),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='ptasks.PTaskVersion', help_text=b'The parent version of this version.', null=True)),
                ('ptask', models.ForeignKey(related_name=b'versions', to='ptasks.PTask', help_text=b'The ptask this version is associated with.')),
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Versions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='ptaskversion',
            unique_together=set([('ptask', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='ptaskassignment',
            unique_together=set([('ptask', 'user')]),
        ),
        migrations.AddField(
            model_name='ptask',
            name='ptask_type',
            field=models.ForeignKey(help_text=b'The type of this ptask.', to='ptasks.PTaskType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ptask',
            unique_together=set([('parent', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='ptask',
            index_together=set([('parent', 'name')]),
        ),
    ]
