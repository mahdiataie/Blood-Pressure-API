# Generated by Django 4.2.3 on 2023-08-16 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_api', '0002_alter_withingsmeasure_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodpressurewarning',
            name='measuretype_withings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_api.withingsmeasuretype'),
        ),
    ]