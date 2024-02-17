# Generated by Django 4.2 on 2024-02-11 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingrequest',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Not Yet'), (1, 'Pending'), (2, 'Processing'), (3, 'Completed'), (-1, 'Expired'), (-2, 'Deleted')], default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='user',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]