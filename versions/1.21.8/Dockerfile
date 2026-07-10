FROM python:3.13-slim AS build

ARG VERSION=1.21.8
ARG BUILD=latest

COPY get-folia.py get-folia.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python get-folia.py --version $VERSION --build $BUILD --output /endkind/server.jar

FROM eclipse-temurin:21 AS runtime

LABEL Author="Endkind Ender <endkind.ender@endkind.net>"

RUN groupadd --system --gid 10001 folia \
    && useradd --system --uid 10001 --gid folia --home-dir /data --shell /usr/sbin/nologin folia \
    && mkdir -p /endkind /data \
    && chown -R folia:folia /endkind /data

COPY --chown=folia:folia entrypoint.sh /endkind/entrypoint.sh
RUN chmod +x /endkind/entrypoint.sh

COPY --from=build --chown=folia:folia /endkind/server.jar /endkind/server.jar

WORKDIR /data
VOLUME /data

ENV MIN_RAM=512M
ENV MAX_RAM=3G
ENV JAVA_FLAGS=""
ENV FOLIA_FLAGS="--nojline"

USER folia

ENTRYPOINT [ "/endkind/entrypoint.sh" ]
