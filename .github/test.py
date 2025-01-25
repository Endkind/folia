import sys

from mcstatus import JavaServer


def check_mc_server(address, port):
    try:
        server = JavaServer.lookup(f"{address}:{port}")

        status = server.status()

        print(f"Server is reachable! Players online: {status.players.online}/{status.players.max}")
        print(f"Version: {status.version.name}")
        return True
    except Exception as e:
        print(f"Minecraft server at {address}:{port} is not reachable or did not respond.")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    SERVER_ADDRESS = "127.0.0.1"
    SERVER_PORT = 25565

    success = check_mc_server(SERVER_ADDRESS, SERVER_PORT)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)
