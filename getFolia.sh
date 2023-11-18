#!/bin/bash
VERSION=$(cat /endkind/folia_version)
BASE_URL="https://api.papermc.io/v2/projects/folia"

if [ $VERSION == "latest" ]; then
    VERSION=$(curl -s "$BASE_URL" | jq -r '.versions | .[-1]')
fi

LATEST_BUILD=$(curl -s "$BASE_URL/versions/$VERSION" | jq -r '.builds | .[-1]')

curl -o "/endkind/server.jar" -L "$BASE_URL/versions/$VERSION/builds/$LATEST_BUILD/downloads/folia-$VERSION-$LATEST_BUILD.jar"
if [ $? -eq 0 ]; then
    echo "Download Volia Version ($VERSION) Build ($LATEST_BUILD)"
else
    echo "An error occurred while downloading Folia. Please try again or recreate the container."
    exit 1
fi
