#!/bin/bash
# ]*[ --------------------------------------------------------------------- ]*[
#  .  github2stackfield - x0-db automatic database initialisation             .
#  .                                                                          .
#  .  Replaces the default x0-db start script.                                .
#  .  Starts PostgreSQL, waits until it accepts connections, applies the       .
#  .  github2stackfield SQL scripts against the x0 database, then keeps        .
#  .  the server running.                                                     .
# ]*[ --------------------------------------------------------------------- ]*[
set -e

chown -R postgres:postgres /var/lib/postgresql/16/main/
chown -R postgres:postgres /var/run/postgresql/

# Start PostgreSQL in the background
su -c "/usr/lib/postgresql/16/bin/postgres -D /var/lib/postgresql/16/main" postgres &
PG_PID=$!

# Wait until PostgreSQL is ready to accept connections
echo "Waiting for PostgreSQL to be ready..."
until su -c "pg_isready -q -U postgres -d x0" postgres 2>/dev/null; do
    sleep 1
done
echo "PostgreSQL is ready."

# Apply github2stackfield database init scripts to the x0 database.
# All scripts are idempotent and safe to re-run on container restart.
echo "Applying github2stackfield database init scripts..."
su -c "psql -d x0 -f /opt/github2sf-init/01-create-schema.sql" postgres
su -c "psql -d x0 -f /opt/github2sf-init/02-insert-config.sql" postgres
su -c "psql -d x0 -f /opt/github2sf-init/03-insert-text.sql" postgres
echo "Database initialisation complete."

# Keep the container alive by waiting for the PostgreSQL process
wait $PG_PID
