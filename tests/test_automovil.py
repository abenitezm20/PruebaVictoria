#Importar unittest para crear las pruebas unitarias
from pickle import TRUE
from signal import raise_signal
import unittest
from src.modelo.automovil import Automovil

#from src.logica.Logica import Logica
from src.logica.Logica import Logica
from src.modelo.declarative_base import Session

from faker import Faker
import random
import string

cadenaAlphanumerica= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
cadenaAlpha= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
cadenanumerica= '1234567890'
import random

def CrearPlaca():
    Placa = ''
    for i in range(3):
        Placa += random.choice(cadenaAlphanumerica)
    for i in range(2):
        Placa += random.choice(cadenaAlpha)
    for i in range(2):
        Placa += random.choice(cadenaAlphanumerica)
    return Placa

def CrearPlacaIncorrecta():
    PlacaIncorrecta = ''
    for i in range(1,10):
        PlacaIncorrecta += random.choice(cadenanumerica)
    for i in range(1):
        PlacaIncorrecta += random.choice(cadenaAlpha)
    for i in range(1,10):
        PlacaIncorrecta += random.choice(cadenanumerica)
    for i in range(1):
        PlacaIncorrecta += random.choice(cadenaAlpha)
    return PlacaIncorrecta

#Clase de ejemplo, debe tener un nombre que termina con el sufijo TestCase, y conservar la herencia
class TestAutomovil(unittest.TestCase):

	#Instancia el atributo logica para cada prueba

    def setUp(self):
        '''Crea una Logica para hacer las pruebas'''
        #self.logica = Logica()
        self.logica = Logica()
        self.session = Session()
        self.data_factory = Faker()
        # Faker.seed(1000)
        self.data = []
        self.AutomovilInicial = []

        for i in range(0,5):
            self.data.append((
            self.data_factory.text(),
            CrearPlaca(),
            self.data_factory.text(),
            float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.text(),
            float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.text(),
            ))
            self.AutomovilInicial.append(
                Automovil(
                    marca = self.data[-1][0],
                    placa = self.data[-1][1],
                    modelo = self.data[-1][2],
                    kilometraje = self.data[-1][3],
                    color = self.data[-1][4],
                    cilindraje = self.data[-1][5],
                    tipo_combustible = self.data[-1][6]
             ))
        self.session.add(self.AutomovilInicial[-1])
        self.session.commit()

    def test_crear_automovil(self):
        '''Prueba la adición de un Automovil'''
        self.data.append((
            self.data_factory.text(),
            CrearPlaca(),
            self.data_factory.text(),
            float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.text(),
            float(str(self.data_factory.random_int(0, 9))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.text()
            )
            )

        resultado = self.logica.crear_auto(
            marca = self.data[-1][0],
            placa = self.data[-1][1],
            modelo = self.data[-1][2],
            kilometraje = self.data[-1][3],
            color = self.data[-1][4],
            cilindraje = self.data[-1][5],
            tipo_combustible = self.data[-1][6]
            )
        self.assertEqual(resultado, True)

    
    def test_crear_automovil_campos_obligatorios(self):
        resultado = self.logica.crear_auto(
            marca = None,
            placa = None,
            modelo = None,
            kilometraje = None,
            color = None,
            cilindraje = None,
            tipo_combustible = None)
        self.assertEqual(resultado, False)

    def test_crear_automovil_validar_Placa(self):
        self.data.append((
            self.data_factory.text(),
            CrearPlacaIncorrecta(),
            self.data_factory.text()+self.data_factory.text(),
            float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.text(),
            float(str(self.data_factory.random_int(0, 9))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.text(),)
            )

        resultado = self.logica.crear_auto(
            marca = self.data[-1][0],
            placa = self.data[-1][1],
            modelo = self.data[-1][2],
            kilometraje = self.data[-1][3],
            color = self.data[-1][4],
            cilindraje = self.data[-1][5],
            tipo_combustible = self.data[-1][6])
        self.assertEqual(resultado, False)

    def test_crear_automovil_unico(self):
        resultado = self.logica.crear_auto(
            marca = self.data[-1][0],
            placa = self.data[-1][1],
            modelo = self.data[-1][2],
            kilometraje = self.data[-1][3],
            color = self.data[-1][4],
            cilindraje = self.data[-1][5],
            tipo_combustible = self.data[-1][6])
        self.assertNotEqual(resultado, True)    

    def test_elemento_en_conjunto(self):
        automovil_nuevo = Automovil(
                    marca = self.data_factory.text(),
                    placa = CrearPlaca(),
                    modelo = self.data_factory.text(),
                    kilometraje = float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
                    color = self.data_factory.text(),
                    cilindraje = float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
                    tipo_combustible = self.data_factory.text(),
                )

        automovil_existente = self.AutomovilInicial[2]

        self.assertIn(automovil_existente, self.AutomovilInicial)
        self.assertNotIn(automovil_nuevo, self.AutomovilInicial)


    def test_verificar_almacenamiento_agregar_vehiculo(self):
        self.data.append((
            self.data_factory.name(),
            CrearPlaca(),
            self.data_factory.name()+self.data_factory.name(),
            float(str(self.data_factory.random_int(0, 500000))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.name(),
            float(str(self.data_factory.random_int(0, 9))+'.'+str(self.data_factory.random_int(0, 9))),
            self.data_factory.name(),)
            )
        
        resultado = self.logica.crear_auto(
            marca = self.data[-1][0],
            placa = self.data[-1][1],
            modelo = self.data[-1][2],
            kilometraje = self.data[-1][3],
            color = self.data[-1][4],
            cilindraje = self.data[-1][5],
            tipo_combustible = self.data[-1][6])

        automovil = self.session.query(Automovil).filter(Automovil.placa == self.data[-1][1]).first()
      
        self.assertEqual(automovil.marca, self.data[-1][0])
        self.assertEqual(automovil.placa, self.data[-1][1])
        self.assertEqual(automovil.modelo, self.data[-1][2])
        self.assertEqual(automovil.kilometraje, self.data[-1][3])
        self.assertEqual(automovil.color, self.data[-1][4])
        self.assertEqual(automovil.cilindraje, self.data[-1][5])
        self.assertEqual(automovil.tipo_combustible, self.data[-1][6])

def test_crear_automovil_validar_Tipo_Dato(self):
        self.data.append((
            self.data_factory.random_int(),
            CrearPlacaIncorrecta(),
            self.data_factory.random_int(),
            self.data_factory.text(),
            self.data_factory.random_int(),
            self.data_factory.text(),
            self.data_factory.random_int())
            )

        resultado = self.logica.crear_auto(
            marca = self.data[-1][0],
            placa = self.data[-1][1],
            modelo = self.data[-1][2],
            kilometraje = self.data[-1][3],
            color = self.data[-1][4],
            cilindraje = self.data[-1][5],
            tipo_combustible = self.data[-1][6])
        self.assertEqual(resultado, False)