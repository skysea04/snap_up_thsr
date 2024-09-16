# Generated by Django 4.2 on 2024-09-16 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_holidayinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingrequest',
            name='type_of_trip',
            field=models.PositiveSmallIntegerField(choices=[(0, '單程')], default=0, help_text='來回票功能尚未開放，請選擇單程', verbose_name='單程/來回'),
        ),
    ]
