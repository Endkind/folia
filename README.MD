# Folia - All Versions

This Docker image provides Folia Minecraft server versions. You can easily run a Minecraft server using this image.


## Quick start

```bash
docker run -it -d -p 25565:25565 --name endkind-folia -e MINECRAFT_EULA=true endkind/folia:latest
```
This command starts a Folia server in detached mode (-d), maps port 25565 from the host to the container, and accepts the Minecraft EULA.


## Installation and Configuration (Recommended)

```bash
docker volume create <servername>

docker run -it -d -p 25565:25565 --name <servername> -v <servername>:/folia -e MAX_RAM=3G -e MINECRAFT_EULA=true --restart=always endkind/folia:latest
```


## Using Specific Versions

When deploying your server for production or if you require version stability, consider using specific image versions. For example:

### Folia 1.19.4
```bash
docker run -it -d -p 25565:25565 -e MINECRAFT_EULA=true endkind/folia:1.19.4
```

By specifying a version like 1.20.1, you ensure that your server runs a known and tested version of Folia.

### All Supported Cersions
- `latest` uses always the newest version
- `1.20.1`
- `1.19.4`


## Environment variables

You can customize your Folia server by setting the following environment variables:

- `MIN_RAM` (default: 512M) - Minimum RAM allocated for the server.
- `MAX_RAM` (default: 1G) - Maximum RAM allocated for the server.
- `MINECRAFT_EULA` (default: false) - Set to `true` to accept the Minecraft EULA.
- `JAVA_FLAGS` - Additional Java flags generated with [flags.sh](https://flags.sh/).
- `PAPERMC_FLAGS` (default: --nojline) - Custom Folia server flags.
- `TZ` (example: Europe/Berlin) - Set the time zone for the server.

These environment variables allow you to tailor your Folia server's configuration to your specific requirements. You can adjust memory allocation, specify custom Java flags, and configure various server settings to suit your needs.


## Additional Information

- [GitHub Repository](https://github.com/Endkind/folia)
- [Visit our website](https://www.endkind.net) for more information about our projects and services.
- Connect to our Minecraft server (crossplay) at `mc.endkind.net` and start your adventure!


## LICENSE

MIT License

Copyright (c) 2023 Endkind Ender <endkind.ender@endkind.net>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
