import json

"""
my old json format

{
  "answer": "ADANEWONE",
  "layout": "\u201c__\u201d _ ___ ___",
  "layout_original": "{\u201c}AD{\u201d }A{ }NEW{ }ONE",
  "caption": "The billboards were so profitable, they decided to",
  "clues": [
    {
      "answer": "SWOON",
      "circles": [
        2,
        4,
        5
      ],
      "jumbled": "OWSNO"
    },
    ...
  ],
  "date": "200104"
}
"""

def parse_clue(clue):
    return {
        'answer': clue['answer'],
        'circles': [int(v) for v in clue['shape']['value'].split(',')],
        'jumbled': clue['answer'],
    }

def parse_layout(solns):
    res = []
    for s in solns:
        pre = s['prefix'] or ''
        suf = s['suffix'] or ''
        res.append(pre + ('_' * len(s['word'])) + suf)

    return ' '.join(res)  # remove final space

def parse_response(resp):
    det = resp['puzzleDetails']
    bon = det['bonusPuzzle']
    return {
        'date': det['date'],
        'clues': [parse_clue(c) for c in det['clues']],
        'caption': bon['caption'],
        'layout': parse_layout(bon['solutions']),
        'layout_original': '',  # not needed by frontend?
        'answer': ''.join([w['word'] for w in bon['solutions']]),
    }


with open('testdata/tca/0709.json', 'r') as f:
    details = json.load(f)

# print(details['puzzleDetails'])

print(json.dumps(parse_response(details), indent=2))