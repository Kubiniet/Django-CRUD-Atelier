# Generated by Django 2.2.24 on 2021-12-28 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AtelierWebApp', '0002_auto_20211228_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='phone2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='phone',
            field=models.CharField(max_length=10),
        ),
    ]