#Importar unittest para crear las pruebas unitarias
import collections
from pickle import TRUE
from signal import raise_signal
import unittest
from src.modelo.automovil import Automovil

from src.logica.Logica import Logica
from src.modelo.declarative_base import Session

from faker import Faker
import random
import string

class TestListaAutomovil(unittest.TestCase):
    def setUp(self):
        '''Crea una Logica para hacer las pruebas'''
        self.logica = Logica()
        self.session = Session()
    
    def test_listar_campos(self):
        '''Valida que los campos retornados en la lista correspondan a un automivil ingresado'''
        resultado = self.logica.dar_autos()
        for auto in resultado:
            automovil_nuevo = Automovil(
                    marca = auto['Marca'],
                    placa = auto['Placa'],
                    modelo = auto['Modelo'],
                    kilometraje = auto['Kilometraje'],
                    color = auto['Color'],
                    cilindraje = auto['Cilindraje'],
                    tipo_combustible = auto['TipoCombustible']
                )
            self.assertIsInstance(automovil_nuevo, Automovil)


    # def test_lista_ordenada(self):
    #     '''Valida que los elementos de la lista se presenten de forma ordenada por marca'''
    #     resultado = self.logica.dar_autos()

    #     resultadoOrdenado = sorted(resultado, key=lambda x: x['Marca'])

    #     self.assertEqual(resultado, resultadoOrdenado)