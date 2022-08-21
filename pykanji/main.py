from bs4 import BeautifulSoup


class KanjiDicReader:
    def __init__(self, soup, limit=None):
        self.soup = soup
        self.characters = self._find_characters(limit=limit)

    def _get(self, parent, element, default=None):
        return parent.element if parent else default

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

    def find_meanings(self, character):
        if not character.reading_meaning:
            return []
        meanings = character.reading_meaning.rmgroup
        return list(
            map(
                lambda x: x.string,
                meanings.find_all("meaning", m_lang=False, recursive=False),
            )
        )

    def find_onyomi(self, character):
        if not character.reading_meaning:
            return []
        readings = character.reading_meaning.rmgroup
        return list(
            map(lambda x: x.string, readings.find_all(r_type="ja_on", recursive=False))
        )

    def find_kunyomi(self, character):
        if not character.reading_meaning:
            return []
        readings = character.reading_meaning.rmgroup
        return list(
            map(lambda x: x.string, readings.find_all(r_type="ja_kun", recursive=False))
        )

    def find_misc(self, character):
        misc_elem = character.misc
        misc = {
            "grade": misc_elem.grade.string if misc_elem.grade else None,
            "stroke_count": misc_elem.stroke_count.string,
            "frequency": misc_elem.freq.string if misc_elem.freq else None,
            "jlpt": misc_elem.jlpt.string if misc_elem.jlpt else None,
        }
        return misc

    def make_all_kanji(self):
        kanji = []
        for character in self.characters:
            kanji.append(self.make_kanji(character))
        return kanji

    def make_kanji(self, character):
        try:
            return Kanji(
                literal=self.find_literal(character),
                meanings=self.find_meanings(character),
                onyomi=self.find_onyomi(character),
                kunyomi=self.find_kunyomi(character),
                misc=self.find_misc(character),
            )
        except AttributeError:
            print(f"Failed on {character.literal.string}")


class Kanji:
    def __init__(self, literal="", meanings=[], onyomi=[], kunyomi=[], misc={}):
        self.literal = literal
        self.meanings = meanings
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.misc = misc

    def __str__(self):
        return f"<{self.literal}>\n meanings={self.meanings}\n onyomi={self.onyomi}\n kunyomi={self.kunyomi}\n misc={self.misc}"


with open("kanjidic2.xml") as fp:
    soup = BeautifulSoup(fp, "xml")

    my_reader = KanjiDicReader(soup=soup, limit=None)

    my_kanji = my_reader.make_all_kanji()

    for kanji in my_kanji:
        print(kanji)
