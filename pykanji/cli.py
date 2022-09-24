import click
from rich.console import Console
from rich.table import Table

from pykanji import crud
from pykanji.database import SessionLocal

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
@click.argument("literal")
def kanji(literal, db=get_db()):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Literal")
    table.add_column("Grade")
    table.add_column("Stroke Count")
    table.add_column("JLPT")
    table.add_column("Frequency")
    table.add_column("Meanings")
    table.add_column("Readings")
    table.add_column("Nanori")

    result = crud.read_kanji(db=db, literal=literal)
    if result is None:
        click.echo("Kanji not found!")
    else:
        table.add_row(
            f"{result.literal}",
            f"{result.grade}",
            f"{result.stroke_count}",
            f"{result.jlpt}",
            f"{result.frequency}",
            f"{', '.join([r.meaning for r in result.meanings])}",
            f"{', '.join([r.reading for r in result.readings])}",
            f"{', '.join([r.nanori for r in result.nanori])}",
        )
        console.print(table)


@click.command()
@click.argument("english_keyword")
def meaning(english_keyword, db=get_db()):
    table = Table(show_header=True, header_style="bold magenta")
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
    table = Table(show_header=True, header_style="bold magenta")
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
