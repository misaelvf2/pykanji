import click
from rich import box
from rich.console import Console
from rich.table import Table

from pykanji import crud
from pykanji.database import SessionLocal
from views import KanjiView

console = Console()


# Dependency
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
@click.argument("literals", nargs=-1)
def kanji(literals, db=get_db()):
    # table = Table(
    #     title="Kanji Information",
    #     box=box.HORIZONTALS,
    #     show_header=True,
    #     show_lines=True,
    #     width=125,
    # )
    # table.add_column("#")
    # table.add_column("Literal")
    # table.add_column("Grade")
    # table.add_column("Stroke Count")
    # table.add_column("JLPT")
    # table.add_column("Frequency")
    # table.add_column("Meanings")
    # table.add_column("Kun'yomi")
    # table.add_column("On'yomi")
    # table.add_column("Nanori")

    view = KanjiView(title="Kanji Information")

    result = crud.read_multiple_kanji(db=db, literals=[literal for literal in literals])
    if result is None:
        click.echo("No Kanji found!")
    else:
        for i, kanji in enumerate(result):
            view.add_kanji(i, kanji)
            # table.add_row(
            #     f"{i}",
            #     f"{kanji.literal}",
            #     f"{kanji.grade}",
            #     f"{kanji.stroke_count}",
            #     f"{kanji.jlpt}",
            #     f"{kanji.frequency}",
            #     f"{', '.join([k.meaning for k in kanji.meanings])}",
            #     f"{', '.join([k.reading for k in kanji.readings if k.category == 'kunyomi'])}",
            #     f"{', '.join([k.reading for k in kanji.readings if k.category == 'onyomi'])}",
            #     f"{', '.join([k.nanori for k in kanji.nanori])}",
            # )
        console.print(view.table)


@click.command()
@click.argument("english_keyword")
def meaning(english_keyword, db=get_db()):
    table = Table(show_header=True)
    table.add_column("#")
    table.add_column("Literal")

    result = crud.read_all_kanji(db=db, meaning=[english_keyword])
    if result is None:
        click.echo("No matching Kanji found!")
    else:
        for i, kanji in enumerate(result):
            table.add_row(f"{i}", f"{kanji.literal}")
        console.print(table)


@click.command()
@click.argument("n")
@click.option("-d", "--descending", is_flag=True, help="Return in descending order.")
def frequent(n, descending, db=get_db()):
    table = Table(
        title=f"{n} {'Least' if descending else 'Most'} Frequent Kanji",
        show_header=True,
        box=box.SIMPLE,
        highlight=True,
    )
    table.add_column("#")
    table.add_column("Literal")
    table.add_column("Frequency")

    result = crud.read_most_frequent_kanji(db=db, n=n, descending=descending)
    if result is None:
        click.echo("None found!")
    else:
        for i, kanji in enumerate(result):
            table.add_row(f"{i}", f"{kanji.literal}", f"{kanji.frequency}")
        console.print(table)


if __name__ == "__main__":
    cli.add_command(kanji)
    cli.add_command(meaning)
    cli.add_command(frequent)
    cli()
