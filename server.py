import psycopg2

conn = psycopg2.connect(
    dbname="netadmin",
    user="netadmin_user",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


import asyncio
import socket
from datetime import datetime
import psycopg2

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="netadmin",
    user="netadmin_user",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

clients = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    data = await reader.read(100)
    message = data.decode().strip()

    if message == "HEARTBEAT":
        clients[addr] = datetime.now()
        print(f"Latido recibido de {addr} a las {clients[addr]}")

        # Guardar en la tabla equipos
        cursor.execute("""
            INSERT INTO equipos (nombre_host, direccion_ip, direccion_mac, estado, ultimo_latido)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (direccion_mac) DO UPDATE
            SET estado = EXCLUDED.estado,
                ultimo_latido = EXCLUDED.ultimo_latido;
        """, (
            f"host-{addr[1]}",   # nombre ficticio
            addr[0],             # IP del cliente
            f"MAC-{addr[1]}",    # MAC ficticia
            "ONLINE",
            clients[addr]
        ))
        conn.commit()

        writer.write(b"ACK")

    elif message == "PING":
        writer.write(b"PONG")
    elif message == "REBOOT":
        writer.write(b"REBOOTING")
    elif message == "SHUTDOWN":
        writer.write(b"SHUTTING DOWN")

    await writer.drain()
    writer.close()

async def tcp_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 9090)
    async with server:
        await server.serve_forever()

asyncio.run(tcp_server())

