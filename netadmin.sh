#!/bin/bash

# Activar entorno virtual
source ~/venv/bin/activate

case "$1" in
  start)
    echo "🔵 Arrancando servicios..."
    # Servidor
    python3 ~/server.py &
    SERVER_PID=$!
    echo "Servidor iniciado con PID $SERVER_PID"

    # Cliente
    python3 ~/client.py &
    CLIENT_PID=$!
    echo "Cliente iniciado con PID $CLIENT_PID"

    # Dashboard
    uvicorn dashboard:app --reload --host 0.0.0.0 --port 8080 &
    DASH_PID=$!
    echo "Dashboard iniciado con PID $DASH_PID"

    # Guardar PIDs
    echo "$SERVER_PID $CLIENT_PID $DASH_PID" > ~/netadmin_pids.txt
    ;;
  
  stop)
    echo "🔴 Deteniendo servicios..."
    if [ -f ~/netadmin_pids.txt ]; then
      for pid in $(cat ~/netadmin_pids.txt); do
        kill $pid 2>/dev/null
      done
      rm ~/netadmin_pids.txt
      echo "Todos los servicios detenidos."
    else
      echo "No hay servicios en ejecución."
    fi
    ;;
  
  *)
    echo "Uso: ./netadmin.sh {start|stop}"
    ;;
esac
