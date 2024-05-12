# Generated by Django 4.2 on 2024-05-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_alter_bookingrequest_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('name', models.CharField(max_length=255, verbose_name='假期名稱')),
                ('adjust_period', models.CharField(max_length=255, verbose_name='疏運期間')),
                ('start_reserve_date', models.DateField(verbose_name='開始預約日期')),
            ],
            options={
                'verbose_name': '假期疏運資訊',
                'verbose_name_plural': '假期疏運資訊',
            },
        ),
    ]
