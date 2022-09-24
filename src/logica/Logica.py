from ast import Or
from cgi import print_exception
from pickle import TRUE
from pydoc import stripid
from src.modelo.automovil import Automovil
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.acciones import Acciones, AutomovilAcciones
from src.modelo.declarative_base import engine, Base, session

import re
#Funcion Utilitaria para validar si un numero es de tipo Float.
def validarFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#Funcion Utilitaria para validar si es de tipo str.
def validarStr(valor):
    try:
        str(valor)
        return True
    except ValueError:
        return False

        
#Funcion utilitaria para validar que la placa tenga al menos 2 caracteres alfabeticos seguidos.
def validarPlaca(placaValidar):
    placaCorrecta = False
    contadorAlpha = 0
    arrayPlaca = list(placaValidar)

    for i in arrayPlaca:
        if(i.isalpha()):
            contadorAlpha+=1
        else:
            contadorAlpha = 0

        if (contadorAlpha >= 2):
            placaCorrecta = TRUE
            break
    return placaCorrecta

'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
class Logica():

    def __init__(self):
        Base.metadata.create_all(engine)
        #Este constructor contiene los datos falsos para probar la interfaz

        self.gastos = [{'Marca':'Volkswagen', 'Gastos':[('2019',1200000),('2020',1300000), ('2021',2000000), ('2022',2500000), \
                        ('Total',7000000)], 'ValorKilometro': 175},\
                       {'Marca':'Renault', 'Gastos':[('2020',900000), ('2021',1100000), ('2022',1300000), \
                        ('Total',3300000)], 'ValorKilometro': 128},]

    
    def dar_autos(self):
        lista_autos = []
        autosconsulta = session.query(Automovil).order_by(Automovil.placa).all()
        if(len(autosconsulta) > 0):
            for dic_auto in autosconsulta:
                lista_autos.append({'Marca':dic_auto.marca, 'Placa':dic_auto.placa, 'Modelo':dic_auto.modelo, 'Kilometraje':dic_auto.kilometraje, 'Color':dic_auto.color, 'Cilindraje':dic_auto.cilindraje, 'TipoCombustible':dic_auto.tipo_combustible, 'Vendido': dic_auto.Vendido, 'ValorVenta': dic_auto.ValorVenta, 'KilometrajeVenta': dic_auto.KilometrajeVenta})
        self.autos = lista_autos.copy()
        return lista_autos

    def dar_auto(self, id_auto):
        return self.autos[id_auto].copy()
    
    def crear_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):

        #Validación de Campos Vacios, si se encuentra algun campo vacio, no se podra grabar el automovil
        if(marca is None or len(str(marca).strip())==0 ) or (placa is None or len(str(placa).strip())==0) or (modelo is None or len(str(modelo).strip())==0) or (kilometraje is None) or (color is None or len(str(color).strip())==0)  or (cilindraje is None) or (tipo_combustible is None or len(str(tipo_combustible).strip())==0):
            return False

        #Validacion de Campos Numericos sean de tipo Float
        if(kilometraje is None):
            kilometraje='None'
        if(cilindraje is None):
            cilindraje='None'

        if(not isinstance(marca, str) or not isinstance(placa, str) or not isinstance(modelo, str) or not isinstance(color, str) or not isinstance(tipo_combustible, str)):
            return False

        if not validarFloat(kilometraje) or not validarFloat(cilindraje):
            return False
        
        #Validacion de campos kilometraje y cilindraje mayores a Cero
        if int(kilometraje) < 0 or int(cilindraje) <= 0:
            return False

        #Validacion de campos placa tenga al menos 2 caracteres tipo letra
        if not validarPlaca(placa):
            return False
        
        unicaMarca = session.query(Automovil).filter(Automovil.marca == marca).all()
        unicaPlaca = session.query(Automovil).filter(Automovil.placa == placa).all()

        if(len(unicaMarca) != 0):
            return False
            
        if len(unicaPlaca) == 0 :
            automovil = Automovil(marca=marca, placa=placa, modelo=modelo, kilometraje=kilometraje, color=color, cilindraje=cilindraje, tipo_combustible=tipo_combustible, Vendido=False, ValorVenta=0, KilometrajeVenta=0)
            session.add(automovil)
            session.commit()
            return True
        else:
            return False


    def editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        print(id)
        PlacaAuto= self.autos[id]['Placa']
        AutomovilEditar=session.query(Automovil).filter(Automovil.placa == PlacaAuto).all()
        id_Automovil=0
        for datos in AutomovilEditar:
            id_Automovil=datos.id
        print(id_Automovil)
        Auto = session.query(Automovil).get(id_Automovil)
        Auto.marca=marca
        Auto.placa=placa
        Auto.modelo=modelo
        Auto.kilometraje=kilometraje
        Auto.color=color
        Auto.cilindraje=cilindraje
        Auto.tipo_combustible=tipo_combustible
        session.add(Auto)
        session.commit()


    def vender_auto(self, id, kilometraje_venta, valor_venta):
        self.autos[id]['ValorVenta'] = valor_venta
        self.autos[id]['KilometrajeVenta'] = kilometraje_venta
        self.autos[id]['Vendido'] = True

    def eliminar_auto(self, id):
        PlacaAuto= self.autos[id]['Placa']
        AutomovilBorrar=session.query(Automovil).filter(Automovil.placa == PlacaAuto).all()
        for autoM in AutomovilBorrar:
            id_Automovil=autoM.id
        AccioneAuto=session.query(Acciones).filter(Acciones.id_auto == id_Automovil).all()
        if(len(AccioneAuto)==0):
            session.query(Automovil).filter(Automovil.placa == PlacaAuto).delete()
            session.commit()
            return True
        return False
        
    def validar_crear_editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        validacion = False
        try:
            float(kilometraje)
            validacion = True
        except ValueError:
            return False
        return validacion
        
    def validar_vender_auto(self, id, kilometraje_venta, valor_venta):
        validacion = False
        try:
            float(kilometraje_venta)
            float(valor_venta)
            validacion = True
        except ValueError:
            validacion = False

        return validacion
        

    def dar_mantenimientos(self):
        lista_mantenimientos = []
        mantenimientosConsulta = session.query(Mantenimiento).order_by(Mantenimiento.nombre).all()
        if(len(mantenimientosConsulta) > 0):
            for dic_man in mantenimientosConsulta:
                lista_mantenimientos.append({'Nombre':dic_man.nombre, 'Descripcion':dic_man.descripcion})
        self.mantenimientos = lista_mantenimientos.copy()
        # return lista_mantenimientos
        return self.mantenimientos.copy()

    def aniadir_mantenimiento(self,nombre,descripcion):

        #Validación de Campos Vacios, si se encuentra algun campo vacio, no se podra grabar el automovil
        if(nombre is None or len(str(nombre).strip())==0) or (descripcion is None):
            return False
        
        #Validacion que campo descripcion tenga al menos 25 caracteres
        if len(descripcion) < 25:
            return False

        #Se consulta si existe otro mantenimiento con el mismo nombre
        unicoNombre = session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).all()
                
        if len(unicoNombre) == 0:
            mantenimiento = Mantenimiento(nombre=nombre, descripcion=descripcion)
            session.add(mantenimiento)
            session.commit()
            return True
        else:
            return False

    
    def editar_mantenimiento(self, id, nombre, descripcion):
        self.mantenimientos[id]['Nombre'] = nombre
        self.mantenimientos[id]['Descripcion'] = descripcion
    
    def eliminar_mantenimiento(self, id):
        del self.mantenimientos[id]

    def validar_crear_editar_mantenimiento(self, nombre, descripcion):
        validacion = False
        if nombre is not None and descripcion is not None:
            validacion = True
        return validacion
        
    def dar_acciones_auto(self, id_auto):

        #print ("A dar acciones llego: " + str(id_auto))

        id_Automovil = 0
        PlacaAuto= self.autos[id_auto]['Placa']
        AutomovilBorrar=session.query(Automovil).filter(Automovil.placa == PlacaAuto).all()
        for autoM in AutomovilBorrar:
            id_Automovil=autoM.id
            #print ("A dar acciones llego id_Automovil: " + str(id_Automovil))
        accionesConsulta=session.query(Acciones).filter(Acciones.id_auto == id_Automovil).all()


        lista_acciones = []
        #accionesConsulta = session.query(AutomovilAcciones).filter(AutomovilAcciones.automovil_id == id_auto).all()
        if(len(accionesConsulta) > 0):
            for dic_accion in accionesConsulta:
                lista_acciones.append({'id':dic_accion.id, 'Mantenimiento':dic_accion.mantenimiento, 'Kilometraje':dic_accion.kilometraje, 'Valor':dic_accion.valor, 'Fecha':dic_accion.fecha})
                #print("Mantenimiento: " + dic_accion.mantenimiento + " - Kilometraje: " + str(dic_accion.kilometraje) + " - Valor: " + str(dic_accion.valor) + " - Fecha: " + dic_accion.fecha)
        self.acciones = lista_acciones.copy()
        return lista_acciones.copy()

    def dar_accion(self, id_auto, id_accion):
        return self.dar_acciones_auto(id_auto)[id_accion].copy()

    def crear_accion(self, mantenimiento, id_auto, valor, kilometraje, fecha):
        # n_accion = {}
        # n_accion['Mantenimiento'] = mantenimiento
        # n_accion['Auto'] = self.autos[id_auto]['Marca']
        # n_accion['Valor'] = valor
        # n_accion['Kilometraje'] = kilometraje
        # n_accion['Fecha'] = fecha
        # self.acciones.append(n_accion)

        #print("Crear Acciones: " + mantenimiento + " - " + str(id_auto) + " - " + str(valor) + " - " + str(kilometraje) + " - " + fecha)
        
        try:
            #print("Creacion Accion")

            PlacaAuto= self.autos[id_auto]['Placa']
            AutomovilBorrar=session.query(Automovil).filter(Automovil.placa == PlacaAuto).all()
            for autoM in AutomovilBorrar:
                id_Automovil=autoM.id
            #print ("A dar acciones llego id_Automovil: " + str(id_Automovil))


            acciones = Acciones(mantenimiento=mantenimiento, valor=valor, kilometraje=kilometraje, fecha=fecha)
            session.add(acciones)
            acciones.id_auto = id_Automovil
            
            session.commit()

            return True
        except:
            print("No pude grabar")
            print_exception
            return False


    def editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):

        try:
            PlacaAuto= self.acciones[id_accion]['id']
            acciones = session.query(Acciones).get(PlacaAuto)
            print("Antes: Mantenimiento:" + acciones.mantenimiento + " id_auto:"+str(acciones.id_auto) + " valor:" + str(acciones.valor) + " kilometraje:" + str(acciones.kilometraje) + " fecha:" + acciones.fecha)
            print("Despuees: Mantenimiento:" + mantenimiento + " id_auto:"+str(id_auto) + " valor:" + str(valor) + " kilometraje:" + str(kilometraje) + " fecha:" + fecha)
            acciones.mantenimiento = mantenimiento
            acciones.valor = valor
            acciones.kilometraje = kilometraje
            acciones.fecha = fecha
            session.add(acciones)
            session.commit()
            return True
        except:
            return False

    def eliminar_accion(self, id_auto, id_accion):
        marca_auto =self.autos[id_auto]['Marca']
        i = 0
        id = 0
        while i < len(self.acciones):
            if self.acciones[i]['Auto'] == marca_auto:
                if id == id_accion:
                    self.acciones.pop(i)
                    return True
                else:
                    id+=1
            i+=1
        
        return False
                

        del self.accion[id_accion]
        
    def validar_crear_editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):
        validacion = False
        try:
            float(kilometraje)
            float(valor)
            validacion = True
        except ValueError:
            validacion = False

        return validacion

    def dar_reporte_ganancias(self, id_auto):
        n_auto = self.autos[id_auto]['Marca']
        
        for gasto in self.gastos:
            if gasto['Marca'] == n_auto:
                return gasto['Gastos'], gasto['ValorKilometro']

        return [('Total',0)], 0