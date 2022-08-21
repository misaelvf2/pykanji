class Kanji:
    def __init__(self, literal="", meanings=[], onyomi=[], kunyomi=[], misc={}):
        self.literal = literal
        self.meanings = meanings
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.misc = misc

    def __str__(self):
        return (
            f"<{self.literal}>\n"
            f"meanings={self.meanings}\n"
            f"onyomi={self.onyomi}\n"
            f"kunyomi={self.kunyomi}\n"
            f"misc={self.misc}"
        )
