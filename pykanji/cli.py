import click

from pykanji import crud
from pykanji.database import SessionLocal


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
    result = crud.read_kanji(db=db, literal=literal)
    if result is None:
        click.echo("Kanji not found!")
    else:
        click.echo(result)


@click.command()
@click.argument("english_keyword")
def meaning(english_keyword, db=get_db()):
    result = crud.read_all_kanji(db=db, meaning=[english_keyword])
    if result is None:
        click.echo("No matching Kanji found!")
    else:
        for i, kanji in enumerate(result):
            click.echo(f"{i} - {kanji.literal}")


@click.command()
@click.argument("n")
@click.option("-d", "--descending", is_flag=True, help="Return in descending order.")
def frequent(n, descending, db=get_db()):
    result = crud.read_most_frequent_kanji(db=db, n=n, descending=descending)
    if result is None:
        click.echo("None found!")
    else:
        for i, kanji in enumerate(result):
            click.echo(f"{i} - {kanji.literal} - {kanji.frequency}")


if __name__ == "__main__":
    cli.add_command(kanji)
    cli.add_command(meaning)
    cli.add_command(frequent)
    cli()
