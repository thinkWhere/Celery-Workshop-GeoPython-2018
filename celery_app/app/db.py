from contextlib import contextmanager

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor


pool = None

def create_connection_pool():
    """Create a connection pool for the worker"""
    pool = ThreadedConnectionPool(1, 4,
                                  dbname="geopython-db",
                                  user="geopython",
                                  host="postgis",
                                  port="5432",
                                  password="geopython")
    return pool

@contextmanager
def get_db_connection():
    try:
        # Setup connection pool is it doesn't exist
        global pool
        if pool is None:
            pool = create_connection_pool()

        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor():
    with get_db_connection() as connection:
      cursor = connection.cursor()
      try:
          yield cursor
          connection.commit()
      finally:
          cursor.close()
