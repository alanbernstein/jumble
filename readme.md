web
===
- python script retrieves+caches data on daily cron
- same script serves data as cleaned up json
- simple "responsive" page works on mobile


todo:
- interactive
- view previous days


cli
===

just run `python jumble.py`

stores data in ~/.cache/jumble

displays the clues like this:
```
CELUN
o__o_

LEABC
o_o__

DINSIG
oo_o__

TONKYT
o__oo_

He rode the mechanical bull because it was on his...

'____-__' ____
```

enter guesses at the `>` prompt, and an updated list of letters for the final answer is shown.