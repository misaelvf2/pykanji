import click
from rich.console import Console

from initdb import create_tables, store_kanji
from pykanji import crud
from pykanji.database import SessionLocal
from views import FrequentKanji, KanjiLookUp, MeaningLookUp

console = Console()


# Get database connection via dependency injection
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "-l",
    "--limit",
    type=int,
    help="Limit the number of Kanji to read from the KanjiDic.",
)
def initdb(limit: int = None):
    create_tables()
    store_kanji(limit=limit)


@click.command()
@click.argument("literals", nargs=-1)
def kanji(literals, db=get_db()):
    view = KanjiLookUp(title="Kanji Information")

    result = crud.read_multiple_kanji(db=db, literals=[literal for literal in literals])
    if result is None:
        click.echo("No Kanji found!")
    else:
        for i, kanji in enumerate(result):
            view.add_kanji(i, kanji)
        console.print(view.table)


@click.command()
@click.argument("english_keyword")
def meaning(english_keyword, db=get_db()):
    view = MeaningLookUp(title=f"Results for {english_keyword}")

    result = crud.read_all_kanji(db=db, meaning=[english_keyword])
    if result is None:
        click.echo("No matching Kanji found!")
    else:
        for i, kanji in enumerate(result):
            view.add_kanji(i, kanji)
        console.print(view.table)


@click.command()
@click.argument("n")
@click.option("-d", "--descending", is_flag=True, help="Return in descending order.")
def frequent(n, descending, db=get_db()):
    view = FrequentKanji(
        title=f"{n} {'Least' if descending else 'Most'} Frequent Kanji"
    )

    result = crud.read_most_frequent_kanji(db=db, n=n, descending=descending)
    if result is None:
        click.echo("None found!")
    else:
        for i, kanji in enumerate(result):
            view.add_kanji(i, kanji)
        console.print(view.table)


if __name__ == "__main__":
    cli.add_command(initdb)
    cli.add_command(kanji)
    cli.add_command(meaning)
    cli.add_command(frequent)
    cli()
