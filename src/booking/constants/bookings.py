from datetime import time
from typing import Dict

from django.db import models

AVAILABLE_DAYS_AFTER_BOOKING = 28

AVAILABLE_TIME_MAP: Dict[str, time] = {
    '1130P': time(23, 30),
    '1100P': time(23, 00),
    '1030P': time(22, 30),
    '1000P': time(22, 00),
    '930P': time(21, 30),
    '900P': time(21, 00),
    '830P': time(20, 30),
    '800P': time(20, 00),
    '730P': time(19, 30),
    '700P': time(19, 00),
    '630P': time(18, 30),
    '600P': time(18, 00),
    '530P': time(17, 30),
    '500P': time(17, 00),
    '430P': time(16, 30),
    '400P': time(16, 00),
    '330P': time(15, 30),
    '300P': time(15, 00),
    '230P': time(14, 30),
    '200P': time(14, 00),
    '130P': time(13, 30),
    '100P': time(13, 00),
    '1230P': time(12, 30),
    '1200N': time(12, 00),
    '1130A': time(11, 30),
    '1100A': time(11, 0),
    '1030A': time(10, 30),
    '1000A': time(10, 0),
    '930A': time(9, 30),
    '900A': time(9, 0),
    '830A': time(8, 30),
    '800A': time(8, 0),
    '730A': time(7, 30),
    '700A': time(7, 0),
    '630A': time(6, 30),
    '600A': time(6, 0),
    '530A': time(5, 30),
    '500A': time(5, 0),
    '1230A': time(0, 30),
    '1201A': time(0, 0),
}


class AvailableTime(models.TextChoices):
    NotChosen = '', ''

    # ZeroZero = '1201A', '00:00'
    # ZeroThirty = '1230A', '00:30'
    FiveZero = '500A', '05:00'
    FiveThirty = '530A', '05:30'
    SixZero = '600A', '06:00',
    SixThirty = '630A', '06:30'
    SevenZero = '700A', '07:00'
    SevenThirty = '730A', '07:30'
    EightZero = '800A', '08:00'
    EightThirty = '830A', '08:30'
    NineZero = '900A', '09:00'
    NineThirty = '930A', '09:30'
    TenZero = '1000A', '10:00'
    TenThirty = '1030A', '10:30'
    ElevenZero = '1100A', '11:00'
    ElevenThirty = '1130A', '11:30'
    TwelveZero = '1200N', '12:00'
    TwelveThirty = '1230P', '12:30'
    ThirteenZero = '100P', '13:00'
    ThirteenThirty = '130P', '13:30'
    FourteenZero = '200P', '14:00'
    FourteenThirty = '230P', '14:30'
    FifteenZero = '300P', '15:00'
    FifteenThirty = '330P', '15:30'
    SixteenZero = '400P', '16:00'
    SixteenThirty = '430P', '16:30'
    SeventeenZero = '500P', '17:00'
    SeventeenThirty = '530P', '17:30'
    EighteenZero = '600P', '18:00'
    EighteenThirty = '630P', '18:30'
    NineteenZero = '700P', '19:00'
    NineteenThirty = '730P', '19:30'
    TwentyZero = '800P', '20:00'
    TwentyThirty = '830P', '20:30'
    TwentyoneZero = '900P', '21:00'
    TwentyoneThirty = '930P', '21:30'
    TwentytwoZero = '1000P', '22:00'
    TwentytwoThirty = '1030P', '22:30'
    TwentythreeZero = '1100P', '23:00'
    TwentythreeThirty = '1130P', '23:30'
    TwentythreeFiftynine = '1201A', '23:59'

    @classmethod
    def get_label_name(cls, value) -> str:
        for val, label in cls.choices:
            if val == value:
                return label
        return ''


class PassengerNum(models.IntegerChoices):
    Zero = 0, '0'
    One = 1, '1'
    Two = 2, '2'
    Three = 3, '3'
    Four = 4, '4'
    Five = 5, '5'
    Six = 6, '6'
    Seven = 7, '7'
    Eight = 8, '8'
    Nine = 9, '9'
    Ten = 10, '10'


DISCOUNT_MAP = {
    '早鳥9折': (90, '早鳥9折'),
    # '學生88折': 88,
    '早鳥8折': (80, '早鳥8折'),
    # '學生75折': 75,
    '早鳥65折': (65, '早鳥65折'),
    # '學生5折': 50,
}

MAX_TICKET_NUM = 10


class Station(models.IntegerChoices):
    Nangang = 1, '南港'
    Taipei = 2, '台北'
    Banqiao = 3, '板橋'
    Taoyuan = 4, '桃園'
    Hsinchu = 5, '新竹'
    Miaoli = 6, '苗栗'
    Taichung = 7, '台中'
    Changhua = 8, '彰化'
    Yunlin = 9, '雲林'
    Chiayi = 10, '嘉義'
    Tainan = 11, '台南'
    Zuouing = 12, '左營'


class TypeOfTrip(models.IntegerChoices):
    ONE_WAY = 0, '單程'
    # ROUND_TRIP = 1, '來回'


class BookingMethod(models.IntegerChoices):
    TIME = 0, '時間'
    TRAIN_NO = 1, '車次'


class SeatPrefer(models.IntegerChoices):
    NO_PREFER = 0, '無'
    PREFER_WINDOW = 1, '靠窗'
    PREFER_AISLE = 2, '靠走道'
