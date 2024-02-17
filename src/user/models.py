from basis.db import BasisModel
from basis.validators import generate_personal_id
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import UniqueConstraint


class InviteCode(BasisModel):
    code = models.CharField(primary_key=True, max_length=8)
    is_used = models.BooleanField(default=False)

    @classmethod
    def create(cls, code: str):
        cls.objects.create(code=code)

    @classmethod
    def get_for_update(cls, code: str) -> 'InviteCode':
        return cls.objects.select_for_update().filter(code=code).first()

    @classmethod
    def is_exist(cls, code: str) -> bool:
        return cls.objects.filter(code=code).exists()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user: 'User' = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BasisModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    invite_code = models.ForeignKey(
        InviteCode,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )
    personal_id = models.CharField(
        max_length=10, blank=True,
        verbose_name='身分證字號',
        help_text='訂票一定要填寫身分證字號，若此欄未填會由系統隨機生成。<br/>早鳥優惠採記名，購買早鳥優惠票者應填寫每位搭乘者中華民國身分證號，乘車時應攜帶與票面登錄證號相符之有效證件正本以供查驗，無法出示有效證件或非本人持用者，視為無票乘車，應照章補票。',
    )
    phone = models.CharField(
        max_length=10, blank=True, verbose_name='手機號碼',
        help_text='訂票成功會寄簡訊通知，本欄位可不填寫，但填了會比較方便。',
    )
    buy_discount_ticket = models.BooleanField(
        default=True, verbose_name='購買早鳥優惠票',
        help_text='本選項乃為不想放置真實身份證字號之使用者設計。',
    )
    use_tgo_account = models.BooleanField(
        default=False, verbose_name='使用 TGO 帳號',
        help_text='TGO 帳號即為身分證字號 (目前僅提供個人用戶，未來會開發企業帳號選項)',
    )
    tgo_account_same_as_personal_id = models.BooleanField(default=True, verbose_name='TGO 帳號與身分證字號相同')
    tgo_account = models.CharField(max_length=255, blank=True, verbose_name='TGO 帳號')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # In this case, email and password are required by default.

    @classmethod
    def create(cls, email: str, hash_pwd: str, code: str):
        cls.objects.create(email=email, password=hash_pwd, invite_code=code)

    @classmethod
    def get(cls, user_id: int) -> 'User':
        return cls.objects.filter(id=user_id).first()

    @classmethod
    def get_by_email(cls, email: str) -> 'User':
        return cls.objects.filter(email=email).first()

    def save(self, *args, **kwargs):
        if self.pk and not self.personal_id:
            self.personal_id = generate_personal_id()

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint('email', name='uniq_email'),
            UniqueConstraint('invite_code', name='uniq_invite_code'),
        ]
        verbose_name_plural = '使用者資訊(請先編輯完再訂票)'
