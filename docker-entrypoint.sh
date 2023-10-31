#!/bin/sh
echo "Created by Endkind Ender (www.endkind.net)"
while true; do
    java -Xms$MIN_RAM -Xmx$MAX_RAM $JAVA_FLAGS -Dcom.mojang.eula.agree=$MINECRAFT_EULA -jar /endkind/server.jar $FOLIA_FLAGS --nogui
done