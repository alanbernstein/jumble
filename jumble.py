#!/usr/local/bin/python
"""test of retrieving daily jumble data from uclick,
the source used by http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html
"""
import os
import re
from datetime import datetime as dt
import requests
import xml.etree.ElementTree as ET


class JumbleClient(object):
    base_url = 'https://www.uclick.com/puzzles/tmjmf/puzzles/tmjmf'
    date_format = '%y%m%d'
    cachefile_base = os.getenv('CACHE', os.path.expanduser('~/.cache')) + '/jumble/'

    def __init__(self):
        if not os.path.isdir(self.cachefile_base):
            os.makedirs(self.cachefile_base)

    def get_jumble(self, date=None):
        if not date:
            date = dt.today()

        jumble_xml = self.get_jumble_from_server_or_cache(date)
        jumble_json = self.parse_jumble_xml(jumble_xml)
        return jumble_json

    def parse_jumble_xml(self, xml_string):
        if 'xml' not in xml_string:
            # not sure why this happens
            raise Exception('request error')

        root = ET.fromstring(xml_string)
        return {
            'date': root.find('Date').attrib['v'],
            'clues': [self.parse_clue(c) for c in root.find('clues')],
            'caption': root.find('caption')[0].attrib['t'],
            'layout': root.find('solution')[0].attrib['layout'],
            'answer': root.find('solution')[0].attrib['a'],
        }

    def parse_clue(self, xml_clue):
        return {
            'jumbled': xml_clue.attrib['j'],
            'answer': xml_clue.attrib['a'],
            'circles': [int(n) for n in xml_clue.attrib['circle'].split(',')],
        }

    def get_jumble_from_server_or_cache(self, date):
        filename = '%s%s.xml' % (self.cachefile_base, dt.strftime(date, self.date_format))
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = f.read()
            print('read jumble cache (%s)' % filename)
            return data
        else:
            xml = self.get_jumble_from_server(date)
            with open(filename, 'w') as f:
                f.write(xml)
            print('wrote to cache (%s)' % filename)
            return xml

    def get_jumble_from_server(self, date):
        url = '%s%s-data.xml' % (self.base_url, dt.strftime(date, self.date_format))
        print('getting jumble from server (%s)' % url)
        resp = requests.get(url)
        return resp.content


def print_jumble(jumble, solved_flags):
    letters = ''
    print('')
    for clue, solved in zip(jumble['clues'], solved_flags):
        print(clue['jumbled'])
        if solved:
            print(clue['answer'])
            for n in clue['circles']:
                letters += clue['answer'][n-1]
        else:
            L = len(clue['jumbled'])
            print(''.join(['_o'[n+1 in clue['circles']] for n in range(L)]))
        print('')

    print(jumble['caption'] + '...')
    print(letters.upper())

    s1 = re.sub('[A-Z]', '_', jumble['layout'])
    s2 = re.sub('[{}]', '', s1)
    print(s2)
    print('')


def print_letters(jumble, solved_flags):
    letters = ''
    for clue, solved in zip(jumble['clues'], solved_flags):
        if solved:
            for n in clue['circles']:
                letters += clue['answer'][n-1]

    print(letters.upper())


def interactive(jumble):
    solved = [False] * 4
    answers = [c['answer'].lower() for c in jumble['clues']]
    t = [dt.now()]

    answer_words = re.sub('[^a-z ]', '', jumble['layout'].lower()).split()

    print_jumble(jumble, solved)

    while True:
        inp = raw_input('> ')
        inp = inp.lower()
        if inp in answers:
            solved[answers.index(inp)] = True
            t.append(dt.now())

        if any([w in answer_words for w in inp.split()]):
            print('"%s" is in solution ' % inp)
            # TODO: store this and show it/remove the used letters

        if inp.replace(' ', '') == jumble['answer'].lower():
            # done, quit
            t.append(dt.now())
            break

        print_letters(jumble, solved)

    print('done! %d sec' % (t[-1] - t[0]).seconds)


if __name__ == '__main__':
    jc = JumbleClient()
    jumble = jc.get_jumble()
    interactive(jumble)
