from celery import Task
import time

from django.db import transaction
from src.celery import app as celery_app
from user.models import User

from .constants.page_htmls import ErrorPage
from .exceptions import BookingException
from .models import BookingForm, BookingRequest, TicketForm, TrainForm, TrainSelector
from .services import PageParser, THSRSession, check_resp_ok
from .utils import recognize_img


@celery_app.task()
def booking(booking_request: BookingRequest):
    sess = THSRSession()
    booking_page = sess.get_booking_page()
    security_img_url = PageParser.get_security_img_url(booking_page)
    security_img_bytes = sess.get_security_img(security_img_url)
    security_code = recognize_img(security_img_bytes)

    booking_form = BookingForm(
        type_of_trip=booking_request.type_of_trip,
        seat_prefer=booking_request.seat_prefer,
        booking_method=booking_request.booking_method,
        depart_station=booking_request.depart_station,
        dest_station=booking_request.dest_station,
        depart_date=booking_request.depart_date.strftime('%Y/%m/%d'),
        depart_time=booking_request.earliest_depart_time,
        adult_num=f'{booking_request.adult_num}F',
        child_num=f'{booking_request.child_num}H',
        disabled_num=f'{booking_request.disabled_num}W',
        elder_num=f'{booking_request.elder_num}E',
        college_num=f'{booking_request.college_num}P',
        security_code=security_code,
    ).model_dump(by_alias=True)

    select_train_page = sess.submit_booking_condition(booking_form)
    ok, err_msg = check_resp_ok(select_train_page)
    while not ok:
        if err_msg == ErrorPage.ERROR_SECURITY_CODE:
            time.sleep(0.2)
            ok, err_msg = check_resp_ok(select_train_page)
        else:
            raise BookingException(err_msg)

    train_lst = PageParser.get_train_lst(select_train_page)
    train = TrainSelector.get_earliest(train_lst)
    train_form = TrainForm(train_value=train.value).model_dump(by_alias=True)

    confirm_ticket_page = sess.select_train(train_form)
    ok, err_msg = check_resp_ok(confirm_ticket_page)
    if not ok:
        raise BookingException(err_msg)

    member_radio = PageParser.get_not_member_radio(confirm_ticket_page)

    user = User.get_by_email(booking_request.user_email)
    ticket_form = TicketForm(
        personal_id=user.personal_id,
        phone=user.phone,
        email=user.email,
        member_radio=member_radio,
    ).model_dump(by_alias=True)

    complete_booking_page = sess.confirm_ticket(ticket_form)
    ok, err_msg = check_resp_ok(complete_booking_page)
    if not ok:
        raise BookingException(err_msg)

    thsr_ticket = PageParser.get_booked_ticket_info(complete_booking_page)
    with transaction.atomic():
        thsr_ticket.save()
        booking_request.thsr_ticket_id = thsr_ticket.pk
        booking_request.save()


@celery_app.task()
def add(x, y):
    return x + y


booking: Task
