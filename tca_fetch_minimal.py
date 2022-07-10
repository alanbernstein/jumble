import cgi
import urllib2
import json

# this is the minimal thing that works to retrieve the jumble clue data from the API.

base_url = 'https://puzzles.tribunecontentagency.com/puzzles/pzzResource/puzzle.do'
data_raw_template = 'apiKey=e06317ec9b0e52363f404c73f8b681b926908f6c22dd46f86040e5fea0e96879&productId=jumbledaily&publicationDate=&prvNxt=&langCode=en-US&ldt=%s'
date_format = '%m/%d/%y'  # 07/09/2022
print('db2<br>\n')
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
 'Cookie': 'JSESSIONID=C4CC6580198345B9695FEB57AC96268E; localeCookie=en_US; _ga=GA1.2.176094494.1657421934; _gid=GA1.2.1150432500.1657421934',
 'Origin': 'https://puzzles.tribunecontentagency.com',
 'Referer': 'https://puzzles.tribunecontentagency.com/puzzles/jumble/jumble.do?apiKey=e06317ec9b0e52363f404c73f8b681b926908f6c22dd46f86040e5fea0e96879&css=https://fun.chicagotribune.com/assets/tca/css/embedder.css&lang=en_US&wlp=true&type=jumbledaily&gd_sdk_referrer_url=https://html5.gamedistribution.com/21a66edc2bc84400acddb3d95487cd68/',
 'Sec-Fetch-Dest': 'empty',
 'Sec-Fetch-Mode': 'cors',
 'Sec-Fetch-Site': 'same-origin',
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
 'X-Requested-With': 'XMLHttpRequest',
 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
 'sec-ch-ua-mobile': '?0',
 'sec-ch-ua-platform': '"macOS"',
    }
print('db3<br>\n')
    
#data = self.data_raw_template % dt.strftime(date, self.date_format)
data = data_raw_template % '07/09/2022'
request = urllib2.Request(base_url, data=data, headers=headers)
resp = urllib2.urlopen(request).read()
resp_json = json.loads(resp)

print(resp_json['puzzleDetails'])
print(resp_json['cdata'][0]['resourceLocation'])

# website path
with open('/home/alanb0/public_html/data/jumble/2022/0709.json', 'w') as f:
    json.dump(resp_json, f)