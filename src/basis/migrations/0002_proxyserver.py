# Generated by Django 4.2 on 2024-09-18 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('port', models.PositiveIntegerField(verbose_name='Port')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否啟用')),
            ],
            options={
                'verbose_name': '代理伺服器',
                'verbose_name_plural': '代理伺服器',
            },
        ),
    ]
