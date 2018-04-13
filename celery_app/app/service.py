import math
import psycopg2

from app.db import get_db_cursor


class ServiceError(Exception):
    """Custom exception for service errors"""
    pass


def geoprocess(x, y):
    """
    Implementation code for celery task
    :param x: x value for task
    :param y: y value for task
    """

    with get_db_cursor() as cur:

        # check for intersection
        query = f"""SELECT gu_a3
             from uk_boundary
             WHERE ST_Intersects(geom, ST_GeomFromEWKT('SRID=27700;POINT({x} {y})'));
             """
        cur.execute(query)

        # determine style code to use
        rows = cur.fetchall()
        if rows:
            style = rows[0][0]
        else:
            style = 'SEA'

        # get ref code
        ref = get_ref(x, y)

        # make object for db and insert it. Insert exceptions will raise to task.
        size = 1000
        xmin = int(x / size) * size
        xmax = xmin + size
        ymin = int(y / size) * size
        ymax = ymin + size
        string_for_db = f"ST_GeometryFromText('POLYGON(({xmin} {ymin},{xmax} {ymin},{xmax} {ymax},{xmin} {ymax},{xmin} {ymin}))',27700)"
        cur.execute(f"INSERT INTO grid_squares (grid_ref, style_cat, geom) VALUES('{ref}', '{style}', {string_for_db})")


def get_ref(e, n):
    # Derived from
    # http://www.movable-type.co.uk/scripts/latlong-gridref.html
    gridChars = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    e100k = math.floor(e / 100000)
    n100k = math.floor(n / 100000)
    l1 = (19 - n100k) - (19 - n100k) % 5 + math.floor((e100k + 10) / 5)
    l2 = (19 - n100k) * 5 % 25 + e100k % 5
    letPair = gridChars[int(l1)] + gridChars[int(l2)]
    e100m = math.trunc(round(float(e) / 100))
    egr = str(e100m).rjust(4, "0")[1:]
    if n >= 1000000:
        n = n - 1000000
    n100m = math.trunc(round(float(n) / 100))
    ngr = str(n100m).rjust(4, "0")[1:]
    return letPair + egr + ngr
