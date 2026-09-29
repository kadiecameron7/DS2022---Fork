import logging
import os
import sys
import mysql.connector
from mysql.connector import Error
import pandas as pd

logging.basicConfig(level=logging.INFO)

DBHOST = os.environ.get("DBHOST")
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")


type_mapping = { # double check type
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "object": "VARCHAR(255)",  # safe default varchar length
    "string": "VARCHAR(255)",
}

def read_data(filename):
    """Read a CSV file into a pandas data frame."""
    logging.info("Reading %s", filename) # add to log
    data = pd.read_csv(filename) # read file
    logging.info("Read %d rows", len(data)) # add to log
    return data

def clean_data(data):
    """Remove rows with missing values and return cleaned data."""
    logging.info("Cleaning data") # add to log
    data = data.dropna() # drops empty values
    logging.info("%d rows left after cleaning", len(data)) # add to log
    return data

def load_data(data, table):
    """Create the table if needed and insert every row."""
    try:
        with mysql.connector.connect( # establishes connection
            host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
            ) as connection:
            with connection.cursor(dictionary=True) as cursor:
                columns = []
                for name, dtype in data.dtypes.items():
                    sql_type = type_mapping.get(str(dtype), "VARCHAR(255)") # checks datatype
                    columns.append(f"`{name}` {sql_type}") # adds to column
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})" # creates table if needed, joins columns
                )

                names = ", ".join(f"`{name}`" for name in data.columns) # adds names
                placeholders = ", ".join(["%s"] * len(data.columns))                
                query = f"INSERT INTO {table} ({names}) VALUES ({placeholders})" # inserts into table
                for row in data.values.tolist():
                    cursor.execute(query, row) # goes row by row for insertion
                connection.commit()
                logging.info("Inserted %d rows into %s", len(data), table) # adds to log
    except Error as e:
        logging.error("Error connection to MySQL: %s", e) # catches any errors for sql



def main():
    """Read, clean, and load data."""
    filename = sys.argv[1] if len(sys.argv) > 1 else "data.csv" # checks for data in file
    data = read_data(filename) # reads file
    data = clean_data(data) # cleans file
    load_data(data, "mock") # loads data into mock file and table

if __name__ == "__main__":
    main() # calls main function
