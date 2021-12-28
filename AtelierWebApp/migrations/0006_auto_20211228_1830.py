# Generated by Django 2.2.24 on 2021-12-28 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AtelierWebApp', '0005_auto_20211228_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='seccion',
            name='service',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='service',
        ),
        migrations.AddField(
            model_name='servicio',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='seccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AtelierWebApp.Seccion'),
        ),
        migrations.DeleteModel(
            name='seccion_genero',
        ),
        migrations.DeleteModel(
            name='service',
        ),
        migrations.AddField(
            model_name='servicio',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AtelierWebApp.Genre'),
        ),
    ]
