import duckdb

# Leemos los datos que originalmente estaban en el parquet con duckdb. Los pasamos a un dataframe.
# Nos quedamos solo con la ciudad de Madrid desde 2021.

con = duckdb.connect(database=":memory:")
con.execute(
    "CREATE VIEW 'gas_prices' AS SELECT * FROM '"+datapath+"';"
)
con.execute("DESCRIBE SELECT * FROM 'gas_prices';").fetchall()

stmt = """
    SELECT *
    FROM 'gas_prices'
    WHERE municipality_name == 'Madrid' AND '2022-01-01' < date AND date < '2022-01-15'
"""

# Create DataFrame with the selected data
df = con.execute(stmt).fetchdf()

