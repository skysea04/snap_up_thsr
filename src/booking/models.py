from dataclasses import dataclass
from datetime import datetime as dt, timedelta as td
from typing import List

from basis.db import BasisModel
from booking.constants.bookings import (
    AVAILABLE_TIMES, AvailableTime, BookingMethod, PassengerNum, SeatPrefer, Station, TypeOfTrip
)
from django.db import models
from pydantic import BaseModel, Field, validator

from .exceptions import BookingException


class BookingRequest(BasisModel):
    user_email = models.EmailField()
    depart_station = models.PositiveSmallIntegerField(choices=Station.choices, default=Station.Nangang)
    dest_station = models.PositiveSmallIntegerField(choices=Station.choices, default=Station.Zuouing)
    type_of_trip = models.PositiveSmallIntegerField(choices=TypeOfTrip.choices, default=TypeOfTrip.ONE_WAY)
    booking_method = models.PositiveSmallIntegerField(choices=BookingMethod.choices, default=BookingMethod.TIME)
    seat_prefer = models.PositiveSmallIntegerField(choices=SeatPrefer.choices, default=SeatPrefer.NO_PREFER)
    adult_num = models.PositiveSmallIntegerField(choices=PassengerNum.choices, default=PassengerNum.One)
    child_num = models.PositiveSmallIntegerField(choices=PassengerNum.choices, default=PassengerNum.Zero)
    disabled_num = models.PositiveSmallIntegerField(choices=PassengerNum.choices, default=PassengerNum.Zero)
    elder_num = models.PositiveSmallIntegerField(choices=PassengerNum.choices, default=PassengerNum.Zero)
    college_num = models.PositiveSmallIntegerField(choices=PassengerNum.choices, default=PassengerNum.Zero)
    depart_date = models.DateField(blank=True)
    earliest_depart_time = models.CharField(
        max_length=10, blank=True, choices=AvailableTime.choices, default=AvailableTime.NotChosen
    )
    latest_arrival_time = models.CharField(
        max_length=10, blank=True, choices=AvailableTime.choices, default=AvailableTime.TwentythreeFiftynine
    )
    train_id = models.CharField(max_length=10, blank=True)
    deleted_at = models.DateTimeField(blank=True)
    thsr_ticket_id = models.PositiveBigIntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_email']),
        ]


class BookingQueue(BasisModel):
    booking_request_id = models.PositiveBigIntegerField()
    booking_date = models.DateField()
    retry_times = models.PositiveSmallIntegerField()
    max_retry_times = models.PositiveSmallIntegerField()


# One booking request flow will save one booking log
class BookingLog(BasisModel):
    class Status(models.IntegerChoices):
        FAIL = -1
        INIT = 0
        SUCCESS = 1

    booking_request_id = models.PositiveBigIntegerField()
    status = models.SmallIntegerField()
    err_msg = models.TextField()
    ticket_id = models.CharField(max_length=10)

    class Meta:
        indexes = [
            models.Index(fields=['booking_request_id']),
        ]


class BookingResult(BasisModel):
    class Status(models.IntegerChoices):
        SUCCESS = 1
        FAIL = -1

    user_email = models.EmailField()
    booking_request_id = models.PositiveBigIntegerField()
    status = models.PositiveSmallIntegerField(choices=Status.choices)
    thsr_ticket_id = models.PositiveBigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['user_email']),
            models.Index(fields=['booking_request_id']),
            models.Index(fields=['thsr_ticket_id']),
        ]


class THSRTicket(BasisModel):
    ticket_id = models.CharField(max_length=10, blank=True)
    total_price = models.CharField(max_length=10, blank=True)
    payment_deadline = models.CharField(max_length=10, blank=True)
    train_id = models.CharField(max_length=10, blank=True)
    seat_num = models.CharField(max_length=50, blank=True)
    date = models.CharField(max_length=10, blank=True)
    depart_time = models.DateTimeField(blank=True)
    arrival_time = models.DateTimeField(blank=True)
    depart_station = models.PositiveSmallIntegerField(choices=Station.choices)
    arrival_station = models.PositiveSmallIntegerField(choices=Station.choices)


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
    depart_time: str = Field(..., serialization_alias='toTimeTable')
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


class TrainForm(BaseModel):
    form_mark: str = Field('', serialization_alias='BookingS2Form:hf:0')
    submit_buttom: str = Field('確認車次', serialization_alias='SubmitButton')
    train_value: str = Field(..., serialization_alias='TrainQueryDataViewPanel:TrainGroup')


class TicketForm(BaseModel):
    personal_id: str = Field(..., serialization_alias='dummyId')
    phone: str = Field(..., serialization_alias='dummyPhone')
    email: str = Field(..., serialization_alias='email')
    member_radio: str = Field(
        ...,
        serialization_alias='TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup',
        description='非高鐵會員, 企業會員 / 高鐵會員 / 企業會員統編',
    )
    member_account: str = Field(
        ...,
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

    passenger_last_name: str = Field(
        '', serialization_alias='TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataLastName')
    passenger_first_name: str = Field(
        '', serialization_alias='TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataFirstName')
    passenger_discount: str = Field(
        '全票/早鳥8折', serialization_alias='TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataTypeName')
    passenger_choice: int = Field(
        0, serialization_alias='TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataInputChoice')
    passenger_id: str = Field(
        'A126189598', serialization_alias='TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataIdNumber')


@dataclass
class Train:
    code: str
    value: str
    departure_time: dt
    arrival_time: dt
    travel_time: td
    discounts: List[int]


class TrainSelector:
    def get_earliest(train_lst: List[Train]):
        return train_lst[0]
