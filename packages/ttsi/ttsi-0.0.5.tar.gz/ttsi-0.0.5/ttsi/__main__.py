import sys
import click

from ttsi.app import app, db


@click.group()
@click.version_option("1.0.0")
def main():
    """A TTSI CLI"""
    print("Welcome to ttsi CLI")
    pass


@main.command()
@click.argument('run', required=False)
def run(**kwargs):
    """Run application
    """
    app.run()

    pass


@main.command()
@click.argument('run', required=False)
def init(**kwargs):
    """Run application
    """
    db.create_all()

    pass


if __name__ == '__main__':
    args = sys.argv
    main()
