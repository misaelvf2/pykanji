-- SQLite
SELECT Kanji.Literal, Readings.Reading FROM Kanji INNER JOIN KanjiReadings ON Kanji.id=KanjiReadings.KanjiID INNER JOIN Readings ON Readings.id=KanjiReadings.ReadingID;