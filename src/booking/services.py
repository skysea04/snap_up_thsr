import time
from datetime import datetime as dt, timedelta as td
from typing import Dict, List, Optional, Tuple, Union

import requests
from booking.constants.bookings import AvailableTime
from bs4 import BeautifulSoup
from bs4.element import Tag

from . import exceptions, utils
from .constants import urls
from .constants.bookings import DISCOUNT_MAP, BookingMethod, Station
from .constants.page_htmls import (
    BookingPage, CompleteBookingPage, ConfirmTicketPage, ErrorPage, SelectTrainPage
)
from .models import BookingForm, BookingRequest, THSRTicket, Train


class THSRSession(requests.Session):
    def get_booking_page(self) -> Tag:
        res = self.get(urls.BOOKING_PAGE, headers=urls.HEADERS, allow_redirects=True)
        return BeautifulSoup(res.content, features='html.parser')

    def get_security_img(self, img_url: str) -> bytes:
        return self.get(img_url, headers=urls.HEADERS).content

    def submit_booking_condition(self, path: str, form_data: Dict) -> Tag:
        res = self.post(
            urls.BASIC.format(path=path),
            headers=urls.HEADERS,
            params=form_data,
            allow_redirects=True,
        )
        return BeautifulSoup(res.content, features='html.parser')

    def select_train(self, path: str, form_data: Dict) -> Tag:
        res = self.post(
            urls.BASIC.format(path=path),
            headers=urls.HEADERS,
            params=form_data,
            allow_redirects=True,
        )
        return BeautifulSoup(res.content, features='html.parser')

    def confirm_ticket(self, path: str, form_data: Dict) -> Tag:
        res = self.post(
            urls.BASIC.format(path=path),
            headers=urls.HEADERS,
            params=form_data,
            allow_redirects=True,
        )
        return BeautifulSoup(res.content, features='html.parser')


class PageParser:
    @staticmethod
    def check_booking_page_ok(booking_page: Tag) -> Tuple[bool, Optional[str]]:
        img_ele = booking_page.find(**BookingPage.SECURITY_IMAGE)
        if not img_ele:
            return False, 'ERROR__THSR_SYSTEM_DENY'

    @staticmethod
    def get_booking_method_radio(booking_page: Tag, booking_request: BookingRequest) -> Dict:
        if booking_request.booking_method == BookingMethod.TIME:
            return booking_page.find(**BookingPage.BOOKING_METHOD_TIME_RADIO).get('value')

        return booking_page.find(**BookingPage.BOOKING_METHOD_TRAIN_NO_RADIO).get('value')

    @staticmethod
    def get_security_img_url(booking_page: Tag) -> str:
        img_ele = booking_page.find(**BookingPage.SECURITY_IMAGE)
        return urls.BASIC.format(path=img_ele['src'])

    @staticmethod
    def get_security_code(sess: THSRSession, booking_page: Tag) -> str:
        security_img_url = PageParser.get_security_img_url(booking_page)
        security_img_bytes = sess.get_security_img(security_img_url)
        return utils.recognize_img(security_img_bytes)

    @staticmethod
    def get_next_page_path(
        page_type: Union[BookingPage, SelectTrainPage, ConfirmTicketPage],
        booking_page: Tag
    ) -> str:
        return booking_page.find(**page_type.NEXT_PAGE_PATH)['action']

    @staticmethod
    def get_train_lst(booking_request: BookingRequest, select_train_page: Tag, buy_discount_ticket: bool) -> List[Train]:
        train_lst = []
        train_elem_lst: List[Tag] = select_train_page.find_all('label', **SelectTrainPage.TRAIN_LIST)

        for train_elem in train_elem_lst:
            str_departure_time = train_elem.find('input').get(SelectTrainPage.DEPARTURE_TIME)
            if str_departure_time < AvailableTime.get_label_name(booking_request.earliest_depart_time):
                continue

            str_arrival_time = train_elem.find('input').get(SelectTrainPage.ARRIVAL_TIME)
            if str_arrival_time.startswith('00'):  # next day
                continue

            if str_arrival_time > AvailableTime.get_label_name(booking_request.latest_arrival_time):
                break

            discount_elems: List[Tag] = train_elem.find(**SelectTrainPage.DISCOUNT_LIST).find_all('span')
            if discount_elems and not buy_discount_ticket:
                continue

            departure_time = dt.strptime(str_departure_time, '%H:%M').time()
            arrival_time = dt.strptime(str_arrival_time, '%H:%M').time()
            train_code = train_elem.find('input').get(SelectTrainPage.TRAIN_CODE)
            form_value = train_elem.find('input').get(SelectTrainPage.FORM_VALUE)
            dt_travel_time = dt.strptime(train_elem.find('input').get(SelectTrainPage.TRAVEL_TIME), '%H:%M')
            travel_time = td(hours=dt_travel_time.hour, minutes=dt_travel_time.minute)
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
    def get_tgo_member_radio(confirm_ticket_page: Tag):
        return confirm_ticket_page.find(**ConfirmTicketPage.TGO_MEMBER).get(ConfirmTicketPage.FORM_VALUE)

    @staticmethod
    def get_discount(confirm_ticket_page: Tag) -> str:
        discount_tag = confirm_ticket_page.find(**ConfirmTicketPage.DISCOUNT)
        if not discount_tag:
            return ''

        return discount_tag.text

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

        depart_station = next(filter(lambda s: s[1] == depart_station_text, Station.choices))[0]
        arrival_station = next(filter(lambda s: s[1] == arrival_station_text, Station.choices))[0]

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


