#!/bin/bash

# Warte, bis MySQL vollständig gestartet ist
while ! mysqladmin ping -h"localhost" --silent; do
    echo "Warten auf das Starten von MySQL ..."
    sleep 3
done

# Verbinde dich mit MySQL und führe die SQL-Befehle aus
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
CREATE DATABASE IF NOT EXISTS mlflow;
CREATE USER IF NOT EXISTS 'mlflow'@'%' IDENTIFIED BY 'mlflow_password';
GRANT ALL PRIVILEGES ON mlflow.* TO 'mlflow'@'%';
FLUSH PRIVILEGES;
EOSQL

echo "Datenbank 'mlflow' und Benutzer 'mlflow' wurden erfolgreich erstellt oder existierten bereits."