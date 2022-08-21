import sqlite3
from contextlib import closing

from bs4 import BeautifulSoup

from KanjiDicReader import KanjiDicReader


def get_kanji():
    with open("kanjidic2.xml") as fp:
        soup = BeautifulSoup(fp, "xml")

        my_reader = KanjiDicReader(soup=soup, limit=100)

        my_kanji = my_reader.make_all_kanji()
    return my_kanji


def create_tables():
    with closing(sqlite3.connect("kanji.db")) as connection:
        with closing(connection.cursor()) as cursor:
            # Create Kanji table
            cursor.execute(
                "CREATE TABLE Kanji (id INTEGER PRIMARY KEY, Literal TEXT, JLPT INTEGER, Frequency INTEGER)"
            )

            # Create Readings table
            cursor.execute(
                "CREATE TABLE Readings (id INTEGER PRIMARY KEY, Category TEXT, Reading TEXT)"
            )

            cursor.execute(
                "CREATE TABLE KanjiReadings (KanjiID INTEGER, ReadingID INTEGER, FOREIGN KEY(KanjiID) REFERENCES Kanji(id), FOREIGN KEY(ReadingID) REFERENCES Reading(id))"
            )

            # Create Meanings table
            cursor.execute(
                "CREATE TABLE Meanings (id INTEGER PRIMARY KEY, KanjiID INTEGER, MeaningID INTEGER, Category TEXT, Reading TEXT, FOREIGN KEY(KanjiID) REFERENCES Kanji(id), FOREIGN KEY(MeaningID) REFERENCES Readings(id))"
            )


def write_to_db():
    my_kanji = get_kanji()
    with closing(sqlite3.connect("kanji.db")) as connection:
        with closing(connection.cursor()) as cursor:
            for kanji in my_kanji:
                # Insert into Kanji table
                cursor.execute(
                    "INSERT INTO Kanji VALUES (NULL, ?, ?, ?)",
                    (kanji.literal, kanji.misc["jlpt"], kanji.misc["frequency"]),
                )

                # Insert into Readings table
                for reading in kanji.onyomi:
                    cursor.execute(
                        "INSERT INTO Readings VALUES (NULL, ?, ?)", ("onyomi", reading)
                    )
                    cursor.execute(
                        "INSERT INTO KanjiReadings VALUES ((SELECT id FROM Kanji WHERE Literal = ?), (SELECT id FROM Readings WHERE Reading = ?))",
                        (kanji.literal, reading),
                    )

        connection.commit()


def read_from_db():
    with closing(sqlite3.connect("kanji.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM kanji").fetchall()
            print(rows)


if __name__ == "__main__":
    create_tables()
    write_to_db()
