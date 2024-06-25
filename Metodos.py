import pandas as pd

class Metodos:

   def  __init__(self,df):
        self.df = df
   

   def agruparSumar(self,*columns):
        if not columns:
            raise ValueError("Debes proporcionar al menos una columna para agrupar.")
        return self.df.groupby(list(columns)).sum().reset_index()


   def agruparMaximo(self, df, *columns):
        if not columns:
            raise ValueError("Debes proporcionar al menos una columna para agrupar.")
        df['MaxValor'] = df.groupby(list(columns))['CANTIDAD'].transform('max')
        df = df[df['CANTIDAD'] == df['MaxValor']]        
        df = df.drop(columns=['MaxValor'])
        return df
             
   def agruparMinimo(self, df, *columns):
        if not columns:
            raise ValueError("Debes proporcionar al menos una columna para agrupar.")
        df['MinValor'] = df.groupby(list(columns))['CANTIDAD'].transform('min')
        df = df[df['CANTIDAD'] == df['MinValor']]
        df = df.drop(columns=['MinValor'])
        
        return df
   
   def generarCSV(self,df,nombre):
        df.to_csv(nombre, index=False)
        print("Archivo generado con exito")
        return True
   
   def eliminarColumnas(self,df,columns):
        return df.drop(columns, axis=1)
   
   def productoMasVendido(self, df, *columns):
        if 'CANTIDAD' not in df.columns or 'CompanyName' not in df.columns:
            raise ValueError("El dataframe debe contener las columnas 'CANTIDAD' y 'CompanyName'.")
        
        # Calcula el máximo por grupo y agrega la columna 'MaxValor'
        df['MaxValor'] = df.groupby(list(columns))['CANTIDAD'].transform('max')
        
        # Filtra las filas que contienen el máximo valor por grupo
        df_maximos = df[df['CANTIDAD'] == df['MaxValor']]
        
        # Elimina la columna 'MaxValor'
        df_maximos = df_maximos.drop(columns=['MaxValor'])
        
        # Devolver solo las columnas relevantes
        return df_maximos

   def productoMenosVendido(self, df, *columns):
          if 'CANTIDAD' not in df.columns or 'CompanyName' not in df.columns:
               raise ValueError("El dataframe debe contener las columnas 'CANTIDAD' y 'CompanyName'.")
          
          # Calcula el mínimo por grupo y agrega la columna 'MinValor'
          df['MinValor'] = df.groupby(list(columns))['CANTIDAD'].transform('min')
          
          # Filtra las filas que contienen el mínimo valor por grupo
          df_minimos = df[df['CANTIDAD'] == df['MinValor']]
          
          # Elimina la columna 'MinValor'
          df_minimos = df_minimos.drop(columns=['MinValor'])
          
          # Devolver solo las columnas relevantes
          return df_minimos
     