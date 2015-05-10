# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import estatedb.thumbs
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=12, unique=True, null=True, blank=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('article_type', models.ForeignKey(to='estatedb.ArticleType')),
                ('claimant', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code_prefix', models.CharField(unique=True, max_length=3)),
                ('next_code', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=256)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='estatedb.Location', null=True)),
            ],
            options={
                'ordering': ['full_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', estatedb.thumbs.ImageWithThumbsField(upload_to=b'photos')),
                ('item', models.ForeignKey(to='estatedb.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('parent', 'name')]),
        ),
        migrations.AddField(
            model_name='item',
            name='contents',
            field=models.ForeignKey(related_name='parent_item', blank=True, to='estatedb.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(related_name='child_items', to='estatedb.Location'),
            preserve_default=True,
        ),
    ]
