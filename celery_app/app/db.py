from contextlib import contextmanager

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor


pool = ThreadedConnectionPool(1, 4,
                              dbname="geopython-db",
                              user="geopython",
                              host="postgis",
                              port="5432",
                              password="geopython")


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()
