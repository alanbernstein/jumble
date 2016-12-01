#!/usr/local/bin/python
"""interactive CLI jumble app
"""
import re
import random
from datetime import datetime as dt

from client import JumbleClient


def main():
    jc = JumbleClient()
    jumble = jc.get_jumble()
    print('http://www.chicagotribune.com/chi-jumbleclassic-htmlpage-htmlstory.html')
    interactive(jumble)


def print_jumble(jumble, solved_flags):
    # print the clues, while accumulating circled letters from the solved ones
    letters = ''
    print('')
    print(jumble['image'])
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
    print(jumble['layout'])
    print('')


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
    main()
