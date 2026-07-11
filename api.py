# api.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
import paramiko

from models import Auditoria  # tu modelo definido con __table_args__ = {"schema": "netadmin"}
from database import get_db   # función que devuelve la sesión de SQLAlchemy

# Crear la aplicación FastAPI
app = FastAPI()

# --- Endpoint de Auditoría vía SSH ---
@app.post("/auditorias")
def realizar_auditoria(ip: str, username: str, password: str, db: Session = Depends(get_db)):
    try:
        # Conexión SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # CPU
        stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)'")
        cpu = stdout.read().decode().strip()

        # RAM
        stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem")
        ram = stdout.read().decode().strip()

        # Espacio libre
        stdin, stdout, stderr = ssh.exec_command("df -h / | tail -1")
        espacio = stdout.read().decode().strip()

        # Velocidad CPU
        stdin, stdout, stderr = ssh.exec_command("lscpu | grep 'MHz'")
        velocidad = stdout.read().decode().strip()

        ssh.close()

        # Guardar en la base de datos
        auditoria = Auditoria(
            ip=ip,
            fecha=datetime.datetime.now(),
            cpu=cpu,
            ram=ram,
            espacio_libre=espacio,
            velocidad=velocidad
        )
        db.add(auditoria)
        db.commit()
        db.refresh(auditoria)

        return {"status": "ok", "auditoria_id": auditoria.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en auditoría: {str(e)}")
