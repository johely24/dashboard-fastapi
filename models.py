from sqlalchemy import Column, Integer, String, TIMESTAMP
from .database import Base

class Auditoria(Base):
    __tablename__ = "auditorias"
    __table_args__ = {"schema": "netadmin"}  # explícito al esquema

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False)
    fecha = Column(TIMESTAMP)
    cpu = Column(String)
    ram = Column(String)
    espacio_libre = Column(String)
    velocidad = Column(String)

