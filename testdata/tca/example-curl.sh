#!/bin/bash
curl 'https://puzzles.tribunecontentagency.com/puzzles/pzzResource/puzzle.do' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Cookie: JSESSIONID=C4CC6580198345B9695FEB57AC96268E; localeCookie=en_US; _ga=GA1.2.176094494.1657421934; _gid=GA1.2.1150432500.1657421934' \
  -H 'Origin: https://puzzles.tribunecontentagency.com' \
  -H 'Referer: https://puzzles.tribunecontentagency.com/puzzles/jumble/jumble.do?apiKey=e06317ec9b0e52363f404c73f8b681b926908f6c22dd46f86040e5fea0e96879&css=https://fun.chicagotribune.com/assets/tca/css/embedder.css&lang=en_US&wlp=true&type=jumbledaily&gd_sdk_referrer_url=https://html5.gamedistribution.com/21a66edc2bc84400acddb3d95487cd68/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw 'apiKey=e06317ec9b0e52363f404c73f8b681b926908f6c22dd46f86040e5fea0e96879&productId=jumbledaily&publicationDate=&prvNxt=&langCode=en-US&ldt=07/09/2022' \
  --compressed