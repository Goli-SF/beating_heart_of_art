import sqlite3
import pandas as pd
import os


class DataStore:

    table_names = ['metropolitan', 'moma']
    prefixes = ['MTRP', 'MOMA']
    image_url_column_names = ['imageURL', 'image_url_1', 'image_url_2']
    embed_url_column_names = ['imageURL', 'embed_url_1', 'embed_url_2']

    def __init__(self, database_name, images_directory="./"):
        self.database_name = database_name
        self.images_directory = images_directory

    def count(self, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'SELECT COUNT(*) FROM {table_name}', conn)

        # close the connection
        conn.close()

        return df

    def list_all_tables(self):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table'", conn)

        # close the connection
        conn.close()

        return df

    def get_images(self, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(
            f'SELECT id, set_name, image_name FROM {table_name}', conn)

        # close the connection
        conn.close()

        # rename image url column to image_url

        # add full path column using path.join
        df['full_path'] = df.apply(
            lambda row: os.path.join(self.images_directory, row['set_name'], row['image_name']), axis=1)

        # print columns
        # print('columns:', df.columns)

        return df

    def get_info_by_ids(self, ids=[]):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # convert object_ids to string
        object_ids = [str(object_id) for object_id in object_ids]

        prefix = id[:4]
        table_name = self.table_names[self.prefixes.index(prefix)]

        # # load metropolitan.csv
        # df = pd.read_sql_query(
        #     f"SELECT * FROM {table_name} WHERE id='{id}'", conn)

        # return all rows with object_id is in object_ids
        df = pd.read_sql_query(
            f"SELECT * FROM {table_name} WHERE id IN ({','.join(ids)})", conn)

        image_url_name = self.image_url_column_names[self.prefixes.index(
            prefix)]
        embed_url_name = self.embed_url_column_names[self.prefixes.index(
            prefix)]

        # copy the image url to a column called image_url
        df['image_url'] = df[image_url_name]
        # copy the embed url to a column called embed_url
        df['embed_url'] = df[embed_url_name]

        # only keep columns id, image_url, embed_url
        df = df[['id', 'image_url', 'embed_url']]

        # close the connection
        conn.close()
        # print columns
        # print('columns:', df.columns)

        return df

    def get_info_by_object_ids(self, table_name, object_ids=[]):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # convert object_ids to string
        object_ids = [str(object_id) for object_id in object_ids]

        # return all rows with object_id is in object_ids
        df = pd.read_sql_query(
            f"SELECT * FROM {table_name} WHERE objectID IN ({','.join(object_ids)})", conn)

        image_url_name = self.image_url_column_names[self.table_names.index(
            table_name)]
        embed_url_name = self.embed_url_column_names[self.table_names.index(
            table_name)]

        # copy the image url to a column called image_url
        df['image_url'] = df[image_url_name]
        # copy the embed url to a column called embed_url
        df['embed_url'] = df[embed_url_name]

        # # only keep columns id, image_url, embed_url
        # df = df[['id', 'image_url', 'embed_url']]

        # close the connection
        conn.close()
        # print columns
        # print('columns:', df.columns)

        return df

    def load_csv_to_sqlite(self, csv_file_name, table_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_csv(csv_file_name)

        # save to sqlite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        # print the first 5 rows from the database
        print(pd.read_sql_query(f'SELECT * FROM {table_name} LIMIT 5', conn))

        # commit
        conn.commit()

        # close the connection
        conn.close()

    def load_sqlite_to_csv(self, table_name, csv_file_name):
        # create an empty sqlite database
        conn = sqlite3.connect(self.database_name)

        # load metropolitan.csv
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)

        # save to sqlite database
        df.to_csv(csv_file_name, index=False)

        # print the first 5 rows from the database
        print(pd.read_csv(csv_file_name).head())

        # close the connection
        conn.close()
