#!/bin/sh

set -e

PGPASSWORD=${POSTGRES_PASSWORD} psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
    CREATE DATABASE ${DB_NAME};
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
    CREATE DATABASE ${HASURA_METADATA_DB};
    GRANT ALL PRIVILEGES ON DATABASE ${HASURA_METADATA_DB} TO ${DB_USER};
EOSQL
