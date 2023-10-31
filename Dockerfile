FROM eclipse-temurin:latest
RUN apt-get update && apt-get install -y \
    curl \
    jq

LABEL Author Endkind Ender <endkind.ender@endkind.net>

ARG FOLIA_VERSION=latest

COPY getFolia.sh /endkind/getFolia.sh
COPY docker-entrypoint.sh /endkind/docker-entrypoint.sh
COPY LICENSE /LICENSE

RUN chmod +x /endkind/getFolia.sh
RUN chmod +x /endkind/docker-entrypoint.sh

RUN /endkind/getFolia.sh

WORKDIR /folia

VOLUME /folia

ENV MIN_RAM=32M
ENV MAX_RAM=512M

ENV JAVA_FLAGS="--add-modules=jdk.incubator.vector -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20"

ENV WATERFALL_FLAGS="--nojline"

ENTRYPOINT ["/endkind/docker-entrypoint.sh"]