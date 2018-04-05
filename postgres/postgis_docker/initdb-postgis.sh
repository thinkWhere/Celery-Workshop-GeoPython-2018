#!/bin/sh

#set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

# Load PostGIS into both template_database and $POSTGRES_DB
echo "Loading PostGIS extensions into $DB"
"${psql[@]}" --dbname=$POSTGRES_DB <<-'EOSQL'
		CREATE EXTENSION IF NOT EXISTS postgis;
EOSQL

"${psql[@]}" --dbname=$POSTGRES_DB -f /geopython.dump