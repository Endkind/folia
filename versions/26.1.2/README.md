# Folia - 26.1.2

This Docker image provides Folia 26.1.2 Minecraft Server. You can easily run a Minecraft server using this image.

## Quick start

```bash
docker run -it -d -p 25565:25565 --name endkind-folia endkind/folia:26.1.2
```

## Installation and Configuration (Recommended)

```bash
docker volume create endkind-folia

docker run -it -d -p 25565:25565 --name endkind-folia -v endkind-folia:/data -e MAX_RAM=3G --restart=always endkind/folia:26.1.2
```

## Environment variables

You can customize your Folia server by setting the following environment variables:

- `MIN_RAM` (default: 512M) - Minimum RAM allocated for the server.
- `MAX_RAM` (default: 3G) - Maximum RAM allocated for the server.
- `JAVA_FLAGS` (default: "") - Additional Java flags for the server.
- `FOLIA_FLAGS` (default: --nojline) - Custom Folia server flags.
- `TZ` (example: Europe/Berlin) - Set the time zone for the server.

These environment variables allow you to tailor your Folia server's configuration to your specific requirements. You can adjust memory allocation, specify custom Java flags, and configure various server settings to suit your needs.

## How to build

```bash
docker build -t endkind/folia:26.1.2 .
```

## Additional Information

- [GitHub Repository](https://github.com/Endkind/folia)
- [Docker Repository](https://hub.docker.com/r/endkind/folia)
- [Docker Compose Example](https://github.com/Endkind/folia/blob/main/docker-compose.yml)
- [Visit our website](https://www.endkind.net) for more information about our projects and services.
- Connect to our Minecraft server (crossplay) at `mc.endkind.net` and start your adventure!

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/) License.

### Other License

This project includes code derived from the [Folia](https://github.com/PaperMC/folia) project.
