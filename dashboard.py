from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psycopg2

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        dbname="netadmin",
        user="netadmin_user",
        password="12345",
        host="localhost",
        port="5432"
    )

@app.get("/", response_class=HTMLResponse)
def read_equipos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_host, direccion_ip, estado, ultimo_latido FROM equipos;")
    rows = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <meta http-equiv="refresh" content="5">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 20px;
            }
            table {
                width: 80%;
                margin: auto;
                border-collapse: collapse;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                background: white;
                border-radius: 8px;
                overflow: hidden;
            }
            th {
                background: #4CAF50;
                color: white;
                padding: 12px;
                text-align: center;
            }
            td {
                padding: 10px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            tr:hover {
                background: #f1f1f1;
            }
            .online {
                color: green;
                font-weight: bold;
            }
            .offline {
                color: red;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🌐 Dashboard de Equipos</h1>
        <table>
            <tr><th>Host</th><th>IP</th><th>Estado</th><th>Último Latido</th></tr>
    """

    for row in rows:
        estado_class = "online" if row[2] == "ONLINE" else "offline"
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td class='{estado_class}'>{row[2]}</td><td>{row[3]}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """
    return html

