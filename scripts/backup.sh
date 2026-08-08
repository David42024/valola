#!/bin/bash
# scripts/backup.sh
# Respaldo de la base de datos y volúmenes locales.

set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="n8n/backups"
DB_USER="valola"
DB_NAME="valola"

mkdir -p "$BACKUP_DIR"

echo ">> Respaldando base de datos..."
docker exec valola-postgres-dev pg_dump -U "$DB_USER" -F c -b -v "$DB_NAME" > "$BACKUP_DIR/postgres_$TIMESTAMP.dump"

echo ">> Respaldando datos de n8n..."
tar -czf "$BACKUP_DIR/n8n_data_$TIMESTAMP.tar.gz" -C n8n/data .

echo ">> Backup completado en $BACKUP_DIR"