# Generated by Django 4.0.1 on 2022-01-20 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_rate_client_isbad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='description',
        ),
        migrations.RemoveField(
            model_name='client',
            name='isbad',
        ),
        migrations.RemoveField(
            model_name='order',
            name='extra_price',
        ),
        migrations.AddField(
            model_name='orderservice',
            name='extra_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
