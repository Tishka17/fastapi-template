from .protocols.database import DatabaseGateway


def generate(database: DatabaseGateway) -> int:
    return database.get_int() ** 2
