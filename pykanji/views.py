from rich import box
from rich.table import Table

from pykanji.models import Kanji


class BaseView:
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
    ):
        self._options = {
            "title": title,
            "box": box_const,
            "show_header": show_header,
            "show_lines": show_lines,
        }

    @property
    def table(self):
        raise NotImplementedError

    @property
    def options(self):
        return self._options

    @property
    def columns(self):
        raise NotImplementedError


class KanjiLookUp(BaseView):
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
        width=125,
    ):
        super().__init__(title, box_const, show_header, show_lines)

        self._columns = [
            "#",
            "Literal",
            "Grade",
            "Stroke Count",
            "JLPT",
            "Frequency",
            "Meanings",
            "Kun'yomi",
            "On'yomi",
            "Nanori",
        ]

        self._options.update({"width": width})

        self._table = Table(**self._options)

        for column in self._columns:
            self._table.add_column(column)

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

    @property
    def columns(self):
        return self._columns


class MeaningLookUp(BaseView):
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
    ):
        super().__init__(title, box_const, show_header, show_lines)

        self._columns = [
            "#",
            "Literal",
        ]

        self._table = Table(**self._options)

        for column in self._columns:
            self._table.add_column(column)

    def add_kanji(self, row_id, kanji: Kanji):
        self._table.add_row(
            f"{row_id}",
            f"{kanji.literal}",
        )

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        return self._columns


class OnyomiLookUp(BaseView):
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
    ):
        super().__init__(title, box_const, show_header, show_lines)

        self._columns = [
            "#",
            "Literal",
            "On'yomi",
        ]

        self._table = Table(**self._options)

        for column in self._columns:
            self._table.add_column(column)

    def add_kanji(self, row_id, kanji: Kanji):
        self._table.add_row(
            f"{row_id}",
            f"{kanji.literal}",
            f"{', '.join([k.reading for k in kanji.readings if k.category == 'onyomi'])}",
        )

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        return self._columns


class FrequentKanji(BaseView):
    def __init__(
        self,
        title,
        box_const=box.HORIZONTALS,
        show_header=True,
        show_lines=True,
    ):
        super().__init__(title, box_const, show_header, show_lines)

        self._columns = {
            "#",
            "Literal",
            "Frequency",
        }

        self._table = Table(**self._options)

        for column in self._columns:
            self._table.add_column(column)

    def add_kanji(self, row_id, kanji: Kanji):
        self._table.add_row(
            f"{row_id}",
            f"{kanji.literal}",
            f"{kanji.frequency}",
        )

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        return self._columns
