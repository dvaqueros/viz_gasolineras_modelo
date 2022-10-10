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
    WHERE date > '2021-01-01' 
"""

df = con.execute(stmt).fetchdf()

print(df)