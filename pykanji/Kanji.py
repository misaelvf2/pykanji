class Kanji:
    def __init__(self, literal="", meanings=[], onyomi=[], kunyomi=[], misc={}):
        self.literal = literal
        self.meanings = meanings
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.misc = misc

    def __str__(self):
        return f"<{self.literal}>\n meanings={self.meanings}\n onyomi={self.onyomi}\n kunyomi={self.kunyomi}\n misc={self.misc}"
