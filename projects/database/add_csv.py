from .database import Database
import argparse

input_csv = 'metropolitan.csv'
table_name = 'metropolitan'
database_name = 'database.db'

# use argparse to parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_csv', type=str, default=input_csv,
                    help='the path to the csv file')
parser.add_argument('--table_name', type=str, default=table_name,
                    help='the name of the table')
parser.add_argument('--database_name', type=str, default=database_name,
                    help='the name of the database')


def main():
    db = Database(database_name)
    db.load_csv_to_sqlite(input_csv, table_name, database_name)


if __name__ == '__main__':
    main()
