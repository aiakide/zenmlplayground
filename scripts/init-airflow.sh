#!/bin/bash

# Warte, bis MySQL vollständig gestartet ist
while ! mysqladmin ping -h"mysql" --silent; do
    echo "Warten auf MySQL..."
    sleep 3
done

# Initialisiere die Airflow-Datenbank
airflow db upgrade

# Erstelle einen Admin-Benutzer, falls erforderlich
if [ "$_AIRFLOW_WWW_USER_CREATE" = "true" ]; then
  airflow users create \
    --username "$_AIRFLOW_WWW_USER_USERNAME" \
    --password "$_AIRFLOW_WWW_USER_PASSWORD" \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com
fi

# Starte den Airflow-Webserver und den Scheduler
#airflow webserver --port 8080 &

#airflow scheduler