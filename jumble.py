#!/usr/local/bin/python
"""test of retrieving daily jumble data from uclick,
the source used by http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html
"""
import os
import re
import random
from datetime import datetime as dt
import urllib2
import xml.etree.ElementTree as ET


class JumbleClient(object):
    base_url = 'https://www.uclick.com/puzzles/tmjmf/puzzles/tmjmf'
    date_format = '%y%m%d'
    cachefile_base = os.getenv('CACHE', os.path.expanduser('~/.cache')) + '/jumble/'

    def __init__(self):
        if not os.path.isdir(self.cachefile_base):
            os.makedirs(self.cachefile_base)

    def get_jumble(self, date=None):
        """public interface"""
        if not date:
            date = dt.today()

        jumble_xml = self.get_jumble_from_server_or_cache(date)
        jumble_json = self.parse_jumble_xml(jumble_xml)
        jumble_json['local_image'] = self.get_local_filename(date, 'gif')
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

    def get_local_filename(self, date, ext):
        return '%s%s.%s' % (self.cachefile_base, dt.strftime(date, self.date_format), ext)

    def get_jumble_from_server_or_cache(self, date):
        xml_filename = self.get_local_filename(date, 'xml')
        gif_filename = self.get_local_filename(date, 'gif')
        if os.path.isfile(xml_filename):
            with open(xml_filename, 'r') as f:
                xml = f.read()
            print('read jumble cache (%s)' % xml_filename)
            return xml
        else:
            xml = self.get_jumble_from_server(date)
            gif = self.get_jumble_from_server(date, 'gif')
            with open(xml_filename, 'w') as f:
                f.write(xml)
            linkname = '%slatest.xml' % self.cachefile_base
            os.unlink(linkname)
            print('unlink %s' % linkname)
            os.symlink(xml_filename, linkname)
            print('link %s' % xml_filename)
            print('wrote to cache (%s)' % xml_filename)
            return xml

    def get_jumble_from_server(self, date, ext='xml'):
        suffix = '-data' if ext == 'xml' else ''
        url = '%s%s%s.%s' % (self.base_url, dt.strftime(date, self.date_format), suffix, ext)
        print('getting jumble from server (%s)' % url)
        resp = urllib2.urlopen(url)
        return resp.read()


def print_jumble(jumble, solved_flags):

    # print the clues, while accumulating circled letters from the solved ones
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

    # print the caption, plus all available circled letters
    print(jumble['caption'] + '...')
    l = list(letters.upper())
    random.shuffle(l)
    print(''.join(l))

    # print the solution layout
    print(get_layout_display(jumble['layout']))
    print('')


def get_layout_display(layout):
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


def print_letters(jumble, solved_flags):
    letters = ''
    for clue, solved in zip(jumble['clues'], solved_flags):
        if solved:
            for n in clue['circles']:
                letters += clue['answer'][n-1]

    l = list(letters.upper())
    random.shuffle(l)
    print(''.join(l))


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

        # print(inp, answer_words) # for debugging
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
    print('http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html')
    interactive(jumble)
