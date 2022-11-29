import duckdb

con = duckdb.connect(database=":memory:")
con.execute(
    "CREATE VIEW 'gas_prices' AS SELECT * FROM '"+datapath+"';"
)
con.execute("DESCRIBE SELECT * FROM 'gas_prices';").fetchall()

stmt = """
    SELECT *
    FROM 'gas_prices'
    WHERE municipality_name == 'Madrid' AND '2021-01-01' < date AND date < '2023-02-01'
"""

# Create DataFrame with the selected data

df = con.execute(stmt).fetchdf()

