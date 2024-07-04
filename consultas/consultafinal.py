def ganancias_por_categoria_año_cliente(self):
          # Calcular los últimos tres años
          max_year = self.df['year'].max()
          ultimos_tres_anos = [max_year - i for i in range(3)]

          # Encontrar el producto más vendido por categoría y año en los últimos tres años
          productos_mas_vendidos = self.df[self.df['year'].isin(ultimos_tres_anos)].groupby(['year', 'CategoryName'])['ventas'].idxmax()
          productos_mas_vendidos = self.df.loc[productos_mas_vendidos]

          # Encontrar el cliente que compró más y menos cada producto por año y categoría
          clientes_por_producto = self.df[self.df['year'].isin(ultimos_tres_anos)].groupby(['year', 'CategoryName', 'ProductName', 'CompanyName'])['ventas'].sum().reset_index()

          cliente_max_por_producto = clientes_por_producto.loc[clientes_por_producto.groupby(['year', 'CategoryName', 'ProductName'])['ventas'].idxmax()]
          cliente_min_por_producto = clientes_por_producto.loc[clientes_por_producto.groupby(['year', 'CategoryName', 'ProductName'])['ventas'].idxmin()]

          # Merge para añadir la información de los clientes
          productos_mas_vendidos = productos_mas_vendidos.merge(cliente_max_por_producto, on=['year', 'CategoryName', 'ProductName'], suffixes=('', '_max'))
          productos_mas_vendidos = productos_mas_vendidos.merge(cliente_min_por_producto, on=['year', 'CategoryName', 'ProductName'], suffixes=('', '_min'))

          # Crear un DataFrame con los productos más vendidos por categoría y año
          def format_product_info(row):
               return f"{row['ProductName']} (Max: {row['CompanyName_max']} - {row['ventas_max']}, Min: {row['CompanyName_min']} - {row['ventas_min']})"

          productos_mas_vendidos['ProductInfo'] = productos_mas_vendidos.apply(format_product_info, axis=1)

          productos_mas_vendidos_df = productos_mas_vendidos.pivot_table(
               index='CategoryName',
               columns='year',
               values='ProductInfo',
               aggfunc='first'  # Tomar el primer valor (que será el producto más vendido)
          ).fillna('')

          # Asegurar que las columnas de los años estén en orden descendente
          productos_mas_vendidos_df = productos_mas_vendidos_df[ultimos_tres_anos]

          productos_mas_vendidos_df.to_excel("Productos_mas_vendidos_en_los_ultimos_años.xlsx")

          return productos_mas_vendidos_df


ganancias_por_categoria_año_cliente