import click
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from models import Kanji, Reading


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "-l", "--literal", required=True, multiple=True, help="The Kanji to look up."
)
def kanji(literal):
    engine = create_engine("sqlite+pysqlite:///../kanji.db", echo=False, future=True)
    stmt = select(Kanji).where(Kanji.literal.in_(literal))
    with Session(engine) as session:
        for row in session.scalars(stmt):
            click.echo(f"{row!r}")


@click.command()
@click.option(
    "-n",
    "--count",
    default=1,
    show_default=True,
    help="Number of most common readings to look up.",
)
def most_common_readings(count):
    engine = create_engine("sqlite+pysqlite:///../kanji.db", echo=False, future=True)
    stmt = (
        select(Reading.reading, func.count(Reading.reading).label("count"))
        .where(Reading.category == "onyomi")
        .order_by(func.count(Reading.reading).desc())
        .group_by(Reading.reading)
        .limit(count)
    )
    with Session(engine) as session:
        for row in session.execute(stmt):
            click.echo(f"Reading: {row[0]}, Frequency: {row[1]}")


if __name__ == "__main__":
    cli.add_command(kanji)
    cli.add_command(most_common_readings)
    cli()
