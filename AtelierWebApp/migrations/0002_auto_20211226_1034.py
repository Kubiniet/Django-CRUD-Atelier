# Generated by Django 2.2.24 on 2021-12-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AtelierWebApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='nunero',
            new_name='numero',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='adress',
            field=models.CharField(max_length=30, verbose_name='La puta direccion'),
        ),
    ]
