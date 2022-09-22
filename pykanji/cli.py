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
@click.option("-l", "--literal", required=True, help="The Kanji to look up.")
def kanji(literal, db=get_db()):
    result = crud.read_kanji(db=db, literal=literal)
    if result is None:
        click.echo("Kanji not found!")
    else:
        click.echo(result)


if __name__ == "__main__":
    cli.add_command(kanji)
    cli()
