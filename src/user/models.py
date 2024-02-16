from basis.db import BasisModel
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
    personal_id = models.CharField(max_length=10, blank=True, verbose_name='身分證字號')
    phone = models.CharField(max_length=10, blank=True, verbose_name='手機號碼')
    use_tgo_account = models.BooleanField(
        default=False,
        verbose_name='使用 TGO 帳號',
        help_text='TGO 帳號即為身分證字號 (目前僅提供個人用戶，未來會開發企業帳號選項)',
    )

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

    class Meta:
        constraints = [
            UniqueConstraint('email', name='uniq_email'),
            UniqueConstraint('invite_code', name='uniq_invite_code'),
        ]
