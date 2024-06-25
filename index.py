from Conexion import Conexion
from Metodos import Metodos
from Menu import Menu
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

            opcion_n = menu.menuNorthwind()
            if opcion_n == '1':
                df = metodos.agruparSumar('AÑO', 'RegionDescription', 'CompanyName')
                df = metodos.eliminarColumnas(df, ['CategoryName', 'ProductName'])
                df =  metodos.agruparMaximo(df, 'AÑO', 'RegionDescription')
                #Hacer matriz
                df = df.pivot(index='AÑO', columns='RegionDescription', values='CompanyName')
                df = df.reset_index()
                print("CONSULTA 1 NORTHWIND")
                print("*** EMPRESAS CON MAYOR VENTA POR AÑO Y REGION ***")
                print(df)
                metodos.generarCSV(df, 'maximos.csv')  

            elif opcion_n == '2':
                pass
            elif opcion_n == '3':
                #agrupar las categorias
                df = metodos.agruparSumar('AÑO','CategoryName', 'ProductName', 'CompanyName')
                metodos.generarCSV(df, 'agrupado.csv')
                #eliminar columnas
                df = metodos.eliminarColumnas(df, ['RegionDescription'])
                #obtener el maximo de cada categoria y minimo de cada categoria
                df = metodos.agruparMaximo(df, 'AÑO', 'CategoryName')



                #generar csv
                #print("CONSULTA 3 NORTHWIND")
                #print("*** EMPRESAS CON MAYOR Y MENOR VENTA POR CATEGORIA Y AÑO ***")
                #print(df)



                df = metodos.generarCSV(df, 'maximos_categoria.csv')

                
               

                pass
            elif opcion_n == '4':
                break
            else:
                print("Opción no válida")
            

    
    
    
   
    
   

    
   
    #abrir text
   
    