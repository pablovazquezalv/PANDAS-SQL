from Conexion import Conexion
from Metodos import Metodos
if __name__ == '__main__':
    
    conexion = Conexion()
    
    
    bd = conexion.use_database("USE northwind")
    
    txt = open("nortwind.txt", "r")
    df = conexion.execute_query(txt.read())


    metodos = Metodos(df)
    df = metodos.agruparSumar('RegionDescription', 'AÑO', 'CompanyName')

    df = metodos.agruparMaximo('RegionDescription', 'AÑO')
    print(df)
    
    #abrir text
   
    