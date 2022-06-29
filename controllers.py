from sqlalchemy import ForeignKey, Identity, create_engine, Table, Column, Integer, String, MetaData, text
from sqlalchemy.orm import declarative_base, relationship, Session, backref
from models import Account, Category


class Database:
    def __init__(self, debug: bool = False) -> None:
        self.engine = create_engine('sqlite:///database.db', echo=debug, future=True)
        self._create_tables()

    @staticmethod
    def _create_tables() -> None:
        meta = MetaData()

        categories = Table(
            'categories', meta,
            Column('id', Integer, primary_key=True),
            Column('name', String)
        )

        accounts = Table(
            'accounts', meta,
            Column('id', Integer, primary_key=True),
            Column('login', String),
            Column('password', String),
            Column('website', String),
            Column('category_id', Integer),
        )

        engine = create_engine('sqlite:///database.db', echo=True, future=True)

        meta.create_all(engine)

    def add_account(self, login: str, password: str, website: str, category_name: str) -> None:
        encrypted_password = password
        category = self.get_category_by_name(category_name)
        if category is None:
            category = Category(name=category_name)

        with Session(self.engine) as session:
            new_account = Account(
                login=login,
                password=password,
                website=website,
                category=category
            )

            session.add(new_account)
            session.commit()

    def add_category(self, name: str) -> None:
        with Session(self.engine) as session:
            new_category = Category(name=name.upper())
            session.add(new_category)
            session.commit()

    def get_all_accounts(self) -> list:
        with self.engine.connect() as connection:
            cursor = connection.execute(text(
                '''
                    SELECT 
                        a.id,
                        a.login,
                        a.website,
                        c.name
                    FROM accounts a
                    LEFT JOIN categories c
                    ON a.category_id = c.id
                '''))
            accounts = cursor.fetchall()
        return accounts

    def get_account(self, login: str, password: str, website: str, category_name: str, account_id: int = None) -> Account:
        pass

    def get_category_by_name(self, category_name: str) -> list:
        with Session(self.engine) as session:
            categories = session.query(Category).filter(Category.name.like(f'%{category_name}%')).all()
            
            to_return = []
            for category in categories:
                to_return.append(category.id)

        return to_return

    def get_account_by_website(self, website_name: str) -> list:
        with Session(self.engine) as session:
            websites = session.query(Account).filter(Account.website.like(f'%{website_name}%')).all()
            
            to_return = []
            for website in websites:
                to_return.append(website.id)

        return to_return
