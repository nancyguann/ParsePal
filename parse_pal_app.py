"""
Nancy Guan
DS3500
Homework 7: Natural Language Processing
5 December 2025
parse_pal_app.py
"""
FDR = 'fdr_speech.txt'
HITLER = 'hitler_speech.txt'
BUSH = 'bush_speech.txt'
REAGAN = 'reagan_speech.txt'
CHURCHILL = 'churchill_speech.txt'
PUTIN = 'putin_speech.txt'
HUSSEIN = 'hussein_speech.txt'
MUSSOLINI = 'mussolini_speech.txt'
STOP_WORDS = 'stop_words.txt'

from parse_pal_parsers import default_parser, propaganda_parser
from parse_pal import ParsePal

def main():
    p = ParsePal()
    p.load_stop_words(STOP_WORDS)

    p.load_text(FDR, 'FDR: Day of Infamy', parser=default_parser)
    p.load_text(BUSH, 'Bush: Axis of Evil', parser=default_parser)
    p.load_text(REAGAN, 'Reagan: Evil Empire', parser=default_parser)
    p.load_text(CHURCHILL, 'Churchill: We Shall Fight on the Beaches', parser=default_parser)
    p.load_text(HITLER, 'Hitler: Invasion of Poland', parser=propaganda_parser)
    p.load_text(MUSSOLINI, 'Mussolini: Rome 1941', parser=propaganda_parser)
    p.load_text(PUTIN, 'Putin: Invasion of Ukraine', parser=propaganda_parser)
    p.load_text(HUSSEIN, 'Hussein: Invasion of Kuwait', parser=propaganda_parser)

    p.wordcount_sankey(k=10)
    p.subplot()
    p.comparative_overlay()

if __name__ == '__main__':
    main()