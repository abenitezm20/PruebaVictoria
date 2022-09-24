from sqlite3 import Date
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.mantenimiento import Mantenimiento

from .declarative_base import Base


class Acciones(Base):
    __tablename__ = 'acciones'
    id = Column(Integer, primary_key=True)
    mantenimiento = Column(String)
    id_auto = Column(Integer, ForeignKey("automovil.id") )
    valor = Column(Float)
    kilometraje  = Column(Float)
    fecha = Column(String)


class MantenimientoAccion(Base):
    __tablename__ = 'MantenimientoAccion'

    mantenimiento_id = Column(
        String,
        ForeignKey('mantenimiento.nombre'),
        primary_key=True)

    acciones_id = Column(
        Integer,
        ForeignKey('acciones.id'),
        primary_key=True)


class AutomovilAcciones(Base):
    __tablename__ = 'AutomovilAcciones'

    automovil_id = Column(
        Integer,
        ForeignKey('automovil.id'),
        primary_key=True)

    acciones_id = Column(
        Integer,
        ForeignKey('acciones.id'),
        primary_key=True)