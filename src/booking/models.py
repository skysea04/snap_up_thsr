from dataclasses import dataclass
from datetime import datetime as dt, time, timedelta as td

from basis.db import BasisModel
from django.db import models
from pydantic import BaseModel, Field, validator
from user.models import User

from . import utils
from .constants.bookings import (
    AVAILABLE_TIMES, MAX_TICKET_NUM, AvailableTime, BookingMethod, PassengerNum, SeatPrefer,
    Station, TypeOfTrip
)
from .exceptions import BookingException


class THSRTicket(BasisModel):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )
    ticket_id = models.CharField(max_length=10, blank=True, verbose_name='訂位代號')
    total_price = models.CharField(max_length=10, blank=True, verbose_name='總金額')
    payment_deadline = models.CharField(max_length=10, blank=True, verbose_name='付款期限')
    train_id = models.CharField(max_length=10, blank=True, verbose_name='車次')
    seat_num = models.CharField(max_length=50, blank=True, verbose_name='座位號碼')
    date = models.CharField(max_length=10, blank=True, verbose_name='乘車日期')
    depart_time = models.CharField(max_length=255, blank=True, verbose_name='出發時間')
    arrival_time = models.CharField(max_length=255, blank=True, verbose_name='抵達時間')
    depart_station = models.PositiveSmallIntegerField(choices=Station.choices, verbose_name='啟程站')
    arrival_station = models.PositiveSmallIntegerField(choices=Station.choices, verbose_name='到達站')

    def __str__(self) -> str:
        return self.ticket_id

    class Meta:
        verbose_name_plural = '已完成訂位資訊'


class BookingRequest(BasisModel):
    class Status(models.IntegerChoices):
        NOT_YET = 0, '尚未進入排程'
        PENDING = 1, '訂購中'
        COMPLETED = 2, '已完成'
        EXPIRED = -1, '已過期'
        DELETED = -2

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        editable=False,
        verbose_name='使用者帳號'
    )
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.PENDING, editable=False, verbose_name='購票狀態')
    thsr_ticket = models.ForeignKey(
        THSRTicket,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        editable=False,
        verbose_name='訂位代號'
    )
    depart_station = models.PositiveSmallIntegerField(
        choices=Station.choices, default=Station.Nangang, verbose_name='啟程站')
    dest_station = models.PositiveSmallIntegerField(
        choices=Station.choices, default=Station.Zuouing, verbose_name='到達站')
    type_of_trip = models.PositiveSmallIntegerField(
        choices=TypeOfTrip.choices, default=TypeOfTrip.ONE_WAY,
        verbose_name='單程/來回', help_text='來回票功能尚未開放，請選擇單程',
    )
    booking_method = models.PositiveSmallIntegerField(
        choices=BookingMethod.choices, default=BookingMethod.TIME, verbose_name='訂票方式')
    seat_prefer = models.PositiveSmallIntegerField(
        choices=SeatPrefer.choices, default=SeatPrefer.NO_PREFER, verbose_name='座位偏好')
    adult_num = models.PositiveSmallIntegerField(
        choices=PassengerNum.choices, default=PassengerNum.One, verbose_name='全票')
    child_num = models.PositiveSmallIntegerField(
        choices=PassengerNum.choices, default=PassengerNum.Zero, verbose_name='孩童票(6-11歲)')
    disabled_num = models.PositiveSmallIntegerField(
        choices=PassengerNum.choices, default=PassengerNum.Zero, verbose_name='愛心票')
    elder_num = models.PositiveSmallIntegerField(
        choices=PassengerNum.choices, default=PassengerNum.Zero, verbose_name='敬老票(65+)')
    college_num = models.PositiveSmallIntegerField(
        choices=PassengerNum.choices, default=PassengerNum.Zero, verbose_name='大學生票')
    depart_date = models.DateField(verbose_name='出發日期')
    train_id = models.CharField(max_length=10, blank=True, verbose_name='車次', help_text='若以車次訂票需填寫')
    earliest_depart_time = models.CharField(
        max_length=10, blank=True, choices=AvailableTime.choices,
        default=AvailableTime.NotChosen, verbose_name='最早出發時間',
        help_text='若以時間訂票需選擇',
    )
    latest_arrival_time = models.CharField(
        max_length=10, blank=True, choices=AvailableTime.choices,
        default=AvailableTime.NotChosen, verbose_name='最晚抵達時間',
        help_text='若以時間訂票需選擇',
    )
    passenger_ids = models.JSONField(
        default=list, blank=True, null=True,
        verbose_name='乘客身分證字號', help_text='僅供優惠票實名制使用，若只訂一張票或確定該時段沒有優惠則不須填寫，填寫格式為 ["A123456789", "B123456789"]',
    )
    error_msg = models.CharField(max_length=255, blank=True, editable=False, verbose_name='錯誤訊息')
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False, verbose_name='刪除時間')

    def total_ticket_amount(self) -> int:
        return sum([self.adult_num, self.child_num, self.disabled_num, self.elder_num, self.college_num])

    def save(self, *args, **kwargs):
        if not self.pk:
            latest_booking_date = utils.get_latest_booking_date()
            if latest_booking_date < self.depart_date:
                self.status = self.Status.NOT_YET

        super().save(*args, **kwargs)

    @classmethod
    def get_all_by_status(cls, status: int) -> list['BookingRequest']:
        return list(
            cls.objects.filter(status=status).order_by('-depart_date')
        )

    class Meta:
        indexes = [
            models.Index(fields=['status', '-depart_date']),
        ]
        verbose_name_plural = '訂票表單(點擊 + Add 開始訂票)'


