# coding:UTF-8
from bs4 import BeautifulSoup

import requests
import configparser

def initialize_config():
    config_init = configparser.ConfigParser()
    config_init.read("bus_departure.ini", encoding="utf-8")
    read_default = config_init["DEFAULT"]
    init = {
        "url": read_default.get("Url"),
        "token": read_default.get("Token")
    }
    return init

def fetch_bus_arrival_status(soup):
    distance_from_station = soup.find_all('span', style="border: 0px; font-size: 18px;")[0].string.strip()
    plan_arrival_time = "".join(soup.find_all('td', style="padding-left: 30px;")[0].text.split()).strip()
    estimate_time = "".join(soup.find_all('td', style="padding-left: 30px;")[2].text.split()).strip()
    expected_arrival_time = "".join(soup.find_all('td', colspan="2")[3].text.split()).strip()
    
    return (
        distance_from_station + "個前の停留所を通過", # N個前の停留所を通過
        plan_arrival_time, # 予定時刻 HH:mm
        expected_arrival_time, # 発車予測 HH:mm
        estimate_time # 約M分で発車します
    )

def send_notification(token, text):
    headers = {'Authorization': 'Bearer ' + token}
    files = {'message': (None, text)}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

if __name__ == "__main__":
    init = initialize_config()
    response = requests.get(init["url"])

    # 200でないときエラー
    if response.status_code != 200:
        print('ステータスコードが200ではありませんでした。')
        print("response.status_code" + response.status_code)
        send_notification(init["token"], '[ERROR]ステータスコードが200ではありませんでした。')
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')
    # デバッグ用テストデータ
    # soup = BeautifulSoup(open("./test.html"), 'html.parser')
    
    # バスの営業時間外のときは取得しない
    error_info_div = soup.find("div", id="errInfo")
    if error_info_div and soup.find("div", id="errInfo").string == "60分以内に接近しているバスはありません。":
        print("情報の取得に失敗しました。60分以内に接近しているバスはありません。")
        send_notification(init["token"], "60分以内に接近しているバスはありません。")
        exit()
    
    arrival_status = fetch_bus_arrival_status(soup)
    send_notification(init["token"], "\n".join(arrival_status))
    print("通知に成功しました。")
    
