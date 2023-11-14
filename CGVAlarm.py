import requests
from bs4 import BeautifulSoup
import time
import sys
from datetime import datetime
from plyer import notification
from twilio.rest import Client

# Twilio 계정으로 문자 알림 
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


def send_SMS(phonenumber):
    message = client.messages.create(
        to="+"+phonenumber,
        from_="your_twilio_phone_number",
        body="결승전 예매가 방금 시작되었습니다! 이 메시지는 자동으로 보내졌습니다. 결승전 예매가 방금 시작되었습니다!!!!!!!!!!!!")
    print(message.sid)


def print_current_time():
    now = datetime.now()
    return now.strftime("%H시 %M분 %S초: ")


def check_class_existence():
    try:
        # 예매 URL
        url = 'https://moviestory.cgv.co.kr/fanpage/mainView;jsessionid=7A6881B663171AE4E9CD5CF474487E62.STORY_node?movieIdx=87751'

        # HTTP GET 요청
        response = requests.get(url, timeout=10)

        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')

        # 특정 클래스 찾기
        class_exists = soup.find_all(class_='btn_bookNow preparing')

        # 클래스 존재 여부에 따른 메시지 출력
        if not class_exists and '추후 예매개시' not in response.text:
            print("예매가 방금 시작되었습니다. 서두르세요!!!!")
            send_SMS('your_phone_number')

            notification.notify(
                title='예매 시작',
                message='CGV 롤드컵 결승 예매가 방금 열렸습니다!!!!!!!!!!! 서두르세여ㅛ!!!!',
                app_icon=None,
                timeout=30,
            )
            time.sleep(5)
            sys.exit(1)

        else:
            print(print_current_time()+"아직 예매가 시작되지 않았습니다.")

    except requests.RequestException as e:
        print("Request 오류:", e)
        sys.exit(1)


# 10초 간격으로 함수 반복 실행
while True:
    check_class_existence()
    time.sleep(10)
