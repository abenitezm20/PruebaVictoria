#Importar unittest para crear las pruebas unitarias
from pickle import TRUE
from signal import raise_signal
import unittest
from src.modelo.mantenimiento import Mantenimiento

from src.logica.Logica import Logica
from src.modelo.declarative_base import Session

from faker import Faker
import random
import string




#Clase de ejemplo, debe tener un nombre que termina con el sufijo TestCase, y conservar la herencia
class TestMantenimiento(unittest.TestCase):

	#Instancia el atributo logica para cada prueba

    def setUp(self):
        '''Crea una Logica para hacer las pruebas'''
        self.logica = Logica()
        self.session = Session()
        self.data_factory = Faker()
        # Faker.seed(1000)
        self.data = []
        self.mantenimientoInicial = []

        for i in range(0,5):
            self.data.append((
                self.data_factory.text(),
                self.data_factory.text(),
            ))
            self.mantenimientoInicial.append(
                Mantenimiento(
                    nombre = self.data[-1][0],
                    descripcion = self.data[-1][1]
             ))
        self.session.add(self.mantenimientoInicial[-1])
        self.session.commit()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()
        '''Consulta todos los Mantenimientos'''
        busqueda = self.session.query(Mantenimiento).all()

        self.session.commit()
        self.session.close()

    def test_aniadir_mantenimiento(self):
        '''Prueba la adición de un mantenimiento'''
        descrip=''
        for i in range(26):
             descrip+=self.data[-1][1]

        self.data.append((
            self.data_factory.unique.name()+str(random.random()),
            descrip
            )) 
        resultado = self.logica.aniadir_mantenimiento(
            nombre = self.data[-1][0],
            descripcion = self.data[-1][1]) 
        self.assertEqual(resultado, True)
        
    def test_aniadir_mantenimiento_duplicado(self):
        '''Prueba la adición de un mantenimiento duplicado'''

        resultado = self.logica.aniadir_mantenimiento(
            nombre = self.data[-1][0],
            descripcion = self.data[-1][1])
        self.assertNotEqual(resultado, True)

    def test_aniadir_mantenimiento_campos_obligatorios(self):
        '''Prueba la adición de un mantenimiento con datos vacios o nulos'''
        resultado = self.logica.aniadir_mantenimiento(
            nombre = None,
            descripcion = None)

        resultado2 = self.logica.aniadir_mantenimiento(
            nombre = " ",
            descripcion = "   ")
               
        self.assertNotEqual(resultado, True)
        self.assertNotEqual(resultado2, True)


    def test_aniadir_mantenimiento_longitud_campos(self):
        '''Prueba la adición de un mantenimiento con campo descripcion inferior 25 caracteres'''
        
        self.data.append((
                self.data_factory.text(),
                self.data_factory.text(),
            ))

        resultado = self.logica.aniadir_mantenimiento(
            nombre = self.data[-1][0],
            descripcion = (self.data[-1][1])[0:24])
        self.assertNotEqual(resultado, True)

    def test_elemento_en_conjunto(self):
        '''Prueba el elemento en conjunto'''
        descrip=''
        for i in range(26):
            descrip+=self.data[-1][1]

        mantenimiento_nuevo = Mantenimiento(
                    nombre = self.data[-1][0],
                    descripcion = descrip)
        mantenimiento_existente = self.mantenimientoInicial[2]

        self.assertIn(mantenimiento_existente, self.mantenimientoInicial)
        self.assertNotIn(mantenimiento_nuevo, self.mantenimientoInicial) 


    def test_verificar_almacenamiento_agregar_mantenimiento(self):
        '''Prueba el almacenamiento despues de agregar el mantenimiento'''

        descrip=''
        for i in range(26):
            descrip+=self.data[-1][1]

        self.data.append((
            self.data_factory.unique.name(),
            descrip
            )) 

        resultado = self.logica.aniadir_mantenimiento(
            nombre = self.data[-1][0],
            descripcion = self.data[-1][1]) 
        
        
        mantenimiento = self.session.query(Mantenimiento).filter(Mantenimiento.nombre == self.data[-1][0]).first()

        self.assertEqual(mantenimiento.nombre, self.data[-1][0])
        self.assertEqual(mantenimiento.descripcion, self.data[-1][1])
    