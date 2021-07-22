from contextlib import contextmanager
from typing import List
from typing import Tuple

import psycopg2

from sqlalchemy import create_engine
from sqlalchemy import text

_database_name = "postgres"
_host = "db"
_port = 5432
_user = "postgres"
_password = None


@contextmanager
def generate_connection(database_name=_database_name, host=_host, port=_port, user=_user, password=_password):
    connection_string = f"dbname={database_name} user={user} password={password} host={host} port={port}"
    connection = None
    try:
        connection = psycopg2.connect(connection_string)
        yield connection
    finally:
        if connection:
            connection.close()


def retrieve_engine(database_name=_database_name, host=_host, port=_port, user=_user, password=_password):
    connection_string = (
        f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        if password
        else f"postgresql://{user}@{host}:{port}/{database_name}"
    )
    return create_engine(connection_string)


def execute_query(raw_query: str, engine=None, connection=None, data=None) -> List[Tuple]:
    def execute(custom_connection, query):
        if data:
            return list(custom_connection.execute(query, data))
        return list(custom_connection.execute(query))

    query_statement = text(raw_query)

    if connection:
        return execute(connection, query_statement)
    else:
        provided_engine = engine is not None
        engine = engine if provided_engine else retrieve_engine()

        try:
            with engine.connect() as connection:
                return execute(connection, query_statement)
        finally:
            if not provided_engine:
                engine.dispose()
