#!/usr/bin/python
"""test of retrieving daily jumble data from uclick,
the source used by http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html
"""
from datetime import datetime as dt
import xml.etree.ElementTree as ET
import os
import urllib2


class JumbleClient(object):
    base_url = 'https://www.uclick.com/puzzles/tmjmf/puzzles/tmjmf'
    date_format = '%y%m%d'
    local_base = '/home/alanb0/public_html'
    web_base = 'http://alanbernstein.net'
    cachefile_base = 'data/jumble'

    def __init__(self):
        if not os.path.isdir(self.local_base + '/' + self.cachefile_base):
            os.makedirs(self.local_base + '/' + self.cachefile_base)

    def get_jumble(self, date=None):
        """public interface"""
        if not date:
            date = dt.today()

        jumble_xml = self.get_jumble_from_server_or_cache(date)
        jumble_json = self.parse_jumble_xml(jumble_xml)
        jumble_json['local_image'] = self.get_web_filename(date, 'gif')
        return jumble_json

    def parse_jumble_xml(self, xml_string):
        if 'xml' not in xml_string:
            # not sure why this happens
            raise Exception('request error')

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

    def get_web_filename(self, date, ext):
        return '%s/%s/%s.%s' % (self.web_base, self.cachefile_base, dt.strftime(date, self.date_format), ext)

    def get_local_filename(self, date, ext):
        return '%s/%s/%s.%s' % (self.local_base, self.cachefile_base, dt.strftime(date, self.date_format), ext)

    def get_jumble_from_server_or_cache(self, date):
        xml_filename = self.get_local_filename(date, 'xml')
        gif_filename = self.get_local_filename(date, 'gif')

        if os.path.isfile(xml_filename):
            with open(xml_filename, 'r') as f:
                xml = f.read()
            # print('read jumble cache (%s)' % xml_filename)
            return xml
        else:
            xml = self.get_jumble_from_server(date)
            gif = self.get_jumble_from_server(date, 'gif')
            with open(xml_filename, 'w') as f:
                f.write(xml)
            with open(gif_filename, 'wb') as f:
                f.write(gif)

            linkname = '%s/%s/latest.xml' % (self.local_base, self.cachefile_base)
            try:
                os.unlink(linkname)
                # print('unlink %s' % linkname)
            except:
                pass
            try:
                os.symlink(xml_filename, linkname)
                # print('link %s' % xml_filename)
            except:
                pass
            # print('wrote to cache (%s)' % xml_filename)
            return xml

    def get_jumble_from_server(self, date, ext='xml'):
        suffix = '-data' if ext == 'xml' else ''
        url = '%s%s%s.%s' % (self.base_url, dt.strftime(date, self.date_format), suffix, ext)
        # print('getting jumble from server (%s)' % url)
        resp = urllib2.urlopen(url)
        return resp.read()


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
