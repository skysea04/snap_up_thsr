from datetime import datetime as dt, timedelta as td

from basis.conf import CURRENT_TZ
from basis.logger import log
from django.db import transaction
from django.utils import timezone as tz
from pydantic import create_model

from .constants.bookings import AVAILABLE_TIME_MAP, BookingMethod
from .constants.page_htmls import ConfirmTicketPage, SelectTrainPage
from .exceptions import BookingException
from .models import BookingForm, BookingRequest, Passenger, TicketForm, TrainForm, TrainSelector
from .services import BookingProcessor, PageParser, THSRSession, check_resp_ok
from .utils import get_latest_booking_date


def booking_task(booking_request: BookingRequest):
    sess = THSRSession()
    user = booking_request.user
    booking_page = sess.get_booking_page()
    ok, err_msg = check_resp_ok(booking_page)
    if not ok:
        raise BookingException(err_msg)

    booking_form = BookingForm.generate_form(
        booking_request=booking_request,
        booking_method_radio=PageParser.get_booking_method_radio(booking_page, booking_request),
        security_code=PageParser.get_security_code(sess, booking_page),
    )

    if booking_request.booking_method == BookingMethod.TIME:
        select_train_page = BookingProcessor.submit_booking_condition(sess, booking_page, booking_form)
        train_lst = PageParser.get_train_lst(booking_request, select_train_page, user.buy_discount_ticket)
        if not train_lst:
            raise BookingException('no train available')

        train = TrainSelector.get_earliest(train_lst)
        train_form = TrainForm(train_value=train.value)

        confirm_ticket_page = sess.select_train(
            PageParser.get_next_page_path(SelectTrainPage, select_train_page),
            train_form.model_dump(by_alias=True),
        )

    else:  # booking_request.booking_method == BookingMethod.TRAIN_NO:
        confirm_ticket_page = BookingProcessor.submit_booking_condition(sess, booking_page, booking_form)

    ok, err_msg = check_resp_ok(confirm_ticket_page)
    if not ok:
        raise BookingException(err_msg)

    passenger_fields = {}
    if discount := PageParser.get_discount(confirm_ticket_page):
        passenger_ids = booking_request.passenger_ids or [user.personal_id]
        passenger_lst = [
            Passenger(
                discount=discount,
                id=p_id,
            ) for p_id in passenger_ids
        ]
        passenger_fields = TicketForm.generate_discount_passenger_fields(passenger_lst)

    DiscountTicketForm = create_model(
        'DiscountTicketForm',
        **passenger_fields,
        __base__=TicketForm,
    )
    ticket_form = DiscountTicketForm(
        personal_id=user.personal_id,
        phone=user.phone,
        email=user.email,
    )
    if user.use_tgo_account:
        ticket_form.member_radio = PageParser.get_tgo_member_radio(confirm_ticket_page)
        if user.tgo_account_same_as_personal_id:
            ticket_form.member_account = user.personal_id
        else:
            ticket_form.member_account = user.tgo_account
    else:
        ticket_form.member_radio = PageParser.get_not_member_radio(confirm_ticket_page)

    complete_booking_page = sess.confirm_ticket(
        PageParser.get_next_page_path(ConfirmTicketPage, confirm_ticket_page),
        ticket_form.model_dump(by_alias=True),
    )
    ok, err_msg = check_resp_ok(complete_booking_page)
    if not ok:
        raise BookingException(err_msg)

    thsr_ticket = PageParser.get_booked_ticket_info(complete_booking_page)
    thsr_ticket.user = user
    with transaction.atomic():
        thsr_ticket.save()

        if booking_request.booking_method:
            booking_request.train_id = thsr_ticket.train_id

        booking_request.thsr_ticket = thsr_ticket
        booking_request.status = BookingRequest.Status.COMPLETED
        booking_request.error_msg = ''
        booking_request.save()


def update_not_yet_requests_to_pending():
    latest_booking_date = get_latest_booking_date()
    not_yet_requests = BookingRequest.get_all_by_status(BookingRequest.Status.NOT_YET)
    for request in not_yet_requests:
        if request.depart_date <= latest_booking_date:
            request.status = BookingRequest.Status.PENDING
            request.save()


def expire_pending_requests():
    pending_requests = BookingRequest.get_all_by_status(BookingRequest.Status.PENDING)
    now = tz.now().astimezone(CURRENT_TZ)
    for request in pending_requests:
        if request.booking_method == BookingMethod.TIME:
            earliest_booking_time = dt.combine(
                request.depart_date,
                AVAILABLE_TIME_MAP[request.earliest_depart_time],
                tzinfo=CURRENT_TZ,
            )
            if now + td(minutes=30) > earliest_booking_time:
                request.status = BookingRequest.Status.EXPIRED
                request.save()

        else:  # Train No
            if now.date() >= request.depart_date:
                request.status = BookingRequest.Status.EXPIRED
                request.save()


def book_all_pending_reqests() -> bool:
    pending_requests = BookingRequest.get_all_by_status(BookingRequest.Status.PENDING)
    counter = 0
    for request in pending_requests:
        try:
            booking_task(request)
            counter += 1
        except BookingException as e:
            log.error(e)
            request.error_msg = str(e)
            request.save()

    return counter == len(pending_requests)
