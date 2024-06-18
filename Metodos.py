import pandas as pd

class Metodos:

   def  __init__(self,df):
        self.df = df
   

   def agruparSumar(self,*columns):
        if not columns:
            raise ValueError("Debes proporcionar al menos una columna para agrupar.")
        return self.df.groupby(list(columns)).sum().reset_index()


   def agruparMaximo(self,*columns):
        if not columns:
            raise ValueError("Debes proporcionar al menos una columna para agrupar.")
        self.df['MaxValor'] = self.df.groupby(list(columns))['CANTIDAD'].transform('max')
        df_maximos = self.df[self.df['CANTIDAD'] == self.df['MaxValor']]
        df_maximos = df_maximos.drop(columns=['MaxValor'])
        return df_maximos.sort_values(['AÑO','RegionDescription'])