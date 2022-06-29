import click

from controllers import Database
from views import Application

@click.command()
@click.option('--debug', '-d', help='Debug SQL in console', is_flag=True, default=False)
def main(debug):
    # database = Database(debug)
    
    # database.add_category('Social media')
    # database.add_category('Work emails')

    # database.add_account(login='rafkow91', password='12345', website='poczta.onet.pl', category='emails')

    # print(database.get_category_by_name('%Emails'))
    # print(database.get_category_by_name('%emails%'))

    app = Application(debug)
    app.run()

if __name__ == '__main__':
    main()