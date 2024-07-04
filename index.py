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
                #agrupar las categorias
              df_ultimos_3_anos = df[df['AÑO'] >= df['AÑO'].max() - 2]

              print("CONSULTA 3 NORTHWIND AÑOS")
              print(df_ultimos_3_anos)

                # Agrupar por año, categoría, producto y compañía, sumando las cantidades
              df_grouped = df_ultimos_3_anos.groupby(['AÑO', 'CategoryName', 'ProductName', 'CompanyName'])['CANTIDAD'].sum().reset_index()

                # Ordenar por año, categoría y cantidad de manera descendente
              df_grouped = df_grouped.sort_values(['AÑO', 'CategoryName', 'CANTIDAD'], ascending=[True, True, False])

                # Obtener el producto más vendido por año y categoría
              producto_mas_vendido_por_anio_categoria = df_grouped.drop_duplicates(['AÑO', 'CategoryName'])

              print(producto_mas_vendido_por_anio_categoria)
              metodos2.generarCSV(producto_mas_vendido_por_anio_categoria, 'producto_mas_vendido_por_anio_categoria.csv')
           

            # Filtrar los datos de los últimos 3 años
              df_ultimos_3 = df2[df2['AÑO'] >= df2['AÑO'].max() - 2]

              print("CONSULTA 3 NORTHWIND AÑOS")
              print(df_ultimos_3)

            # Agrupar por año, categoría, producto y compañía, sumando las cantidades
              df_group = df_ultimos_3.groupby(['AÑO', 'CategoryName', 'ProductName', 'CompanyName'])['CANTIDAD'].sum().reset_index()

            # Ordenar por año, categoría y cantidad de manera descendente
              df_group = df_group.sort_values(['AÑO', 'CategoryName', 'CANTIDAD'], ascending=[True, True, False])

            # Obtener el producto más vendido por año y categoría
              producto_mas_vendido = df_group.drop_duplicates(['AÑO', 'CategoryName'])

              print(producto_mas_vendido)
              metodos.generarCSV(producto_mas_vendido, 'producto_mas_vendido_por_anio_categoria.csv')

            # Ordenar por año, categoría y cantidad de manera ascendente para encontrar el cliente que menos compró
              df_grouped_min = df_group.sort_values(['AÑO', 'CategoryName', 'CANTIDAD'], ascending=[True, True, True])

            # Obtener el cliente que menos compró por año y categoría
              cliente_menos_compro_por_anio_categoria = df_grouped_min.drop_duplicates(['AÑO', 'CategoryName'])

              print(cliente_menos_compro_por_anio_categoria)
              metodos.generarCSV(cliente_menos_compro_por_anio_categoria, 'cliente_menos_compro_por_anio_categoria.csv')
              
              matriz_datos = {}

                # Obtener las categorías únicas
              categorias = producto_mas_vendido_por_anio_categoria['CategoryName'].unique()

                # Iterar sobre cada categoría
              for categoria in categorias:
                    matriz_datos[categoria] = {}
                    
                    # Filtrar los datos por categoría
                    df_prod_mas_vendido = producto_mas_vendido_por_anio_categoria[producto_mas_vendido_por_anio_categoria['CategoryName'] == categoria]
                    df_cli_menos_compro = cliente_menos_compro_por_anio_categoria[cliente_menos_compro_por_anio_categoria['CategoryName'] == categoria]
                    
                    # Obtener los años únicos ordenados
                    anos_unicos = sorted(df_prod_mas_vendido['AÑO'].unique(), reverse=True)[:3]
                    
                    # Iterar sobre los años
                    for idx, ano in enumerate(anos_unicos):
                        matriz_datos[categoria][f"Año_{idx + 1}"] = {}
                        
                        # Filtrar datos por año y obtener productos más vendidos y menos comprados
                        df_prod_vendido_ano = df_prod_mas_vendido[df_prod_mas_vendido['AÑO'] == ano].reset_index(drop=True)
                        df_cli_menos_ano = df_cli_menos_compro[df_cli_menos_compro['AÑO'] == ano].reset_index(drop=True)
                        
                        if not df_prod_vendido_ano.empty:
                            producto_mas_vendido = {
                                'Producto': df_prod_vendido_ano.iloc[0]['ProductName'],
                                'Cliente que más compró': df_prod_vendido_ano.iloc[0]['CompanyName'],
                                'Cantidad': df_prod_vendido_ano.iloc[0]['CANTIDAD']
                            }
                            matriz_datos[categoria][f"Año_{idx + 1}"]['Producto más vendido'] = producto_mas_vendido
                        
                        if not df_cli_menos_ano.empty:
                            cliente_menos_compro = {
                                'Producto': df_cli_menos_ano.iloc[0]['ProductName'],
                                'Cliente que menos compró': df_cli_menos_ano.iloc[0]['CompanyName'],
                                'Cantidad': df_cli_menos_ano.iloc[0]['CANTIDAD']
                            }
                            matriz_datos[categoria][f"Año_{idx + 1}"]['Cliente menos compró'] = cliente_menos_compro

                # Convertir el diccionario en un DataFrame para visualización o exportación
                        df_matriz = pd.DataFrame([(categoria, datos) for categoria, datos in matriz_datos.items()], columns=['CategoryName', 'Datos'])

                        print(df_matriz)
                        metodos.generarCSV(df_matriz, 'matriz.csv')
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
   
    