import math

import psycopg2


class ServiceError(Exception):
    """Custom exception for service errors"""
    pass


def do_task(x, y):
    """
    :param x:
    :param y:
    :return:
    """
    # TODO: update docstring
    # TODO: connection pooling?
    with psycopg2.connect(dbname="geopython-db", user="geopython", host="postgis", port="5432", password="geopython") as conn:
        with conn.cursor() as cur:
            # find out if point intersects uk.  If not throw exception
            query = f"""SELECT gu_a3
                 from uk_boundary
                 WHERE ST_Intersects(geom, ST_GeometryFromText('SRID=27700;POINT({x} {y})'));
                 """
            cur.execute(query)

            rows = cur.fetchall()

            if rows:
                style = rows[0][0]
            else:
                style = 'SEA'

            # get os grid ref
            bng_grid_ref = get_os_grid_reference(x, y)

            # makegrid square
            size = 1000
            xmin = int(x / size) * size
            xmax = xmin + size
            ymin = int(y / size) * size
            ymax = ymin + size

            string_for_polygon = f"ST_GeometryFromText('POLYGON(({xmin} {ymin},{xmax} {ymin},{xmax} {ymax},{xmin} {ymax},{xmin} {ymin}))',27700)"

            # insert to db.  Insert exceptions will raise to task
            # TODO make grid ref unique in db
            cur.execute(f"INSERT INTO grid_squares (grid_ref, style_cat, geom) VALUES('{bng_grid_ref}', '{style}', {string_for_polygon})")

# Derived from
# http://www.movable-type.co.uk/scripts/latlong-gridref.html


def get_os_grid_reference(e, n):


    # Note no I
    gridChars = "ABCDEFGHJKLMNOPQRSTUVWXYZ"

    # get the 100km-grid indices
    e100k = math.floor(e / 100000)
    n100k = math.floor(n / 100000)

    #if e100k or n100k:
    #    return ''

    # translate those into numeric equivalents
    # of the grid letters
    l1 = (19 - n100k) - (19 - n100k) % 5 + math.floor((e100k + 10) / 5)
    l2 = (19 - n100k) * 5 % 25 + e100k % 5

    letPair = gridChars[int(l1)] + gridChars[int(l2)]

    # strip 100km-grid indices from easting & northing,
    # round to 100m
    e100m = math.trunc(round(float(e) / 100))
    egr = str(e100m).rjust(4, "0")[1:]
    if n >= 1000000:
        n = n - 1000000  # Fix Shetland northings
    n100m = math.trunc(round(float(n) / 100))
    ngr = str(n100m).rjust(4, "0")[1:]

    return letPair + egr + ngr
