import duckdb

con = duckdb.connect(database=":memory:")
con.execute(
    "CREATE VIEW 'gas_prices' AS SELECT * FROM '"+datapath+"';"
)
con.execute("DESCRIBE SELECT * FROM 'gas_prices';").fetchall()

# 
stmt = """
    SELECT *
    FROM 'gas_prices'
    WHERE '2021-01-01' < date AND date < '2021-02-01' AND province_name == 'BALEARS (ILLES)'
"""

# Create DataFrame with the selected data

df = con.execute(stmt).fetchdf()

# Initial data analysis and null values filling
print('     ')
print('#########################################################')
print('     DATA TYPE, NON-NULL VARIABLES AND MEMORY USAGE')
print('#########################################################')
print('     ')
print(df.info())
print('     ')
print('---------- Filling NaN ...')
df= df.fillna(0)
print('---------- NaN remaining:', df.isnull().sum().sum())
print('     ')

# Download selected dataset into .csv

##df.to_csv('datos.csv')
