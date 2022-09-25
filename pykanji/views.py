from rich import box
from rich.table import Table

from models import Kanji


class KanjiLookUp:
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
        width=125,
    ):
        self._columns = {
            "title": title,
            "box": box_const,
            "show_header": show_header,
            "show_lines": show_lines,
            "width": width,
        }

        self._table = Table(**self._columns)
        self._table.add_column("#")
        self._table.add_column("Literal")
        self._table.add_column("Grade")
        self._table.add_column("Stroke Count")
        self._table.add_column("JLPT")
        self._table.add_column("Frequency")
        self._table.add_column("Meanings")
        self._table.add_column("Kun'yomi")
        self._table.add_column("On'yomi")
        self._table.add_column("Nanori")

    def add_kanji(self, row_id, kanji: Kanji):
        self._table.add_row(
            f"{row_id}",
            f"{kanji.literal}",
            f"{kanji.grade}",
            f"{kanji.stroke_count}",
            f"{kanji.jlpt}",
            f"{', '.join([k.meaning for k in kanji.meanings])}",
            f"{', '.join([k.reading for k in kanji.readings if k.category == 'kunyomi'])}",
            f"{', '.join([k.reading for k in kanji.readings if k.category == 'onyomi'])}",
            f"{', '.join([k.nanori for k in kanji.nanori])}",
        )

    @property
    def table(self):
        return self._table


class MeaningLookUp:
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
    ):
        self._columns = {
            "title": title,
            "box": box_const,
            "show_header": show_header,
            "show_lines": show_lines,
        }

        self._table = Table(**self._columns)
        self._table.add_column("#")
        self._table.add_column("Literal")

    def add_kanji(self, row_id, kanji: Kanji):
        self._table.add_row(
            f"{row_id}",
            f"{kanji.literal}",
        )

    @property
    def table(self):
        return self._table


class FrequentKanji:
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
    ):
        self._columns = {
            "title": title,
            "box": box_const,
            "show_header": show_header,
            "show_lines": show_lines,
        }

        self._table = Table(**self._columns)
        self._table.add_column("#")
        self._table.add_column("Literal")
        self._table.add_column("Frequency")

    def add_kanji(self, row_id, kanji: Kanji):
        self._table.add_row(
            f"{row_id}",
            f"{kanji.literal}",
            f"{kanji.frequency}",
        )

    @property
    def table(self):
        return self._table
