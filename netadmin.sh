#!/bin/bash

# Activar entorno virtual
source ~/dashboard-fastapi/venv/bin/activate

case "$1" in
  start)
    echo " Arrancando servicios..."

    # Servidor
    python3 ~/dashboard-fastapi/server.py &
    SERVER_PID=$!
    echo "Servidor iniciado con PID $SERVER_PID"

    # Cliente
    python3 ~/dashboard-fastapi/client.py &
    CLIENT_PID=$!
    echo "Cliente iniciado con PID $CLIENT_PID"

    # Dashboard (FastAPI con Uvicorn)
    uvicorn dashboard:app --host 0.0.0.0 --port 8080 &
    DASH_PID=$!
    echo "Dashboard iniciado con PID $DASH_PID"

    # ngrok
    ngrok http 8080 &
    NGROK_PID=$!
    echo "ngrok iniciado con PID $NGROK_PID"

    # Guardar PIDs
    echo "$SERVER_PID $CLIENT_PID $DASH_PID $NGROK_PID" > ~/dashboard-fastapi/netadmin_pids.txt
    ;;
  
  stop)
    echo "Deteniendo servicios..."
    if [ -f ~/dashboard-fastapi/netadmin_pids.txt ]; then
      for pid in $(cat ~/dashboard-fastapi/netadmin_pids.txt); do
        kill $pid 2>/dev/null
      done
      rm ~/dashboard-fastapi/netadmin_pids.txt
      echo "Todos los servicios detenidos."
    else
      echo "No hay servicios en ejecución."
    fi
    ;;
  
  *)
    echo "Uso: ./netadmin.sh {start|stop}"
    ;;
esac
