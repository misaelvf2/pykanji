from models import Kanji, Meaning, Nanori, Reading


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
        return [
            x.string
            for x in meanings.find_all("meaning", m_lang=False, recursive=False)
        ]

    def find_readings(self, character):
        result = self.find_onyomi(character)
        result.extend(self.find_kunyomi(character))
        return result

    def find_onyomi(self, character):
        if not character.reading_meaning:
            return []
        readings = character.reading_meaning.rmgroup
        return [
            (x.string, "onyomi")
            for x in readings.find_all(r_type="ja_on", recursive=False)
        ]

    def find_kunyomi(self, character):
        if not character.reading_meaning:
            return []
        readings = character.reading_meaning.rmgroup
        return [
            (x.string, "kunyomi")
            for x in readings.find_all(r_type="ja_kun", recursive=False)
        ]

    def find_misc(self, character):
        misc_elem = character.misc
        misc = {
            "grade": int(misc_elem.grade.string) if misc_elem.grade else 0,
            "stroke_count": int(misc_elem.stroke_count.string),
            "frequency": int(misc_elem.freq.string) if misc_elem.freq else 0,
            "jlpt": int(misc_elem.jlpt.string) if misc_elem.jlpt else 0,
        }
        return misc

    def find_grade(self, character):
        misc_elem = character.misc
        return int(misc_elem.grade.string) if misc_elem.grade else 0

    def find_stroke_count(self, character):
        misc_elem = character.misc
        return int(misc_elem.stroke_count.string) if misc_elem.stroke_count else 0

    def find_jlpt(self, character):
        misc_elem = character.misc
        return int(misc_elem.jlpt.string) if misc_elem.jlpt else 0

    def find_frequency(self, character):
        misc_elem = character.misc
        return int(misc_elem.freq.string) if misc_elem.freq else 0

    def find_nanori(self, character):
        if not character.reading_meaning:
            return []
        if not character.reading_meaning.nanori:
            return []
        reading_meaning = character.reading_meaning
        return [x.string for x in reading_meaning.find_all("nanori", recursive=False)]

    def make_all_kanji(self):
        for character in self.characters:
            yield self.make_kanji(character)

    def make_kanji(self, character):
        try:
            return Kanji(
                literal=self.find_literal(character),
                grade=self.find_grade(character),
                stroke_count=self.find_stroke_count(character),
                jlpt=self.find_jlpt(character),
                frequency=self.find_frequency(character),
                meanings=[
                    Meaning(meaning=meaning)
                    for meaning in self.find_meanings(character)
                ],
                readings=[
                    Reading(category=category, reading=reading)
                    for reading, category in self.find_readings(character)
                ],
                nanori=[
                    Nanori(nanori=nanori) for nanori in self.find_nanori(character)
                ],
            )
        except AttributeError:
            print(f"Failed on {character.literal.string}")
