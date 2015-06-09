# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import estatedb.thumbs
import audit_log.models.fields
import mptt.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('estatedb', '0002_auto_20150608_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTypeAuditLogEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=64, db_index=True)),
                ('action_id', models.AutoField(serialize=False, primary_key=True)),
                ('action_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('action_type', models.CharField(max_length=1, editable=False, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(related_name='_articletype_audit_log_entry', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemAuditLogEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('code', models.CharField(db_index=True, max_length=12, null=True, blank=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('action_id', models.AutoField(serialize=False, primary_key=True)),
                ('action_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('action_type', models.CharField(max_length=1, editable=False, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(related_name='_item_audit_log_entry', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('article_type', models.ForeignKey(to='estatedb.ArticleType')),
                ('claimant', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('contents', models.ForeignKey(related_name='_auditlog_parent_item', blank=True, to='estatedb.Location', null=True)),
                ('location', models.ForeignKey(related_name='_auditlog_child_items', to='estatedb.Location')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationAuditLogEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('code_prefix', models.CharField(max_length=3, db_index=True)),
                ('next_code', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=256)),
                ('action_id', models.AutoField(serialize=False, primary_key=True)),
                ('action_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('action_type', models.CharField(max_length=1, editable=False, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(related_name='_location_audit_log_entry', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='_auditlog_children', blank=True, to='estatedb.Location', null=True)),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoAuditLogEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('photo', estatedb.thumbs.ImageWithThumbsField(upload_to=b'photos')),
                ('order', models.PositiveIntegerField(default=0)),
                ('action_id', models.AutoField(serialize=False, primary_key=True)),
                ('action_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('action_type', models.CharField(max_length=1, editable=False, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(related_name='_photo_audit_log_entry', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('item', models.ForeignKey(to='estatedb.Item')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
    ]
