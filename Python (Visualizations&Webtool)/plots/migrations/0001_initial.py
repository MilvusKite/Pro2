# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeatMat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('pickledValueMatrix', models.TextField()),
                ('pickledValueRowDiseaseNames', models.TextField()),
                ('pickledValueColGroupNames', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('folding', models.FloatField(null=True, blank=True)),
                ('trafficking', models.FloatField(null=True, blank=True)),
                ('clearance', models.FloatField(null=True, blank=True)),
                ('metabolism', models.FloatField(null=True, blank=True)),
                ('signaling', models.FloatField(null=True, blank=True)),
                ('synthesis', models.FloatField(null=True, blank=True)),
                ('ER', models.FloatField(null=True, blank=True)),
                ('HSP100', models.FloatField(null=True, blank=True)),
                ('HSP40', models.FloatField(null=True, blank=True)),
                ('HSP60', models.FloatField(null=True, blank=True)),
                ('HSP70', models.FloatField(null=True, blank=True)),
                ('HSP90', models.FloatField(null=True, blank=True)),
                ('MITO', models.FloatField(null=True, blank=True)),
                ('PFD', models.FloatField(null=True, blank=True)),
                ('sHSP', models.FloatField(null=True, blank=True)),
                ('TPR', models.FloatField(null=True, blank=True)),
                ('foldingMax', models.FloatField(null=True, blank=True)),
                ('traffickingMax', models.FloatField(null=True, blank=True)),
                ('clearanceMax', models.FloatField(null=True, blank=True)),
                ('metabolismMax', models.FloatField(null=True, blank=True)),
                ('signalingMax', models.FloatField(null=True, blank=True)),
                ('synthesisMax', models.FloatField(null=True, blank=True)),
                ('ERMax', models.FloatField(null=True, blank=True)),
                ('HSP100Max', models.FloatField(null=True, blank=True)),
                ('HSP40Max', models.FloatField(null=True, blank=True)),
                ('HSP60Max', models.FloatField(null=True, blank=True)),
                ('HSP70Max', models.FloatField(null=True, blank=True)),
                ('HSP90Max', models.FloatField(null=True, blank=True)),
                ('MITOMax', models.FloatField(null=True, blank=True)),
                ('PFDMax', models.FloatField(null=True, blank=True)),
                ('sHSPMax', models.FloatField(null=True, blank=True)),
                ('TPRMax', models.FloatField(null=True, blank=True)),
                ('foldingMin', models.FloatField(null=True, blank=True)),
                ('traffickingMin', models.FloatField(null=True, blank=True)),
                ('clearanceMin', models.FloatField(null=True, blank=True)),
                ('metabolismMin', models.FloatField(null=True, blank=True)),
                ('signalingMin', models.FloatField(null=True, blank=True)),
                ('synthesisMin', models.FloatField(null=True, blank=True)),
                ('ERMin', models.FloatField(null=True, blank=True)),
                ('HSP100Min', models.FloatField(null=True, blank=True)),
                ('HSP40Min', models.FloatField(null=True, blank=True)),
                ('HSP60Min', models.FloatField(null=True, blank=True)),
                ('HSP70Min', models.FloatField(null=True, blank=True)),
                ('HSP90Min', models.FloatField(null=True, blank=True)),
                ('MITOMin', models.FloatField(null=True, blank=True)),
                ('PFDMin', models.FloatField(null=True, blank=True)),
                ('sHSPMin', models.FloatField(null=True, blank=True)),
                ('TPRMin', models.FloatField(null=True, blank=True)),
            ],
        ),
    ]
