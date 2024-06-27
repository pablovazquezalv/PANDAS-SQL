from Conexion import Conexion
from Metodos import Metodos
from Menu import Menu
import pandas as pd
if __name__ == '__main__':
    
    conexion = Conexion()
    menu = Menu()

    while True:
       opcion = menu.menu()

       if opcion == '1':   
        while True:
            bd = conexion.use_database("USE northwind")
            txt = open("nortwind.txt", "r")
            df = conexion.execute_query(txt.read())
            metodos = Metodos(df)
            metodos.generarCSV(df, 'northwind.csv')
            opcion_n = menu.menuNorthwind()
            if opcion_n == '1':
                df = metodos.agruparSumar('AÑO', 'RegionDescription', 'CompanyName')
                df = metodos.eliminarColumnas(df, ['CategoryName', 'ProductName'])
                df =  metodos.agruparMaximo(df, 'AÑO', 'RegionDescription')
                #Hacer matriz
                df = df.pivot(index='AÑO', columns='RegionDescription', values='CompanyName')
                df = df.reset_index()
                print("CONSULTA 1 NORTHWIND")
                print("*** los clientes que mas ganancia obtuvieron por año, y región ***")
                print(df)
                metodos.generarCSV(df, 'maximos.csv')  

            elif opcion_n == '2':
                print("CONSULTA 2 NORTHWIND")
                print("**Ganancias por Región**")

                df = metodos.agruparSuma(df)
                print(df)

                metodos.generarCSV(df, 'ganaciasxregion.csv')

            elif opcion_n == '3':
                #agrupar las categorias
                df = metodos.agruparSumar('AÑO', 'CategoryName', 'ProductName', 'CompanyName')

                metodos.generarCSV(df, 'maximos2.csv')
                #filtrar los tres ultimos años
                

                #eliminar columnas
                df = metodos.eliminarColumnas(df, ['RegionDescription'])

                #obtener el producto mas vendido
                df = metodos.productoMasVendido(df, 'AÑO', 'CategoryName')

                metodos.generarCSV(df, 'maximos2.csv')  
                pass
            elif opcion_n == '4':
                break
            else:
                print("Opción no válida")
        
       elif opcion == '2':
           while True:
               bd = conexion.use_database("USE pubs")
               txt = open("pubs.txt", "r")
               query = "SELECT  authors.au_lname,    titles.title_id,    titles.title,  titles.price ,sales.qty ,titleauthor.royaltyper FROM titles LEFT JOIN sales ON titles.title_id = sales.title_id LEFT JOIN titleauthor ON titles.title_id = titleauthor.title_id LEFT JOIN authors ON titleauthor.au_id = authors.au_id ORDER BY  titles.title_id"
               df = conexion.execute_query(query)
               metodos = Metodos(df)
               opcion_n = menu.menuPubs()
               if opcion_n == '1':
                   df = conexion.execute_query(txt.read())
                   metodos = Metodos(df)
                   #agrupar por autor
                   df = metodos.agruparSumar('au_lname', 'title', 'price', 'qty', 'royaltyper')


                   metodos.generarCSV(df, 'pubs.csv')
                   
               elif opcion_n == '2':
                   pass
              
    
    
    
   
    
   

    
   
    #abrir text
   
    