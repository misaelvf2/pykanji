from bs4 import BeautifulSoup

from KanjiDicReader import KanjiDicReader

with open("kanjidic2.xml") as fp:
    soup = BeautifulSoup(fp, "xml")

    my_reader = KanjiDicReader(soup=soup, limit=None)

    my_kanji = my_reader.make_all_kanji()

    for kanji in my_kanji:
        print(kanji)
