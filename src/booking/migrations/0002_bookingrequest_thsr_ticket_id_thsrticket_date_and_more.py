# Generated by Django 4.2 on 2023-11-07 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingrequest',
            name='thsr_ticket_id',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='thsrticket',
            name='date',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='thsrticket',
            name='seat_num',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='thsrticket',
            name='total_price',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='thsrticket',
            name='train_id',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='adult_num',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=1),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='child_num',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='college_num',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='disabled_num',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='elder_num',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0),
        ),
        migrations.AlterField(
            model_name='thsrticket',
            name='arrival_station',
            field=models.PositiveSmallIntegerField(choices=[(1, '南港'), (2, '台北'), (3, '板橋'), (4, '桃園'), (5, '新竹'), (6, '苗栗'), (7, '台中'), (8, '彰化'), (9, '雲林'), (10, '嘉義'), (11, '台南'), (12, '左營')]),
        ),
        migrations.AlterField(
            model_name='thsrticket',
            name='depart_station',
            field=models.PositiveSmallIntegerField(choices=[(1, '南港'), (2, '台北'), (3, '板橋'), (4, '桃園'), (5, '新竹'), (6, '苗栗'), (7, '台中'), (8, '彰化'), (9, '雲林'), (10, '嘉義'), (11, '台南'), (12, '左營')]),
        ),
    ]
