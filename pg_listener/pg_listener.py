import logging
import select

import psycopg2
from psycopg2._psycopg import connection
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logger = logging.getLogger(__name__)


def conn_from_django(django_connection):
    db_settings = django_connection.settings_dict
    dsn = f"dbname='{db_settings['NAME']}' " \
          f"user='{db_settings['USER']}' " \
          f"host='{db_settings['HOST']}' " \
          f"password='{db_settings['PASSWORD']}'"

    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return conn


def on_db_event(conn: connection, channel: str):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"LISTEN {channel};")
            logger.info(f"Waiting for notifications on channel '{channel}'.")

            while True:
                if select.select([conn], [], [], 5) != ([], [], []):
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        yield notify.payload
