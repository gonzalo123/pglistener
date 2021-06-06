import os

import psycopg2
import pytest


DSN = f"dbname='{os.getenv('POSTGRES_DB')}' " \
      f"user='{os.getenv('POSTGRES_USER')}' " \
      f"host='{os.getenv('POSTGRES_HOST')}' " \
      f"password='{os.getenv('POSTGRES_PASSWORD')}'"


@pytest.fixture()
def conn():
    conn = psycopg2.connect(DSN)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    yield conn
