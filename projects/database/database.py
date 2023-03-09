import sqlite3
import pandas as pd


def load_csv_to_sqlite(csv_file_name, table_name, database_name):
    # create an empty sqlite database
    conn = sqlite3.connect(database_name)

    # load metropolitan.csv
    df = pd.read_csv(csv_file_name)

    # save to sqlite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # print the first 5 rows from the database
    print(pd.read_sql_query(f'SELECT * FROM {table_name} LIMIT 5', conn))

    # close the connection
    conn.close()


def load_sqlite_to_csv(database_name, table_name, csv_file_name):
    # create an empty sqlite database
    conn = sqlite3.connect(database_name)

    # load metropolitan.csv
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)

    # save to sqlite database
    df.to_csv(csv_file_name, index=False)

    # print the first 5 rows from the database
    print(pd.read_csv(csv_file_name).head())

    # close the connection
    conn.close()
