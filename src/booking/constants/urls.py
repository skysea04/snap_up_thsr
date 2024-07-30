HEADERS = {
    'Host': 'irs.thsrc.com.tw',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-TW,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
}


BASIC = 'https://irs.thsrc.com.tw{path}'
BOOKING_PAGE = 'https://irs.thsrc.com.tw/IMINT/?locale=tw'
LATEST_BOOKING_DATE = 'https://www.thsrc.com.tw/RawData/EAIIRS_{today_date}.xml'

# class URL:
#     BASIC = 'https://irs.thsrc.com.tw'
#     BOOKING_PAGE = 'https://irs.thsrc.com.tw/IMINT/?locale=tw'
#     SUBMIT_FORM = 'https://irs.thsrc.com.tw/IMINT/;jsessionid={}?wicket:interface=:0:BookingS1Form::IFormSubmitListener'
#     SELECT_TRAIN = 'https://irs.thsrc.com.tw/IMINT/?wicket:interface=:1:BookingS2Form::IFormSubmitListener'
#     CONFIRM_TICKET = 'https://irs.thsrc.com.tw/IMINT/?wicket:interface=:2:BookingS3Form::IFormSubmitListener'
