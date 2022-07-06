from base64 import urlsafe_b64encode
from random import sample
from string import ascii_letters

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import dotenv_values
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import Session

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

    def add_account(self, login: str, password: str, website: str, category_name: str) -> bool:
        accounts = self.search_in_website_name(website)
        accounts_list = [account.login for account in accounts]

        if login in accounts_list:
            return False

        encrypted_password = PasswordEncryptor(password)

        try:
            category = self.get_category_by_name(category_name)[0]
        except IndexError:
            category = Category(name=category_name.lower())

        with Session(self.engine) as session:
            new_account = Account(
                login=login,
                password=encrypted_password.encrypt(),
                website=website,
                category=category
            )

            session.add(new_account)
            session.commit()

        return True

    def add_category(self, name: str) -> None:
        with Session(self.engine) as session:
            existed_categories = session.query(Category).all()
            categories = [category.name for category in existed_categories]

            if name.lower() not in categories:
                new_category = Category(name=name.lower())
                session.add(new_category)
                session.commit()
                return True
        
        return False

    def get_all_accounts(self) -> list:
        with Session(self.engine) as session:
            accounts = session.query(Account).all()

        return accounts

    def get_password(self, account_id: int) -> str:
        with Session(self.engine) as session:
            account = session.query(Account).filter(Account.id == account_id).first()
        password_encryptor = PasswordEncryptor(account.password)
        return password_encryptor.decrypt()

    def get_all_categories(self) -> list:
        with Session(self.engine) as session:
            return session.query(Category).all()

    def get_category_id_by_name(self, category_name: str) -> list:
        with Session(self.engine) as session:
            categories = session.query(Category).filter(
                Category.name.like(f'%{category_name}%')).all()

            to_return = []
            for category in categories:
                to_return.append(category.id)

        return to_return

    def get_category_by_name(self, category_name: str) -> Category:
        with Session(self.engine) as session:
            categories = session.query(Category).filter(
                Category.name.like(f'%{category_name}%')).all()

        return categories

    def search_in_website_name(self, website_name: str) -> list:
        with Session(self.engine) as session:
            return session.query(Account).filter(Account.website.like(f'%{website_name}%')).all()

    def search_in_username(self, username: str) -> list:
        with Session(self.engine) as session:
            return session.query(Account).filter(Account.login.like(f'%{username}%')).all()

    def search_in_category_name(self, category_name: str) -> list:
        category_ids = self.get_category_id_by_name(category_name)

        to_return = []

        for category_id in category_ids:
            with Session(self.engine) as session:
                accounts = session.query(Account).filter(Account.category_id == category_id).all()
            for account in accounts:
                to_return.append(account)
        return to_return


class PasswordEncryptor:
    def __init__(self, password) -> None:
        self.password = password
        self.fernet = self._generate_fernet()

    @staticmethod
    def _get_data_from_env(data: str) -> str:
        while True:
            try:
                my_data = dotenv_values()[data]
                break
            except KeyError:
                with open('.env', mode='a', encoding='utf-8') as settings:
                    settings.write(f'{data}="{"".join(sample(ascii_letters, k=10))}"\n')

        return my_data

    def _generate_fernet(self) -> bytes:
        salt = self._get_data_from_env('salt')
        password = self._get_data_from_env('password')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512,
            length=32,
            salt=salt.encode('utf-8'),
            iterations=390000
        )

        return Fernet(urlsafe_b64encode(kdf.derive(password.encode('utf-8'))))

    def encrypt(self):
        return self.fernet.encrypt(self.password.encode('utf-8'))

    def decrypt(self):
        return self.fernet.decrypt(self.password)
