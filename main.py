import click

from views import Application


@click.command()
@click.option('--debug', '-d', help='Debug SQL in console', is_flag=True, default=False)
def main(debug):
    app = Application(debug)
    app.run()


if __name__ == '__main__':
    main()
