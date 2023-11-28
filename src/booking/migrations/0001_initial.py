# Generated by Django 4.2 on 2023-10-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_request_id', models.PositiveBigIntegerField()),
                ('status', models.SmallIntegerField()),
                ('err_msg', models.TextField()),
                ('ticket_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='BookingQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_request_id', models.PositiveBigIntegerField()),
                ('booking_date', models.DateField()),
                ('retry_times', models.PositiveSmallIntegerField()),
                ('max_retry_times', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('depart_station', models.PositiveSmallIntegerField(choices=[(1, '南港'), (2, '台北'), (3, '板橋'), (4, '桃園'), (5, '新竹'), (6, '苗栗'), (7, '台中'), (8, '彰化'), (9, '雲林'), (10, '嘉義'), (11, '台南'), (12, '左營')], default=1)),
                ('dest_station', models.PositiveSmallIntegerField(choices=[(1, '南港'), (2, '台北'), (3, '板橋'), (4, '桃園'), (5, '新竹'), (6, '苗栗'), (7, '台中'), (8, '彰化'), (9, '雲林'), (10, '嘉義'), (11, '台南'), (12, '左營')], default=12)),
                ('type_of_trip', models.PositiveSmallIntegerField(choices=[(0, 'One Way'), (1, 'Round Trip')], default=0)),
                ('booking_method', models.PositiveSmallIntegerField(choices=[(0, 'radio31'), (1, 'radio33')], default=0)),
                ('seat_prefer', models.PositiveSmallIntegerField(choices=[(0, 'No Prefer'), (1, 'Prefer Window'), (2, 'Prefer Aisle')], default=0)),
                ('adult_num', models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine'), (10, 'Ten')], default=1)),
                ('child_num', models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine'), (10, 'Ten')], default=0)),
                ('disabled_num', models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine'), (10, 'Ten')], default=0)),
                ('elder_num', models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine'), (10, 'Ten')], default=0)),
                ('college_num', models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine'), (10, 'Ten')], default=0)),
                ('depart_date', models.DateField(blank=True)),
                ('earliest_depart_time', models.CharField(blank=True, choices=[('', ''), ('500A', '05:00'), ('530A', '05:30'), ('600A', '06:00'), ('630A', '06:30'), ('700A', '07:00'), ('730A', '07:30'), ('800A', '08:00'), ('830A', '08:30'), ('900A', '09:00'), ('930A', '09:30'), ('1000A', '10:00'), ('1030A', '10:30'), ('1100A', '11:00'), ('1130A', '11:30'), ('1200N', '12:00'), ('1230P', '12:30'), ('100P', '13:00'), ('130P', '13:30'), ('200P', '14:00'), ('230P', '14:30'), ('300P', '15:00'), ('330P', '15:30'), ('400P', '16:00'), ('430P', '16:30'), ('500P', '17:00'), ('530P', '17:30'), ('600P', '18:00'), ('630P', '18:30'), ('700P', '19:00'), ('730P', '19:30'), ('800P', '20:00'), ('830P', '20:30'), ('900P', '21:00'), ('930P', '21:30'), ('1000P', '22:00'), ('1030P', '22:30'), ('1100P', '23:00'), ('1130P', '23:30'), ('1201A', '23:59')], default='', max_length=10)),
                ('latest_arrival_time', models.CharField(blank=True, choices=[('', ''), ('500A', '05:00'), ('530A', '05:30'), ('600A', '06:00'), ('630A', '06:30'), ('700A', '07:00'), ('730A', '07:30'), ('800A', '08:00'), ('830A', '08:30'), ('900A', '09:00'), ('930A', '09:30'), ('1000A', '10:00'), ('1030A', '10:30'), ('1100A', '11:00'), ('1130A', '11:30'), ('1200N', '12:00'), ('1230P', '12:30'), ('100P', '13:00'), ('130P', '13:30'), ('200P', '14:00'), ('230P', '14:30'), ('300P', '15:00'), ('330P', '15:30'), ('400P', '16:00'), ('430P', '16:30'), ('500P', '17:00'), ('530P', '17:30'), ('600P', '18:00'), ('630P', '18:30'), ('700P', '19:00'), ('730P', '19:30'), ('800P', '20:00'), ('830P', '20:30'), ('900P', '21:00'), ('930P', '21:30'), ('1000P', '22:00'), ('1030P', '22:30'), ('1100P', '23:00'), ('1130P', '23:30'), ('1201A', '23:59')], default='1201A', max_length=10)),
                ('train_id', models.CharField(blank=True, max_length=10)),
                ('deleted_at', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookingResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('booking_request_id', models.PositiveBigIntegerField()),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Success'), (-1, 'Fail')])),
                ('thsr_ticket_id', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='THSRTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket_id', models.CharField(blank=True, max_length=10)),
                ('payment_deadline', models.CharField(blank=True, max_length=10)),
                ('depart_time', models.DateTimeField(blank=True)),
                ('arrival_time', models.DateTimeField(blank=True)),
                ('depart_station', models.CharField(blank=True, max_length=10)),
                ('arrival_station', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='bookingresult',
            index=models.Index(fields=['user_email'], name='booking_boo_user_em_08d164_idx'),
        ),
        migrations.AddIndex(
            model_name='bookingresult',
            index=models.Index(fields=['booking_request_id'], name='booking_boo_booking_03208c_idx'),
        ),
        migrations.AddIndex(
            model_name='bookingresult',
            index=models.Index(fields=['thsr_ticket_id'], name='booking_boo_thsr_ti_915693_idx'),
        ),
        migrations.AddIndex(
            model_name='bookingrequest',
            index=models.Index(fields=['user_email'], name='booking_boo_user_em_d76ad1_idx'),
        ),
        migrations.AddIndex(
            model_name='bookinglog',
            index=models.Index(fields=['booking_request_id'], name='booking_boo_booking_3e6357_idx'),
        ),
    ]
