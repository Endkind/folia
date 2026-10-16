#!/bin/bash

while [ true ]; do
    java -Xms${MIN_RAM} -Xmx${MAX_RAM} ${JAVA_FLAGS} -jar /endkind/server.jar ${FOLIA_FLAGS}

    echo Server restarting...
    echo Press CTRL + C to stop.
done
