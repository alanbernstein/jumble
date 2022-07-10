import json
import os
import urllib2
import xml.etree.ElementTree as ET
from datetime import datetime as dt


class JumbleClient(object):
    """
    handles retrieving, caching, and formatting jumble data from source server
    default implementation is for local use
    new tca data found via
    - user site: https://fun.chicagotribune.com/game/tca-jumble-daily
    - puzzle frame: https://puzzles.tribunecontentagency.com/puzzles/jumble/jumble.do?apiKey=e06317ec9b0e52363f404c73f8b681b926908f6c22dd46f86040e5fea0e96879&css=https://fun.chicagotribune.com/assets/tca/css/embedder.css&lang=en_US&wlp=true&type=jumbledaily&gd_sdk_referrer_url=https://html5.gamedistribution.com/21a66edc2bc84400acddb3d95487cd68/

    old uclick data found via http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html
    """

    #base_url = 'https://www.uclick.com/puzzles/tmjmf/puzzles/tmjmf'
    #date_format = '%y%m%d'

    base_url = 'https://puzzles.tribunecontentagency.com/puzzles/pzzResource/puzzle.do'
    data_raw_template = 'apiKey=e06317ec9b0e52363f404c73f8b681b926908f6c22dd46f86040e5fea0e96879&productId=jumbledaily&publicationDate=&prvNxt=&langCode=en-US&ldt=%s'
    date_format = '%m/%d/%y'  # 07/09/2022
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

    cachefile_base = os.getenv('CACHE', os.path.expanduser('~/.cache')) + '/jumble/'

    def __init__(self):
        if not os.path.isdir(self.cachefile_base):
            os.makedirs(self.cachefile_base)

    def get_jumble(self, date=None):
        """public interface"""
        if not date:
            date = dt.today()

        jumble_json = self.get_jumble_from_server_or_cache(date)
        #jumble_json = self.parse_jumble_xml(jumble_xml)
        #jumble_json['image'] = self.get_image_filename(date)
        return jumble_json

    def get_image_filename(self, date):
        return self.get_local_filename(date, 'gif')

    def parse_jumble_xml(self, xml_string):
        root = ET.fromstring(xml_string)
        layout_original = root.find('solution')[0].attrib['layout'],
        if type(layout_original) == tuple:
            # what is this for... cant remember
            layout_original = layout_original[0]
        return {
            'date': root.find('Date').attrib['v'],
            'clues': [self.parse_clue(c) for c in root.find('clues')],
            'caption': root.find('caption')[0].attrib['t'],
            'layout_original': layout_original,
            'layout': format_layout(layout_original),
            'answer': root.find('solution')[0].attrib['a'],
        }

    def parse_clue(self, xml_clue):
        return {
            'jumbled': xml_clue.attrib['j'],
            'answer': xml_clue.attrib['a'],
            'circles': [int(n) for n in xml_clue.attrib['circle'].split(',')],
        }

    def get_local_filename(self, date, ext):
        return '%s%s.%s' % (self.cachefile_base, dt.strftime(date, self.date_format), ext)

    def get_jumble_from_server_or_cache(self, date):
        details_filename = self.get_local_filename(date, 'json')
        gif_filename = self.get_local_filename(date, 'gif')

        if os.path.isfile(details_filename):
            with open(details_filename, 'r') as f:
                details = f.read()
            print('read jumble cache (%s)' % details_filename)
            return details
        else:
            details = self.get_jumble_from_server(date)
            gif = self.get_jumble_from_server(date, 'gif')
            with open(details_filename, 'w') as f:
                f.write(details)
            with open(gif_filename, 'wb') as f:
                f.write(gif)

            linkname = '%slatest.xml' % self.cachefile_base
            try:
                os.unlink(linkname)
                # print('unlink %s' % linkname)
            except:
                pass
            try:
                os.symlink(details_filename, linkname)
                # print('link %s' % xml_filename)
            except:
                pass
            # print('wrote to cache (%s)' % xml_filename)
            return details

    def get_jumble_from_server_old(self, date, ext='xml'):
        suffix = '-data' if ext == 'xml' else ''
        url = '%s%s%s.%s' % (self.base_url, dt.strftime(date, self.date_format), suffix, ext)
        # print('getting jumble from server (%s)' % url)
        resp = urllib2.urlopen(url)
        return resp.read()

    def get_jumble_from_server(self, date, ext='json'):
        data = self.data_raw_template % dt.strftime(date, self.date_format)
        request = urllib2.Request(self.base_url, data=data, headers=self.headers)
        resp = urllib2.urlopen(request).read()
        resp_json = json.loads(resp)
        return resp_json


class WebClient(JumbleClient):
    """
    minimal extension of client, to deal with path issues of being a web app
    """
    local_base = os.getenv('JUMBLE_LOCAL_BASE', '/home/user/')
    web_base = os.getenv('SITE_URL', 'www.example.com')
    cachefile_base = 'data/jumble'

    def __init__(self):
        # override to deal with cache path
        if not os.path.isdir(self.local_base + '/' + self.cachefile_base):
            os.makedirs(self.local_base + '/' + self.cachefile_base)

    def get_image_filename(self, date):
        # override: image filename must be remote, not local
        return self.get_web_filename(date, 'gif')

    def get_web_filename(self, date, ext):
        # helper for get_image_filename
        return '%s/%s/%s.%s' % (self.web_base, self.cachefile_base, dt.strftime(date, self.date_format), ext)

    def get_local_filename(self, date, ext):
        # override to deal with cache path
        return '%s/%s/%s.%s' % (self.local_base, self.cachefile_base, dt.strftime(date, self.date_format), ext)


def format_layout(layout):
    """
    needs to be parsed:
    'OUT{ TO }PASTURE' -> solution = OUTPASTURE, display = "___ TO _______"
    just use state machine to track whether inside parens
    """
    # too naive:
    # s1 = re.sub('[A-Z]', '_', layout)
    # s2 = re.sub('[{}]', '', s1)

    disp = ''
    state = 0
    for c in layout:
        if c == '{':
            state = 1
        elif c == '}':
            state = 0
        elif state == 0 and c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            disp += '_'
        else:
            disp += c
    return disp
