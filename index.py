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
            df2 = df.copy()
            metodos = Metodos(df)
            metodos2 = Metodos(df2)
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
             
            # Filtrar los datos de los últimos 3 años
              df_ultimos_3 = df[df['AÑO'] >= df['AÑO'].max() - 2]

              print("CONSULTA 3 NORTHWIND AÑOS")
              print(df_ultimos_3)

            # Agrupar por año, categoría, producto y compañía, sumando las cantidades
              df_group = df_ultimos_3.groupby(['AÑO', 'CategoryName', 'ProductName', 'CompanyName'])['CANTIDAD'].sum().reset_index()

            # Ordenar por año, categoría y cantidad de manera descendente
              df_group = df_group.sort_values(['AÑO', 'CategoryName', 'CANTIDAD'], ascending=[True, True, False])

            # Obtener el producto más vendido por año y categoría
              producto_mas_vendido = df_group.drop_duplicates(['AÑO', 'CategoryName'])

              print(producto_mas_vendido)
              metodos.generarCSV(producto_mas_vendido, 'producto_mas_vendido.csv')

              #en el df2 que es la copia de df,buscar los productos menos vendidos por año y categoría que sean los mismos que los más vendidos
              df2 = df2[df2['AÑO'] >= df2['AÑO'].max() - 2]

# Obtener los productos menos vendidos que coinciden con los más vendidos
              productos_menos_vendidos = df2.merge(producto_mas_vendido[['AÑO', 'CategoryName', 'ProductName']], on=['AÑO', 'CategoryName', 'ProductName'], how='inner')
              productos_menos_vendidos = productos_menos_vendidos.groupby(['AÑO', 'CategoryName', 'ProductName', 'CompanyName'])['CANTIDAD'].sum().reset_index()
              productos_menos_vendidos = productos_menos_vendidos.sort_values(['AÑO', 'CategoryName', 'CANTIDAD'], ascending=[True, True, True])

             
              print("\nProductos menos vendidos por año y categoría:")
              print(productos_menos_vendidos)
              metodos.generarCSV(productos_menos_vendidos, 'productos_menos_vendidos.csv')
              ###########
              df_grouped = productos_menos_vendidos.groupby(['AÑO', 'CategoryName','ProductName']).agg({
    'CANTIDAD': ['max', 'min']
}).reset_index()

# Renombrar las columnas para claridad
              df_grouped.columns = ['AÑO', 'CategoryName', 'ProductName', 'Max_CANTIDAD', 'Min_CANTIDAD']

                # Unir con el DataFrame original para obtener los clientes que corresponden a los valores máximos
              df_max = pd.merge(df_grouped[['AÑO', 'CategoryName', 'ProductName', 'Max_CANTIDAD']], productos_menos_vendidos, 
                                left_on=['AÑO', 'CategoryName', 'ProductName', 'Max_CANTIDAD'], 
                                right_on=['AÑO', 'CategoryName', 'ProductName', 'CANTIDAD']).drop_duplicates()

                # Unir con el DataFrame original para obtener los clientes que corresponden a los valores mínimos
              df_min = pd.merge(df_grouped[['AÑO', 'CategoryName', 'ProductName', 'Min_CANTIDAD']], productos_menos_vendidos, 
                                left_on=['AÑO', 'CategoryName', 'ProductName', 'Min_CANTIDAD'], 
                                right_on=['AÑO', 'CategoryName', 'ProductName', 'CANTIDAD']).drop_duplicates()

                # Renombrar las columnas para claridad
              df_max.rename(columns={'CompanyName': 'Max_CompanyName'}, inplace=True)
              df_min.rename(columns={'CompanyName': 'Min_CompanyName'}, inplace=True)

                # Unir los DataFrames de valores máximos y mínimos
              df_grouped = pd.merge(df_max, df_min, on=['AÑO', 'CategoryName', 'ProductName'])

              print("Máximo y mínimo de CANTIDAD por AÑO y CategoryName, y los clientes correspondientes:")
              print(df_grouped)
              metodos.generarCSV(df_grouped, 'max_min_cantidad.csv')

              df_grouped['Info'] = df_grouped['ProductName'] + ', ' + df_grouped['Max_CompanyName'] + ' ' + df_grouped['Max_CANTIDAD'].astype(str) + ', ' + df_grouped['Min_CompanyName'] + ' ' + df_grouped['Min_CANTIDAD'].astype(str)

                # Reorganizar los datos con pivot_table()
              df_pivot = df_grouped.pivot_table(index='CategoryName', columns='AÑO', values='Info', aggfunc='first')

              print(df_pivot)
              metodos.generarCSV(df_pivot.reset_index(), 'pivot_table.csv')
              
            elif opcion_n == '4':
            
                break
            else:
                print("Opción no válida")
        
       elif opcion == '2':
           while True:
               bd = conexion.use_database("USE pubs")
               query = "SELECT titles.title_id,TB1.au_id, SUM(titles.price * sales.qty * TB1.royaltyper / 100) AS TotalSales FROM titles  INNER JOIN sales ON sales.title_id = titles.title_id INNER JOIN  ( SELECT authors.au_id, titleauthor.title_id, titleauthor.royaltyper FROM authors INNER JOIN titleauthor ON authors.au_id = titleauthor.au_id ) AS TB1 ON TB1.title_id = titles.title_id GROUP BY TB1.au_id,titles.title_id UNION SELECT DISTINCT titles.title_id, 'Anónimo' AS Autor,SUM(titles.price * sales.qty * (100 - COALESCE(TB1.total_royalty, 0)) / 100) AS TotalSales FROM sales  INNER JOIN titles ON sales.title_id = titles.title_id LEFT JOIN (    SELECT title_id, SUM(royaltyper) AS total_royalty  FROM titleauthor GROUP BY title_id ) AS TB1 ON titles.title_id = TB1.title_id GROUP BY titles.title_id ORDER BY TotalSales;"
               df = conexion.execute_query(query)
               metodos = Metodos(df)
               opcion_n = menu.menuPubs()
               if opcion_n == '1':
                   metodos = Metodos(df)

                   grouped_df = metodos.base(df)
                   metodos.generarCSV(grouped_df, 'pubs.csv')
                    # Mostrar el resultado
                   print("CONSULTA 1 PUBS")
                   print("*** Los autores con sus ganacias ***")
                   print(grouped_df)
               elif opcion_n == '2':
                   break
              
    
    
    
   
    
   

    
   
    #abrir text
   
    