class BookingProcessor:
    @staticmethod
    def submit_booking_condition(sess: THSRSession, booking_page: Tag, booking_form: BookingForm) -> Tag:
        next_page = sess.submit_booking_condition(
            PageParser.get_next_page_path(BookingPage, booking_page),
            booking_form.model_dump(by_alias=True),
        )
        ok, err_msg = check_resp_ok(next_page)

        err_cnt = 0
        while not ok:
            if err_msg == ErrorPage.ERROR_SECURITY_CODE and err_cnt < 3:
                err_cnt += 1
                time.sleep(0.1)
                booking_page = sess.get_booking_page()
                booking_form.security_code = PageParser.get_security_code(sess, booking_page),
                next_page = sess.submit_booking_condition(
                    PageParser.get_next_page_path(BookingPage, booking_page),
                    booking_form.model_dump(by_alias=True),
                )
                ok, err_msg = check_resp_ok(next_page)
            else:
                raise exceptions.BookingException(err_msg)

        return next_page


def get_holidays_reservation_start_date():
    res = requests.get(urls.HOLIDAY_RESERVATION_START_DATE, headers=urls.HEADERS)
    page = BeautifulSoup(res.content, features='html.parser')
    return page.find('div', class_='news').text


def check_resp_ok(page: Tag) -> Tuple[bool, Optional[str]]:
    maintenance_tag = page.find(ErrorPage.in_maintenance)
    if maintenance_tag:
        return False, '高鐵系統維護中'

    feedback_tag = page.find(**ErrorPage.ERROR_FEEDBACK)
    if feedback_tag:
        return False, feedback_tag.find('span').text

    error_msg = page.find(**ErrorPage.ERROR_MESSAGE)
    if error_msg:
        return False, '高鐵系統拒絕訂票'

    error_msg = page.find(ErrorPage.server_busy)
    if error_msg:
        return False, '高鐵系統忙碌中'

    error_content = page.find(**ErrorPage.ERROR_CONTENT)
    if error_content:
        return False, error_content.find('p').text

    reach_limit = page.find(**ErrorPage.ERROR_REACH_LIMIT)
    if reach_limit:
        return False, reach_limit

    return True, None
