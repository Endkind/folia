FROM python:3.13-slim AS build

ARG VERSION=latest
ARG BUILD=latest

COPY get-folia.py get-folia.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN python get-folia.py --version $VERSION --build $BUILD --output /endkind/server.jar

FROM eclipse-temurin:latest AS runtime

LABEL Author="Endkind Ender <endkind.ender@endkind.net>"

COPY entrypoint.sh /endkind/entrypoint.sh
RUN chmod +x /endkind/entrypoint.sh

COPY --from=build /endkind/server.jar /endkind/server.jar

WORKDIR /data
VOLUME /data

ENV MIN_RAM=512M
ENV MAX_RAM=3G
ENV JAVA_FLAGS=""
ENV FOLIA_FLAGS="--nojline"

ENTRYPOINT [ "/endkind/entrypoint.sh" ]
