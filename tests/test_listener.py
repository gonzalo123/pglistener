from pg_listener import on_db_event


def test_listener(conn):
    for payload in on_db_event(conn, 'channel'):
        assert 'xxx' == payload