class BookingCondition(BaseModel):
    start_station: int
    dest_station: int
    earliest_departure_time: dt
    latest_arrival_time: dt

    type_of_trip: int = TypeOfTrip.ONE_WAY
    seat_prefer: int = SeatPrefer.NO_PREFER
    booking_method: str = BookingMethod.TIME
    adult_num: int = 1
    child_num: int = 0
    disabled_num: int = 0
    elder_num: int = 0
    college_num: int = 0

    def get_request_departure_time(self) -> str:
        departure_time = next(filter(lambda t: t[0] < self.earliest_departure_time.time(), AVAILABLE_TIMES), None)
        if not departure_time:
            raise BookingException('Wrong Departure Time')

        return departure_time[1]


class BookingForm(BaseModel):
    form_mark: str = Field('', serialization_alias='BookingS1Form:hf:0')
    type_of_trip: int = Field(..., serialization_alias='tripCon:typesoftrip')
    class_type: int = Field(0, serialization_alias='trainCon:trainRadioGroup')
    seat_prefer: int = Field(..., serialization_alias='seatCon:seatRadioGroup')
    booking_method: str = Field(..., serialization_alias='bookingMethod')
    depart_station: int = Field(..., serialization_alias='selectStartStation')
    dest_station: int = Field(..., serialization_alias='selectDestinationStation')

    depart_date: str = Field(..., serialization_alias='toTimeInputField')
    back_date: str = Field(None, serialization_alias='backTimeInputField')
    depart_time: str = Field(None, serialization_alias='toTimeTable')
    depart_train_id: int = Field(None, serialization_alias='toTrainIDInputField')
    back_time: str = Field(None, serialization_alias='backTimeTable')
    back_train_id: int = Field(None, serialization_alias='backTrainIDInputField')
    adult_num: str = Field('1F', serialization_alias='ticketPanel:rows:0:ticketAmount')
    child_num: str = Field('0H', serialization_alias='ticketPanel:rows:1:ticketAmount')
    disabled_num: str = Field('0W', serialization_alias='ticketPanel:rows:2:ticketAmount')
    elder_num: str = Field('0E', serialization_alias='ticketPanel:rows:3:ticketAmount')
    college_num: str = Field('0P', serialization_alias='ticketPanel:rows:4:ticketAmount')
    security_code: str = Field(..., serialization_alias='homeCaptcha:securityCode')
    submit_button: str = Field('開始查詢', serialization_alias='SubmitButton')

    early_bird_setting: int = Field(0, serialization_alias='trainTypeContainer:typesoftrain')
    portal_tag: bool = Field(False, serialization_alias='portalTag')  # False

    @validator('type_of_trip')
    def check_type_of_trip(cls, value):
        if value not in [0, 1]:
            raise ValueError(f'Invalid type of trip: {value}')
        return value

    @classmethod
    def generate_form(cls, booking_request: BookingRequest, booking_method_radio: str, security_code: str) -> 'BookingForm':
        form = cls(
            type_of_trip=booking_request.type_of_trip,
            seat_prefer=booking_request.seat_prefer,
            booking_method=booking_method_radio,
            depart_station=booking_request.depart_station,
            dest_station=booking_request.dest_station,
            depart_date=booking_request.depart_date.strftime('%Y/%m/%d'),
            adult_num=f'{booking_request.adult_num}F',
            child_num=f'{booking_request.child_num}H',
            disabled_num=f'{booking_request.disabled_num}W',
            elder_num=f'{booking_request.elder_num}E',
            college_num=f'{booking_request.college_num}P',
            security_code=security_code,
        )

        if booking_request.booking_method == BookingMethod.TIME:
            form.depart_time = booking_request.earliest_depart_time
        elif booking_request.booking_method == BookingMethod.TRAIN_NO:
            form.depart_train_id = booking_request.train_id

        return form


