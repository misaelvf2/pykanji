from Kanji import Kanji


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
            "grade": int(misc_elem.grade.string) if misc_elem.grade else 0,
            "stroke_count": int(misc_elem.stroke_count.string),
            "frequency": int(misc_elem.freq.string) if misc_elem.freq else 0,
            "jlpt": int(misc_elem.jlpt.string) if misc_elem.jlpt else 0,
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
