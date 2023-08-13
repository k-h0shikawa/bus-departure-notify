# 概要

バスの到着情報をlineに通知するバッチです。

下記のサイトからバスの運行情報をスクレイピングしています。

https://keisei-townbus.bus-navigation.jp/wgsys/wgp/search.htm

※個人情報のため、スクレイピング対象のURLはiniファイルを使用しています。

cronでバス使用予定日に定期実行しています。

## 使い方

下記のiniファイルをクローンした同フォルダに配置

``` bus_departure.ini
Url = [[スクレイピング対象のURL]]
Token = [[LINE Notifyのアクセストークン]]
```

トークンは以下より取得


https://notify-bot.line.me/ja/



### 出力例
```
N個前の停留所を通過
予定時刻HH:mm
発車予測HH:mm
約M分で発車します
```

### Dockerを使用する場合
*host*
``` sh
docker build -t bus_departure .
docker run -it bus_departure /bin/sh
```

*container*
``` sh
crontab -e
* * * * * sh /workspace/script.sh >> /var/log/cron.log
cron && tail -f /var/log/cron.log
# stop command
service cron stop
```