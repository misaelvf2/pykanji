from bs4 import BeautifulSoup


class KanjiDicReader:
    def __init__(self, soup, limit=None):
        self.soup = soup
        self.characters = self._find_characters(limit=limit)

    def _find_characters(self, limit):
        first_character = self._find_first_character()
        characters = [first_character]
        if limit is None:
            rest_of_characters = first_character.find_next_siblings(
                "character", limit=None
            )
            characters.extend(rest_of_characters)
        elif limit > 1:
            rest_of_characters = first_character.find_next_siblings(
                "character", limit=limit - 1
            )
            characters.extend(rest_of_characters)
        return characters

    def _find_first_character(self):
        return self.soup.find("character")

    def find_literal(self, character):
        return character.literal.string

    def find_onyomi(self, character):
        readings = character.reading_meaning.rmgroup
        return list(map(lambda x: x.string, readings.find_all(r_type="ja_on")))

    def find_kunyomi(self, character):
        readings = character.reading_meaning.rmgroup
        return list(map(lambda x: x.string, readings.find_all(r_type="ja_kun")))

    def make_all_kanji(self):
        kanji = []
        for character in self.characters:
            kanji.append(self.make_kanji(character))
        return kanji

    def make_kanji(self, character):
        return Kanji(
            literal=self.find_literal(character),
            onyomi=self.find_onyomi(character),
            kunyomi=self.find_kunyomi(character),
        )


class Kanji:
    def __init__(self, literal="", onyomi=[], kunyomi=[]):
        self.literal = literal
        self.onyomi = onyomi
        self.kunyomi = kunyomi

    def __str__(self):
        return f"<{self.literal}>\n onyomi={self.onyomi}\n kunyomi={self.kunyomi}"


with open("kanjidic2.xml") as fp:
    soup = BeautifulSoup(fp, "xml")

    my_reader = KanjiDicReader(soup=soup, limit=5)

    my_kanji = my_reader.make_all_kanji()

    for kanji in my_kanji:
        print(kanji)
