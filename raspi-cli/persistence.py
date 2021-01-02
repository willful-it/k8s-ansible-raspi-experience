import os
from pathlib import Path

import peewee


class Host(peewee.Model):
    ip = peewee.CharField()
    mac = peewee.CharField()
    hostname = peewee.CharField()
    role = peewee.CharField()


class Token(peewee.Model):
    value = peewee.CharField()
    available = peewee.BooleanField()


class PersistenceService:
    def __init__(self, filename='inventory.db', create_db=True,  db=None):

        self.__filename = filename

        self.__database = peewee.SqliteDatabase(filename)

        models = [Host, Token]
        self.__database.bind(models)
        self.__database.create_tables(models)

    def get_host_by_mac(self, mac: str) -> Host:
        """Returns a host by its mac address

        Args:
            mac (str): The mac address to search for

        Returns:
            Host: The host if found, None otherwise
        """

        return Host.get(mac=mac)

    def create_host(self, mac: str, ip: str,
                    hostname: str, role: str = None) -> Host:
        """Creates an host

        Args:
            mac (str): The host mac address
            ip (str): The host ipv4 address
            hostname (str): The host name
            role (str, optional): The role of the host. Defaults to None.

        Returns:
            Host: The created host
        """

        return Host.create(ip=ip, mac=mac, hostname=hostname, role=role)

    def create_token(self, value: str) -> Token:
        return Token.create(value=value, available=True)

    def count_tokens(self, available=True) -> Token:
        return Token.select().where(Token.available).count()

    def get_available_tokens(self):
        return Token.select().where(Token.available)

    def use_token(self, id: int):
        token = Token.get_by_id(id)
        token.available = False
        token.save()

    def delete_database(self):
        for path in Path().rglob(self.__filename):
            os.remove(path)
