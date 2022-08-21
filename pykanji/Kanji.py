from collections import namedtuple


class Kanji:
    def __init__(self, literal="", meanings=[], onyomi=[], kunyomi=[], misc={}):
        self._literal = literal
        self._meanings = meanings
        self._onyomi = onyomi
        self._kunyomi = kunyomi
        self._misc = misc

    @property
    def literal(self):
        return self._literal

    @property
    def meanings(self):
        return self._meanings

    @property
    def readings(self):
        Readings = namedtuple("Readings", ["onyomi", "kunyomi"])
        return Readings(self.onyomi, self.kunyomi)

    @property
    def onyomi(self):
        return self._onyomi

    @property
    def kunyomi(self):
        return self._kunyomi

    @property
    def misc(self):
        return self._misc

    def __str__(self):
        return (
            f"<{self.literal}>\n"
            f"meanings={self.meanings}\n"
            f"onyomi={self.onyomi}\n"
            f"kunyomi={self.kunyomi}\n"
            f"misc={self.misc}"
        )
