# Generated by Django 4.2 on 2024-09-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('content', models.TextField(verbose_name='內容')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否啟用')),
                ('level', models.PositiveSmallIntegerField(choices=[(10, 'debug'), (20, 'info'), (25, 'success'), (30, 'warning'), (40, 'error')], verbose_name='等級')),
            ],
            options={
                'verbose_name': '系統訊息',
                'verbose_name_plural': '系統訊息',
            },
        ),
    ]