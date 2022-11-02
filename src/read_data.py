import duckdb

con = duckdb.connect(database=":memory:")
con.execute(
    "CREATE VIEW 'gas_prices' AS SELECT * FROM '"+datapath+"';"
)
con.execute("DESCRIBE SELECT * FROM 'gas_prices';").fetchall()

#stmt = """
#    SELECT COUNT(*)
#    FROM 'gas_prices'
#"""

stmt = """
    SELECT *
    FROM 'gas_prices'
    WHERE '2021-01-01' < date AND date < '2021-02-01' AND province_name == 'BALEARS (ILLES)'
"""

df = con.execute(stmt).fetchdf()
df.to_csv('datos.csv')

print(df)