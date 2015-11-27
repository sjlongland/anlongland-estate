# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estatedb', '0003_articletypeauditlogentry_itemauditlogentry_locationauditlogentry_photoauditlogentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationauditlogentry',
            name='action_user',
        ),
        migrations.RemoveField(
            model_name='locationauditlogentry',
            name='parent',
        ),
        migrations.DeleteModel(
            name='LocationAuditLogEntry',
        ),
    ]
