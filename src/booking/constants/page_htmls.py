# Page 1 查詢車次
class BookingPage:
    SECURITY_IMAGE = {'id': 'BookingS1Form_homeCaptcha_passCode'}  # 驗證碼圖片
    SEAT_PREFER_RADIO = {'id': 'BookingS1Form_seatCon_seatRadioGroup'}  # 無偏好 靠窗 靠走道
    TYPE_OF_TRIP = {'id': 'BookingS1Form_tripCon_typesoftrip'}  # 單程、來回
    BOOKING_METHOD_TIME_RADIO = {
        'name': 'input',
        'attrs': {'data-target': 'search-by-time'}
    }
    BOOKING_METHOD_TRAIN_NO_RADIO = {
        'name': 'input',
        'attrs': {'data-target': 'search-by-trainNo'}
    }
    NEXT_PAGE_PATH = {'id': 'BookingS1Form'}


# Page 2 選擇車次
class SelectTrainPage:
    GO_PANEL = {'id': 'BookingS2Form_TrainQueryDataViewPanel'}  # 去程
    BACK_PANEL = {'id': 'BookingS2Form_TrainQueryDataViewPanel2'}  # 回程
    TRAIN_LIST = {'class': 'result-item'}
    DISCOUNT_LIST = {'class': 'discount'}
    FORM_VALUE = 'value'
    ARRIVAL_TIME = 'queryarrival'
    DEPARTURE_TIME = 'querydeparture'
    DEPARTURE_DATE = 'querydeparturedate'
    TRAIN_CODE = 'querycode'
    TRAVEL_TIME = 'queryestimatedtime'
    NEXT_PAGE_PATH = {'id': 'BookingS2Form'}


# Page 3 取票資訊
class ConfirmTicketPage:
    TGO_MEMBER = {
        'name': 'input',
        'attrs': {'id': 'memberSystemRadio1'},
    }
    NOT_MEMBER = {
        'name': 'input',
        'attrs': {'id': 'memberSystemRadio3'},
    }
    DISCOUNT = {'class': 'early-bird'}
    NEXT_PAGE_PATH = {'id': 'BookingS3FormSP'}
    FORM_VALUE = 'value'


# Page 4 完成訂位
class CompleteBookingPage:
    TICKET_ID = {
        'name': 'p',
        'attrs': {'class': 'pnr-code'},
    }
    PAYMENT_DEADLINE = {'text': '（付款期限：'}
    TOTAL_PRICE = {'id': 'setTrainTotalPriceValue'}
    TICKET_DATE = {
        'name': 'span',
        'attrs': {'class': 'date'}
    }
    TICKET_DEPARTURE_STATION = {
        'name': 'p',
        'attrs': {'class': 'departure-stn'}
    }
    TICKET_ARRIVAL_STATION = {
        'name': 'p',
        'attrs': {'class': 'arrival-stn'}
    }
    TICKET_DEPARTURE_TIME = {'id': 'setTrainDeparture0'}
    TICKET_ARRIVAL_TIME = {'id': 'setTrainArrival0'}
    TICKECT_TRAIN_ID = {'id': 'setTrainCode0'}
    TICKET_SEAT_NUM = {
        'name': 'div',
        'attrs': {'class': 'seat-label'}
    }
    TICKET_AMOUNT = {
        'name': 'p',
        'text': '票數'
    }


# Error
class ErrorPage:
    ERROR_FEEDBACK = {'class': 'feedbackPanelERROR'}
    ERROR_MESSAGE = {'text': '抱歉，無法繼續提供您訂票的服務，可能發生原因及解決方法如下：'}
    ERROR_MESSAGE_SYSTEM_BUSY = {'text': '系統忙碌中，請耐心等候，並請勿使用「重新整理」鍵或離開本頁面。'}
    ERROR_CONTENT = {'class': 'error-content'}

    ERROR_SECURITY_CODE = '檢測碼輸入錯誤，請確認後重新輸入，謝謝！'
    ERROR_NO_TRAIN = '去程查無可售車次或選購的車票已售完，請重新輸入訂票條件。'
