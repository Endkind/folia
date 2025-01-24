# Folia - All Versions

This Docker image provides Folia Minecraft server versions. You can easily run a Minecraft server using this image.

## Quick start

```bash
docker run -it -d -p 25565:25565 --name endkind-folia -e MINECRAFT_EULA=true endkind/folia:latest
```

This command starts a Folia server in detached mode (-d), maps port 25565 from the host to the container, and accepts the Minecraft EULA.

## Installation and Configuration (Recommended)

```bash
docker volume create endkind-folia

docker run -it -d -p 25565:25565 --name endkind-folia -v endkind-folia:/folia -e MAX_RAM=3G -e MINECRAFT_EULA=true --restart=always endkind/folia:latest
```

## Using Specific Versions

When deploying your server for production or if you require version stability, consider using specific image versions. For example:

### Folia 1.19.4

```bash
docker run -it -d -p 25565:25565 -e MINECRAFT_EULA=true endkind/folia:1.19.4
```

By specifying a version like 1.20.1, you ensure that your server runs a known and tested version of Folia.

### All Supported Versions

- `latest` uses always the newest version
- `1.21.4`
- `1.20.1`, `1.20.2`, `1.20.4`, `1.20.6`
- `1.19.4`

## Environment variables

You can customize your Folia server by setting the following environment variables:

- `MIN_RAM` (default: 512M) - Minimum RAM allocated for the server.
- `MAX_RAM` (default: 1G) - Maximum RAM allocated for the server.
- `MINECRAFT_EULA` (default: false) - Set to `true` to accept the Minecraft EULA.
- `JAVA_FLAGS` - Additional Java flags generated with [flags.sh](https://flags.sh/).
- `FOLIA_FLAGS` (default: --nojline) - Custom Folia server flags.
- `TZ` (example: Europe/Berlin) - Set the time zone for the server.

These environment variables allow you to tailor your Folia server's configuration to your specific requirements. You can adjust memory allocation, specify custom Java flags, and configure various server settings to suit your needs.

## How to build

Replace `<version>` with the desired version.

```bash
docker build --build-arg FOLIA_VERSION=<version> -t endkind/folia:<version> .
```

## Additional Information

- [GitHub Repository](https://github.com/Endkind/folia)
- [Docker Repository](https://hub.docker.com/r/endkind/folia)
- [Visit our website](https://www.endkind.net) for more information about our projects and services.
- Connect to our Minecraft server (crossplay) at `mc.endkind.net` and start your adventure!

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/) License.

### Other License

This project includes code derived from the [Folia](https://github.com/PaperMC/folia) project.