class TrainForm(BaseModel):
    form_mark: str = Field('', serialization_alias='BookingS2Form:hf:0')
    submit_buttom: str = Field('確認車次', serialization_alias='SubmitButton')
    train_value: str = Field(..., serialization_alias='TrainQueryDataViewPanel:TrainGroup')


class Passenger(BaseModel):
    discount: str
    id: str


class TicketForm(BaseModel):
    personal_id: str = Field(..., serialization_alias='dummyId')
    phone: str = Field(..., serialization_alias='dummyPhone')
    email: str = Field(..., serialization_alias='email')
    member_radio: str = Field(
        '',
        serialization_alias='TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup',
        description='非高鐵會員, 企業會員 / 高鐵會員 / 企業會員統編',
    )
    member_account: str = Field(
        '',
        serialization_alias='TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup:memberShipNumber',
        description='高鐵會員帳號 (選擇登入高鐵會員時使用)'
    )
    form_mark: str = Field('', serialization_alias='BookingS3FormSP:hf:0')
    id_input_radio: int = Field(0, serialization_alias='idInputRadio', description='0: 身份證字號 / 1: 護照號碼')
    diff_over: int = Field(1, serialization_alias='diffOver')
    agree: str = Field('on', serialization_alias='agree')
    go_back_m: str = Field('', serialization_alias='isGoBackM')
    back_home: str = Field('', serialization_alias='backHome')
    tgo_error: int = Field(1, serialization_alias='TgoError')

    @classmethod
    def generate_passenger_fields(cls, passenger: Passenger, idx: int) -> dict:
        return {
            f'passenger_last_name_{idx}': (str, Field(
                '', serialization_alias=f'TicketPassengerInfoInputPanel:passengerDataView:{idx}:passengerDataView2:passengerDataLastName'
            )),
            f'passenger_first_name_{idx}': (str, Field(
                '', serialization_alias=f'TicketPassengerInfoInputPanel:passengerDataView:{idx}:passengerDataView2:passengerDataFirstName'
            )),
            f'passenger_discount_{idx}': (str, Field(
                passenger.discount, serialization_alias=f'TicketPassengerInfoInputPanel:passengerDataView:{idx}:passengerDataView2:passengerDataTypeName'
            )),
            f'passenger_choice_{idx}': (int, Field(
                0, serialization_alias=f'TicketPassengerInfoInputPanel:passengerDataView:{idx}:passengerDataView2:passengerDataInputChoice'
            )),
            f'passenger_id_{idx}': (str, Field(
                passenger.id, serialization_alias=f'TicketPassengerInfoInputPanel:passengerDataView:{idx}:passengerDataView2:passengerDataIdNumber'
            )),
        }

    @classmethod
    def generate_discount_passenger_fields(cls, passengers: list[Passenger]) -> dict:
        passenger_fields = {}
        for idx, passenger in enumerate(passengers):
            passenger_fields.update(cls.generate_passenger_fields(passenger, idx))

        # for key, value in passenger_fields.items():
        #     setattr(self, key, value)

        return passenger_fields


@dataclass
class Train:
    code: str
    value: str
    departure_time: time
    arrival_time: time
    travel_time: td
    discounts: list[int]


class TrainSelector:
    @staticmethod
    def get_earliest(train_lst: list[Train]) -> Train:
        return train_lst[0]
