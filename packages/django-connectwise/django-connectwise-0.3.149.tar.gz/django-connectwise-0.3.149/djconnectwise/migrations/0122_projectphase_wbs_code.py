# Generated by Django 2.1.14 on 2020-09-09 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djconnectwise', '0121_syncjob_skipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphase',
            name='wbs_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
