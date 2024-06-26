class Menu:

   def __init__(self):
      pass
   
   def menu(self):
      print("Selecciona una opción")
      print("1 - Northwind")
      print("2 - Pubs")
      opcion = input("Opción: ")    
      return opcion
   
   def menuNorthwind(self):
      print("Selecciona una opción")
      print("1-Consulta 1 (Regiones con mayor cantidad de productos vendidos y usuarios que más compraron)")
      print("2-Consulta 2")
      print("3-Consulta 3")
      print("4-Salir")
      opcion = input("Opción: ")
      return opcion

   def menuPubs(self):
      print("Selecciona una opción")
      print("1-Consulta 1")
      opcion = input("Opción: ")
      return opcion
    