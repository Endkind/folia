#!/bin/bash

FOLIA_VERSION=${FOLIA_VERSION:-latest}

LATEST_VERSION_URL="https://papermc.io/api/v2/projects/folia"

if [ "$FOLIA_VERSION" == "latest" ]; then
  LATEST_VERSION=$(curl -s "$LATEST_VERSION_URL" | jq -r '.versions | .[-1]')
else
  LATEST_VERSION="$FOLIA_VERSION"
fi

if [ -z "$LATEST_VERSION" ]; then
  echo "Konnte keine Informationen zur neuesten Folia-Version abrufen."
  exit 1
fi

LATEST_BUILD_URL="https://papermc.io/api/v2/projects/folia/versions/$LATEST_VERSION"

LATEST_BUILD=$(curl -s "$LATEST_BUILD_URL" | jq -r '.builds | .[-1]')

if [ -z "$LATEST_BUILD" ]; then
  echo "Konnte keine Informationen zur neuesten Build-Nummer abrufen."
  exit 1
fi

DOWNLOAD_URL="https://papermc.io/api/v2/projects/folia/versions/$LATEST_VERSION/builds/$LATEST_BUILD/downloads/folia-$LATEST_VERSION-$LATEST_BUILD.jar"

DOWNLOAD_DIR="/endkind"

DESTINATION="$DOWNLOAD_DIR/server.jar"

mkdir -p "$DOWNLOAD_DIR"

curl -o "$DESTINATION" -L "$DOWNLOAD_URL"

if [ $? -eq 0 ]; then
  echo "Neueste Folia-Version ($LATEST_VERSION), Build $LATEST_BUILD heruntergeladen und gespeichert unter: $DESTINATION"
else
  echo "Fehler beim Herunterladen der neuesten Folia-Version."
  exit 1
fi
