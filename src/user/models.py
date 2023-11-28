from basis.db import BasisModel
# from booking.constants.bookings import BookingMethod, SeatPrefer, TypeOfTrip
from django.db import models
from django.db.models import UniqueConstraint


# Create your models here.
class User(BasisModel):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=8)
    personal_id = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(name='uniq_email', fields=['email']),
            UniqueConstraint(name='uniq_invite_code', fields=['invite_code']),
        ]

    @classmethod
    def create(cls, email: str, hash_pwd: str, code: str):
        cls.objects.create(email=email, password=hash_pwd, invite_code=code)

    @classmethod
    def get(cls, id: int) -> 'User':
        return cls.objects.filter(id=id).first()

    @classmethod
    def get_by_email(cls, email: str) -> 'User':
        return cls.objects.filter(email=email).first()


class InviteCode(BasisModel):
    id = models.CharField(primary_key=True, max_length=8, editable=False)
    is_used = models.BooleanField(default=False)

    @classmethod
    def create(cls, code: str):
        cls.objects.create(id=code)

    @classmethod
    def get_for_update(cls, code: str) -> 'InviteCode':
        return cls.objects.select_for_update().filter(id=code).first()
