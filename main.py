import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="northwind",
)

mycursor = mydb.cursor()

mycursor.execute("USE northwind")

query = """SELECT TB1.RegionDescription,YEAR(orders.OrderDate) AS AÑO,
SUM(`order details`.UnitPrice * `order details`.Quantity) AS CANTIDAD,
Categories.CategoryName,Customers.CompanyName,Products.ProductName
FROM orders 
INNER JOIN `order details` ON `order details`.OrderID = orders.OrderID 
INNER JOIN Products ON Products.ProductID =`order details`.ProductID
INNER JOIN Categories ON Categories.CategoryID = Products.CategoryID
INNER JOIN Customers ON  Customers.CustomerID = orders.CustomerID
INNER JOIN 
(
SELECT DISTINCT region.RegionDescription,employeeterritories.EmployeeID 
FROM  region INNER JOIN  territories ON region.RegionID = territories.RegionID 
INNER JOIN   employeeterritories ON employeeterritories.TerritoryID = territories.TerritoryID
GROUP BY  region.RegionDescription,employeeterritories.EmployeeID
) AS TB1
ON orders.EmployeeID = TB1.EmployeeID
GROUP BY  TB1.RegionDescription,YEAR(orders.OrderDate),
orders.CustomerID,Categories.CategoryName,Products.ProductName"""


mycursor.execute(query)

myresult = mycursor.fetchall()

column_names = [i[0] for i in mycursor.description]


df = pd.DataFrame(myresult, columns=column_names)

#definir el dataframe
df = df[['RegionDescription', 'AÑO', 'CANTIDAD', 'CompanyName']]

df = df.groupby(['RegionDescription', 'AÑO', 'CompanyName']).sum().reset_index()


df['MaxValor'] = df.groupby(['RegionDescription', 'AÑO'])['CANTIDAD'].transform('max')

df_maximos = df[df['CANTIDAD'] == df['MaxValor']]

# Eliminar la columna temporal 'MaxValor'
df_maximos = df_maximos.drop(columns=['MaxValor'])

# Imprimir el resultado
by_year = df_maximos.sort_values(['AÑO','RegionDescription'])

print("**************************")
print("CONSULTA 2")
print(by_year)  
by_year.to_csv('consulta1.csv', index=False)

# Consulta 2

df_2 = pd.DataFrame(myresult, columns=column_names)



#ganacias por autor