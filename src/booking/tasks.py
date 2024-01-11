from django.db import transaction
from pydantic import create_model
from user.models import User

from .constants.bookings import BookingMethod
from .constants.page_htmls import BookingPage, ConfirmTicketPage, ErrorPage, SelectTrainPage
from .exceptions import BookingException
from .models import BookingForm, BookingRequest, Passenger, TicketForm, TrainForm, TrainSelector
from .services import BookingProcessor, PageParser, THSRSession, check_resp_ok


def booking_task(booking_request: BookingRequest):
    sess = THSRSession()
    booking_page = sess.get_booking_page()
    booking_form = BookingForm.generate_form(
        booking_request=booking_request,
        booking_method_radio=PageParser.get_booking_method_radio(booking_page, booking_request),
        security_code=PageParser.get_security_code(sess, booking_page),
    )

    if booking_request.booking_method == BookingMethod.TIME:
        select_train_page = BookingProcessor.submit_booking_condition(sess, booking_page, booking_form)
        train_lst = PageParser.get_train_lst(select_train_page)
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

    user = User.get_by_email(booking_request.user_email)
    passenger_fields = {}
    if discount := PageParser.get_discount(confirm_ticket_page):
        passenger_lst = [
            Passenger(
                discount=discount,
                id=p_id,
            ) for p_id in booking_request.passenger_ids
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
        ticket_form.member_account = user.personal_id
    else:
        ticket_form = PageParser.get_not_member_radio(confirm_ticket_page)

    complete_booking_page = sess.confirm_ticket(
        PageParser.get_next_page_path(ConfirmTicketPage, confirm_ticket_page),
        ticket_form.model_dump(by_alias=True),
    )
    ok, err_msg = check_resp_ok(complete_booking_page)
    if not ok:
        raise BookingException(err_msg)

    thsr_ticket = PageParser.get_booked_ticket_info(complete_booking_page)
    with transaction.atomic():
        thsr_ticket.save()
        booking_request.thsr_ticket = thsr_ticket
        booking_request.status = BookingRequest.Status.COMPLETED
        booking_request.save()
