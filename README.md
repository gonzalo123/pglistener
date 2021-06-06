## Listen to PostgreSQL events with pg_notify and Python

With PostgreSQL we can easily publish and listen events from one connection to another. It's cool because those
notifications belong on a transaction. In this example I'm going to create a wrapper to help me to listen the events
with Python.

To notify events I only need to use pg_notify function. For example:

```postgresql
select pg_notify('channel', 'xxx')
```

To listen the events

```python
import psycopg2

from pg_listener import on_db_event

dsn = f"dbname='gonzalo123' user='username' host='localhost' password='password'"

conn = psycopg2.connect(dsn)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

for payload in on_db_event(conn, 'channel'):
    print(payload)
```

The magic resides in on_db_event. We need to pass a psycopg2 connection and the channel name. We can iterate over the function and retrieve the payload when someone triggers the event on that channel

```python
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
```

As I often use django and django uses one connection wrapper I need to create a native psycopg2 connection. Maybe it's possible to retrieve it from django connection (show me if you know how to do it).

```python
def conn_from_django(django_connection):
    db_settings = django_connection.settings_dict
    dsn = f"dbname='{db_settings['NAME']}' " \
          f"user='{db_settings['USER']}' " \
          f"host='{db_settings['HOST']}' " \
          f"password='{db_settings['PASSWORD']}'"

    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return conn
```

You can install the library using pip

```commandline
pip install pglistener-gonzalo123
```
