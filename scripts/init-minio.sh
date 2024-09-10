#!/bin/sh
/usr/bin/docker-entrypoint.sh server /data --console-address :9001 &

# Hole die Prozess ID (PID) des MinIO-Servers
MINIO_PID=$!
# Warte, bis der MinIO-Server auf Port 9000 verfügbar ist
until curl --output /dev/null --silent --head --fail http://0.0.0.0:9001; do
  echo "Warten auf MinIO..."
  sleep 1
done

# Setze den MinIO-Client alias
mc alias set myminio http://0.0.0.0:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Erstelle den Bucket 'zenml', wenn er noch nicht existiert
if ! mc ls myminio/zenml > /dev/null 2>&1; then
  mc mb myminio/zenml
fi

echo "Bucket 'zenml' erstellt oder existierte bereits."

# Halte den MinIO-Server am Laufen
wait $MINIO_PID
