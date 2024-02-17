# Generated by Django 4.2 on 2024-02-17 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_invitecode_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '使用者資訊(僅能看到自己的資料)'},
        ),
        migrations.AddField(
            model_name='user',
            name='buy_discount_ticket',
            field=models.BooleanField(default=True, help_text='本選項乃為不想放置真實身份證字號之使用者設計。', verbose_name='購買早鳥優惠票'),
        ),
        migrations.AddField(
            model_name='user',
            name='tgo_account',
            field=models.CharField(blank=True, max_length=255, verbose_name='TGO 帳號'),
        ),
        migrations.AddField(
            model_name='user',
            name='tgo_account_same_as_personal_id',
            field=models.BooleanField(default=True, verbose_name='TGO 帳號與身分證字號相同'),
        ),
        migrations.AlterField(
            model_name='user',
            name='personal_id',
            field=models.CharField(blank=True, help_text='訂票一定要填寫身分證字號，若此欄未填會由系統隨機生成。<br/>早鳥優惠採記名，購買早鳥優惠票者應填寫每位搭乘者中華民國身分證號，乘車時應攜帶與票面登錄證號相符之有效證件正本以供查驗，無法出示有效證件或非本人持用者，視為無票乘車，應照章補票。', max_length=10, verbose_name='身分證字號'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, help_text='訂票成功會寄簡訊通知，本欄位可不填寫，但填了會比較方便。', max_length=10, verbose_name='手機號碼'),
        ),
    ]