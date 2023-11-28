from datetime import datetime as dt, timedelta as td
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Session

from .constants import urls
from .constants.bookings import DISCOUNT_MAP, Station
from .constants.page_htmls import (
    BookingPage, CompleteBookingPage, ConfirmTicketPage, ErrorPage, SelectTrainPage
)
from .models import THSRTicket, Train


class THSRSession(Session):
    def get_booking_page(self) -> Tag:
        res = self.get(urls.BOOKING_PAGE, headers=urls.HEADERS, allow_redirects=True)
        return BeautifulSoup(res.content, features='html.parser')

    def get_security_img(self, img_url: str) -> bytes:
        return self.get(img_url, headers=urls.HEADERS).content

    def submit_booking_condition(self, form_data: Dict) -> Tag:
        res = self.post(
            urls.SUBMIT_FORM.format(self.cookies["JSESSIONID"]),
            headers=urls.HEADERS,
            params=form_data,
            allow_redirects=True
        )
        return BeautifulSoup(res.content, features='html.parser')

    def select_train(self, form_data: Dict) -> Tag:
        res = self.post(
            urls.SELECT_TRAIN,
            headers=urls.HEADERS,
            params=form_data,
            allow_redirects=True,
        )
        return BeautifulSoup(res.content, features='html.parser')

    def confirm_ticket(self, form_data: Dict) -> Tag:
        res = self.post(
            urls.CONFIRM_TICKET,
            headers=urls.HEADERS,
            params=form_data,
            allow_redirects=True,
        )
        return BeautifulSoup(res.content, features='html.parser')


def check_resp_ok(page: Tag) -> Tuple[bool, Optional[str]]:
    error_tag = page.find(**ErrorPage.ERROR_FEEDBACK)
    if error_tag:
        return False, error_tag.find('span').text

    error_msg = page.find(**ErrorPage.ERROR_MESSAGE)
    if error_msg:
        return False, 'ERROR__THSR_SYSTEM_DENY'

    return True, None


class PageParser():
    @staticmethod
    def get_security_img_url(booking_page: Tag) -> str:
        img_ele = booking_page.find(**BookingPage.SECURITY_IMAGE)
        return urls.BASIC + img_ele['src']

    @staticmethod
    def get_train_lst(select_train_page: Tag) -> List[Train]:
        train_lst = []
        train_elem_list: List[Tag] = select_train_page.find_all('label', **SelectTrainPage.TRAIN_LIST)

        for train_elem in train_elem_list:
            train_code = train_elem.find('input').get(SelectTrainPage.TRAIN_CODE)
            form_value = train_elem.find('input').get(SelectTrainPage.FORM_VALUE)
            dt_travel_time = dt.strptime(train_elem.find('input').get(SelectTrainPage.TRAVEL_TIME), '%H:%M')
            str_departure_date = train_elem.find('input').get(SelectTrainPage.DEPARTURE_DATE)
            str_departure_time = train_elem.find('input').get(SelectTrainPage.DEPARTURE_TIME)
            str_arrival_time = train_elem.find('input').get(SelectTrainPage.ARRIVAL_TIME)

            travel_time = td(hours=dt_travel_time.hour, minutes=dt_travel_time.minute)
            departure_time = dt.strptime(f'2023/{str_departure_date} {str_departure_time}', '%Y/%m/%d %H:%M')
            arrival_time = dt.strptime(f'2023/{str_departure_date} {str_arrival_time}', '%Y/%m/%d %H:%M')

            discount_elems: List[Tag] = train_elem.find(**SelectTrainPage.DISCOUNT_LIST).find_all('span')
            discounts = [DISCOUNT_MAP[d.text] for d in discount_elems]

            train_lst.append(Train(
                code=train_code,
                value=form_value,
                travel_time=travel_time,
                departure_time=departure_time,
                arrival_time=arrival_time,
                discounts=discounts,
            ))

        return train_lst

    @staticmethod
    def get_not_member_radio(confirm_ticket_page: Tag):
        return confirm_ticket_page.find(**ConfirmTicketPage.NOT_MEMBER).get(ConfirmTicketPage.FORM_VALUE)

    @staticmethod
    def get_booked_ticket_info(page: Tag) -> THSRTicket:
        ticket_id = page.find(**CompleteBookingPage.TICKET_ID).find('span').text
        payment_deadline = page.find(**CompleteBookingPage.PAYMENT_DEADLINE).find_next().text
        total_price = page.find(**CompleteBookingPage.TOTAL_PRICE).text
        train_id = page.find(**CompleteBookingPage.TICKECT_TRAIN_ID).text
        depart_time = page.find(**CompleteBookingPage.TICKET_DEPARTURE_TIME).text
        arrival_time = page.find(**CompleteBookingPage.TICKET_ARRIVAL_TIME).text
        seat_num = page.find(**CompleteBookingPage.TICKET_SEAT_NUM).find_next().text
        depart_station_text = page.find(**CompleteBookingPage.TICKET_DEPARTURE_STATION).find_next().text
        arrival_station_text = page.find(**CompleteBookingPage.TICKET_ARRIVAL_STATION).find_next().text
        # ticket_amount = page.find(**CompleteBookingPage.TICKET_AMOUNT).find_next().text.strip().replace('\xa0', ' ')
        date = page.find(**CompleteBookingPage.TICKET_DATE).find_next().text

        depart_station = next(filter(lambda s: s[1] == depart_station_text, Station.choices))
        arrival_station = next(filter(lambda s: s[1] == arrival_station_text, Station.choices))

        return THSRTicket(
            ticket_id=ticket_id,
            total_price=total_price,
            payment_deadline=payment_deadline,
            train_id=train_id,
            seat_num=seat_num,
            date=date,
            depart_time=depart_time,
            arrival_time=arrival_time,
            depart_station=depart_station,
            arrival_station=arrival_station,
        )
