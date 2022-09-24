
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Automovil(Base):
    __tablename__ = 'automovil'

    id = Column(Integer, primary_key=True)
    marca = Column(String)
    placa  = Column(String)
    modelo  = Column(String)
    kilometraje  = Column(Float)
    color  = Column(String)
    cilindraje = Column(Float)
    tipo_combustible  = Column(String)
    Vendido = Column(Boolean)
    ValorVenta = Column(Float)
    KilometrajeVenta = Column(Float)
    acciones = Column(Integer, ForeignKey('acciones.id'))