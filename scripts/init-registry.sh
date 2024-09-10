#!/bin/sh

# Benutzername und Passwort für die Authentifizierung
USERNAME=myuser
PASSWORD=mypassword

# Funktion zur Erstellung einer neuen htpasswd Datei oder zum Hinzufügen eines Benutzers
create_or_update_htpasswd() {
  if [ ! -f /auth/htpasswd ]; then
    echo "Erstelle htpasswd Datei und Benutzer"
    mkdir /auth/htpasswd
    htpasswd -c -B -b /auth/htpasswd/users.htpasswd $USERNAME $PASSWORD
  fi
}
# Initialisiere htpasswd Datei
create_or_update_htpasswd

# Starte die Registry
registry serve /etc/docker/registry/config.yml