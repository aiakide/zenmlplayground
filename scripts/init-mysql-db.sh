#!/bin/bash

# Warte, bis MySQL vollständig gestartet ist
while ! mysqladmin ping -h"localhost" --silent; do
    echo "Warten auf das Starten von MySQL ..."
    sleep 3
done

# Verbinde dich mit MySQL und führe die SQL-Befehle aus
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
CREATE DATABASE IF NOT EXISTS airflow;
CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflow_password';
GRANT ALL PRIVILEGES ON airflow.* TO 'airflow'@'%';
FLUSH PRIVILEGES;
EOSQL

echo "Datenbank 'airflow' und Benutzer 'airflow' wurden erfolgreich erstellt oder existierten bereits."