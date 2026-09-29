import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
logging.basicConfig(level=logging.INFO)

DBHOST = os.environ.get("DBHOST")
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")

try: # establishes sql connection
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DBNAME)
    cur = db.cursor()
except mysql.connector.Error as e: # catches error
    logging.error("Could not connect to MySQL: %s", e)
    db = None
    cur = None

def get_data_by_group(value):
    """Return mock rows by `group` using ``value`` (list of tuples)."""
    logging.info("Querying mock for group = %s", value) # adds to log
    query = "SELECT * FROM mock WHERE `group` = %s;" # selects rows where the group appears
    try:
        cur.execute(query, (value,)) # cursor executes search for the value
        results = cur.fetchall()
        output = []
        for r in results: # adds each result to output
            output.append(r)
        return output
    except mysql.connector.Error as e: # catches errors
        logging.error("MySQL Error: %s", e)
        return None

def plot_counts(groupby):
    """Count plot by `groupby`, show bar chart, return dataframe."""
    logging.info("Counting rows in mock grouped by %s", groupby) # adds to log
    query = f"SELECT `{groupby}`, COUNT(*) FROM mock GROUP BY `{groupby}`" # group by given group
    df = pd.DataFrame()
    try:
        cur.execute(query) # cursor finds groups
        results = cur.fetchall()
        output = []
        for r in results:
            output.append(r) # adds each result to output
        logging.info("Got counts for %d distinct values", len(output)) # adds to log
        df = pd.DataFrame(output, columns=[groupby, "count"]) # creates dataframe from output and group
        df.plot.bar(x=groupby, y="count", legend=False) # creates bar chart
        plt.xlabel(groupby) # x axis label
        plt.ylabel("count") # y axis label
        plt.tight_layout() 
        plt.show() # shows bar chart
        return df
    except mysql.connector.Error as e: # catches errors
        logging.error("MySQL Error: %s", e)
        return None

def main():
    """Run the mock queries and close database connection."""
    if cur is None or db is None: # if sql connection didn't work
        logging.error("No database connection available, exiting")
        return

    print("=== rows where group = state ===")
    print(get_data_by_group("state")) # gets data sorted by state

    print("=== counts by group ===")
    plot_counts("group") # groups and plots by state

    cur.close() # closes connection and database
    db.close()

if __name__ == "__main__":
    main() # calls main function